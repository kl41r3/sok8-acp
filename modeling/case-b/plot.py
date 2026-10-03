#!/usr/bin/env python3
"""Basic Case B figure: exact optimal-policy expectations, never LLM trajectories."""
from pathlib import Path
import argparse,json,csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path,default=Path(__file__).parent/"figures");args=parser.parse_args()
    data=json.loads((Path(__file__).parent/"data/theory.json").read_text())
    ids=["VOLUNTARY","OBLIGATED_025","OBLIGATED_1","COMPLAINT_025"]
    labels=["Voluntary","Task-bound\n$\\rho=0.25$","Task-bound\n$\\rho=1$","Complaint\n$\\rho=0.25$"]
    rows=[{"policy":p,"high_effort_share":data["policies"][p]["forward"]["G"]["rates"]["high_effort"],"task_success_probability":data["policies"][p]["forward"]["G"]["rates"]["success"]} for p in ids]
    args.output.mkdir(parents=True,exist_ok=True)
    with (args.output/"plotted-values.csv").open("w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    plt.rcParams.update({"font.family":"DejaVu Sans","font.size":9,"axes.labelsize":10,"axes.titlesize":11,"legend.fontsize":9,"xtick.labelsize":9,"ytick.labelsize":9,"pdf.fonttype":42,"svg.fonttype":"none"})
    fig,ax=plt.subplots(figsize=(7,3.1));x=np.arange(4);width=.34
    for offset,key,color,hatch,label in [(-width/2,"high_effort_share","#4965b0","", "High effort"),(width/2,"task_success_probability","#f36f43","//","Task success")]:
        values=[100*r[key] for r in rows];bars=ax.bar(x+offset,values,width,color=color,hatch=hatch,label=label,edgecolor="#18324A",linewidth=.5)
        for bar,value in zip(bars,values):ax.text(bar.get_x()+bar.get_width()/2,value+1.5,f"{value:.2f}%".rstrip("0").replace(".00%","%"),ha="center",va="bottom",fontsize=9)
    ax.set_xticks(x,labels);ax.set_ylim(0,105);ax.set_ylabel("Eight-round average (%)");ax.set_yticks([0,25,50,75,100]);ax.grid(axis="y",alpha=.2);ax.set_axisbelow(True);ax.spines[["top","right"]].set_visible(False);ax.legend(loc="upper left",frameon=False,ncol=2)
    fig.tight_layout(pad=.7)
    for extension in ("pdf","svg","png"):fig.savefig(args.output/f"case-b-policy-comparison.{extension}",dpi=300,metadata={"Creator":"Matplotlib"} if extension=="pdf" else None)
    plt.close(fig)
if __name__=="__main__":main()
