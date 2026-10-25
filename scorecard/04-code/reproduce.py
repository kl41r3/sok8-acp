#!/usr/bin/env python3
"""Aggregate saved chat judgments, apply author decisions, and render fresh data."""
import argparse
from collections import Counter
import csv
from fractions import Fraction
import itertools
import json
import os
from pathlib import Path
import statistics
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MODELS = ['agnes-2.5-flash', 'deepseek-v4-flash', 'qwen3.7-plus']
DIMS = ['C', 'I', 'A', 'EM', 'S']
PROPERTIES = ['auth_safety', 'exec_correct', 'econ_finality', 'price_correct', 'auditability', 'compliance', 'recoverability']


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(path):
    return json.loads(path.read_text())


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def agreement(vectors):
    """Agreement over 40 pre-adjudication cells, using half-step categories."""
    pairs = []
    for model_a, model_b in itertools.combinations(MODELS, 2):
        x, y = vectors[model_a], vectors[model_b]
        n = len(x)
        cx, cy = Counter(x), Counter(y)
        kappas = {}
        for label, weight in [('unweighted', lambda i, j: int(i != j)),
                              ('quadratic_weighted', lambda i, j: (i - j) ** 2)]:
            observed = sum(weight(i, j) for i, j in zip(x, y))
            expected = sum(Fraction(cx[i] * cy[j], n) * weight(i, j) for i in range(5) for j in range(5))
            require(expected != 0, 'Undefined kappa')
            kappas[label] = float(1 - Fraction(observed) / expected)
        pairs.append({'model_a': model_a, 'model_b': model_b, **kappas})
    n_cells, n_raters = len(next(iter(vectors.values()))), len(MODELS)
    counts = [Counter(vectors[m][i] for m in MODELS) for i in range(n_cells)]
    observed = sum(Fraction(sum(v * (v - 1) for v in c.values()), n_raters * (n_raters - 1)) for c in counts) / n_cells
    totals = Counter(v for m in MODELS for v in vectors[m])
    expected = sum(Fraction(n, n_cells * n_raters) ** 2 for n in totals.values())
    return {'unit': '40 protocol-dimension cells before author adjudication',
            'category_order': [0, 0.5, 1, 1.5, 2], 'model_order': MODELS,
            'pairwise_cohens_kappa': pairs,
            'mean_unweighted_cohens_kappa': statistics.mean(r['unweighted'] for r in pairs),
            'fleiss_kappa': float((observed - expected) / (1 - expected)),
            'rating_counts': {str(k / 2): totals[k] for k in range(5)},
            'scope': 'Inter-model agreement, not human inter-rater reliability.'}


