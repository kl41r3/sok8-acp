# Manuscript modeling figures

These are the four final, caption-free layouts prepared for one-column LaTeX
placement. They reuse the verified frozen extension datasets; exporting a
figure does not rerun or change either economic model.

| Export | Role | Frozen input |
|---|---|---|
| `case-a-review-fallback.pdf` | Main Case A comparison | `modeling/case-a/fallback/results/decision-grid.csv` |
| `case-b-evidence-loss.pdf` | Main Case B comparison | `modeling/case-b/evidence-loss/results/main-grid.csv` |
| `app-case-a-review-costs.pdf` | Supporting cost sensitivity | `modeling/case-a/fallback/results/cost-sensitivity.csv` |
| `app-case-b-effort-sensitivity.pdf` | Supporting effort sensitivity | `modeling/case-b/evidence-loss/results/main-grid.csv` and `cost-horizon-sensitivity.csv` |

## Regenerate

With the root `requirements.txt` installed in Python 3.12:

```sh
python -B modeling/figures/build.py --output outputs/manuscript-figures
```

Choose a new output directory. The script resolves paths from its own location,
so it can also be invoked by absolute path from another working directory.
It verifies each input CSV against the root integrity manifest and exports
four PDFs plus editable SVGs and PNG previews in `previews/`. Its
`verification.json` records input hashes, figure dimensions, font minima,
and checks for clipped text and embedded captions or titles.

Frozen copies are in `figures/modeling/`. Each PDF is 3.30 inches wide, with
text at least eight points at native size. The repository reproduction command
regenerates all twelve exports, checks the layout audit, and reports byte
agreement with these copies. Rendering bytes can vary by platform; use the
extension runner's `--exact-figures` flag to enforce an identical build.
In LaTeX, use `figure` with
`\includegraphics[width=\columnwidth]{...}` and supply captions separately.
Panel letters, axis labels, and legends remain inside the figures.

The wider diagnostic plots in each extension's `results/` directory are
preserved separately. The original Case A and Case B baseline plots are also
unchanged. All figures illustrate conditional model outputs, not measured
behavior or estimated transaction frequencies.
