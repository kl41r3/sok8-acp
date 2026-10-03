#!/usr/bin/env python3
"""Reproduce frozen taxonomy-corpus selection arithmetic without network access."""
import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("ACM", "IEEE", "AAAI", "IJCAI", "AAMAS")
OUTPUTS = ("final-selection-records.csv", "source-counts.csv",
           "identifier-selection.csv", "included-identifiers.csv", "counts.json")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_csv(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def write_csv(path, rows):
    require(bool(rows), "Unexpected empty output " + path.name)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def verify_package():
    manifest = json.loads((ROOT / "MANIFEST.json").read_text(encoding="utf-8"))
    checks = {}
    for line in (ROOT / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        require(relative not in checks, "Duplicate checksum " + relative)
        path = ROOT / relative
        require(path.resolve().is_relative_to(ROOT), "Checksum escapes package")
        require(not any(part.is_symlink() for part in (path, *path.parents) if part != ROOT and ROOT in part.parents),
                "Symlink in package path " + relative)
        require(path.is_file() and sha(path) == digest, "Checksum mismatch " + relative)
        checks[relative] = digest
    require(set(checks) == {x["path"] for x in manifest["files"]} | {"MANIFEST.json"},
            "Manifest and checksum coverage differ")
    actual_files = set()
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        require(not path.is_symlink(), "Symlink in package " + str(relative))
        if relative.parts[0] == "outputs":
            continue
        if path.is_file():
            actual_files.add(str(relative))
    require(actual_files == set(checks) | {"SHA256SUMS"},
            "Unmanifested or missing file in package")
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        require(checks[entry["path"]] == entry["sha256"] and
                path.stat().st_size == entry["bytes"], "Manifest mismatch " + entry["path"])
        if "rows" in entry:
            rows = read_csv(path)
            require(len(rows) == entry["rows"], "Row count mismatch " + entry["path"])
            require(list(rows[0]) == entry["columns"], "CSV schema mismatch " + entry["path"])
    return len(checks)


def generate(output):
    rows = read_csv(ROOT / "data/records.csv")
    overlay = read_csv(ROOT / "data/selection-overlay.csv")
    row_keys = {(r["source"], r["recordID"]) for r in rows}
    overlay_by = {(r["source"], r["recordID"]): r for r in overlay}
    require(len(row_keys) == len(rows), "Duplicate source-record key")
    require(len(overlay_by) == len(overlay), "Duplicate overlay key")
    require(set(overlay_by).issubset(row_keys), "Overlay references absent records")
    require(set(r["source"] for r in rows) == set(SOURCES), "Unexpected sources")
    for r in rows:
        require(r["scientific_disposition"] in {"include", "exclude", "pending"},
                "Unexpected scientific disposition")
        require(r["union_identifier_key"].startswith(("doi:", "platform:", "primary-url:")),
                "Unrecognized frozen typed identifier")
        require(bool(r["normalized_identifier"]), "Missing frozen identifier")
    pending = {(r["source"], r["recordID"]) for r in rows
               if r["scientific_disposition"] == "pending" and r["source"] != "AAMAS"}
    require(set(overlay_by) == pending, "Overlay does not exactly cover scientific pending selection rows")
    for r in overlay:
        require(r["prior_status"] == r["scientific_disposition"] == "pending" and
                r["final_selection"] == "not_included" and
                r["reason"] == "user_directed_exclusion_of_unresolved",
                "Overlay changed scientific status or administrative reason")
    selection = []
    for r in rows:
        key = (r["source"], r["recordID"])
        if r["source"] == "AAMAS":
            final, basis = "not_applicable_relation_only", "relation_only_no_selection_assignment"
        elif r["source"] == "IEEE" and r["track"] == "official_standard":
            final, basis = "separate_standard_track", "separate_normative_standard_not_academic_selection"
        elif r["scientific_disposition"] == "include":
            final, basis = "included", "original_source_inclusion"
        elif r["scientific_disposition"] == "exclude":
            final, basis = "not_included", "original_source_rule_or_evidence_exclusion"
        else:
            require(key in overlay_by, "Missing administrative disposition")
            require(overlay_by[key]["union_identifier_key"] == r["union_identifier_key"],
                    "Overlay typed identifier mismatch")
            final, basis = "not_included", "user_directed_exclusion_of_unresolved"
        selection.append({**r, "final_selection": final, "selection_basis": basis})
    selection.sort(key=lambda r: (SOURCES.index(r["source"]), r["recordID"]))
    source_counts = []
    for source in SOURCES:
        members = [r for r in selection if r["source"] == source]
        track = [r for r in members if r["final_selection"] in {"included", "not_included"}]
        source_counts.append({
            "source": source, "all_source_records": len(members), "selection_track_records": len(track),
            "included_source_records": sum(r["final_selection"] == "included" for r in track),
            "original_rule_or_evidence_excluded_records": sum(r["selection_basis"] == "original_source_rule_or_evidence_exclusion" for r in track),
            "user_directed_not_included_unresolved_records": sum(r["selection_basis"] == "user_directed_exclusion_of_unresolved" for r in track),
            "final_not_included_records": sum(r["final_selection"] == "not_included" for r in track),
            "final_selection_pending_records": 0 if track else "",
            "scientific_pending_preserved_records": sum(r["scientific_disposition"] == "pending" for r in track),
            "separate_standard_records": sum(r["final_selection"] == "separate_standard_track" for r in members),
            "relation_only_records": sum(r["final_selection"] == "not_applicable_relation_only" for r in members),
        })
    groups = defaultdict(list)
    for row in selection:
        groups[row["union_identifier_key"]].append(row)
    identifiers = []
    for key, members in sorted(groups.items()):
        states = {r["final_selection"] for r in members}
        final = next(x for x in ("included", "not_included", "separate_standard_track", "not_applicable_relation_only") if x in states)
        identifiers.append({
            "union_identifier_key": key, "normalized_identifier": members[0]["normalized_identifier"],
            "source_record_count": len(members),
            "source_members": json.dumps(sorted({r["source"] for r in members}), separators=(",", ":")),
            "source_record_members": json.dumps([[r["source"], r["recordID"]] for r in members], separators=(",", ":")),
            "original_scientific_dispositions": json.dumps(sorted({r["scientific_disposition"] for r in members}), separators=(",", ":")),
            "final_selection": final,
            "user_disposition_source_record_count": sum(r["selection_basis"] == "user_directed_exclusion_of_unresolved" for r in members),
            "global_scientific_verdict": "Unassigned", "independent_work_count": "", "version_count": "",
        })
    included = [r for r in identifiers if r["final_selection"] == "included"]
    totals = Counter(r["final_selection"] for r in selection)
    ids = Counter(r["final_selection"] for r in identifiers)
    bases = Counter(r["selection_basis"] for r in selection)
    counts = {
        "scope": "frozen source-record selection and typed-identifier arithmetic",
        "source_record_frame": len(selection),
        "selection_track_source_records": totals["included"] + totals["not_included"],
        "included_source_records": totals["included"],
        "original_rule_or_evidence_exclusions": bases["original_source_rule_or_evidence_exclusion"],
        "user_not_included_unresolved": bases["user_directed_exclusion_of_unresolved"],
        "final_not_included_source_records": totals["not_included"],
        "final_selection_pending_source_records": 0,
        "scientific_pending_selection_records_preserved": len(pending),
        "separate_standard_source_records": totals["separate_standard_track"],
        "relation_only_source_records": totals["not_applicable_relation_only"],
        "all_typed_identifiers": len(identifiers),
        "selection_track_typed_identifiers": ids["included"] + ids["not_included"],
        "included_typed_identifiers": len(included), "not_included_typed_identifiers": ids["not_included"],
        "exact_source_row_repeat_deduction": len(selection) - len(identifiers),
        "included_source_row_repeat_deduction": totals["included"] - len(included),
        "user_overlay_typed_identifiers": len({r["union_identifier_key"] for r in overlay}),
        "W_independent_works": None, "V_verified_versions": None,
        "scientific_coverage_work_version_acceptance": "Partial",
    }
    require(counts["source_record_frame"] == counts["selection_track_source_records"] +
            counts["separate_standard_source_records"] + counts["relation_only_source_records"], "Source frame arithmetic failed")
    require(counts["selection_track_source_records"] == counts["included_source_records"] +
            counts["original_rule_or_evidence_exclusions"] + counts["user_not_included_unresolved"], "Selection arithmetic failed")
    require(not any(r["user_disposition_source_record_count"] for r in included),
            "Overlay unexpectedly affects a currently source-included identifier")
    queries = read_csv(ROOT / "data/query-counts.csv")
    require(Counter(r["source"] for r in queries) == Counter({s: 31 for s in SOURCES}), "Query table coverage mismatch")
    require(Counter(r["actual_field"] for r in queries if r["source"] == "ACM") == Counter({"Abstract": 27, "AllField": 4}), "ACM frozen field policy mismatch")
    require(len({r["expression_id"] for r in queries if r["source"] == "IEEE"}) == 27, "V2 expression-alias count mismatch")
    require(len(read_csv(ROOT / "data/gate-matrix.csv")) == 40, "Gate scope table coverage mismatch")
    write_csv(output / OUTPUTS[0], selection)
    write_csv(output / OUTPUTS[1], source_counts)
    write_csv(output / OUTPUTS[2], identifiers)
    write_csv(output / OUTPUTS[3], included)
    (output / OUTPUTS[4]).write_text(json.dumps(counts, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for name in OUTPUTS:
        require(sha(output / name) == sha(ROOT / "expected" / name), "Reproduction mismatch " + name)
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="New or empty output directory; defaults to outputs/run")
    parser.add_argument("--check-only", action="store_true", help="Validate and reproduce in a temporary directory")
    args = parser.parse_args()
    require(not (args.check_only and args.output), "Choose --check-only or --output")
    checked = verify_package()
    if args.check_only:
        with tempfile.TemporaryDirectory(prefix="taxonomy-check-") as tmp:
            counts = generate(Path(tmp))
    else:
        output = (args.output or ROOT / "outputs/run").resolve()
        require(not any(output == (ROOT / p).resolve() or output.is_relative_to((ROOT / p).resolve()) for p in ("data", "expected", "code", "docs")), "Output would overwrite frozen package content")
        require(not output.exists() or (output.is_dir() and not any(output.iterdir())), "Output directory must be new or empty")
        output.mkdir(parents=True, exist_ok=True)
        counts = generate(output)
    print(json.dumps({"status": "Verified offline mechanical reproduction", "checksummed_files": checked,
                      "matched_expected_outputs": len(OUTPUTS), "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, StopIteration, json.JSONDecodeError) as error:
        print("Validation failed: " + str(error), file=sys.stderr)
        sys.exit(1)
