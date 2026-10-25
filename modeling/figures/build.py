#!/usr/bin/env python3
"""Export the four caption-free manuscript figures at native one-column width.

Reads hash-checked frozen model datasets; never changes model calculations.
Run from any directory with Python 3.12 and the root requirements installed.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.text import Text

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "modeling/extensions"))
from plot_style import setup, INK, BLUE, BURGUNDY

setup()
plt.rcParams.update({"font.size": 8.1, "axes.labelsize": 8.5,
                     "xtick.labelsize": 8.1, "ytick.labelsize": 8.1,
                     "legend.fontsize": 8.0})
WIDTH = 3.30
SPECS = []
INPUTS = []


def data(root, relative):
    path = root / relative
    manifest = json.loads((root / "MANIFEST.json").read_text())
    expected = next(r["sha256"] for r in manifest["files"] if r["path"] == relative)
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError("Frozen input changed: " + relative)
    INPUTS.append({"path": relative, "sha256": actual})
    with path.open(newline="") as stream:
        return list(csv.DictReader(stream))


def panel(ax, label):
    ax.text(.025, .96, label, transform=ax.transAxes, va="top", ha="left",
            fontsize=9, fontweight="bold",
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": .9, "pad": 2})


def save(fig, output, stem, input_rows):
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    texts = [t for t in fig.findobj(match=lambda x: isinstance(x, Text))
             if t.get_visible() and t.get_text().strip()]
    minimum = min(t.get_fontsize() for t in texts)
    if minimum < 8:
        raise AssertionError("Font below 8 pt")
    for t in texts:
        box = t.get_window_extent(renderer)
        if box.x0 < -1 or box.y0 < -1 or box.x1 > fig.bbox.width+1 or box.y1 > fig.bbox.height+1:
            raise AssertionError("Clipped label: " + t.get_text())
    if fig.texts or any(ax.get_title() for ax in fig.axes):
        raise AssertionError("Embedded title or caption")
    output.mkdir(parents=True, exist_ok=True)
    preview = output / "previews"
    preview.mkdir(exist_ok=True)
    fig.savefig(output/(stem+".pdf"), dpi=300,
                metadata={"Author": "", "Creator": "Scientific model figure",
                          "CreationDate": None, "ModDate": None})
    fig.savefig(preview/(stem+".png"), dpi=200)
    fig.savefig(preview/(stem+".svg"), metadata={"Date": None})
    SPECS.append({"file": stem+".pdf", "width_inches": float(fig.get_size_inches()[0]),
                  "height_inches": float(fig.get_size_inches()[1]),
                  "minimum_font_points": minimum, "input_rows": input_rows,
                  "embedded_titles": False, "embedded_captions": False,
                  "text_within_canvas": True})
    plt.close(fig)


def matrix(rows, xkey, ykey, value):
    xs = sorted({float(r[xkey]) for r in rows})
    ys = sorted({float(r[ykey]) for r in rows})
    look = {(float(r[xkey]), float(r[ykey])): float(r[value]) for r in rows}
    if len(look) != len(xs)*len(ys):
        raise ValueError("Incomplete or duplicate grid")
    return *np.meshgrid(xs, ys), np.array([[look[x, y] for x in xs] for y in ys])


def main():
    global SPECS, INPUTS
    SPECS, INPUTS = [], []
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPO / "outputs/manuscript-figures")
    args = parser.parse_args()
    OUT = args.output.resolve()
    if OUT.exists():
        raise ValueError("Choose a new output directory.")
    rows=data(REPO,"modeling/case-a/fallback/results/decision-grid.csv")
    names=["autonomy_no_user_gain","autonomy_user_would_benefit","review_user_benefits",
           "review_user_harmed","review_user_indifferent"]
    colors=["#E8EDF2","#F0C66C","#92CBB5","#C66582","#C7BBDA"]
    fig=plt.figure(figsize=(WIDTH,4.25))
    axes=[fig.add_axes([.19,.66,.78,.30]),fig.add_axes([.19,.32,.78,.30])]
    for ax,policy,tag in zip(axes,["CANCEL","FALLBACK"],["(a)","(b)"]):
        part=[dict(r,number=names.index(r["region"])) for r in rows if r["policy"]==policy]
        X,Q,Z=matrix(part,"cap_ratio","q","number")
        ax.pcolormesh(X,Q,Z,cmap=ListedColormap(colors),
                      norm=BoundaryNorm(np.arange(-.5,5.5,1),5),shading="nearest",rasterized=True)
        _,_,agent=matrix(part,"cap_ratio","q","agent_review_gain")
        _,_,user=matrix(part,"cap_ratio","q","user_review_gain")
        ax.contour(X,Q,agent,levels=[0],colors=[INK],linewidths=1)
        ax.contour(X,Q,user,levels=[0],colors=[BURGUNDY],linewidths=1,linestyles="--")
        ax.set(xlim=(0,1.2),ylim=(0,1),ylabel=r"Review probability, $q$")
        ax.set_xticks([0,.3,.6,.9,1.2]);ax.set_yticks([0,.5,1])
        panel(ax,tag)
    axes[0].tick_params(labelbottom=False)
    axes[1].set_xlabel(r"Relative cap, $d/\theta$")
    handles=[Patch(facecolor=c) for c in colors]+[
        Line2D([],[],color=INK,linewidth=1),
        Line2D([],[],color=BURGUNDY,linewidth=1,linestyle="--")]
    labels=["No review; no gain","No review; user gains","Review; user gains",
            "Review; user harmed","Review; user indifferent","Agent indifference","User indifference"]
    fig.legend(handles,labels,loc="lower center",bbox_to_anchor=(.5,.012),ncol=2,
               frameon=False,fontsize=8,handlelength=1.1,columnspacing=.7,handletextpad=.4)
    save(fig,OUT,"case-a-review-fallback",len(rows))

    rows=data(REPO,"modeling/case-a/fallback/results/cost-sensitivity.csv")
    fig=plt.figure(figsize=(WIDTH,2.40))
    axes=[fig.add_axes([.18,.44,.32,.51]),fig.add_axes([.63,.44,.32,.51])]
    for ax,policy,tag in zip(axes,["CANCEL","FALLBACK"],["(a)","(b)"]):
        part=[r for r in rows if r["policy"]==policy]
        X,Y,Z=matrix(part,"user_cost","agent_cost","harmful_interval_width")
        im=ax.pcolormesh(X,Y,Z,cmap="RdPu",vmin=0,vmax=1,shading="nearest",rasterized=True)
        ax.set(xlabel=r"$\kappa/\theta^2$")
        ax.set_xticks([0,.15,.3]);ax.set_xticklabels(["0",".15",".3"])
        ax.set_yticks([0,.15,.3]);ax.set_yticklabels(["0",".15",".3"])
        panel(ax,tag)
    axes[0].set_ylabel(r"$\eta/\theta^2$")
    cb=fig.colorbar(im,cax=fig.add_axes([.26,.19,.61,.045]),orientation="horizontal",ticks=[0,.5,1])
    cb.set_label("Harmful interval width",fontsize=8)
    save(fig,OUT,"app-case-a-review-costs",len(rows))

    rows=data(REPO,"modeling/case-b/evidence-loss/results/main-grid.csv")
    strict=[r for r in rows if r["policy"]=="STRICT" and r["initial"]=="G"]
    fig=plt.figure(figsize=(WIDTH,3.65))
    axes=[fig.add_axes([.18,.58,.59,.38]),fig.add_axes([.18,.15,.59,.38])]
    cbaxes=[fig.add_axes([.81,.58,.025,.38]),fig.add_axes([.81,.15,.025,.38])]
    for ax,cax,key,tag,cmap,low,high,ticks,label in [
        (axes[0],cbaxes[0],"success","(a)","YlGnBu",30,82.5,[30,60,82.5],"Task success (%)"),
        (axes[1],cbaxes[1],"successful_task_bad_update_due_to_loss","(b)","RdPu",0,50,[0,25,50],"Adverse updates (%)"),
    ]:
        X,Y,Z=matrix(strict,"epsilon","rho",key)
        im=ax.pcolormesh(X,Y,100*Z,cmap=cmap,vmin=low,vmax=high,shading="nearest",rasterized=True)
        ax.set(xlim=(0,1),ylim=(0,1),ylabel=r"Monitoring, $\rho$")
        ax.set_xticks([0,.25,.5,.75,1]);ax.set_yticks([0,.5,1])
        cb=fig.colorbar(im,cax=cax,ticks=ticks)
        cb.set_label(label,fontsize=8.1);cb.ax.tick_params(labelsize=8.1)
        panel(ax,tag)
    axes[0].tick_params(labelbottom=False)
    axes[1].set_xlabel(r"Evidence loss, $\varepsilon$")
    save(fig,OUT,"case-b-evidence-loss",len(rows))

    supporting=data(REPO,"modeling/case-b/evidence-loss/results/cost-horizon-sensitivity.csv")
    fig=plt.figure(figsize=(WIDTH,4.2))
    axes=[fig.add_axes([.18,.64,.79,.32]),fig.add_axes([.18,.16,.79,.31])]
    for rho,color in [(.25,BLUE),(.5,BURGUNDY),(1,"#298263")]:
        line=sorted([r for r in strict if float(r["rho"])==rho],key=lambda r:float(r["epsilon"]))
        axes[0].plot([float(r["epsilon"]) for r in line],[100*float(r["high_effort"]) for r in line],
                     color=color,linewidth=1.4,marker="o",markersize=2,label=fr"$\rho={rho:g}$")
    axes[0].axhline(0,color="#6B7280",linestyle="--",linewidth=1,label="HOLD")
    axes[0].set(xlabel=r"Evidence loss, $\varepsilon$",ylabel="High-effort tasks (%)",
                xlim=(0,1),ylim=(-3,100))
    axes[0].set_xticks([0,.25,.5,.75,1]);axes[0].set_xticklabels(["0",".25",".5",".75","1"])
    axes[0].set_yticks([0,50,100])
    fig.legend(*axes[0].get_legend_handles_labels(),loc="lower center",bbox_to_anchor=(.55,.50),
               ncol=4,frameon=False,fontsize=8,handlelength=.8,columnspacing=.6,handletextpad=.3)
    for cost,color in [(.05,BLUE),(.15,BURGUNDY),(.3,"#298263")]:
        line=sorted([r for r in supporting if r["policy"]=="STRICT" and r["initial"]=="G"
                     and float(r["rho"])==.25 and float(r["epsilon"])==.1
                     and float(r["high_cost"])==cost],key=lambda r:float(r["horizon"]))
        axes[1].plot([float(r["horizon"]) for r in line],[100*float(r["high_effort"]) for r in line],
                     color=color,linewidth=1.4,marker="o",markersize=2.5,label=fr"$c={cost:g}$")
    axes[1].set(xlabel="Number of rounds",ylabel="High-effort tasks (%)",ylim=(-3,100))
    axes[1].set_xticks([1,4,8,16]);axes[1].set_yticks([0,50,100])
    fig.legend(*axes[1].get_legend_handles_labels(),loc="lower center",bbox_to_anchor=(.55,.005),
               ncol=3,frameon=False,fontsize=8,handlelength=1,columnspacing=1)
    for ax,tag in zip(axes,["(a)","(b)"]):
        panel(ax,tag)
        ax.spines[["top","right"]].set_visible(False);ax.grid(axis="y",color="#DDE4EA",linewidth=.6)
    save(fig,OUT,"app-case-b-effort-sensitivity",len(supporting))
    (OUT/"verification.json").write_text(json.dumps({
        "source_inputs":INPUTS,"figures":SPECS,
        "scope":"Layout-only single-column exports of verified data; unchanged model calculations.",
        "passed":True},indent=2)+"\n")
    print(json.dumps(SPECS,indent=2))


if __name__=="__main__":
    main()
