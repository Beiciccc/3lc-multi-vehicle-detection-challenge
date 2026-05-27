#!/usr/bin/env python3
"""Clip normalized YOLO submission boxes inside image bounds."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def clip_submission(src: Path, dst: Path, eps: float) -> dict[str, int | float | str]:
    adjusted = 0
    removed = 0
    boxes = 0

    dst.parent.mkdir(parents=True, exist_ok=True)
    with src.open(newline="") as f, dst.open("w", newline="") as g:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(g, fieldnames=["id", "image_id", "prediction_string"])
        writer.writeheader()

        for row in reader:
            output: list[str] = []
            pred = (row.get("prediction_string") or "").strip()
            if pred and pred.lower() != "no box":
                tokens = pred.split()
                if len(tokens) % 6:
                    raise ValueError(
                        f"Row {row.get('id')} has {len(tokens)} prediction tokens, "
                        "not a multiple of 6"
                    )
                for i in range(0, len(tokens), 6):
                    cls = tokens[i]
                    conf = float(tokens[i + 1])
                    xc, yc, bw, bh = map(float, tokens[i + 2 : i + 6])

                    x1 = xc - bw / 2
                    y1 = yc - bh / 2
                    x2 = xc + bw / 2
                    y2 = yc + bh / 2

                    cx1 = min(1.0 - eps, max(eps, x1))
                    cy1 = min(1.0 - eps, max(eps, y1))
                    cx2 = min(1.0 - eps, max(eps, x2))
                    cy2 = min(1.0 - eps, max(eps, y2))

                    if (cx1, cy1, cx2, cy2) != (x1, y1, x2, y2):
                        adjusted += 1

                    new_w = cx2 - cx1
                    new_h = cy2 - cy1
                    if new_w <= 0 or new_h <= 0:
                        removed += 1
                        continue

                    output.extend(
                        [
                            cls,
                            f"{conf:.8f}",
                            f"{(cx1 + cx2) / 2:.8f}",
                            f"{(cy1 + cy2) / 2:.8f}",
                            f"{new_w:.8f}",
                            f"{new_h:.8f}",
                        ]
                    )
                    boxes += 1

            writer.writerow(
                {
                    "id": row["id"],
                    "image_id": row["image_id"],
                    "prediction_string": " ".join(output) if output else "no box",
                }
            )

    return {
        "src": str(src),
        "dst": str(dst),
        "eps": eps,
        "boxes": boxes,
        "adjusted": adjusted,
        "removed": removed,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=Path)
    parser.add_argument("dst", type=Path)
    parser.add_argument("--eps", type=float, default=1e-6)
    args = parser.parse_args()

    stats = clip_submission(args.src, args.dst, args.eps)
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
