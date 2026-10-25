"""Shared scientific figure styling and deterministic, anonymous exports."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.text import Text

INK = "#18324A"
BLUE = "#245F8B"
GREEN = "#298263"
BURGUNDY = "#A30543"


def setup():
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 9,
        "axes.labelsize": 9, "axes.titlesize": 10,
        "xtick.labelsize": 8.3, "ytick.labelsize": 8.3,
        "legend.fontsize": 8.3, "pdf.fonttype": 42,
        "svg.fonttype": "none", "svg.hashsalt": "economic-model-extensions",
        "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": INK,
        "axes.linewidth": .7, "savefig.facecolor": "white",
    })


def export(fig, directory, stem):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    fig.canvas.draw()
    texts = [t for t in fig.findobj(match=lambda t: isinstance(t, Text))
             if t.get_visible() and t.get_text().strip()]
    minimum = min(t.get_fontsize() for t in texts)
    if minimum < 8:
        raise ValueError("Figure contains text smaller than 8 pt")
    renderer = fig.canvas.get_renderer()
    for text in texts:
        box = text.get_window_extent(renderer)
        if (box.x0 < -1 or box.y0 < -1 or box.x1 > fig.bbox.width+1
                or box.y1 > fig.bbox.height+1):
            raise ValueError("Text outside figure canvas: " + text.get_text())
    for ext in ("pdf", "svg", "png"):
        metadata = ({"Creator": "Scientific model figure", "Author": "",
                     "CreationDate": None, "ModDate": None} if ext == "pdf"
                    else {"Date": None} if ext == "svg" else {})
        fig.savefig(directory / f"{stem}.{ext}", dpi=300, metadata=metadata)
    width, height = fig.get_size_inches()
    plt.close(fig)
    return {"stem": stem, "width_inches": float(width), "height_inches": float(height),
            "minimum_font_points_at_native_size": minimum,
            "formats": ["pdf", "svg", "png"], "text_within_canvas": True,
            "visual_quantity": "deterministic model output"}


def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")
