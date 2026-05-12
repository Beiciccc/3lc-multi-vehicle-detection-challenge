# Experiment Write-up

## Method

The score-chasing workflow uses the competition-provided data only and keeps the model budget fixed to YOLOv8n. The most stable public checkpoint remains R1, a YOLOv8n model trained from scratch for 10 epochs at 640 px with AdamW and no pretrained weights.

The official 3LC starter code is retained, but current runs used a fallback Ultralytics entrypoint because the available runtime does not have a usable 3LC API key. No external data, pseudo-labels, ensembles, TTA, distillation, or pretrained weights were used.

## Findings

Longer training improved local validation but hurt public leaderboard score. R2 and R3 showed that local validation can overestimate public performance, especially when confidence filtering is hardened.

The public leaderboard favored high-recall inference from the shorter R1 checkpoint. Reducing NMS IoU from the original `0.65` improved public score by removing duplicate or low-quality overlaps while retaining low-confidence detections.

The best observed point is R15: `conf=0.001`, `iou=0.46625`, public LB `0.82769`. The May 7 R16-R18 sweep around that point did not improve it.

## Latest Results

| Round | Checkpoint | Inference | Boxes | Public LB |
|---|---|---|---:|---:|
| R13 | R1 | conf=0.0011, iou=0.46875 | 48422 | 0.82691 |
| R14 | R1 | conf=0.0009, iou=0.46875 | 53101 | 0.82765 |
| R15 | R1 | conf=0.001, iou=0.46625 | 50368 | 0.82769 |
| R16 | R1 | conf=0.001, iou=0.46675 | 50406 | 0.82768 |
| R17 | R1 | conf=0.001, iou=0.46575 | 50283 | 0.82765 |
| R18 | R1 | conf=0.001, iou=0.466375 | 50343 | 0.82765 |

Current best: R15, public LB `0.82769`.

## Next Direction

Pure NMS interpolation around R15 is saturated. Next useful work should focus on compliant data-centric improvements through the official 3LC workflow if credentials are available, or on short YOLOv8n-from-scratch seed/augmentation variants calibrated with R15-style inference.

## May 12 Update

The May 12 loop tested output-only post-processing around R15 after NMS micro-sweeps had saturated. Bbox shrinkage, bbox expansion, and ultra-low-confidence filtering all underperformed R15:

| Round | Source | Post-processing | Boxes | Public LB |
|---|---|---|---:|---:|
| R19 | R15 output | bbox scale 0.985 | 50368 | 0.82644 |
| R20 | R15 output | bbox scale 1.010 | 50368 | 0.82760 |
| R21 | R15 output | confidence floor 0.00105 | 49215 | 0.82695 |

Conclusion: preserve R15 geometry and low-confidence tail. The next useful step is a new compliant YOLOv8n-from-scratch checkpoint, then apply R15-style inference calibration.
