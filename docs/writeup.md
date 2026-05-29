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
| R38 | 2026-05-20 | R1 weights, 640, conf 0.0008, iou 0.46625 | 0.82769 |
| R39 | 2026-05-20 | R1 weights, 640, conf 0.0006, iou 0.46625 | 0.82769 |
| R40 | 2026-05-20 | R1 weights, 640, conf 0.0008, iou 0.46575 | 0.82768 |
| R42 | 2026-05-21 | YOLOv8n scratch seed 42, 12 epochs, 640, conf 0.0006, iou 0.46625 | 0.81293 |
| R44 | 2026-05-21 | R1 weights, 640, conf 0.0007, iou 0.46625 | 0.82769 |
| R45 | 2026-05-21 | R1 weights, 640, conf 0.0007, iou 0.466375 | 0.82768 |
| R46a | 2026-05-22 | R1 weights, 640, conf 0.0005, iou 0.46625 | 0.82864 |
| R46b | 2026-05-22 | R1 weights, 640, conf 0.00065, iou 0.46625 | 0.82769 |
| R49 | 2026-05-22 | R1 weights, 640, conf 0.00045, iou 0.46625 | 0.82864 |
| R50 | 2026-05-23 | R1 weights, 640, conf 0.000475, iou 0.46625 | 0.82864 |
| R51 | 2026-05-23 | R1 weights, 640, conf 0.000525, iou 0.46625 | 0.82864 |
| R52 | 2026-05-23 | R1 weights, 640, conf 0.0005, iou 0.466125 | 0.82862 |
| R53 | 2026-05-24 | R49 output, keep van to 0.00045, filter truck/car/bus below 0.0005 | 0.82864 |
| R54 | 2026-05-24 | R49 output, keep car/van to 0.00045, filter truck/bus below 0.0005 | 0.82864 |
| R55 | 2026-05-24 | R49 output, filter car below 0.0005, keep truck/van/bus to 0.00045 | 0.82864 |
| R58 | 2026-05-25 | R1 weights, 640, conf 0.00055, iou 0.46625 | 0.82833 |
| R59 | 2026-05-25 | R1 weights, 640, conf 0.0005, iou 0.466375 | 0.82862 |
| R56 | 2026-05-25 | R1 weights, 640, conf 0.0005, iou 0.466375 | 0.82862 |
| R61 | 2026-05-26 | R49 output, filter truck below 0.0005, keep car/van/bus to 0.00045 | 0.82864 |
| R62 | 2026-05-26 | R49 output, filter bus below 0.0005, keep truck/car/van to 0.00045 | 0.82864 |
| R60 | 2026-05-26 | R49 output, filter truck/car below 0.0005, keep van/bus to 0.00045 | 0.82864 |
| R63 | 2026-05-27 | R49 output, filter van below 0.0005, keep truck/car/bus to 0.00045 | 0.82864 |
| R64 | 2026-05-27 | R49 output, filter truck/van below 0.0005, keep car/bus to 0.00045 | 0.82864 |
| R65 | 2026-05-27 | R49 output, filter bus/van below 0.0005, keep truck/car to 0.00045 | 0.82864 |
| R66a | 2026-05-29 | R49 output, filter car/bus below 0.0005, keep truck/van to 0.00045 | 0.82864 |
| R67a | 2026-05-29 | R49 output, filter car/van below 0.0005, keep truck/bus to 0.00045 | 0.82864 |
| R66b | 2026-05-29 | R2 weights, 640, conf 0.00045, iou 0.46625 | 0.82271 |
| R72 | 2026-05-29 UTC | R34 seed123 weights, 640, conf 0.0005, iou 0.46625 | 0.82548 |
| R73 | 2026-05-29 UTC | R41 early-stop seed42 weights, 640, conf 0.0005, iou 0.46625 | 0.82838 |
| R74 | 2026-05-29 UTC | R2 weights, 640, conf 0.0005, iou 0.46625 | 0.82271 |

