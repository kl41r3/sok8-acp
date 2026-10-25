#!/usr/bin/env python3
"""Reconstruct selection, exact-identifier union and layer coding offline."""
import argparse
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path

TAX = Path(__file__).resolve().parents[1]
PACKAGE = TAX.parent
SOURCES = ['ACM', 'IEEE', 'AAAI', 'IJCAI']
LAYERS = [f'L{i}' for i in range(1, 9)]
FIELDS = ['record_id', 'title', 'source', 'identifier', 'identifier_key',
          'decision', 'reason', 'screening_rule', 'evidence_level']


def require(value, message):
    if not value:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def csvwrite(path, rows):
    require(bool(rows), f'No rows for {path.name}')
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


def selection(output, source_records, decisions):
    require(len(source_records) == 5241, 'Source frame differs')
    source_index = {(r['source'], r['record_id']): r for r in source_records}
    require(len(source_index) == len(source_records), 'Duplicate source record')
    require(len(decisions) == 5217, 'Academic selection frame differs')
    require(len({(r['source'], r['record_id']) for r in decisions}) == len(decisions), 'Duplicate screening decision')
    rows = [{k: r[k] for k in FIELDS} for r in decisions]
    rows.sort(key=lambda r: (SOURCES.index(r['source']), r['record_id']))
    groups = defaultdict(list)
    for row in rows:
        key = (row['source'], row['record_id'])
        require(key in source_index, f'Missing source: {key}')
        require(source_index[key]['identifier'].casefold() == row['identifier'].casefold(), f'Identity mismatch: {key}')
        require(row['decision'] in {'include', 'exclude'}, f'Invalid selection: {key}')
        require(all(row.values()), f'Missing selection field: {key}')
        groups[row['identifier_key']].append(row)
    identifiers = []
    for key, members in sorted(groups.items()):
        identifiers.append({
            'identifier_key': key, 'identifier': members[0]['identifier'],
            'source_record_count': len(members),
            'source_members': json.dumps(sorted({r['source'] for r in members})),
            'source_record_members': json.dumps([[r['source'], r['record_id']] for r in members]),
            'decision': 'include' if any(r['decision'] == 'include' for r in members) else 'exclude',
        })
    included = [r for r in identifiers if r['decision'] == 'include']
    by_source = {}
    for source in SOURCES:
        members = [r for r in rows if r['source'] == source]
        counts = Counter(r['decision'] for r in members)
        by_source[source] = {'records': len(members), 'include': counts['include'], 'exclude': counts['exclude']}
    statuses = Counter(r['decision'] for r in rows)
    frame_ids = {r['identifier'].casefold() for r in source_records}
    summary = {
        'source_frame_records': len(source_records), 'source_frame_identifiers': len(frame_ids),
        'source_records': len(rows), 'included_source_records': statuses['include'],
        'excluded_source_records': statuses['exclude'], 'typed_identifiers': len(groups),
        'included_typed_identifiers': len(included),
        'included_source_row_repeat_deduction': statuses['include'] - len(included),
        'by_source': by_source,
    }
    require(len(included) == 1301, 'Included identifier population differs')
    csvwrite(output / 'screening-decisions-all-source-records-5217.csv', rows)
    csvwrite(output / 'screening-decisions-all-identifiers-5184.csv', identifiers)
    csvwrite(output / 'included-identifiers-1301.csv', included)
    csvwrite(output / 'screening-counts-by-source-4.csv', [{'source': s, **v} for s, v in by_source.items()])
    write(output / 'screening-summary-source-records-5217.json', summary)
    return {r['identifier_key'] for r in included}, source_index


