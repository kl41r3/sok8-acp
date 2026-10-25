#!/usr/bin/env python3
"""Render retained Workshop charts from the freshly reconstructed score table."""
import argparse
import csv
import json
from pathlib import Path
from types import SimpleNamespace

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import Patch, Rectangle

import plot_style
from plot_style import C, ORIGIN_COLOR, mix, new_fig

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scores', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    scores = list(csv.DictReader(args.scores.open()))
    meta = json.loads((ROOT / '02-judgments/protocols.json').read_text())
    assert [r['protocol'] for r in scores] == [r['protocol'] for r in meta]
    dims = ['C', 'I', 'A', 'EM', 'S']
    for r, m in zip(scores, meta):
        assert r['layer'] == m['layer'] and float(r['total']) == sum(float(r[d]) for d in dims)
    data = SimpleNamespace(PROTOCOLS=[(r['protocol'], r['layer'], m['origin'], [float(r[d]) for d in dims], float(r['total'])) for r, m in zip(scores, meta)], SCORE_DIMS=dims)
    output = args.output.resolve()
    assert not output.is_relative_to(ROOT.parent), 'Plot output must be outside this package'
    output.mkdir(parents=True, exist_ok=True)
    plot_style.apply_style()
    # Use the bundled font, stable IDs, and no clock metadata for byte-identical exports.
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'svg.hashsalt': 'neurips-workshop-scorecard-v1'})

    def save(fig, stem):
        for ext in ['pdf', 'svg', 'png']:
            metadata = {'CreationDate': None, 'ModDate': None} if ext == 'pdf' else {'Date': None} if ext == 'svg' else None
            fig.savefig(output / f'{stem}.{ext}', dpi=300, bbox_inches='tight', pad_inches=0.03,
                        facecolor=C['paper'], edgecolor=C['paper'], metadata=metadata)
        plt.close(fig)

    namespace = dict(np=np, plt=plt, to_rgb=to_rgb, Patch=Patch, Rectangle=Rectangle,
                     C=C, ORIGIN_COLOR=ORIGIN_COLOR, mix=mix, new_fig=new_fig, save=save,
                     D=data, W=3.42, W_FULL=5.55)
    exec(compile((ROOT / '04-code/geometry.py').read_text(), 'geometry.py', 'exec'), namespace)
    namespace['fig_scorecard']()
    namespace['fig_radars']()
    fig = namespace['_origin_strip'](3.82, 1.52, radar_w=0.276, key_w=0.168, g_in=0.014, gap=0.028, stacked=False)
    save(fig, 'origin-radar-overlay')


if __name__ == '__main__':
    main()
