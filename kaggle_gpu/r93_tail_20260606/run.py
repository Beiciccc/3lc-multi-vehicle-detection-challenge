#!/usr/bin/env python3
"""Generate R93 tail-filter candidates in a Kaggle GPU-enabled runtime.

All candidates are post-processing of one YOLOv8n 640px single-checkpoint
submission: no external data, no TTA, no ensemble, no pseudo-labeling.
"""
from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path
from statistics import mean, median

CLASS_NAMES = {0: "truck", 1: "car", 2: "van", 3: "bus"}
BASE = Path(__file__).resolve().parent / "r93_baseline_submission.csv"
OUT = Path("/kaggle/working/submissions_20260606") if Path("/kaggle/working").exists() else Path("submissions_20260606")


def find_sample() -> Path | None:
    roots = [Path("/kaggle/input"), Path.cwd()]
    for root in roots:
        if not root.exists():
            continue
        hits = list(root.rglob("sample_submission.csv"))
        if hits:
            return hits[0]
    return None


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def audit(path: Path, sample_rows: list[dict[str, str]] | None = None) -> dict:
    rows = read_rows(path)
    errors: list[str] = []
    if sample_rows is not None:
        if len(rows) != len(sample_rows):
            errors.append(f"row count mismatch: {len(rows)} vs {len(sample_rows)}")
    counts = []
    by_class = {str(k): 0 for k in CLASS_NAMES}
    total = 0
    nonempty = 0
    for idx, row in enumerate(rows):
        if sample_rows is not None:
            s = sample_rows[idx]
            if row.get("id") != s.get("id") or row.get("image_id") != s.get("image_id"):
                errors.append(f"id/image mismatch at row {idx}")
                break
        ps = (row.get("prediction_string") or "").strip()
        if ps == "no box":
            counts.append(0)
            continue
        toks = ps.split()
        if len(toks) % 6:
            errors.append(f"bad token count at row {idx}")
            counts.append(0)
            continue
        n = 0
        nonempty += 1
        for j in range(0, len(toks), 6):
            try:
                c = int(toks[j]); vals = [float(v) for v in toks[j+1:j+6]]
            except Exception:
                errors.append(f"parse error row {idx} token {j}")
                continue
            if c not in CLASS_NAMES:
                errors.append(f"bad class row {idx}")
            if not all(math.isfinite(v) and 0.0 <= v <= 1.0 for v in vals):
                errors.append(f"range error row {idx}")
            if vals[3] <= 0.0 or vals[4] <= 0.0:
                errors.append(f"nonpositive box row {idx}")
            by_class[str(c)] = by_class.get(str(c), 0) + 1
            total += 1; n += 1
        counts.append(n)
    sorted_counts = sorted(counts)
    return {
        "ok": not errors,
        "errors": errors[:20],
        "rows": len(rows),
        "nonempty": nonempty,
        "total_boxes": total,
        "boxes_by_class": by_class,
        "per_image": {
            "mean": float(mean(counts)) if counts else 0.0,
            "median": float(median(counts)) if counts else 0.0,
            "p95": sorted_counts[int(0.95 * len(sorted_counts))-1] if counts else 0,
            "p99": sorted_counts[int(0.99 * len(sorted_counts))-1] if counts else 0,
            "max": max(counts) if counts else 0,
            "near_max_det_290": sum(1 for x in counts if x >= 290),
        },
    }


def filter_submission(source: Path, out: Path, thresholds: dict[int, float], note: str, sample_rows: list[dict[str, str]] | None) -> dict:
    rows = read_rows(source)
    dropped = {str(k): 0 for k in CLASS_NAMES}
    kept = {str(k): 0 for k in CLASS_NAMES}
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "image_id", "prediction_string"])
        writer.writeheader()
        for row in rows:
            ps = row["prediction_string"].strip()
            parts: list[str] = []
            if ps != "no box":
                toks = ps.split()
                for i in range(0, len(toks), 6):
                    c = int(toks[i]); conf = float(toks[i+1])
                    floor = thresholds.get(c)
                    if floor is not None and conf < floor:
                        dropped[str(c)] += 1
                        continue
                    kept[str(c)] += 1
                    parts.extend(toks[i:i+6])
            writer.writerow({"id": row["id"], "image_id": row["image_id"], "prediction_string": " ".join(parts) if parts else "no box"})
    aud = audit(out, sample_rows)
    if not aud["ok"]:
        raise RuntimeError(f"audit failed for {out}: {aud['errors']}")
    summary = {
        "source": str(source),
        "submission": str(out),
        "thresholds": {str(k): v for k, v in thresholds.items()},
        "dropped_by_class": dropped,
        "kept_by_class": kept,
        "audit": aud,
        "note": note,
        "rule_note": "single YOLOv8n 640px checkpoint output; post-processing only; no TTA, no ensemble, no pseudo-labeling, no external data",
        "gpu_runtime": os.environ.get("KAGGLE_KERNEL_RUN_TYPE", "unknown"),
    }
    out.with_suffix(".json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    print("R93 tail checks 2026-06-06")
    print(f"base={BASE}")
    print(f"cuda_visible={os.environ.get('CUDA_VISIBLE_DEVICES', '')}")
    sample_path = find_sample()
    sample_rows = read_rows(sample_path) if sample_path else None
    print(f"sample={sample_path}")
    OUT.mkdir(parents=True, exist_ok=True)
    baseline_audit = audit(BASE, sample_rows)
    print(json.dumps({"baseline_audit": baseline_audit}, indent=2))
    candidates = [
        ("r103", "r103_r93_filter_van0001_keep_others000075_submission.csv", {2: 0.0001}, "filter van below 0.0001; keep truck/car/bus at R93 floor"),
        ("r104", "r104_r93_filter_car00008_keep_others000075_submission.csv", {1: 0.00008}, "filter car below 0.00008; keep truck/van/bus at R93 floor"),
        ("r105", "r105_r93_filter_truck00011_keep_others000075_submission.csv", {0: 0.00011}, "filter truck below 0.00011; keep car/van/bus at R93 floor"),
        ("r106", "r106_r93_filter_car000085_keep_others000075_submission.csv", {1: 0.000085}, "filter car below 0.000085; keep truck/van/bus at R93 floor"),
        ("r107", "r107_r93_filter_van00009_keep_others000075_submission.csv", {2: 0.00009}, "filter van below 0.00009; keep truck/car/bus at R93 floor"),
        ("r108", "r108_r93_filter_truckvan0001_keep_carbus000075_submission.csv", {0: 0.0001, 2: 0.0001}, "filter truck+van below 0.0001; keep car/bus at R93 floor"),
        ("r109", "r109_r93_filter_car00009_keep_others000075_submission.csv", {1: 0.00009}, "filter car below 0.00009; keep truck/van/bus at R93 floor"),
    ]
    summaries = []
    for run, filename, thresholds, note in candidates:
        print(f"export {run}: {note}", flush=True)
        summaries.append(filter_submission(BASE, OUT / filename, thresholds, note, sample_rows))
    run_summary = {
        "baseline": str(BASE),
        "baseline_audit": baseline_audit,
        "sample": str(sample_path) if sample_path else None,
        "candidates": summaries,
        "rule_note": "single YOLOv8n 640px checkpoint output; post-processing only; no TTA, no ensemble, no pseudo-labeling, no external data",
    }
    (OUT / "run_summary.json").write_text(json.dumps(run_summary, indent=2), encoding="utf-8")
    print(json.dumps(run_summary, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
