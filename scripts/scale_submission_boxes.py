#!/usr/bin/env python3
"""Scale normalized YOLO submission boxes around their centers."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--source", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--summary", type=Path, required=True)
    p.add_argument("--scale", type=float, required=True)
    p.add_argument("--eps", type=float, default=1e-6)
    p.add_argument("--note", default="")
    return p.parse_args()


def clamp_box(xc: float, yc: float, w: float, h: float, eps: float) -> tuple[float, float, float, float] | None:
    x1 = max(eps, xc - w / 2.0)
    y1 = max(eps, yc - h / 2.0)
    x2 = min(1.0 - eps, xc + w / 2.0)
    y2 = min(1.0 - eps, yc + h / 2.0)
    new_w = x2 - x1
    new_h = y2 - y1
    if new_w <= 0.0 or new_h <= 0.0:
        return None
    return (x1 + x2) / 2.0, (y1 + y2) / 2.0, new_w, new_h


def main() -> int:
    args = parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.summary.parent.mkdir(parents=True, exist_ok=True)

    rows = 0
    nonempty = 0
    boxes = 0
    removed = 0
    adjusted = 0
    by_class: dict[str, int] = {"0": 0, "1": 0, "2": 0, "3": 0}

    with args.source.open(newline="", encoding="utf-8-sig") as src, args.out.open("w", newline="", encoding="utf-8") as dst:
        reader = csv.DictReader(src)
        writer = csv.DictWriter(dst, fieldnames=["id", "image_id", "prediction_string"])
        writer.writeheader()

        for row in reader:
            rows += 1
            pred = (row.get("prediction_string") or "").strip()
            out_tokens: list[str] = []
            if pred and pred != "no box":
                tokens = pred.split()
                if len(tokens) % 6:
                    raise ValueError(f"row {rows}: token count is not a multiple of 6")
                for i in range(0, len(tokens), 6):
                    cls = tokens[i]
                    conf = float(tokens[i + 1])
                    xc, yc, w, h = (float(v) for v in tokens[i + 2 : i + 6])
                    scaled = clamp_box(xc, yc, w * args.scale, h * args.scale, args.eps)
                    if scaled is None:
                        removed += 1
                        continue
                    nxc, nyc, nw, nh = scaled
                    if (nxc, nyc, nw, nh) != (xc, yc, w, h):
                        adjusted += 1
                    out_tokens.extend([cls, f"{conf:.8f}", f"{nxc:.8f}", f"{nyc:.8f}", f"{nw:.8f}", f"{nh:.8f}"])
                    boxes += 1
                    by_class[cls] = by_class.get(cls, 0) + 1
            out_pred = " ".join(out_tokens) if out_tokens else "no box"
            if out_pred != "no box":
                nonempty += 1
            writer.writerow({"id": row["id"], "image_id": row["image_id"], "prediction_string": out_pred})

    summary = {
        "source": str(args.source),
        "submission": str(args.out),
        "scale": args.scale,
        "eps": args.eps,
        "rows": rows,
        "nonempty": nonempty,
        "total_boxes": boxes,
        "removed": removed,
        "adjusted": adjusted,
        "boxes_by_class": by_class,
        "note": args.note,
        "rule_note": "post-processing of one YOLOv8n checkpoint submission; no TTA, no ensemble, no pseudo-labeling",
    }
    args.summary.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