def prepare(output, source_records, included):
    index = {(r['source'], r['record_id']): (i, r) for i, r in enumerate(source_records)}
    population = []
    for row in read(TAX / '02-source-evidence/annotation-population.json'):
        i, source = index[(row['source'], row['source_record_id'])]
        require(source['identifier'].casefold() == row['identifier_key'].split(':', 1)[1].casefold(), f'Annotation identity: {row["record_id"]}')
        require(bool(source['public_dates']), f'Missing date: {row["record_id"]}')
        packet = dict(row, evidence=[{
            'evidence_id': 'abstract', 'level': 'abstract', 'text': source['abstract'],
            'locator': f'02-source-evidence/records.json#/{i}/abstract',
        }], year=min(int(d[:4]) for d in source['public_dates']))
        population.append(packet)
    require(len(population) == len({r['record_id'] for r in population}) == 1301, 'Annotation ID coverage')
    require({r['identifier_key'] for r in population} == included, 'Annotation/selection population mismatch')
    write(output / 'annotation-inputs.json', population)
    return population


def classification(value):
    if value == 'not_evidenced':
        return
    require(isinstance(value, list) and value and value == sorted(set(value)) and set(value) <= set(LAYERS), 'Invalid layer set')


def annotation(output, population, only_job=None):
    byid = {p['record_id']: p for p in population}
    supplements = read(TAX / '02-source-evidence/supplements.json')
    execution = read(TAX / '03-screening-review/layer-annotation/execution.json')
    jobs = execution['jobs']
    base = TAX / '03-screening-review/layer-annotation'

    def packet_evidence(packet, job):
        result = {e['evidence_id']: e for e in packet['evidence']}
        for i, e in enumerate(supplements.get(f'{job}/{packet["record_id"]}', [])):
            require(job.startswith('C'), 'Supplement supplied to an initial rater')
            binding = e['identity_binding']
            identifier = binding.get('identifier_key', 'doi:' + binding.get('doi', ''))
            require(identifier.casefold() == packet['identifier_key'].casefold(), 'Supplement identity')
            require(e['evidence_id'] not in result, 'Duplicate evidence ID')
            result[e['evidence_id']] = dict(e, locator=f'02-source-evidence/supplements.json#/{job}~1{packet["record_id"]}/{i}/text')
        return result

    def job_rows(job):
        folder = 'adjudications' if job.startswith('C') else 'annotations'
        data = read(base / folder / f'{job}.json')
        require(data['job_id'] == job and data['model'] == 'gpt-6-astra' and data['reasoning_effort'] == 'high' and data['method_version'] == '2.0.0', f'Job configuration: {job}')
        require(job in jobs, f'Missing execution configuration: {job}')
        require(all(c['model'] == 'gpt-6-astra' and c['reasoning_effort'] == 'high' for c in jobs[job]['model_contexts']), f'Model configuration: {job}')
        records = data['records']
        require(len({r['record_id'] for r in records}) == len(records), f'Duplicate job record: {job}')
        for r in records:
            packet = byid[r['record_id']]
            require(r['identifier_key'] == packet['identifier_key'], f'Job identity: {job}')
            classification(r['classification'])
            require(all(isinstance(r.get(k), str) and r[k].strip() for k in ['rationale', 'mechanism']), 'Missing scientific rationale')
            ev = packet_evidence(packet, job)
            require('abstract' in r['evidence_read'] and set(r['evidence_read']) <= set(ev), 'Reading scope mismatch')
            if not job.startswith('C'):
                require(r['evidence_read'] == ['abstract'], 'Initial evidence differs')
            else:
                require(bool(r.get('adjudication_reason')), 'Missing adjudication reason')
            labels = r['classification']
            if labels == 'not_evidenced':
                require(r['not_evidenced_reason'] in {'outside_layer_functions', 'insufficient_evidence', 'evidence_unavailable'}, 'Missing not_evidenced reason')
                require(all(e['layer'] is None for e in r['evidence']), 'Unexpected positive evidence')
            else:
                require(r['not_evidenced_reason'] is None, 'Positive labels with not_evidenced reason')
                require({e['layer'] for e in r['evidence']} == set(labels), 'Layer/evidence coverage differs')
            for e in r['evidence']:
                require(e['evidence_id'] in r['evidence_read'], 'Unread evidence cited')
                require(e['quote'] and e['quote'] in ev[e['evidence_id']]['text'], f'Exact quotation differs: {job}/{r["record_id"]}')
        return records

    if only_job:
        records = job_rows(only_job)
        print(json.dumps({'job': only_job, 'records': len(records)}))
        return
    final = {}; pairs = []; evidence = []; assigned = set()
    for batch in range(1, 15):
        aa, bb, cc = [f'{role}{batch:02}' for role in 'ABC']
        a, b = job_rows(aa), job_rows(bb)
        require([r['record_id'] for r in a] == [r['record_id'] for r in b], 'Paired coverage differs')
        require(jobs[aa]['context_id'] != jobs[bb]['context_id'], 'Shared initial context')
        disagree = {x['record_id'] for x, y in zip(a, b) if x['classification'] != y['classification']}
        c = {r['record_id']: r for r in job_rows(cc)} if disagree else {}
        require(set(c) == disagree, 'Adjudications differ from exact disagreements')
        if disagree:
            require(jobs[cc]['context_id'] not in {jobs[aa]['context_id'], jobs[bb]['context_id']}, 'Shared adjudication context')
        for x, y in zip(a, b):
            rid = x['record_id']; require(rid not in assigned, 'Overlapping batches'); assigned.add(rid)
            same = x['classification'] == y['classification']
            r = dict(x if same else c[rid]); job = aa if same else cc
            origin = 'dual_consensus' if same else 'adjudication'
            locators = [f'03-screening-review/layer-annotation/annotations/{j}.json' for j in (aa, bb)]
            if not same: locators.append(f'03-screening-review/layer-annotation/adjudications/{cc}.json')
            r.update(decision_origin=origin, method_version='2.0.0', decision_locators=locators)
            final[rid] = r
            pairs.append({'record_id': rid, 'identifier_key': x['identifier_key'], 'batch': f'{batch:02}',
                          'classification_A': json.dumps(x['classification']), 'classification_B': json.dumps(y['classification']),
                          'exact_agreement': same, 'adjudicated': not same, 'final_classification': json.dumps(r['classification'])})
            ev = packet_evidence(byid[rid], job)
            for e in r['evidence']:
                src = ev[e['evidence_id']]; start = src['text'].index(e['quote'])
                evidence.append({'record_id': rid, 'identifier_key': r['identifier_key'], 'layer': e['layer'],
                                 'origin': origin, 'evidence_id': e['evidence_id'], 'quote': e['quote'], 'rationale': e['rationale'],
                                 'start': start, 'end': start + len(e['quote']),
                                 'offset_unit': 'Unicode code points; end exclusive; first exact occurrence',
                                 'source_locator': src['locator'], 'source_level': src['level']})
    require(assigned == set(byid), 'Incomplete final coverage')
    rows = []; detailed = []
    for p in population:
        r = final[p['record_id']]; detailed.append(r)
        labels = [] if r['classification'] == 'not_evidenced' else r['classification']
        rows.append({'record_id': p['record_id'], 'identifier_key': p['identifier_key'], 'title': p['title'],
                     'year': p['year'], 'source': p['source'], 'primary_url': p['primary_url'],
                     'classification': ';'.join(labels) if labels else 'not_evidenced', **{l: int(l in labels) for l in LAYERS},
                     'decision_origin': r['decision_origin'], 'method_version': '2.0.0', 'model': 'gpt-6-astra',
                     'reasoning_effort': 'high', 'mechanism': r['mechanism'], 'rationale': r['rationale'],
                     'not_evidenced_reason': r['not_evidenced_reason'], 'evidence_read': ';'.join(r['evidence_read']),
                     'decision_locators': json.dumps(r['decision_locators'], ensure_ascii=False)})
    agreed = sum(p['exact_agreement'] for p in pairs)
    summary = {'population': len(population), 'unit': 'distinct included typed identifier', 'method_version': '2.0.0',
               'double_coded_records': len(population), 'initial_annotations': len(population)*2,
               'initial_exact_agreement': agreed, 'initial_exact_agreement_rate': agreed/len(population),
               'total_adjudications': len(population)-agreed, 'classified': sum(r['classification'] != 'not_evidenced' for r in rows),
               'not_evidenced': sum(r['classification'] == 'not_evidenced' for r in rows),
               'layer_counts': {l: sum(r[l] for r in rows) for l in LAYERS},
               'decision_origin_counts': dict(Counter(r['decision_origin'] for r in rows)),
               'evidence_scope_counts': dict(Counter(r['evidence_read'] for r in rows)),
               'model': 'gpt-6-astra', 'reasoning_effort': 'high'}
    csvwrite(output.parent / 'included-literature-classifications-1301.csv', rows); write(output / 'final-classification-decisions-1301.json', detailed)
    csvwrite(output / 'independent-ratings-and-adjudication-1301.csv', pairs); csvwrite(output / 'classification-evidence-quotes-1709.csv', evidence)
    write(output / 'classification-summary-included-identifiers-1301.json', summary)
    return rows


