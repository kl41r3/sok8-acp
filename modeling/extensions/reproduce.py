#!/usr/bin/env python3
"""Verify and regenerate the additive Case A/B extensions and manuscript figures."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(args, env):
    result = subprocess.run([sys.executable, "-B", *map(str, args)],
                            cwd=ROOT, env=env, text=True, capture_output=True)
    if result.returncode:
        print(result.stdout, file=sys.stderr)
        print(result.stderr, file=sys.stderr)
        result.check_returncode()


def protected_baseline():
    inventory = read(ROOT / "modeling/extensions/baseline-files.json")
    for name, expected in inventory["protected_files"].items():
        require(sha(ROOT / name) == expected, "Original file changed: " + name)
    return len(inventory["protected_files"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "outputs/model-extensions")
    parser.add_argument("--exact-figures", action="store_true",
                        help="Also require byte-identical PDF/SVG/PNG exports.")
    args = parser.parse_args()
    out = args.output.resolve()
    require(not out.exists(), "Choose a new output directory.")
    protected = protected_baseline()
    out.mkdir(parents=True)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1",
               MPLCONFIGDIR=str(out / ".mpl-cache"), XDG_CACHE_HOME=str(out / ".cache"))
    summary = {"protected_original_files_byte_identical": protected}
    identical = 0
    specifications = [
        ("case_a_costly_fallback", "modeling/case-a/fallback", "case-a-costly-fallback",
         ["decision-grid.csv", "cost-sensitivity.csv", "summary.json"]),
        ("case_b_evidence_loss", "modeling/case-b/evidence-loss", "case-b-evidence-loss",
         ["main-grid.csv", "cost-horizon-sensitivity.csv", "control-cells.csv",
          "round-paths.csv", "representative-solutions.json", "summary.json"]),
    ]
    for key, source, folder, files in specifications:
        generated = out / folder
        run([ROOT / source / "analyze.py", "--output", generated], env)
        for name in files:
            require(sha(generated / name) == sha(ROOT / source / "results" / name),
                    "Extension result differs: " + source + "/" + name)
            identical += 1
        validation = read(generated / "validation.json")
        require(validation["passed"], "Extension verification failed: " + key)
        for figure in validation["figures"]:
            require(figure["minimum_font_points_at_native_size"] >= 8
                    and figure["text_within_canvas"], "Invalid figure specification")
            for extension in figure["formats"]:
                require((generated / (figure["stem"] + "." + extension)).is_file(),
                        "Missing diagnostic figure export")
        summary[key] = validation
    summary["generated_datasets_byte_identical"] = identical
    generated = out / "manuscript-figures"
    run([ROOT / "modeling/figures/build.py", "--output", generated], env)
    audit = read(generated / "verification.json")
    require(audit["passed"] and len(audit["figures"]) == 4, "Manuscript figure audit")
    for spec in audit["figures"]:
        require(spec["width_inches"] == 3.3 and spec["minimum_font_points"] >= 8
                and spec["text_within_canvas"] and not spec["embedded_captions"]
                and not spec["embedded_titles"], "Invalid one-column layout")
    expected = ROOT / "figures/modeling"
    exports = sorted(p for p in expected.rglob("*")
                     if p.is_file() and p.suffix in {".pdf", ".png", ".svg"})
    require(len(exports) == 12, "Expected four figures in three formats")
    identical_exports = 0
    for path in exports:
        rel = path.relative_to(expected)
        require((generated / rel).is_file(), "Missing manuscript export: " + str(rel))
        identical_exports += sha(generated / rel) == sha(path)
    require(read(expected / "verification.json") == audit, "Figure audit differs")
    if args.exact_figures:
        require(identical_exports == len(exports), "Manuscript export bytes differ")
    summary["manuscript_figures"] = {"figures": audit["figures"],
                                     "exports_generated": len(exports),
                                     "exports_byte_identical": identical_exports,
                                     "exact_bytes_required": args.exact_figures,
                                     "passed": True}
    summary["api_calls"] = 0
    summary["passed"] = True
    (out / "verification.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
