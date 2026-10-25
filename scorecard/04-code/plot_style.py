"""Publication style shared by every demo figure.

Palette is the retained Workshop color card. Neutrals stay off-card so
labels remain black on white. Craft (white field, vector export, dual
encoding, compact canvas) follows Chen Liu's figures4papers conventions:
https://github.com/ChenLiu-1996/figures4papers
"""

from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgb


ROOT = Path(__file__).resolve().parent
FIGDIR = ROOT / "figures"

# AGENTS.md Color Card
# #a30543  #f36f43  #fbda83  #e9f4a3  #80cba4  #4965b0
C = {
    "wine": "#a30543",
    "coral": "#f36f43",
    "gold": "#fbda83",
    "lime": "#e9f4a3",
    "mint": "#80cba4",
    "blue": "#4965b0",
    "ink": "#1A1A1A",
    "muted": "#5A5A5A",
    "rule": "#B5B5B5",
    "grid": "#E6E6E6",
    "paper": "#FFFFFF",
}

# Semantic aliases used by the figures
C["webtwo"] = C["coral"]
C["webthree"] = C["blue"]
C["hybrid"] = C["mint"]
C["exante"] = C["gold"]
C["interim"] = C["coral"]
C["expost"] = C["wine"]
C["ok"] = C["mint"]
C["alert"] = C["wine"]
C["amber"] = C["gold"]


def apply_style() -> None:
    mpl.rcParams.update(
        {
            "font.family": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "font.size": 10,
            "axes.titlesize": 10.5,
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 8.5,
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.edgecolor": C["ink"],
            "axes.labelcolor": C["ink"],
            "xtick.color": C["ink"],
            "ytick.color": C["ink"],
            "text.color": C["ink"],
            "figure.facecolor": C["paper"],
            "axes.facecolor": C["paper"],
            "savefig.facecolor": C["paper"],
            "savefig.edgecolor": C["paper"],
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "legend.frameon": False,
            "axes.unicode_minus": False,
            "hatch.linewidth": 0.6,
        }
    )


def new_fig(width: float, height: float):
    fig = plt.figure(figsize=(width, height), facecolor=C["paper"], dpi=150)
    fig.patch.set_facecolor(C["paper"])
    return fig


def save(fig, stem: str) -> None:
    FIGDIR.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "png", "svg"):
        fig.savefig(
            FIGDIR / f"{stem}.{ext}",
            dpi=300,
            bbox_inches="tight",
            pad_inches=0.03,
            facecolor=C["paper"],
            edgecolor=C["paper"],
        )
    plt.close(fig)


def mix(hex_color: str, white_w: float) -> str:
    r, g, b = to_rgb(hex_color)
    r = r * (1 - white_w) + white_w
    g = g * (1 - white_w) + white_w
    b = b * (1 - white_w) + white_w
    return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))


C["gap"] = mix(C["wine"], 0.88)


def sequential_card() -> LinearSegmentedColormap:
    return LinearSegmentedColormap.from_list(
        "cardseq",
        [C["paper"], C["lime"], C["mint"], C["blue"]],
    )


def panel_label(ax, letter: str, x: float = -0.02, y: float = 1.08) -> None:
    ax.text(
        x,
        y,
        f"({letter})",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        fontsize=11,
        fontweight="bold",
        color=C["ink"],
        clip_on=False,
    )


PHASE_COLOR = {
    "ex ante": C["exante"],
    "interim": C["interim"],
    "ex post": C["expost"],
}

ORIGIN_COLOR = {
    "Web2": C["webtwo"],
    "Web3": C["webthree"],
    "Hybrid": C["hybrid"],
}

VERDICT_COLOR = {
    "Strong": C["ok"],
    "Partial": C["amber"],
    "Weak": C["interim"],
    "Unoccupied": C["alert"],
}