def analysis(output, rows):
    analyzed = [r for r in rows if r['classification'] != 'not_evidenced']
    csvwrite(output / 'literature-with-layer-labels-771.csv', analyzed)
    csvwrite(output / 'literature-with-layer-labels-2023-onward-207.csv', [r for r in analyzed if r['year'] >= 2023])
    table = []
    for name, period in [('before_2023', [r for r in analyzed if r['year'] < 2023]),
                         ('2023_onward', [r for r in analyzed if r['year'] >= 2023])]:
        for layer in LAYERS:
            count = sum(r[layer] for r in period)
            table.append({'period': name, 'layer': layer, 'records': count, 'denominator': len(period), 'share': count/len(period)})
    csvwrite(output / 'layer-counts-and-shares-by-period-16.csv', table)
    csvwrite(output / 'labeled-literature-counts-by-source-4.csv', [{'source': s, 'analyzed': sum(r['source'] == s for r in analyzed)} for s in SOURCES])


def generate(output):
    output.mkdir(parents=True, exist_ok=True)
    sources = read(TAX / '02-source-evidence/records.json')
    results = output / '04-final-selection'
    results.mkdir(parents=True, exist_ok=True)
    included, _ = selection(results, sources, read(TAX / '03-screening-review/records.json'))
    population = prepare(results, sources, included)
    rows = annotation(results, population)
    analysis(results, rows)
    return rows


