#!/usr/bin/env python3
"""Shared theme, sizing, legibility, and export helpers for paper figures."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.text import Text
import yaml

DEFAULT_THEME = Path(__file__).resolve().parent / "theme.yaml"


def load_theme(path: str | Path = DEFAULT_THEME) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def apply_theme(theme: dict[str, Any]) -> None:
    colors = theme["colors"]
    typo = theme["typography"]
    lines = theme["lines"]
    plt.rcParams.update(
        {
            "font.family": typo["family"],
            "font.size": typo["tick_pt"],
            "axes.labelsize": typo["label_pt"],
            "axes.titlesize": typo["title_pt"],
            "xtick.labelsize": typo["tick_pt"],
            "ytick.labelsize": typo["tick_pt"],
            "legend.fontsize": typo["legend_pt"],
            "text.color": colors["ink"],
            "axes.labelcolor": colors["ink"],
            "axes.edgecolor": colors["ink"],
            "xtick.color": colors["ink"],
            "ytick.color": colors["ink"],
            "axes.linewidth": lines["axis_width"],
            "axes.grid": True,
            "axes.axisbelow": True,
            "grid.color": colors["divider"],
            "grid.linewidth": lines["grid_width"],
            "grid.alpha": 0.55,
            "lines.linewidth": lines["data_width"],
            "lines.markersize": lines["marker_size"],
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )


def figure_size(theme: dict[str, Any], placement: str = "single", height_ratio: float | None = None) -> tuple[float, float]:
    key = {
        "single": "single_column_in",
        "intermediate": "intermediate_in",
        "double": "double_column_in",
    }[placement]
    width = float(theme["sizes"][key])
    ratio = float(height_ratio or theme["sizes"]["aspect_ratio"])
    return width, width * ratio


def style_series(theme: dict[str, Any], index: int) -> dict[str, Any]:
    colors = theme["categorical"]
    return {
        "color": colors[index % len(colors)],
        "linestyle": theme["linestyles"][index % len(theme["linestyles"])],
        "marker": theme["markers"][index % len(theme["markers"])],
    }


def finish_axes(ax: Any, *, grid_axis: str = "y") -> None:
    ax.grid(True, axis=grid_axis)
    ax.grid(False, axis="x" if grid_axis == "y" else "y")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)


def assert_legibility(fig: Any, minimum_pt: float = 8.0) -> None:
    violations: list[str] = []
    for item in fig.findobj(match=lambda artist: isinstance(artist, Text)):
        if not item.get_visible() or not item.get_text().strip():
            continue
        size = float(item.get_fontsize())
        if size + 1e-9 < minimum_pt:
            snippet = item.get_text().replace("\n", " ")[:40]
            violations.append(f"{size:g} pt: {snippet!r}")
    if violations:
        raise ValueError("Final-size legibility gate failed: " + "; ".join(violations))


def save_figure(fig: Any, output_stem: str | Path, theme: dict[str, Any]) -> list[Path]:
    minimum = float(theme["typography"]["minimum_pt"])
    assert_legibility(fig, minimum)
    stem = Path(output_stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    for suffix, options in (
        (".pdf", {}),
        (".svg", {}),
        (".png", {"dpi": int(theme["export"]["png_dpi"])}),
    ):
        path = stem.with_suffix(suffix)
        fig.savefig(path, bbox_inches="tight", pad_inches=0.04, **options)
        outputs.append(path)
    return outputs
