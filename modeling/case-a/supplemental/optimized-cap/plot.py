#!/usr/bin/env python3
"""Minimal three-panel figure; all values are read from saved results."""
from pathlib import Path
import sys
import json
import csv
import hashlib
import importlib.metadata as md

ROOT=Path(__file__).resolve().parent
from plot_utils import load_theme,apply_theme,finish_axes,save_figure
import matplotlib.pyplot as plt
import numpy as np


def main():
    theme=load_theme(ROOT/'theme.yaml');apply_theme(theme)
    rows=list(csv.DictReader((ROOT/'continuous-results.csv').open()))
    summary=json.loads((ROOT/'summary.json').read_text())
    q=np.array([float(r['q']) for r in rows]);qc=summary['q_critical']
    no_review=np.array([r['regime']=='no_review' for r in rows])
    old=list(csv.DictReader((ROOT.parent/'five-q/grid_optima.csv').open()))
    specs=[('d','Optimal cap',1),('mean_user_loss','Expected user loss',1),('review_share','Review share (%)',100)]
    fig,axes=plt.subplots(1,3,figsize=(7,2.8))
    for ax,(key,title,scale) in zip(axes,specs):
        ys=np.array([float(r[key])*scale for r in rows])
        if key=='mean_user_loss':
            ax.plot(q,ys,color='#4965b0')
        else:
            for mask,branch in [(no_review,'no_review'),(~no_review,'review')]:
                x=list(q[mask]);y=list(ys[mask]);v=summary['at_switch'][branch][key]*scale
                if branch=='no_review':x.append(qc);y.append(v)
                else:x.insert(0,qc);y.insert(0,v)
                ax.plot(x,y,color='#4965b0')
                ax.plot(qc,v,'o',mfc='white',mec='#4965b0',ms=4)
        ax.axvline(qc,color='#a30543',ls='--',lw=1)
        ax.plot([float(r['q']) for r in old],[float(r[key])*scale for r in old],
                'o',color='#f36f43',ms=4,linestyle='none')
        ax.set_title(title);ax.set_xlabel('Timely review probability q')
        ax.set_xlim(0,1.01);ax.set_xticks([0,.5,1]);finish_axes(ax)
    axes[0].set_ylim(0,1);axes[2].set_ylim(-2,100)
    fig.suptitle(f'Case A: continuous cap optimization; switch at q = {qc:.4f}',fontsize=11)
    fig.tight_layout(rect=(0,0,1,.88))
    outputs=save_figure(fig,ROOT/'case-a-continuous',theme)
    # A 7-inch, 150-dpi check preview, separate from the 300-dpi deliverable.
    fig.savefig(ROOT/'final-size-preview.png',dpi=150)
    receipt={'status':'Pending visual inspection','width_inches':7,'minimum_font_pt':8,
             'theme':'Scholar Blue 1.1.0, project-palette override',
             'theme_sha256':hashlib.sha256((ROOT/'theme.yaml').read_bytes()).hexdigest(),
             'data_sha256':hashlib.sha256((ROOT/'continuous-results.csv').read_bytes()).hexdigest(),
             'source_q_rows':len(rows),'figure_type':'three basic line plots; optimal-policy jumps are not smoothed',
             'encodings':{'blue':'continuous-cap numerical optimum','orange_markers':'previous five discrete-grid observations','red_dashed':'equal-loss strategy switch'},
             'uncertainty':'Deterministic analytic integration and numerical optimization; no empirical confidence intervals',
             'dependencies':{m:md.version(m) for m in ['numpy','matplotlib','PyYAML']},
             'outputs':[p.name for p in outputs]}
    (ROOT/'figure-audit.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print('Created PDF, SVG, PNG and final-size preview from saved CSV.')


if __name__=='__main__':main()
