#!/usr/bin/env python3
"""Train a YOLOv8n-from-scratch baseline and export low-confidence submissions.

Competition-safe setup: provided competition data only, YOLOv8n YAML/random
initialization, 640 px input, single checkpoint, no TTA, no ensemble, no
pseudo-labeling, no distillation.
"""
from __future__ import annotations

import csv
import json
import math
import os
import random
import subprocess
import sys
import time
from pathlib import Path


def ensure_packages() -> None:
    # Kaggle may assign a P100 (sm_60). Current default torch wheels can omit
    # Pascal support, so pin a CUDA 12.4 PyTorch build that supports this GPU.
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-q",
        "--force-reinstall",
        "torch==2.5.1",
        "torchvision==0.20.1",
        "--index-url",
        "https://download.pytorch.org/whl/cu124",
    ])
    subprocess.check_call([
        sys.executable,
        "-m",
        "pip",
        "install",
        "-q",
        "ultralytics==8.4.60",
        "PyYAML",
    ])


ensure_packages()

import numpy as np
import torch
import yaml
from ultralytics import YOLO

CLASS_NAMES = {0: "truck", 1: "car", 2: "van", 3: "bus"}
BOUNDARY_EPS = 1e-6


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.benchmark = True


def find_starter_dir() -> Path:
    roots = [Path("/kaggle/input"), Path.cwd()]
    candidates: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        candidates.extend(root.rglob("sample_submission.csv"))
    for sample in candidates:
        base = sample.parent
        required = [
            base / "data/train/images",
            base / "data/train/labels",
            base / "data/val/images",
            base / "data/val/labels",
            base / "data/test/images",
        ]
        if all(p.is_dir() for p in required):
            return base
    raise FileNotFoundError("Could not locate competition_starter with data and sample_submission.csv")


def write_dataset_yaml(starter_dir: Path, out: Path) -> None:
    cfg = {
        "path": str(starter_dir),
        "train": "data/train/images",
        "val": "data/val/images",
        "test": "data/test/images",
        "nc": 4,
        "names": CLASS_NAMES,
    }
    out.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")


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


def audit_submission(sample_rows: list[dict[str, str]], submission_path: Path) -> dict:
    with submission_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    errors: list[str] = []
    if not rows:
        errors.append("submission has no rows")
    elif list(rows[0].keys()) != ["id", "image_id", "prediction_string"]:
        errors.append(f"bad columns: {list(rows[0].keys())}")
    if len(rows) != len(sample_rows):
        errors.append(f"row count mismatch sample={len(sample_rows)} submission={len(rows)}")
    total_boxes = 0
    nonempty = 0
    per_image_counts: list[int] = []
    by_class = {str(c): 0 for c in CLASS_NAMES}
    for i, (sample, row) in enumerate(zip(sample_rows, rows)):
        if sample["id"] != row["id"] or sample["image_id"] != row["image_id"]:
            errors.append(f"id/image mismatch at row {i}")
            break
        ps = str(row["prediction_string"]).strip()
        if ps == "no box":
            per_image_counts.append(0)
            continue
        toks = ps.split()
        if len(toks) % 6:
            errors.append(f"bad token count at row {i}")
            per_image_counts.append(0)
            continue
        nonempty += 1
        n = 0
        for j in range(0, len(toks), 6):
            try:
                c = int(toks[j])
                vals = [float(v) for v in toks[j + 1 : j + 6]]
            except Exception:
                errors.append(f"parse error row {i} token {j}")
                continue
            if c not in CLASS_NAMES:
                errors.append(f"bad class {c} row {i}")
            if not all(math.isfinite(v) and 0.0 <= v <= 1.0 for v in vals):
                errors.append(f"range error row {i}")
            if vals[3] <= 0.0 or vals[4] <= 0.0:
                errors.append(f"nonpositive box row {i}")
            by_class[str(c)] = by_class.get(str(c), 0) + 1
            total_boxes += 1
            n += 1
        per_image_counts.append(n)
    sorted_counts = sorted(per_image_counts)
    return {
        "ok": not errors,
        "errors": errors[:20],
        "rows": len(rows),
        "nonempty": nonempty,
        "total_boxes": total_boxes,
        "boxes_by_class": by_class,
        "per_image": {
            "mean": float(np.mean(per_image_counts)) if per_image_counts else 0.0,
            "median": float(np.median(per_image_counts)) if per_image_counts else 0.0,
            "p95": int(sorted_counts[int(0.95 * len(sorted_counts)) - 1]) if sorted_counts else 0,
            "p99": int(sorted_counts[int(0.99 * len(sorted_counts)) - 1]) if sorted_counts else 0,
            "max": max(per_image_counts) if per_image_counts else 0,
            "near_max_det_290": sum(1 for x in per_image_counts if x >= 290),
        },
    }


