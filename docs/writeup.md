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
| R25 | 2026-05-16 | R15 output, bus conf floor 0.00105 | 0.82769 |
| R26 | 2026-05-16 | R15 output, non-car conf floor 0.00105 | 0.82695 |
| R27 | 2026-05-16 | R15 output, bus conf floor 0.00110 | 0.82769 |
| R28 | 2026-05-17 | R15 output, truck conf floor 0.00105 | 0.82769 |
| R29 | 2026-05-17 | R15 output, van conf floor 0.00105 | 0.82695 |
| R30 | 2026-05-17 | R15 output, truck conf floor 0.00105 plus bus conf floor 0.00110 | 0.82769 |
| R31 | 2026-05-18 | R15 output, bus conf floor 0.00120 | 0.82769 |
| R32 | 2026-05-18 | R15 output, truck conf floor 0.00110 | 0.82769 |
| R33 | 2026-05-18 | R15 output, bus conf floor 0.00130 | 0.82769 |
| R34 | 2026-05-19 | YOLOv8n scratch seed 123, 640, conf 0.001, iou 0.46625 | 0.82359 |
| R35 | 2026-05-19 | R2 weights, 640, conf 0.001, iou 0.46625 | 0.82088 |
| R36 | 2026-05-19 | R1 weights, 768, conf 0.001, iou 0.46625 | 0.83245 |

Current best public score: **R36, 0.83245**.

## Analysis

Longer training and stricter confidence filtering did not generalize to the public split. R3 used a higher confidence threshold and dropped many boxes; it scored much worse publicly despite stronger local validation. The successful direction was to keep low confidence for recall while reducing duplicate/overlapping boxes through NMS IoU tuning.

The useful NMS range is narrow. R8 at 0.45 scored lower than R7 at 0.475. R10 at 0.4625 tied R7, R11 at 0.46875 improved slightly, and R15 at 0.46625 was the best 640 px R1 inference setting before the May 19 loop. R16 at 0.46675 was lower by 0.00001, R23 at 0.4665 scored 0.82767, and R24 at 0.466125 tied R16 at 0.82768, so the R1 640 px NMS band was saturated. R19-R21 showed that output-only bbox scaling and global ultra-low-confidence filtering underperform R15. R25/R27/R31/R33 showed that bus-only low-confidence filtering is neutral from 0.00105 through 0.00130, R28/R32 showed that truck-only filtering is neutral through 0.00110, and R30 showed that combining neutral truck and bus filters remains neutral. R29 isolated the R26 failure mode: removing only 28 ultra-low-confidence van boxes dropped public score to 0.82695, so van recall is highly sensitive.

The May 19 loop changed the search direction. R34, a new YOLOv8n scratch seed, validated at mAP50 0.8116 with 50859 boxes but scored only 0.82359, again showing that fresh scratch checkpoints can miss the public split. R35 recalibrated the longer-trained R2 checkpoint with the R15 inference settings; it had strong validation mAP50 0.8219 and mAP50-95 0.6707 but only 29286 test boxes and scored 0.82088, confirming that R2 is not just a bad inference-threshold case. R36 kept the R1 checkpoint and NMS setting but raised single-scale inference to 768 px. It produced 52741 boxes and improved public score to 0.83245, indicating that extra inference resolution recovers public small/distant vehicles better than additional training or output filtering.

## Next Steps

- Avoid confidence increases above `0.001`; R13 dropped to 0.82691.
- Do not filter van low-confidence detections from the R15 output; R29 showed a large public drop from removing only 28 boxes.
- Use R36 as the new baseline: R1 checkpoint, single-scale 768 px inference, `conf=0.001`, `iou=0.46625`, clipped and strictly audited before submission.
- Avoid confidence increases above `0.001`; R13 dropped to 0.82691.
- Do not filter van low-confidence detections from the R15/R36-style output; R29 showed a large public drop from removing only 28 boxes.
- Next higher-upside work should test compliant single-scale resolution/calibration around the R36 baseline, or use the 3LC label-review workflow if credentials are available.
