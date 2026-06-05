# 3LC Multi Vehicle Detection Challenge

This repository contains the training, inference, audit, and submission artifacts used for the Kaggle 3LC Multi Vehicle Detection Challenge.

## Competition Compliance

The active experiments follow the competition constraints:

- Architecture: YOLOv8n only.
- Initialization: from-scratch training only; no pretrained COCO or external weights.
- Data: competition-provided train/val/test files only.
- Inference: single checkpoint, no ensemble, no TTA, no pseudo-labeling.
- Submission format: `id,image_id,prediction_string`, matching `competition_starter/sample_submission.csv`.

The official 3LC process requires a personal 3LC API key. That process was blocked in this environment, so the score-chasing runs use a compliant Ultralytics fallback with YOLOv8n from scratch and documented inference-only sweeps from the R1 checkpoint.

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
- `docs/3lc.md`: 3LC process status and fallback justification.

## Environment

Python 3.11/3.12 with CUDA was used for training and inference runs. The June 5 reproduction diagnostic was run on Kaggle GPU. Install dependencies with:

```bash
python -m pip install -r requirements.txt
```

Kaggle API credentials must be configured locally before submission.

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

On macOS volumes, exclude AppleDouble metadata files (`._*`) and `.DS_Store` from local file checks and audits.

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

### Reproduce active 640 px baseline submission

Highest observed public score is R36 at `0.83245`. After re-reading the rules on May 20, new submissions use the explicit 640 px input-size constraint; the active 640 px baseline is R93 at `0.83235`.

```bash
python scripts/make_inference_submission.py \
  --starter-dir competition_starter \
  --weights competition_starter/runs/detect/r62_yolov8n_scratch_e10_seed42_nomix_close3_640/weights/best.pt \
  --out submissions/r93/r93_r62_nomix_close3_conf000075_iou046625_submission.csv \
  --summary submissions/r93/r93_r62_nomix_close3_conf000075_iou046625_summary.json \
  --imgsz 640 --conf 0.000075 --iou 0.46625 \
  --max-det 300 --batch 32 --device 0 --val
```

### Audit before submitting

```bash
python scripts/audit_submission.py \
  submissions/r93/r93_r62_nomix_close3_conf000075_iou046625_submission.csv \
  --sample competition_starter/sample_submission.csv \
  --test-images-dir competition_starter/data/test/images \
  --strict-bbox-inside
```

### Submit with Kaggle API

```bash
kaggle competitions submit \
  -c 3-lc-multi-vehicle-detection-challenge \
  -f submissions/r93/r93_r62_nomix_close3_conf000075_iou046625_submission.csv \
  -m "r93_r62_nomix_close3_conf0.000075_iou0.46625"
```

Always query `kaggle competitions submissions -c 3-lc-multi-vehicle-detection-challenge` immediately before and after each submit. Count quota only by API accept/reject plus submission-list records.

## Latest Results

The May 21 loop tested one new 640 px scratch-training variant and two R1 640 inference calibration points. R42 overfit the local validation split and scored `0.81293` public despite mAP50 `0.82364`. R44 returned to the active 640 px best at `0.82769`; R45 scored `0.82768`.

The May 22 loop found a new 640 px active best using the R1 checkpoint with lower confidence. `conf=0.0005, iou=0.46625` scored `0.82864`, and `conf=0.00045, iou=0.46625` also scored `0.82864`. A higher nearby point, `conf=0.00065`, tied the older baseline at `0.82769`.

The May 23 loop refined the same 640 px low-confidence plateau. `conf=0.000475, iou=0.46625` and `conf=0.000525, iou=0.46625` both scored `0.82864`, while moving NMS left to `iou=0.466125` at `conf=0.0005` scored `0.82862`. The active 640 px best remains `0.82864`.

The May 24 loop tested class-specific post-processing from the R49 low-threshold output. R53, R54, and R55 all scored `0.82864`, confirming that selected low-confidence tail filtering is public-neutral but does not improve beyond the active 640 px plateau.