Highest observed public score: **R36, 0.83245**. After re-reading the rules on 2026-05-20, new submissions use the explicit 640 px input-size constraint; the best 640 px public score is **0.82864** from R46a/R49/R50/R51/R53/R54/R55/R60/R61/R62/R63/R64/R65/R66a/R67a.

## Analysis

Longer training and stricter confidence filtering did not generalize to the public split. R3 used a higher confidence threshold and dropped many boxes; it scored much worse publicly despite stronger local validation. The successful direction was to keep low confidence for recall while reducing duplicate/overlapping boxes through NMS IoU tuning.

The useful NMS range is narrow. R8 at 0.45 scored lower than R7 at 0.475. R10 at 0.4625 tied R7, R11 at 0.46875 improved slightly, and R15 at 0.46625 was the best 640 px R1 inference setting before the May 19 loop. R16 at 0.46675 was lower by 0.00001, R23 at 0.4665 scored 0.82767, and R24 at 0.466125 tied R16 at 0.82768, so the R1 640 px NMS band was saturated. R19-R21 showed that output-only bbox scaling and global ultra-low-confidence filtering underperform R15. R25/R27/R31/R33 showed that bus-only low-confidence filtering is neutral from 0.00105 through 0.00130, R28/R32 showed that truck-only filtering is neutral through 0.00110, and R30 showed that combining neutral truck and bus filters remains neutral. R29 isolated the R26 failure mode: removing only 28 ultra-low-confidence van boxes dropped public score to 0.82695, so van recall is highly sensitive.

The May 19 loop changed the search direction. R34, a new YOLOv8n scratch seed, validated at mAP50 0.8116 with 50859 boxes but scored only 0.82359, again showing that fresh scratch checkpoints can miss the public split. R35 recalibrated the longer-trained R2 checkpoint with the R15 inference settings; it had strong validation mAP50 0.8219 and mAP50-95 0.6707 but only 29286 test boxes and scored 0.82088, confirming that R2 is not just a bad inference-threshold case. R36 kept the R1 checkpoint and NMS setting but raised single-scale inference to 768 px. It produced 52741 boxes and improved public score to 0.83245. However, the rules page explicitly states input size 640 px, so later submissions treat 640 px as the active constraint.

The May 20 loop retested the R1 checkpoint under the 640 px constraint. Class-agnostic NMS was rejected before submission because validation mAP50 dropped to 0.7756. Lowering confidence to 0.0008 (R38) and 0.0006 (R39) increased test box counts to 55755 and 63610 but both only tied the 640 px public best at 0.82769. Lowering NMS IoU slightly with the 0.0008 confidence setting (R40) scored 0.82768. This shows that the 640 px R1 operating point is still saturated: additional low-confidence recall is public-neutral, while over-suppression or class-agnostic suppression is harmful.

The May 21 loop tested whether the R1 training recipe benefits from different training duration at 640 px. R42 trained for 12 epochs and achieved local val mAP50 0.8236 with 63548 test boxes, but public score dropped sharply to 0.81293. This confirms that the validation split is not reliable for ranking fresh scratch checkpoints and that longer training can overfit away from the public distribution. The remaining quota was redirected to R1 inference controls: R44 at `conf=0.0007, iou=0.46625` tied the active 640 px best at 0.82769, while R45 at `iou=0.466375` scored 0.82768.

The May 22 loop found that the R1 640 operating point was not fully saturated on the low-confidence side. At the same `iou=0.46625`, lowering confidence to `0.0005` produced 69462 boxes and improved public score to 0.82864. A nearby higher threshold, `0.00065`, returned to 0.82769, while a lower threshold, `0.00045`, produced 73131 boxes and tied 0.82864. The useful 640 px region therefore shifted to `conf≈0.00045-0.0005` with the original R1 checkpoint and `iou=0.46625`.

The May 23 loop refined the low-confidence plateau under the 640 px constraint. R50 at `conf=0.000475` and R51 at `conf=0.000525`, both with `iou=0.46625`, tied the active 640 px best at 0.82864. R52 kept `conf=0.0005` but moved NMS left to `iou=0.466125` and scored 0.82862, confirming that the NMS left shoulder remains slightly worse than the established `0.46625` setting. R53, a class-aware post-processing candidate derived from R49, passed local audit but was rejected by Kaggle with HTTP 400 and produced no submission-list record on May 23.

