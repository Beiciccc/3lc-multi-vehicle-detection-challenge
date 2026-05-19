# 3LC Multi Vehicle Detection Challenge

This repository contains the training, inference, audit, and submission artifacts used for the Kaggle 3LC Multi Vehicle Detection Challenge.

## Competition Compliance

The active experiments follow the competition constraints:

- Architecture: YOLOv8n only.
- Initialization: from-scratch training only; no pretrained COCO or external weights.
- Data: competition-provided train/val/test files only.
- Inference: single checkpoint, no ensemble, no TTA, no pseudo-labeling.
- Submission format: `id,image_id,prediction_string`, matching `competition_starter/sample_submission.csv`.

The official 3LC workflow requires a personal 3LC API key. That workflow was blocked in this environment, so the score-chasing runs use a compliant Ultralytics fallback with YOLOv8n from scratch and documented inference-only sweeps from the R1 checkpoint.

## Repository Layout

- `competition_starter/`: official starter kit, data layout, configs, training and prediction entrypoints.
- `scripts/yolo_fallback_pipeline.py`: compliant fallback training + inference pipeline.
- `scripts/make_inference_submission.py`: reproducible inference from an existing YOLOv8n checkpoint.
- `scripts/clip_submission.py`: normalized bbox clipping before strict submission audit.
- `scripts/audit_submission.py`: local submission validator.
- `submissions/`: generated submission CSVs and JSON summaries.
- `logs/`: Kaggle submit/poll logs, audit logs, and run logs.
- `experiments/run_log.md`: chronological experiment log.
- `docs/writeup.md`: brief methodology and results write-up.
- `docs/proof.md`: proof index for submissions, scores, and audits.
- `docs/3lc.md`: 3LC workflow status and fallback justification.

## Environment

Python 3.11 was used on the remote GPU server with an NVIDIA RTX 4080. Install dependencies with:

```bash
python -m pip install -r requirements.txt
```

Kaggle credentials must be configured separately in `~/.kaggle/kaggle.json` for API submission.

## Data

Expected data layout:

```text
competition_starter/data/train/images
competition_starter/data/train/labels
competition_starter/data/val/images
competition_starter/data/val/labels
competition_starter/data/test/images
competition_starter/sample_submission.csv
```

On macOS volumes, exclude AppleDouble metadata files (`._*`) and `.DS_Store` from syncs and audits.

## Reproduction

### Train fallback YOLOv8n from scratch

```bash
python scripts/yolo_fallback_pipeline.py \
  --starter-dir competition_starter \
  --run-name r1_yolov8n_scratch_e10_640 \
  --epochs 10 --batch 16 --imgsz 640 \
  --device 0 --workers 4 \
  --optimizer AdamW --lr0 0.003 --lrf 0.01 \
  --warmup-epochs 0.5 --mosaic 1.0 --mixup 0.05 \
  --close-mosaic 1 --pred-conf 0.001 --pred-iou 0.65
```

### Reproduce current best public submission

Current best public score after the May 19 loop is R36 at `0.83245`.

```bash
python scripts/make_inference_submission.py \
  --starter-dir competition_starter \
  --weights competition_starter/runs/detect/r1_yolov8n_scratch_e10_640/weights/best.pt \
  --out submissions/r36/r36_r1_imgsz768_conf001_iou046625_submission.csv \
  --summary submissions/r36/r36_r1_imgsz768_conf001_iou046625_summary.json \
  --imgsz 768 --conf 0.001 --iou 0.46625 \
  --max-det 300 --batch 24 --device 0 --val
python scripts/clip_submission.py \
  submissions/r36/r36_r1_imgsz768_conf001_iou046625_submission.csv \
  submissions/r36/r36_r1_imgsz768_conf001_iou046625_submission_clipped.csv
```

### Audit before submitting

```bash
python scripts/audit_submission.py \
  submissions/r36/r36_r1_imgsz768_conf001_iou046625_submission_clipped.csv \
  --sample competition_starter/sample_submission.csv \
  --test-images-dir competition_starter/data/test/images \
  --strict-bbox-inside
```

### Submit with Kaggle API

```bash
kaggle competitions submit \
  -c 3-lc-multi-vehicle-detection-challenge \
  -f submissions/r36/r36_r1_imgsz768_conf001_iou046625_submission_clipped.csv \
  -m "r36_r1_imgsz768_conf0.001_iou0.46625_clipped"
```

Always query `kaggle competitions submissions -c 3-lc-multi-vehicle-detection-challenge` immediately before and after each submit. Count quota only by API accept/reject plus submission-list records.
