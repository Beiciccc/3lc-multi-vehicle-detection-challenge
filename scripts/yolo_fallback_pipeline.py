#!/usr/bin/env python3
"""
Fallback YOLOv8n-from-scratch training and submission generation.

This is used only when the official 3LC starter workflow is blocked by a
missing 3LC API key. It keeps the architecture and no-pretraining constraints:
YOLOv8n YAML, random initialization, single model, no TTA/ensemble.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import random
import time
from pathlib import Path

import numpy as np
import torch
import yaml
from ultralytics import YOLO


CLASS_NAMES = {0: "truck", 1: "car", 2: "van", 3: "bus"}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--starter-dir", type=Path, default=Path.cwd())
    p.add_argument("--run-name", required=True)
    p.add_argument("--epochs", type=int, default=10)
    p.add_argument("--batch", type=int, default=16)
    p.add_argument("--imgsz", type=int, default=640)
    p.add_argument("--device", default="0")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--optimizer", default="AdamW")
    p.add_argument("--lr0", type=float, default=0.003)
    p.add_argument("--lrf", type=float, default=0.01)
    p.add_argument("--momentum", type=float, default=0.937)
    p.add_argument("--weight-decay", type=float, default=0.0005)
    p.add_argument("--warmup-epochs", type=float, default=0.5)
    p.add_argument("--patience", type=int, default=20)
    p.add_argument("--mosaic", type=float, default=1.0)
    p.add_argument("--mixup", type=float, default=0.05)
    p.add_argument("--copy-paste", type=float, default=0.0)
    p.add_argument("--close-mosaic", type=int, default=1)
    p.add_argument("--fliplr", type=float, default=0.5)
    p.add_argument("--translate", type=float, default=0.1)
    p.add_argument("--scale", type=float, default=0.5)
    p.add_argument("--amp", action="store_true", help="Enable AMP. Default is off to avoid Ultralytics pretrained AMP checks.")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--pred-conf", type=float, default=0.001)
    p.add_argument("--pred-iou", type=float, default=0.65)
    p.add_argument("--pred-batch", type=int, default=16)
    p.add_argument("--max-det", type=int, default=300)
    return p.parse_args()


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = True


def write_dataset_yaml(starter_dir: Path, run_name: str) -> Path:
    out = starter_dir / f"dataset_{run_name}.yaml"
    cfg = {
        "path": str(starter_dir.resolve()),
        "train": "data/train/images",
        "val": "data/val/images",
        "test": "data/test/images",
        "nc": 4,
        "names": CLASS_NAMES,
    }
    out.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    return out


def find_image(test_dir: Path, stem: str) -> Path | None:
    for ext in (".jpg", ".jpeg", ".png", ".bmp", ".webp"):
        p = test_dir / f"{stem}{ext}"
        if p.is_file():
            return p
    matches = list(test_dir.glob(stem + ".*"))
    return matches[0] if matches else None


def result_to_prediction_string(result) -> str:
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
        if x2 <= x1 or y2 <= y1:
            continue
        x = ((x1 + x2) / 2.0) / float(w_img)
        y = ((y1 + y2) / 2.0) / float(h_img)
        w = (x2 - x1) / float(w_img)
        h = (y2 - y1) / float(h_img)
        cf = min(1.0, max(0.0, cf))
        if c not in CLASS_NAMES or w <= 0.0 or h <= 0.0:
            continue
        parts.extend([str(c), f"{cf:.8f}", f"{x:.8f}", f"{y:.8f}", f"{w:.8f}", f"{h:.8f}"])
    return " ".join(parts) if parts else "no box"


def validate_submission(sample_path: Path, submission_path: Path) -> dict:
    with sample_path.open(newline="", encoding="utf-8") as f:
        sample_rows = list(csv.DictReader(f))
    with submission_path.open(newline="", encoding="utf-8") as f:
        sub_rows = list(csv.DictReader(f))

    errors: list[str] = []
    if not sub_rows:
        errors.append("submission has no rows")
    if sub_rows and list(sub_rows[0].keys()) != ["id", "image_id", "prediction_string"]:
        errors.append(f"bad columns: {list(sub_rows[0].keys())}")
    if len(sample_rows) != len(sub_rows):
        errors.append(f"row count mismatch sample={len(sample_rows)} submission={len(sub_rows)}")

    total_boxes = 0
    nonempty = 0
    for i, (sample, sub) in enumerate(zip(sample_rows, sub_rows)):
        if sample["id"] != sub["id"] or sample["image_id"] != sub["image_id"]:
            errors.append(f"id mismatch at row {i}: sample={sample} submission={sub}")
            break
        ps = str(sub["prediction_string"]).strip()
        if ps == "no box":
            continue
        toks = ps.split()
        if len(toks) % 6:
            errors.append(f"row {i} token count not divisible by 6")
            continue
        nonempty += 1
        for j in range(0, len(toks), 6):
            try:
                c = int(toks[j])
                vals = [float(v) for v in toks[j + 1 : j + 6]]
            except Exception:
                errors.append(f"row {i} parse error near token {j}")
                continue
            if c not in CLASS_NAMES:
                errors.append(f"row {i} invalid class {c}")
            if not all(math.isfinite(v) and 0.0 <= v <= 1.0 for v in vals):
                errors.append(f"row {i} values out of range near token {j}")
            if vals[3] <= 0.0 or vals[4] <= 0.0:
                errors.append(f"row {i} non-positive bbox near token {j}")
            total_boxes += 1

    return {
        "ok": not errors,
        "errors": errors[:20],
        "rows": len(sub_rows),
        "nonempty": nonempty,
        "total_boxes": total_boxes,
    }


def main() -> int:
    args = parse_args()
    starter_dir = args.starter_dir.resolve()
    os.chdir(starter_dir)
    seed_everything(args.seed)

    dataset_yaml = write_dataset_yaml(starter_dir, args.run_name)
    run_dir = starter_dir / "runs" / "detect" / args.run_name
    sub_dir = starter_dir / "submissions"
    sub_dir.mkdir(parents=True, exist_ok=True)
    summary_path = sub_dir / f"{args.run_name}_summary.json"
    submission_path = sub_dir / f"{args.run_name}_submission.csv"

    print("=" * 70)
    print(f"TRAIN {args.run_name}")
    print("=" * 70)
    print(f"starter_dir={starter_dir}")
    print(f"dataset_yaml={dataset_yaml}")
    print(f"torch={torch.__version__} cuda={torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"gpu={torch.cuda.get_device_name(0)}")

    model = YOLO("yolov8n.yaml")
    t0 = time.time()
    results = model.train(
        data=str(dataset_yaml),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        workers=args.workers,
        project=str(starter_dir / "runs" / "detect"),
        name=args.run_name,
        exist_ok=True,
        pretrained=False,
        optimizer=args.optimizer,
        lr0=args.lr0,
        lrf=args.lrf,
        cos_lr=True,
        momentum=args.momentum,
        weight_decay=args.weight_decay,
        warmup_epochs=args.warmup_epochs,
        patience=args.patience,
        mosaic=args.mosaic,
        mixup=args.mixup,
        copy_paste=args.copy_paste,
        close_mosaic=args.close_mosaic,
        fliplr=args.fliplr,
        translate=args.translate,
        scale=args.scale,
        cache=False,
        amp=bool(args.amp),
        seed=args.seed,
        verbose=True,
    )
    train_minutes = (time.time() - t0) / 60.0
    best_weights = Path(results.save_dir) / "weights" / "best.pt"
    if not best_weights.is_file():
        raise FileNotFoundError(f"best weights missing: {best_weights}")

    print("=" * 70)
    print("VALIDATE")
    print("=" * 70)
    val_model = YOLO(str(best_weights))
    val_results = val_model.val(
        data=str(dataset_yaml),
        split="val",
        imgsz=args.imgsz,
        device=args.device,
        conf=0.001,
        iou=0.5,
        batch=args.batch,
        verbose=False,
    )
    map50 = float(getattr(val_results.box, "map50", float("nan")))
    map5095 = float(getattr(val_results.box, "map", float("nan")))

    print("=" * 70)
    print("PREDICT")
    print("=" * 70)
    sample_path = starter_dir / "sample_submission.csv"
    test_dir = starter_dir / "data" / "test" / "images"
    with sample_path.open(newline="", encoding="utf-8") as f:
        sample_rows = list(csv.DictReader(f))
    stems = [str(r["image_id"]).strip() for r in sample_rows]
    paths: list[Path] = []
    missing: list[str] = []
    for stem in stems:
        p = find_image(test_dir, stem)
        if p is None:
            missing.append(stem)
        else:
            paths.append(p)
    if missing:
        raise RuntimeError(f"Missing {len(missing)} test images, first={missing[:5]}")

    pred_model = YOLO(str(best_weights))
    pred_by_stem: dict[str, str] = {}
    bs = max(1, args.pred_batch)
    for start in range(0, len(paths), bs):
        chunk = paths[start : start + bs]
        preds = pred_model.predict(
            source=[str(p) for p in chunk],
            imgsz=args.imgsz,
            conf=args.pred_conf,
            iou=args.pred_iou,
            max_det=args.max_det,
            batch=min(bs, len(chunk)),
            device=args.device,
            verbose=False,
        )
        for p, res in zip(chunk, preds):
            pred_by_stem[p.stem] = result_to_prediction_string(res)
        print(f"predicted {min(start + bs, len(paths))}/{len(paths)}")

    with submission_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "image_id", "prediction_string"])
        writer.writeheader()
        for row, stem in zip(sample_rows, stems):
            writer.writerow(
                {
                    "id": row["id"],
                    "image_id": stem,
                    "prediction_string": pred_by_stem.get(stem, "no box"),
                }
            )

    audit = validate_submission(sample_path, submission_path)
    if not audit["ok"]:
        raise RuntimeError(f"Submission audit failed: {audit['errors']}")

    summary = {
        "run_name": args.run_name,
        "best_weights": str(best_weights),
        "submission": str(submission_path),
        "train_minutes": train_minutes,
        "val_map50": map50,
        "val_map50_95": map5095,
        "audit": audit,
        "args": vars(args) | {"starter_dir": str(starter_dir)},
        "rule_note": "Fallback path because official 3LC workflow needs a 3LC API key; model is YOLOv8n.yaml from scratch with no pretraining.",
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
