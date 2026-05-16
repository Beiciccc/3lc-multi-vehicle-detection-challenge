#!/usr/bin/env python3
"""Filter an existing Kaggle detection submission by class-specific confidence floors.

This is single-submission post-processing only: no ensembling, no TTA, no external data.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

CLASS_NAMES = {0: "truck", 1: "car", 2: "van", 3: "bus"}


def parse_thresholds(items: list[str]) -> dict[int, float]:
    out: dict[int, float] = {}
    for item in items:
        if ":" not in item:
            raise ValueError(f"bad threshold {item!r}; expected class:conf")
        c_raw, v_raw = item.split(":", 1)
        c = int(c_raw)
        v = float(v_raw)
        if c not in CLASS_NAMES:
            raise ValueError(f"invalid class {c}")
        if not 0.0 <= v <= 1.0:
            raise ValueError(f"invalid threshold {v}")
        out[c] = v
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--summary", type=Path, required=True)
    p.add_argument("--min-conf", action="append", default=[], help="Class-specific floor, e.g. 3:0.00105")
    p.add_argument("--note", default="")
    args = p.parse_args()

    thresholds = parse_thresholds(args.min_conf)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.summary.parent.mkdir(parents=True, exist_ok=True)

    rows = 0
    nonempty = 0
    kept = 0
    dropped_by_class = {str(c): 0 for c in CLASS_NAMES}
    kept_by_class = {str(c): 0 for c in CLASS_NAMES}

    with args.source.open(newline="", encoding="utf-8") as src, args.out.open("w", newline="", encoding="utf-8") as dst:
        reader = csv.DictReader(src)
        writer = csv.DictWriter(dst, fieldnames=["id", "image_id", "prediction_string"])
        writer.writeheader()
        for row in reader:
            rows += 1
            ps = str(row["prediction_string"]).strip()
            parts: list[str] = []
            if ps and ps != "no box":
                toks = ps.split()
                if len(toks) % 6:
                    raise ValueError(f"bad token count at row {rows}")
                for i in range(0, len(toks), 6):
                    c = int(toks[i])
                    conf = float(toks[i + 1])
                    floor = thresholds.get(c)
                    if floor is not None and conf < floor:
                        dropped_by_class[str(c)] += 1
                        continue
                    parts.extend(toks[i : i + 6])
                    kept_by_class[str(c)] += 1
                    kept += 1
            out_ps = " ".join(parts) if parts else "no box"
            if out_ps != "no box":
                nonempty += 1
            writer.writerow({"id": row["id"], "image_id": row["image_id"], "prediction_string": out_ps})

    summary = {
        "source": str(args.source),
        "submission": str(args.out),
        "thresholds": {str(k): v for k, v in thresholds.items()},
        "rows": rows,
        "nonempty": nonempty,
        "total_boxes": kept,
        "kept_by_class": kept_by_class,
        "dropped_by_class": dropped_by_class,
        "note": args.note,
        "rule_note": "post-processing of one YOLOv8n checkpoint submission; no TTA, no ensemble, no pseudo-labeling",
    }
    args.summary.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
