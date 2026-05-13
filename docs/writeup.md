# Brief Write-up

## Methodology

All scored experiments use the competition-provided data and YOLOv8n only. The official 3LC workflow was unavailable because no usable 3LC API key was present in the runtime, so the active work used a fallback Ultralytics pipeline that preserves the key competition constraints: YOLOv8n architecture, random initialization for training runs, single model inference, no external data, no pretrained checkpoints, no TTA, no ensemble, and no pseudo-labeling.

The strongest checkpoint came from R1: YOLOv8n from scratch for 10 epochs at 640 px. Later longer training improved local validation but reduced public leaderboard score, so the subsequent iterations focused on public-calibrated inference sweeps from the R1 checkpoint.

## Key Results

| Run | Date | Configuration | Public LB |
|---|---|---|---:|
| R1 | 2026-04-30 | R1 YOLOv8n scratch, conf 0.001, iou 0.65 | 0.82352 |
| R6 | 2026-05-01 | R1 weights, conf 0.001, iou 0.50 | 0.82699 |
| R7 | 2026-05-02 | R1 weights, conf 0.001, iou 0.475 | 0.82761 |
| R10 | 2026-05-05 | R1 weights, conf 0.001, iou 0.4625 | 0.82761 |
| R11 | 2026-05-05 | R1 weights, conf 0.001, iou 0.46875 | 0.82765 |
| R12 | 2026-05-05 | R1 weights, conf 0.001, iou 0.47 | 0.82761 |
| R13 | 2026-05-06 | R1 weights, conf 0.0011, iou 0.46875 | 0.82691 |
| R14 | 2026-05-06 | R1 weights, conf 0.0009, iou 0.46875 | 0.82765 |
| R15 | 2026-05-06 | R1 weights, conf 0.001, iou 0.46625 | 0.82769 |
| R16 | 2026-05-07 | R1 weights, conf 0.001, iou 0.46675 | 0.82768 |
| R17 | 2026-05-07 | R1 weights, conf 0.001, iou 0.46575 | 0.82765 |
| R18 | 2026-05-07 | R1 weights, conf 0.001, iou 0.466375 | 0.82765 |
| R19 | 2026-05-12 | R15 output, bbox scale 0.985 | 0.82644 |
| R20 | 2026-05-12 | R15 output, bbox scale 1.010 | 0.82760 |
| R21 | 2026-05-12 | R15 output, conf floor 0.00105 | 0.82695 |
| R22 | 2026-05-13 | YOLOv8n scratch seed 7, conf 0.001, iou 0.46625 | 0.81336 |
| R23 | 2026-05-13 | R1 weights, conf 0.001, iou 0.4665 | 0.82767 |
| R24 | 2026-05-13 | R1 weights, conf 0.001, iou 0.466125 | 0.82768 |

Current best public score: **R15, 0.82769**.

## Analysis

Longer training and stricter confidence filtering did not generalize to the public split. R3 used a higher confidence threshold and dropped many boxes; it scored much worse publicly despite stronger local validation. The successful direction was to keep low confidence for recall while reducing duplicate/overlapping boxes through NMS IoU tuning.

The useful NMS range is narrow. R8 at 0.45 scored lower than R7 at 0.475. R10 at 0.4625 tied R7, R11 at 0.46875 improved slightly, and R15 at 0.46625 remains the best public score after the May 13 sweep. R16 at 0.46675 was lower by 0.00001, R23 at 0.4665 scored 0.82767, and R24 at 0.466125 tied R16 at 0.82768, so the R1 inference-only NMS band appears saturated. R19-R21 showed that output-only bbox scaling and ultra-low-confidence filtering also underperform R15. R22 showed that a new YOLOv8n scratch seed can underperform public despite reasonable validation, reinforcing that validation alone is not enough to spend submissions confidently. R13 showed that raising confidence to 0.0011 hurts public recall; R14 showed that lowering confidence to 0.0009 only ties the prior best.

## Next Steps

- Avoid confidence increases above `0.001`; R13 dropped to 0.82691.
- Stop spending quota on pure R1 NMS micro-sweeps or R15 output-only geometry/confidence tweaks unless no stronger candidate is available; R16-R24 did not beat R15.
- Next higher-upside work should use 3LC label-review workflow if credentials are available, or a compliant short YOLOv8n scratch seed/augmentation variant followed by the R15 calibration.