def export_submission(
    model: YOLO,
    paths: list[Path],
    sample_rows: list[dict[str, str]],
    out_path: Path,
    imgsz: int,
    conf: float,
    iou: float,
    max_det: int,
    batch: int,
    device: str,
) -> dict:
    pred_by_stem: dict[str, str] = {}
    for start in range(0, len(paths), batch):
        chunk = paths[start : start + batch]
        results = model.predict(
            source=[str(p) for p in chunk],
            imgsz=imgsz,
            conf=conf,
            iou=iou,
            max_det=max_det,
            batch=min(batch, len(chunk)),
            device=device,
            agnostic_nms=False,
            verbose=False,
        )
        for p, res in zip(chunk, results):
            pred_by_stem[p.stem] = prediction_string(res)
        print(f"{out_path.name}: predicted {min(start + batch, len(paths))}/{len(paths)}", flush=True)

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "image_id", "prediction_string"])
        writer.writeheader()
        for row in sample_rows:
            stem = str(row["image_id"]).strip()
            writer.writerow({"id": row["id"], "image_id": stem, "prediction_string": pred_by_stem.get(stem, "no box")})
    audit = audit_submission(sample_rows, out_path)
    if not audit["ok"]:
        raise RuntimeError(f"audit failed for {out_path}: {audit['errors']}")
    return audit


