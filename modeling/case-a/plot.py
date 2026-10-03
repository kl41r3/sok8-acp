#!/usr/bin/env python3
from pathlib import Path
import csv
import hashlib
import json
import importlib.metadata as md
import numpy as np
from plot_utils import load_theme,apply_theme,save_figure,finish_axes
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
ROOT=Path(__file__).resolve().parent
DATA=ROOT/'data'
FIG=ROOT/'figures'
FIG.mkdir(exist_ok=True)


def main():
    theme=load_theme(ROOT/'theme.yaml');apply_theme(theme)
    data=np.load(DATA/'independent-grid.npz');q=data['q'];d=data['d']
    colors=['#4965b0','#80cba4','#e9f4a3','#fbda83','#f36f43','#a30543']
    cmap=LinearSegmentedColormap.from_list('SoK magnitude',colors)
    fig,axes=plt.subplots(1,2,figsize=(7,3.4),layout='constrained')
    for ax,key,title,maxval,label in zip(axes,['mean_user_loss','review_share'],
                                         ['Expected user loss L(q,d)','Review share R(q,d)'],[.34,100],['Loss','Percent']):
        z=data[key]*(100 if key=='review_share' else 1)
        im=ax.pcolormesh(q,d,z.T,shading='nearest',cmap=cmap,vmin=0,vmax=maxval,rasterized=True)
        ax.set_title(title);ax.set_xlabel('Timely review probability q');ax.set_ylabel('Autonomy cap d')
        ax.set_xlim(0,1);ax.set_ylim(0,1.2);ax.set_xticks([0,.5,1]);ax.set_yticks([0,.4,.8,1.2]);ax.grid(False)
        fig.colorbar(im,ax=ax,label=label,shrink=.9)
    save_figure(fig,FIG/'independent-qd-heatmaps',theme)
    fig.savefig(FIG/'heatmaps-final-size.png',dpi=150)
    # These slices hold d fixed over the entire q range.
    slices=list(csv.DictReader((DATA/'fixed-d-slices.csv').open()))
    ds=sorted({float(r['d']) for r in slices})
    fig2,axes2=plt.subplots(1,2,figsize=(7,3),layout='constrained')
    for i,di in enumerate(ds):
        rows=[r for r in slices if float(r['d'])==di]
        for ax,key,scale in zip(axes2,['mean_user_loss','review_share'],[1,100]):
            ax.plot([float(r['q']) for r in rows],[float(r[key])*scale for r in rows],
                    color=['#4965b0','#a30543','#f36f43','#80cba4'][i],
                    linestyle=['-','--','-.',':'][i],label=f'd = {di:g}')
    for ax,title,ylabel in zip(axes2,['User loss at fixed d','Review share at fixed d'],['Expected loss','Percent']):
        ax.set_title(title);ax.set_xlabel('Timely review probability q');ax.set_ylabel(ylabel)
        ax.set_xlim(0,1);ax.set_xticks([0,.5,1]);finish_axes(ax);ax.legend(frameon=False)
    save_figure(fig2,FIG/'fixed-d-curves',theme)
    fig2.savefig(FIG/'curves-final-size.png',dpi=150)
    audit={'status':'Pending visual inspection','figures':['independent-qd-heatmaps','fixed-d-curves'],
           'width_inches':7,'minimum_text_pt':8,'theme':'Scholar Blue 1.1.0 with preserved SoK palette',
           'data_pairs':int(data['mean_user_loss'].size),'d_optimization':False,
           'heatmap_axes':{'x':'q, fixed independently from d','y':'d, fixed independently from q'},
           'uncertainty':'Deterministic analytic expectations; no empirical confidence intervals',
           'heatmap_rendering':'Rasterized cells in PDF/SVG, vector labels; complete numeric matrix retained in CSV/NPZ',
           'dependencies':{m:md.version(m) for m in ['numpy','matplotlib','PyYAML']},
           'CSV_sha256':hashlib.sha256((DATA/'independent-grid.csv').read_bytes()).hexdigest()}
    (FIG/'figure-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    print('Generated basic two-parameter heatmaps and fixed-d curves, each in PNG/PDF/SVG.')


if __name__=='__main__':main()