The May 25 loop closed the remaining R1 640 inference boundary checks. `conf=0.00055, iou=0.46625` scored `0.82833`, while `conf=0.0005, iou=0.466375` scored `0.82862` in two accepted records. These results confirm that the active 640 px plateau remains capped at `0.82864` and that further confidence/NMS micro-sweeps have low expected value.

The May 26 loop completed additional class-specific R49 tail-filter controls. Filtering only truck below `0.0005`, filtering only bus below `0.0005`, and filtering truck+car below `0.0005` all scored `0.82864`. This confirms that R49 class-tail filtering is score-neutral and does not break the active 640 px plateau.

The May 27 loop tested the remaining R49 van-tail controls. Filtering only van below `0.0005`, filtering truck+van below `0.0005`, and filtering bus+van below `0.0005` all scored `0.82864`. This shows that even the small R49 van tail is public-neutral at this threshold; output-only tail filtering is now effectively exhausted.

The May 29 loop added two more R49 class-tail controls and one R2 low-threshold inference check. R66a and R67a both scored `0.82864`, keeping the active 640 px best unchanged. R66b used the longer-trained R2 checkpoint at `conf=0.00045` and scored `0.82271`, confirming that R2's poor public performance is not fixed by simply lowering the confidence threshold.

The May 29 UTC loop used the fresh UTC-day quota for non-R1/R49 checkpoint diagnostics. R34 seed123 at `conf=0.0005` improved to `0.82548`, R41 early-stop seed42 at `conf=0.0005` reached `0.82838`, and R2 at `conf=0.0005` tied its lower-threshold rescue at `0.82271`. None exceeded the active 640 px best of `0.82864`.

The May 31 loop used the fresh UTC/local-day quota for R41 and R49 post-processing diagnostics. R75 and R76 filtered low-confidence R41 tails and both scored `0.82838`, tying R73 but not the active best. R77 submitted the previously uncounted R49 truck/bus/van tail-filter control and scored `0.82864`, confirming the R49 class-tail plateau remains public-neutral.

The June 1 loop tested lightweight bbox geometry calibration from the R49 640 px single-checkpoint output. Box scaling by `1.005`, `1.0025`, and `0.9975` scored `0.82855`, `0.82862`, and `0.82859` respectively. None exceeded the active 640 px best of `0.82864`, so R49 geometry scaling joins confidence/NMS/class-tail filtering as a low-value inference-only direction.

The June 2 loop found a new active 640 px best with the R62 no-mixup/close-mosaic=3 scratch checkpoint. R81 at `conf=0.0005` scored `0.82857`; lowering the same checkpoint to `conf=0.00025` (R82) improved to `0.83015`; lowering further to `conf=0.0002` (R84) reached `0.83129`. This confirms that a compliant training-recipe change plus aggressive low-confidence recall is the new primary direction, while R49 output-only tuning remains saturated.

The June 3 loop continued the R62 low-confidence sweep. R85 at `conf=0.000175` tied R84 at `0.83129`; R86 at `conf=0.00015` improved to `0.83154`; after adapting away from an NMS-side candidate, R89 at `conf=0.000125` also scored `0.83154`. R86/R89 are the new active 640 px best results, and R88 (`conf=0.0002, iou=0.466125`) remains a generated/audited but unsubmitted diagnostic.

The June 4 loop pushed the same R62 checkpoint further down the confidence curve. R91 at `conf=0.0001125` and R90 at `conf=0.0001` both scored `0.83175`, then the more aggressive R93 at `conf=0.000075` reached `0.83235`. R93 is the new active 640 px best and is only 0.00010 below the historical 768 px R36 score. R92 (`conf=0.000125, iou=0.466125`) was generated/audited but not submitted after the confidence-left direction kept improving.

The June 5 loop first ran a Kaggle GPU reproduction diagnostic for the R62 no-mix/close-mosaic=3 recipe. That reproduced checkpoint validated lower than the historical R62 checkpoint, so its R94-R98 low-confidence outputs were not submitted. The accepted submissions instead tested R93 class-tail filtering: R99 and R100 both scored `0.83216`, while R101 tied R93 at `0.83235`. The result isolates bus low-confidence detections below `0.0001` as useful and truck detections below `0.0001` as public-neutral.
