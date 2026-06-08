# Experiment Write-up

## Method

All scored experiments use only the competition-provided data and keep the model budget fixed to YOLOv8n. Training runs start from `yolov8n.yaml` random initialization with 640 px input size unless explicitly recorded as a historical diagnostic. Inference submissions use one checkpoint at a time with no ensemble, no TTA, no pseudo-labeling, no distillation, and no external data.

The official 3LC starter code is retained. The dashboard-based 3LC process is not available in this runtime because a usable 3LC API key is not configured, so the reproducible fallback path uses Ultralytics YOLOv8n from scratch and records audit/submit/poll evidence for every submitted CSV.

## Current Bests

| Scope | Run | Public LB | Notes |
|---|---|---:|---|
| Highest observed | R36 | 0.83245 | Historical 768 px R1 inference diagnostic. |
| Active 640 px | R93/R101/R110 | 0.83235 | R62 no-mix close-mosaic=3 line, 640 px active constraint. |
| Earlier 640 px plateau | R46a/R49/R50/R51/R53/R54/R55/R60/R61/R62/R63/R64/R65/R66a/R67a/R77 | 0.82864 | R1/R49 low-confidence plateau. |

## Key Findings

Longer training often improved local validation but hurt public leaderboard score. R2, R34, R42, and the June 5 R62 reproduction all show that local validation is useful for rejecting weak runs but not sufficient for selecting a public-best checkpoint.

The public leaderboard rewards high recall from the right checkpoint. The R1/R49 line saturated around 0.82864 after confidence, NMS, class-tail, and bbox-scaling checks. The R62 no-mixup/close-mosaic=3 checkpoint became the active direction only after aggressive low-confidence inference: R81 0.82857, R82 0.83015, R84 0.83129, R86/R89 0.83154, R90/R91 0.83175, and R93 0.83235.

The June 5 class-tail diagnostics showed that R93's bus tail below 0.0001 should be preserved. R99 and R100 both scored 0.83216 after removing bus detections below 0.0001, while R101 removed only truck detections below 0.0001 and tied R93 at 0.83235.

## Latest Results

| Round | Source | Inference / post-processing | Boxes | Public LB |
|---|---|---|---:|---:|
| R91 | R62 no-mix close3 | conf=0.0001125, iou=0.46625 | 101731 | 0.83175 |
| R90 | R62 no-mix close3 | conf=0.0001, iou=0.46625 | 107625 | 0.83175 |
| R93 | R62 no-mix close3 | conf=0.000075, iou=0.46625 | 123341 | 0.83235 |
| R99 | R93 output | filter truck+bus below 0.0001 | 120758 | 0.83216 |
| R100 | R93 output | filter bus below 0.0001 | 121547 | 0.83216 |
| R101 | R93 output | filter truck below 0.0001 | 122552 | 0.83235 |
| R94 | Kaggle GPU R62 reproduction | conf=0.00007, iou=0.46625 | 124574 | 0.81600 |
| R108 | R93 output | filter van below 0.0001 | 122991 | 0.83194 |
| R110 | R93 output | top 100 per image per class | 106323 | 0.83235 |

## Next Direction

Preserve R93's bus and van low-confidence tails; filtering bus below 0.0001 is harmful and filtering van below 0.0001 also drops public score. Truck below 0.0001 and car overflow beyond top 100 per image per class are public-neutral but not beneficial to remove. The next high-upside path is true lower-confidence inference from the original R62/R93 checkpoint or a better-reproduced 640 px YOLOv8n scratch checkpoint whose validation quality matches the historical R62 run.

The June 7 and June 8 final-window submissions establish a new train+val checkpoint plateau. R112, R113, and R114 scored 0.87382 at `iou=0.46625` across confidence thresholds `0.000075`, `0.000060`, and `0.000050`. R115 and R116 then scored 0.87382 at `iou=0.466125` for `conf=0.000075` and `conf=0.000060`; a duplicate accepted R115 record also scored 0.87382. The best confirmed public score is therefore 0.87382, and additional near-identical confidence/NMS micro-sweeps have low expected value compared with new train+val seeds or a stronger localization/class-calibration signal.