def generate(output):
    metadata = load(ROOT / '02-judgments/protocols.json')
    names = [p['protocol'] for p in metadata]
    require(len(set(names)) == 8, 'Expected eight protocols')
    medians = {}
    model_rows = []
    observed_gaps = []
    for model in MODELS:
        rounds = []
        for rnd in [1, 2, 3]:
            rec = load(ROOT / f'02-judgments/{model}/round_{rnd}.json')
            require(rec['model'] == model and rec['round'] == rnd, 'Round identity mismatch')
            require(rec['temperature'] == {1: 0, 2: 0.3, 3: 0.6}[rnd], 'Round configuration differs')
            rows = rec['protocols']
            require(len(rows) == 8 and {r['protocol'] for r in rows} == set(names), 'Round coverage differs')
            for r in rows:
                require(all(r[d] in [0, 0.5, 1, 1.5, 2] for d in DIMS), 'Invalid saved score')
                require(set(r['cells']) == set(DIMS), 'Missing cell evidence')
                for d in DIMS:
                    keys = set(r['cells'][d])
                    require({'promise', 'failure', 'metric', 'locator'} <= keys <= {'promise', 'evidence', 'failure', 'metric', 'locator', 'score'}, 'Cell schema differs')
                    if 'evidence' not in keys:
                        observed_gaps.append({'model': model, 'round': rnd, 'protocol': r['protocol'], 'dimension': d, 'missing_field': 'evidence'})
                count = sum(r[p] in {'yes', 'partial'} for p in PROPERTIES)
                require(count == r['A_count'], 'Saved property count differs')
                require(r['A'] == (0 if count <= 1 else 1 if count <= 4 else 2), 'Saved normalization differs')
            rounds.append({r['protocol']: r for r in rows})
        medians[model] = {p: {d: float(statistics.median(r[p][d] for r in rounds)) for d in DIMS} for p in names}
        for p in names:
            row = medians[model][p]
            model_rows.append({'model': model, 'protocol': p, **row, 'total': sum(row.values())})
    require(observed_gaps == load(ROOT / '02-judgments/schema-notes.json')['missing_cell_fields'], 'Saved evidence-field gaps differ')
    write_csv(output / '03-results/model-medians-24.csv', model_rows)
    baseline = []
    for p in names:
        scores = {d: float(statistics.median(medians[m][p][d] for m in MODELS)) for d in DIMS}
        spreads = []
        for d in DIMS:
            vals = [medians[m][p][d] for m in MODELS]
            if max(vals) - min(vals) >= 1:
                spreads.append(f'{d} {min(vals)}-{max(vals)}')
        baseline.append({'protocol': p, **scores, 'total': sum(scores.values()), 'spread': '; '.join(spreads) if spreads else 'agree within 1'})
    write_csv(output / '03-results/cross-model-median-8.csv', baseline)
    author = load(ROOT / '02-judgments/author-decisions-11.json')
    require(author['model_order'] == MODELS and len(author['decisions']) == 11, 'Author lock differs')
    changes = {}
    audit = []
    for r in author['decisions']:
        p, d = r['protocol'], r['dimension']
        require(p in names and d in DIMS and (p, d) not in changes, 'Invalid author cell')
        require(r['model_medians_in_order'] == [medians[m][p][d] for m in MODELS], 'Author input medians differ')
        spread = max(r['model_medians_in_order']) - min(r['model_medians_in_order'])
        require((r['gate'] == 'spread' and spread >= 1) or (r['gate'] == 'object' and p == 'Kleros'), 'Author gate differs')
        require(r['locked_score'] in [0, 0.5, 1, 1.5, 2], 'Invalid author score')
        changes[p, d] = r['locked_score']
        before = next(x for x in baseline if x['protocol'] == p)[d]
        audit.append({'cell_id': r['cell_id'], 'protocol': p, 'dimension': d,
                      'gate': r['gate'], 'model_median': before, 'locked_score': r['locked_score'],
                      'changed': before != r['locked_score']})
    expected_gates = {(p, d) for p in names for d in DIMS if max(medians[m][p][d] for m in MODELS) - min(medians[m][p][d] for m in MODELS) >= 1}
    require(expected_gates == {(r['protocol'], r['dimension']) for r in author['decisions'] if r['gate'] == 'spread'}, 'Spread-gated coverage differs')
    final = []
    for meta, base in zip(metadata, baseline):
        scores = {d: float(changes.get((meta['protocol'], d), base[d])) for d in DIMS}
        final.append({'protocol': meta['protocol'], 'layer': meta['layer'], **scores,
                      'total': sum(scores.values()), 'source': meta['score_source']})
    write_csv(output / 'final-scores-8.csv', final)
    write_csv(output / '03-results/adjudication-audit-11.csv', audit)
    vectors = {m: [int(medians[m][p][d] * 2) for p in names for d in DIMS] for m in MODELS}
    write_json(output / '03-results/inter-model-agreement.json', agreement(vectors))
    return final


def compare(output):
    expected = [ROOT / 'final-scores-8.csv', *sorted((ROOT / '03-results').glob('*'))]
    tables = 0
    for p in expected:
        if p.suffix not in {'.csv', '.json'}:
            continue
        target = output / p.relative_to(ROOT)
        require(target.is_file() and target.read_bytes() == p.read_bytes(), f'Regenerated table differs: {p.name}')
        tables += 1
    return tables


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    require(not output.is_relative_to(ROOT.parent), 'Output must be outside this package')
    require(not output.exists() or not any(output.iterdir()), 'Output must be new or empty')
    output.mkdir(parents=True, exist_ok=True)
    generate(output)
    tables = compare(output)
    env = os.environ | {'MPLBACKEND': 'Agg', 'MPLCONFIGDIR': str(output / '.matplotlib'), 'PYTHONDONTWRITEBYTECODE': '1'}
    subprocess.run([sys.executable, '-B', str(ROOT / '04-code/plot.py'), '--scores', str(output / 'final-scores-8.csv'), '--output', str(output / 'figures')], check=True, env=env)
    figures = list((ROOT / 'figures').glob('*'))
    require(len(figures) == 9, 'Expected three charts in PDF, SVG, and PNG')
    for p in figures:
        require((output / 'figures' / p.name).read_bytes() == p.read_bytes(), f'Regenerated figure differs: {p.name}')
    print(json.dumps({'protocols': 8, 'dimensions': 5, 'saved_model_rounds': 9, 'author_cells': 11,
                      'tables_checked': tables, 'figure_files_checked': len(figures), 'api_calls': 0}, indent=2))


if __name__ == '__main__':
    main()
