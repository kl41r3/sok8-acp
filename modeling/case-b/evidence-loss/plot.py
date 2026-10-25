"""Plot generated Case B datasets; no policy values are computed here."""
from pathlib import Path
import argparse
import csv
import json
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parents[1]/"extensions"))
from plot_style import setup,export,INK,BLUE,BURGUNDY


def read_csv(path):
    with Path(path).open(newline="") as f:
        rows=list(csv.DictReader(f))
    return [{k:(v if k in ("run_id","policy","initial") else float(v)) for k,v in row.items()} for row in rows]


def plot(data,output):
    setup();data=Path(data);output=Path(output)
    rows=read_csv(data/"main-grid.csv")
    strict=[r for r in rows if r["policy"]=="STRICT" and r["initial"]=="G"]
    hold=[r for r in rows if r["policy"]=="HOLD" and r["initial"]=="G"]
    if not all(r["high_effort"]==0 and r["success"]==.3 and r["successful_task_bad_update_due_to_loss"]==0 for r in hold):
        raise AssertionError("HOLD benchmark")
    eps=sorted({r["epsilon"] for r in strict});rho=sorted({r["rho"] for r in strict})
    X,Y=np.meshgrid(eps,rho)
    def matrix(key):
        lookup={(r["rho"],r["epsilon"]):r[key] for r in strict}
        return 100*np.array([[lookup[y,x] for x in eps] for y in rho])
    fig,axes=plt.subplots(1,2,figsize=(7,3.5))
    fig.subplots_adjust(left=.085,right=.965,bottom=.26,top=.80,wspace=.42)
    for ax,key,title,cmap,vmin,vmax,ticks in [
        (axes[0],"success","(a) Actual task success","YlGnBu",30,82.5,[30,45,60,75,82.5]),
        (axes[1],"successful_task_bad_update_due_to_loss","(b) Successful task, adverse update","RdPu",0,50,[0,10,20,30,40,50]),
    ]:
        im=ax.pcolormesh(X,Y,matrix(key),cmap=cmap,vmin=vmin,vmax=vmax,shading="nearest",rasterized=True)
        ax.set_title(title,loc="left",fontsize=9.5,pad=9)
        ax.set_xlabel(r"Submitted evidence loss, $\varepsilon$")
        ax.set_xticks([0,.25,.5,.75,1]);ax.set_yticks([0,.25,.5,.75,1])
        ax.set_xlim(0,1);ax.set_ylim(0,1)
        cb=fig.colorbar(im,ax=ax,fraction=.055,pad=.04,ticks=ticks)
        cb.ax.tick_params(labelsize=8.2)
    axes[0].set_ylabel(r"Monitoring probability, $\rho$")
    fig.text(.5,.94,"Strict missing-evidence rule; eight rounds, initial reputation G",ha="center",fontsize=9)
    fig.text(.5,.105,"Colors: percent of all tasks. An adverse update need not be a G-to-B transition.",ha="center",fontsize=8.2)
    fig.text(.5,.045,"State-preserving missing rule from G: 30% task success and no loss-induced adverse updates.",ha="center",fontsize=8.2)
    main=export(fig,output,"case-b-evidence-availability")

    fig,axes=plt.subplots(1,2,figsize=(7,3.85))
    fig.subplots_adjust(left=.09,right=.98,bottom=.36,top=.82,wspace=.33)
    for r,color in [(.25,BLUE),(.5,BURGUNDY),(1,"#298263")]:
        line=sorted([row for row in strict if row["rho"]==r],key=lambda z:z["epsilon"])
        axes[0].plot([z["epsilon"] for z in line],[100*z["high_effort"] for z in line],
                     color=color,linewidth=1.7,marker="o",markersize=2.3,label=fr"$\rho={r:g}$")
    axes[0].axhline(0,color="#6B7280",linestyle="--",linewidth=1,label="Hold missing")
    axes[0].set_title("(a) Effort response to evidence loss",loc="left",fontsize=9.5)
    axes[0].set(xlabel=r"Evidence loss, $\varepsilon$",ylabel="High-effort tasks (%)",xlim=(0,1),ylim=(-2,100))
    axes[0].set_xticks([0,.25,.5,.75,1]);axes[0].set_yticks([0,25,50,75,100])
    fig.legend(*axes[0].get_legend_handles_labels(),loc="lower center",bbox_to_anchor=(.27,.09),
               ncol=2,frameon=False,fontsize=8.2,handlelength=1.3,columnspacing=1.2)
    sensitivity=read_csv(data/"cost-horizon-sensitivity.csv")
    for c,color in [(.05,BLUE),(.15,BURGUNDY),(.3,"#298263")]:
        line=sorted([r for r in sensitivity if r["policy"]=="STRICT" and r["initial"]=="G"
                     and r["rho"]==.25 and r["epsilon"]==.1 and r["high_cost"]==c],
                    key=lambda z:z["horizon"])
        axes[1].plot([z["horizon"] for z in line],[100*z["high_effort"] for z in line],
                     color=color,linewidth=1.7,marker="o",markersize=3,label=fr"$c={c:g}$")
    axes[1].set_title("(b) Cost and horizon sensitivity",loc="left",fontsize=9.5)
    axes[1].set(xlabel="Number of rounds",ylabel="High-effort tasks (%)",ylim=(-2,100))
    axes[1].set_xticks([1,4,8,16]);axes[1].set_yticks([0,25,50,75,100])
    fig.legend(*axes[1].get_legend_handles_labels(),loc="lower center",bbox_to_anchor=(.755,.12),
               ncol=3,frameon=False,fontsize=8.2,handlelength=1.0,columnspacing=.7)
    for ax in axes:
        ax.spines[["top","right"]].set_visible(False);ax.grid(axis="y",color="#DDE4EA",linewidth=.6)
    fig.text(.5,.94,"Initial G; other payoffs fixed at the baseline values",ha="center",fontsize=9)
    fig.text(.5,.025,r"Panel (b): $\rho=0.25$, $\varepsilon=0.10$. Every final round selects low effort.",ha="center",fontsize=8.2)
    support=export(fig,output,"case-b-effort-sensitivity")
    return [main,support]


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(plot(args.data,args.output),indent=2))
