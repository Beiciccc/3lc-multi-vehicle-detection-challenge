#!/usr/bin/env python3
"""Generate a Kaggle submission from an existing YOLO checkpoint.

Competition-safe inference helper: single YOLOv8n checkpoint, no TTA, no ensemble.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
from pathlib import Path

import numpy as np
from ultralytics import YOLO

CLASS_NAMES = {0: "truck", 1: "car", 2: "van", 3: "bus"}
BOUNDARY_EPS = 1e-6


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--starter-dir", type=Path, default=Path("competition_starter"))
    p.add_argument("--weights", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--summary", type=Path, required=True)
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--conf", type=float, default=0.001)
    p.add_argument("--iou", type=float, default=0.65)
    p.add_argument("--max-det", type=int, default=300)
    p.add_argument("--batch", type=int, default=16)
    p.add_argument("--device", default="0")
    p.add_argument("--val", action="store_true")
    p.add_argument("--note", default="")
    return p.parse_args()


def find_image(test_dir: Path, stem: str) -> Path | None:
    for ext in (".jpg", ".jpeg", ".png", ".bmp", ".webp"):
        p = test_dir / f"{stem}{ext}"
        if p.is_file():
            return p
    matches = list(test_dir.glob(stem + ".*"))
    return matches[0] if matches else None


def prediction_string(result) -> str:
    boxes = getattr(result, "boxes", None)
    if boxes is None or len(boxes) == 0:
        return "no box"
    h_img, w_img = result.orig_shape
    xyxy = boxes.xyxy.detach().cpu().numpy()
    cls = boxes.cls.detach().cpu().numpy().astype(int)
    conf = boxes.conf.detach().cpu().numpy()
    order = np.argsort(-conf)
    parts: list[str] = []
    for idx in order:
        c = int(cls[idx])
        cf = float(conf[idx])
        x1, y1, x2, y2 = (float(v) for v in xyxy[idx])
        x1 = min(float(w_img), max(0.0, x1))
        y1 = min(float(h_img), max(0.0, y1))
        x2 = min(float(w_img), max(0.0, x2))
        y2 = min(float(h_img), max(0.0, y2))
        if x2 <= x1 or y2 <= y1 or c not in CLASS_NAMES:
            continue
        x = ((x1 + x2) / 2.0) / float(w_img)
        y = ((y1 + y2) / 2.0) / float(h_img)
        w = (x2 - x1) / float(w_img)
        h = (y2 - y1) / float(h_img)
        cf = min(1.0, max(0.0, cf))
        if w <= 0.0 or h <= 0.0:
            continue
        w = min(1.0 - 2 * BOUNDARY_EPS, max(1e-8, w))
        h = min(1.0 - 2 * BOUNDARY_EPS, max(1e-8, h))
        x = min(1.0 - w / 2.0 - BOUNDARY_EPS, max(w / 2.0 + BOUNDARY_EPS, x))
        y = min(1.0 - h / 2.0 - BOUNDARY_EPS, max(h / 2.0 + BOUNDARY_EPS, y))
        parts.extend([str(c), f"{cf:.8f}", f"{x:.8f}", f"{y:.8f}", f"{w:.8f}", f"{h:.8f}"])
    return " ".join(parts) if parts else "no box"


def audit_submission(sample_path: Path, submission_path: Path) -> dict:
    with sample_path.open(newline="", encoding="utf-8") as f:
        sample_rows = list(csv.DictReader(f))
    with submission_path.open(newline="", encoding="utf-8") as f:
        sub_rows = list(csv.DictReader(f))
    errors: list[str] = []
    columns = list(sub_rows[0].keys()) if sub_rows else []
    if columns != ["id", "image_id", "prediction_string"]:
        errors.append("bad columns")
    if len(sample_rows) != len(sub_rows):
        errors.append(f"row count mismatch sample={len(sample_rows)} sub={len(sub_rows)}")
    total_boxes = 0
    nonempty = 0
    for i, (s, r) in enumerate(zip(sample_rows, sub_rows)):
        if s["id"] != r["id"] or s["image_id"] != r["image_id"]:
            errors.append(f"id/image mismatch at row {i}")
            break
        ps = str(r["prediction_string"]).strip()
        if ps == "no box":
            continue
        toks = ps.split()
        if len(toks) % 6:
            errors.append(f"bad token count at row {i}")
            continue
        nonempty += 1
        for j in range(0, len(toks), 6):
            try:
                c = int(toks[j])
                vals = [float(v) for v in toks[j + 1:j + 6]]
            except Exception:
                errors.append(f"parse error row {i} token {j}")
                continue
            if c not in CLASS_NAMES:
                errors.append(f"bad class {c} row {i}")
            if not all(math.isfinite(v) and 0.0 <= v <= 1.0 for v in vals):
                errors.append(f"range error row {i}")
            if vals[3] <= 0.0 or vals[4] <= 0.0:
                errors.append(f"nonpositive box row {i}")
            total_boxes += 1
    return {"ok": not errors, "errors": errors[:20], "rows": len(sub_rows), "nonempty": nonempty, "total_boxes": total_boxes}


def main() -> int:
    args = parse_args()
    starter_dir = args.starter_dir.resolve()
    weights = args.weights if args.weights.is_absolute() else (Path.cwd() / args.weights).resolve()
    out_path = args.out if args.out.is_absolute() else (Path.cwd() / args.out).resolve()
    summary_path = args.summary if args.summary.is_absolute() else (Path.cwd() / args.summary).resolve()
    sample_path = starter_dir / "sample_submission.csv"
    test_dir = starter_dir / "data" / "test" / "images"
    dataset_yaml = starter_dir / "dataset.yaml"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    os.chdir(starter_dir)

    with sample_path.open(newline="", encoding="utf-8") as f:
        sample_rows = list(csv.DictReader(f))
    paths: list[Path] = []
    missing: list[str] = []
    for row in sample_rows:
        stem = str(row["image_id"]).strip()
        p = find_image(test_dir, stem)
        if p is None:
            missing.append(stem)
        else:
            paths.append(p)
    if missing:
        raise RuntimeError(f"missing {len(missing)} test images, first={missing[:5]}")

    model = YOLO(str(weights))
    val_metrics = None
    if args.val:
        vr = model.val(data=str(dataset_yaml), split="val", imgsz=args.imgsz, device=args.device, conf=args.conf, iou=args.iou, batch=args.batch, verbose=False)
        val_metrics = {"map50": float(vr.box.map50), "map50_95": float(vr.box.map)}

    pred_by_stem: dict[str, str] = {}
    bs = max(1, int(args.batch))
    for start in range(0, len(paths), bs):
        chunk = paths[start:start + bs]
        results = model.predict(source=[str(p) for p in chunk], imgsz=args.imgsz, conf=args.conf, iou=args.iou, max_det=args.max_det, batch=min(bs, len(chunk)), device=args.device, verbose=False)
        for p, res in zip(chunk, results):
            pred_by_stem[p.stem] = prediction_string(res)
        print(f"predicted {min(start + bs, len(paths))}/{len(paths)}")

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "image_id", "prediction_string"])
        writer.writeheader()
        for row in sample_rows:
            stem = str(row["image_id"]).strip()
            writer.writerow({"id": row["id"], "image_id": stem, "prediction_string": pred_by_stem.get(stem, "no box")})

    audit = audit_submission(sample_path, out_path)
    if not audit["ok"]:
        raise RuntimeError(f"audit failed: {audit['errors']}")
    summary = {
        "weights": str(weights),
        "submission": str(out_path),
        "imgsz": args.imgsz,
        "conf": args.conf,
        "iou": args.iou,
        "max_det": args.max_det,
        "batch": args.batch,
        "device": args.device,
        "val_metrics": val_metrics,
        "audit": audit,
        "note": args.note,
        "rule_note": "single YOLOv8n checkpoint inference, no TTA, no ensemble, no pseudo-labeling",
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