def main() -> int:
    started = time.time()
    seed_everything(42)
    work_dir = Path("/kaggle/working") if Path("/kaggle/working").exists() else Path.cwd()
    starter_dir = find_starter_dir()
    dataset_yaml = work_dir / "dataset_r62_nomix_close3.yaml"
    write_dataset_yaml(starter_dir, dataset_yaml)

    print("=" * 80)
    print("R62 low-confidence sweep")
    print(f"starter_dir={starter_dir}")
    print(f"dataset_yaml={dataset_yaml}")
    print(f"torch={torch.__version__} cuda={torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"gpu={torch.cuda.get_device_name(0)}")
    print("=" * 80, flush=True)

    device = "0" if torch.cuda.is_available() else "cpu"
    run_name = "r62_yolov8n_scratch_e10_seed42_nomix_close3_640_repro_20260605"
    model = YOLO("yolov8n.yaml")
    train_start = time.time()
    train_results = model.train(
        data=str(dataset_yaml),
        epochs=10,
        imgsz=640,
        batch=16,
        device=device,
        workers=2,
        project=str(work_dir / "runs" / "detect"),
        name=run_name,
        exist_ok=True,
        pretrained=False,
        optimizer="AdamW",
        lr0=0.003,
        lrf=0.01,
        cos_lr=True,
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=0.5,
        patience=20,
        mosaic=1.0,
        mixup=0.0,
        copy_paste=0.0,
        close_mosaic=3,
        fliplr=0.5,
        translate=0.1,
        scale=0.5,
        cache=False,
        amp=False,
        seed=42,
        verbose=True,
    )
    train_minutes = (time.time() - train_start) / 60.0
    best_weights = Path(train_results.save_dir) / "weights" / "best.pt"
    if not best_weights.is_file():
        raise FileNotFoundError(best_weights)

    trained_model = YOLO(str(best_weights))
    val_results = trained_model.val(
        data=str(dataset_yaml),
        split="val",
        imgsz=640,
        device=device,
        conf=0.001,
        iou=0.5,
        batch=16,
        verbose=False,
    )
    val_metrics = {"map50": float(val_results.box.map50), "map50_95": float(val_results.box.map)}

    sample_path = starter_dir / "sample_submission.csv"
    test_dir = starter_dir / "data" / "test" / "images"
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

    out_dir = work_dir / "submissions_20260605"
    out_dir.mkdir(parents=True, exist_ok=True)
    candidates = [
        {"round": "r94", "conf": 0.000070, "iou": 0.46625, "max_det": 300},
        {"round": "r95", "conf": 0.000065, "iou": 0.46625, "max_det": 300},
        {"round": "r96", "conf": 0.000060, "iou": 0.46625, "max_det": 300},
        {"round": "r97", "conf": 0.000050, "iou": 0.46625, "max_det": 300},
        {"round": "r98", "conf": 0.000060, "iou": 0.466125, "max_det": 300},
    ]
    summaries: list[dict] = []
    for cfg in candidates:
        tag = f"{cfg['round']}_r62_nomix_close3_conf{cfg['conf']:.8f}_iou{cfg['iou']:.6f}".replace(".", "")
        sub_path = out_dir / f"{tag}_submission.csv"
        print("=" * 80)
        print(f"EXPORT {cfg['round']} conf={cfg['conf']} iou={cfg['iou']} max_det={cfg['max_det']}")
        print("=" * 80, flush=True)
        audit = export_submission(
            trained_model,
            paths,
            sample_rows,
            sub_path,
            imgsz=640,
            conf=float(cfg["conf"]),
            iou=float(cfg["iou"]),
            max_det=int(cfg["max_det"]),
            batch=32,
            device=device,
        )
        summary = {
            "round": cfg["round"],
            "weights": str(best_weights),
            "submission": str(sub_path),
            "imgsz": 640,
            "conf": cfg["conf"],
            "iou": cfg["iou"],
            "max_det": cfg["max_det"],
            "batch": 32,
            "device": device,
            "agnostic_nms": False,
            "val_metrics": val_metrics,
            "audit": audit,
            "note": f"{cfg['round']} 2026-06-05: R62 nomix close_mosaic=3 reproduction, low confidence sweep",
            "rule_note": "single YOLOv8n checkpoint, yolov8n.yaml random initialization, provided competition data only, 640 px, no TTA, no ensemble, no pseudo-labeling, no distillation",
        }
        summary_path = out_dir / f"{tag}_summary.json"
        summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        summaries.append(summary)
        print(json.dumps(summary, indent=2), flush=True)

    run_summary = {
        "run_name": run_name,
        "starter_dir": str(starter_dir),
        "dataset_yaml": str(dataset_yaml),
        "best_weights": str(best_weights),
        "train_minutes": train_minutes,
        "val_metrics": val_metrics,
        "total_minutes": (time.time() - started) / 60.0,
        "train_args": {
            "epochs": 10,
            "batch": 16,
            "imgsz": 640,
            "optimizer": "AdamW",
            "lr0": 0.003,
            "lrf": 0.01,
            "momentum": 0.937,
            "weight_decay": 0.0005,
            "warmup_epochs": 0.5,
            "mosaic": 1.0,
            "mixup": 0.0,
            "close_mosaic": 3,
            "seed": 42,
            "pretrained": False,
            "amp": False,
        },
        "candidates": summaries,
        "rule_note": "single YOLOv8n checkpoint, yolov8n.yaml random initialization, provided competition data only, 640 px, no TTA, no ensemble, no pseudo-labeling, no distillation",
    }
    (out_dir / "run_summary.json").write_text(json.dumps(run_summary, indent=2), encoding="utf-8")
    print("=" * 80)
    print("RUN SUMMARY")
    print(json.dumps(run_summary, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