def compare_outputs(output):
    expected = [TAX / 'included-literature-classifications-1301.csv']
    expected.extend(sorted((TAX / '04-final-selection').glob('*')))
    for p in expected:
        if p.suffix not in {'.csv', '.json'}: continue
        other = output / p.relative_to(TAX)
        require(other.is_file(), f'Missing regenerated output: {p.name}')
        require(other.read_bytes() == p.read_bytes(), f'Regenerated output differs: {p.name}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path, help='New or empty directory outside this package')
    parser.add_argument('--taxonomy-only', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--validate-job', help='Check one saved A/B/C job against the distributed evidence')
    args = parser.parse_args()
    output = args.output.resolve()
    require(not output.is_relative_to(PACKAGE), 'Output must be outside the release package')
    require(not output.exists() or not any(output.iterdir()), 'Output must be new or empty')
    if args.validate_job:
        output.mkdir(parents=True, exist_ok=True)
        sources = read(TAX / '02-source-evidence/records.json')
        included, _ = selection(output, sources, read(TAX / '03-screening-review/records.json'))
        population = prepare(output, sources, included)
        annotation(output, population, only_job=args.validate_job)
        return
    rows = generate(output / 'taxonomy')
    compare_outputs(output / 'taxonomy')
    print(json.dumps({'included_identifiers': len(rows), 'analyzed': sum(r['classification'] != 'not_evidenced' for r in rows),
                      'recent_analyzed': sum(r['classification'] != 'not_evidenced' and r['year'] >= 2023 for r in rows),
                      'api_calls': 0, 'output': str(output)}, indent=2))


if __name__ == '__main__':
    main()