The May 24 loop tested class-aware filtering from the R49 low-threshold output. R53 kept van detections down to 0.00045 while filtering truck/car/bus below 0.0005; R54 kept car/van down to 0.00045 while filtering truck/bus; R55 filtered only car below 0.0005. All three scored 0.82864. This confirms that these low-confidence class tails can be altered without hurting public score, but the R1 640 px inference-only region remains capped at the same plateau.

The May 25 loop closed the remaining R1 640 inference boundary checks. R58 at `conf=0.00055, iou=0.46625` dropped to 0.82833, showing that the right confidence edge is below 0.00055. R59 and R56 both tested `conf=0.0005, iou=0.466375` and scored 0.82862, matching the earlier conclusion that moving away from `iou=0.46625` in either direction is slightly worse.

The May 26 loop completed R49 class-tail filtering controls under the active 640 px constraint. R61 removed only 120 low-confidence truck boxes, R62 removed only 405 low-confidence bus boxes, and R60 removed 120 truck plus 3080 car low-confidence boxes. All three scored 0.82864. Together with R53-R55, this closes the main safe class-filter combinations from the R49 output: truck, car, bus, and their low-confidence combinations are public-neutral when van is retained, but none improves beyond the plateau.

The May 27 loop tested the remaining R49 van-tail question. R63 removed only 64 van boxes below 0.0005, R64 removed those van boxes plus the 120 low-confidence truck boxes, and R65 removed those van boxes plus the 405 low-confidence bus boxes. All three scored 0.82864. This differs from the earlier R15/R29 failure case: at the lower R49 threshold, the tiny van tail is public-neutral. The practical conclusion is unchanged: class-tail filtering can preserve the plateau but has not produced a public improvement.

The May 29 loop confirmed both remaining failure modes. Additional R49 class-tail combinations (car+bus and car+van filtering at 0.0005) still tie 0.82864 and therefore add evidence that the R49 post-processing space is public-neutral but exhausted. The R2 checkpoint improved from its previous 0.82088 when the confidence threshold was lowered to 0.00045, but only to 0.82271, with substantially fewer boxes than the R1/R49 low-threshold operating point. This indicates R2's gap is not just threshold miscalibration; it is a generalization issue relative to R1.

The May 29 UTC loop used the next UTC-day quota to compare non-R1 checkpoints at the R1-style low-confidence operating point. R72 showed that lowering R34 seed123 from `conf=0.001` to `0.0005` improves public score from 0.82359 to 0.82548, but the checkpoint still trails the R1/R49 plateau. R73 showed that the R41 early-stop seed42 checkpoint is much closer, scoring 0.82838 with 80177 boxes, but still under the 0.82864 active best. R74 showed that R2 at `conf=0.0005` ties the 0.00045 result at 0.82271, so the R2 rescue curve is flat and far below the plateau.

## Next Steps

- Avoid confidence increases above `0.001`; R13 dropped to 0.82691.
- Do not filter van low-confidence detections from the R15 output; R29 showed a large public drop from removing only 28 boxes.
- Use R46a/R49/R50/R51/R53/R54/R55/R60/R61/R62/R63/R64/R65/R66a/R67a as active 640 px tie baselines, but treat further inference-only tail filtering as saturated unless a new diagnostic identifies a specific error mode.
- Further R1 confidence/NMS micro-sweeps have low expected value; both NMS shoulders and the confidence right edge underperformed the 0.82864 plateau.
- Avoid confidence increases above `0.001`; R13 dropped to 0.82691.
- Do not filter van low-confidence detections from the R15/R36-style output; R29 showed a large public drop from removing only 28 boxes.
- Next higher-upside work should use the 3LC label-review workflow if credentials are available, or run rule-constrained 640 px training/label diagnostics rather than more R1 confidence/NMS/class-tail micro-sweeps.
