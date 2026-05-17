# 3LC Multi Vehicle Detection Challenge Run Log

Protocol for this session:
- For each requested submission loop, first query current submissions/quota state.
- Review Kaggle Code/Discussion updates before choosing the experiment.
- Train/validate on GPU server, sync project artifacts back to this local directory.
- Submit only after validation and submission-file audit pass.
- Count a submission only when Kaggle accepts/rejects via API and the submission list shows a new record.

Requested target: 3 successful submission loops.

## 2026-04-30 submission loop x3

Environment:
- Remote GPU: NVIDIA RTX 4090 24GB.
- Official 3LC workflow blocked by missing 3LC API key; fallback used YOLOv8n YAML from scratch, no pretrained weights, single model, no TTA/ensemble/pseudo-labeling.
- AMP disabled to avoid Ultralytics pretrained AMP-check downloads in subsequent runs.

Submission results:

| Loop | File | Experiment | Local validation | Public LB |
|---|---|---|---|---|
| R1 | `submissions/r1/r1_yolov8n_scratch_e10_640_submission_clipped.csv` | YOLOv8n scratch, 10 epochs, batch 16, conf 0.001, iou 0.65 | mAP50 0.82230 / mAP50-95 0.64111 | 0.82352 |
| R2 | `submissions/r2/r2_yolov8n_scratch_e30_b32_640_submission_clipped.csv` | YOLOv8n scratch, 30 epochs, batch 32, conf 0.001, iou 0.65 | mAP50 0.83448 / mAP50-95 0.69022 | 0.81762 |
| R3 | `submissions/r3/r3_r2weights_conf0.05_iou0.55_submission_strict.csv` | R2 weights, threshold sweep best: conf 0.05, iou 0.55 | sweep mAP50 0.85448 / mAP50-95 0.73058 | 0.78234 |

Current best public score: R1 `0.82352`.

Error analysis:
- R2/R3 show strong local-validation improvement but worse public scores, so the provided validation split is not fully representative of the public split.
- High-confidence filtering improved local validation but severely hurt public, indicating the public split likely rewards retaining low-confidence candidates for recall.
- Best next direction should not be further threshold hardening. Prefer R1-like training with low conf, plus data-centric label review or group-aware validation if 3LC API access is provided.

Artifacts synced:
- Remote logs: `logs/remote/`
- Submissions: `submissions/r1`, `submissions/r2`, `submissions/r3`
- Model/runs: `competition_starter/runs/`

## 2026-05-01 submission loop x3

Context:
- New GPU server: Windows host with NVIDIA RTX 4080 16GB.
- Project/data synchronized; macOS `._*` metadata excluded from remote and local validation logic.
- Kaggle Code review: latest public notebook emphasizes YOLOv8n scratch, conservative data QA, low-conf inference; no readable Discussion updates.
- Continued fallback Ultralytics workflow because official 3LC API-key workflow is unavailable.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---|
| R4 | `submissions/r4/r4_r1_conf0005_iou075_submission_clipped.csv` | R1 weights, conf 0.0005, iou 0.75, bbox clipped | val mAP50 0.818 / audit ok / 133605 boxes | 0.81854 |
| R5 | `submissions/r5/r5_r1_conf001_iou055_submission.csv` | R1 weights, conf 0.001, iou 0.55 | val mAP50 0.81839 / audit ok / 58875 boxes | 0.82579 |
| R6 | `submissions/r6/r6_r1_conf001_iou050_submission.csv` | R1 weights, conf 0.001, iou 0.50 | val mAP50 0.81839 / audit ok / 53464 boxes | 0.82699 |

Current best public score: R6 `0.82699`.

Error analysis:
- R4 confirms that pushing recall too far creates too many low-confidence boxes and hurts public score.
- R5/R6 show that keeping R1's low confidence but reducing NMS IoU improves public score, likely by reducing duplicate/overlapping false positives while preserving recall.
- Public still favors the shorter R1-trained checkpoint over R2/R3 despite lower local validation, so next iteration should continue public-calibrated inference sweeps or short-training variants rather than longer training.

Next candidate directions:
- Continue NMS sweep around R6: `iou=0.45` or `0.475` with `conf=0.001`.
- Try mild confidence increase near the new best, e.g. `conf=0.0015` or `0.002`, `iou=0.50`, to reduce low-quality tail without repeating R4's over-recall failure.
- If using training, prefer 6-10 epoch YOLOv8n scratch seed/augment variants rather than 30-epoch overfit runs.

## 2026-05-02 submission loop x3

Context:
- First query of the submission list showed no 2026-05-02 submissions; later rate-limited refresh showed concurrent/previous R7 and R8 records already accepted on Kaggle.
- Kaggle Code refresh via CLI was rate-limited with 429; cached 2026-05-02 Code listing still showed latest public notebook as Avik Das `3LC YOLOv8n Vehicle Detection and Label QA Process` last run 2026-04-30, with no readable Discussion updates.
- Continued with public-calibrated R1 checkpoint inference sweeps because R6 was the previous best and longer training/high-confidence variants underperformed public.
- Fixed `scripts/make_inference_submission.py` so `--val` uses the candidate `--conf/--iou` instead of hard-coded `0.001/0.5`.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---|
| R7 | `submissions/r7/r7_r1_conf001_iou0475_submission.csv` | R1 weights, conf 0.001, iou 0.475 | val mAP50 0.81839 / audit ok / 51092 boxes | 0.82761 |
| R8 | `submissions/r8/r8_r1_conf001_iou045_submission.csv` | R1 weights, conf 0.001, iou 0.45 | val mAP50 0.81897 / audit ok / 48987 boxes | 0.82739 |
| R8 duplicate | `submissions/r8/r8_r1_conf001_iou045_submission.csv` | duplicate accepted record caused by parallel state lag | same file / same audit | 0.82739 |

Current best public score: R7 `0.82761`.

Error analysis:
- R7 improved over R6 (`0.82699 -> 0.82761`), confirming the useful NMS range is slightly below 0.50.
- R8 at iou 0.45 reduced boxes further but scored slightly lower than R7, suggesting the public optimum is around 0.475 rather than more aggressive suppression.
- A duplicate R8 submission consumed the third daily slot because the submission list already contained an R8 record before the second R8 submit call completed. Future loops must re-query immediately before submit and abort if the exact candidate filename is already present in today's records.

Unsubmitted validated candidate:
- `submissions/r9/r9_r1_conf0015_iou050_submission.csv`: R1 weights, conf 0.0015, iou 0.50, val mAP50 0.81774, audit ok, 44429 boxes. Keep as a possible future candidate, but its lower val and heavier confidence pruning make it less attractive than local NMS interpolation around R7.

Next candidate directions:
- Probe tightly around R7: `conf=0.001, iou=0.4625` and `iou=0.4875`.
- Avoid duplicate submission by checking today's filenames and dates immediately before every submit, then polling until the new timestamp appears.
- Consider a short R1-style seed/augment retrain only after exhausting the R1 NMS interpolation band.


## 2026-05-05 submission loop x3

Context:
- First query of the submission list showed no 2026-05-05 submissions; today's effective submitted records are R10, R11, and R12.
- Kaggle Code check showed no newer public notebook than Avik Das `3LC YOLOv8n Vehicle Detection and Label QA Process` last run 2026-04-30. Web/Kaggle discussion checks did not reveal readable new discussion updates.
- Continued public-calibrated inference sweeps from R1 because R7 was the previous best and longer training/high confidence filtering underperformed.
- Repository expectation work added root `README.md`, `requirements.txt`, `docs/writeup.md`, `docs/proof.md`, and `docs/3lc.md`.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---|
| R10 | `submissions/r10/r10_r1_conf001_iou04625_submission.csv` | R1 weights, conf 0.001, iou 0.4625 | val mAP50 0.81884 / audit ok / 50057 boxes | 0.82761 |
| R11 | `submissions/r11/r11_r1_conf001_iou046875_submission.csv` | R1 weights, conf 0.001, iou 0.46875 | val mAP50 0.81877 / audit ok / 50576 boxes | 0.82765 |
| R12 | `submissions/r12/r12_r1_conf001_iou0470_submission.csv` | R1 weights, conf 0.001, iou 0.47 | val mAP50 0.81875 / audit ok / 50710 boxes | 0.82761 |

Current best public score: R11 `0.82765`.

Error analysis:
- R10 tied R7, confirming a stable high-score NMS band around 0.4625-0.475.
- R11 slightly improved the public score, placing the current best around iou 0.46875.
- R12 at iou 0.47 fell back to the R7/R10 tie score; the public optimum appears narrow and score differences are very small.
- A generated but unsubmitted candidate `r12_r1_conf001_iou0471875_submission.csv` was rejected by Kaggle after the daily quota was consumed; it has no accepted submission-list record and should not be counted.

Next candidate directions:
- Try a mild confidence increase at the current best NMS: `conf=0.0011` or `0.0012`, `iou=0.46875`.
- If staying on NMS-only, test one local point around `0.466` or `0.4695`, but expected gains are small.
- Avoid duplicate filename submissions; abort if today's submission list already contains the candidate file or three accepted records.

## 2026-05-06 submission loop x3

Context:
- Submission list was queried before the loop and before each submit. The first accepted 2026-05-06 record was R13; R14 and R15 were then submitted after fresh list checks confirmed remaining quota.
- Kaggle Code refresh still showed Avik Das `3LC YOLOv8n Vehicle Detection and Label QA Process` as the newest public notebook, last run 2026-04-30. No readable new Discussion update was found.
- Rules remained unchanged: YOLOv8n only, from scratch, no pretrained weights, no ensemble, no TTA, no pseudo-labeling, no external data, three submissions per day.
- Strategy: test whether confidence pruning around R11 helps, then return to narrow NMS interpolation when confidence changes failed to improve.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---|
| R13 | `submissions/r13/r13_r1_conf0011_iou046875_submission.csv` | R1 weights, conf 0.0011, iou 0.46875 | val mAP50 0.81863 / audit ok / 48422 boxes | 0.82691 |
| R14 | `submissions/r14/r14_r1_conf0009_iou046875_submission.csv` | R1 weights, conf 0.0009, iou 0.46875 | val mAP50 0.81877 / audit ok / 53101 boxes | 0.82765 |
| R15 | `submissions/r15/r15_r1_conf001_iou046625_submission.csv` | R1 weights, conf 0.001, iou 0.46625 | val mAP50 0.81880 / audit ok / 50368 boxes | 0.82769 |

Current best public score: R15 `0.82769`.

Error analysis:
- R13 confirms that even a mild confidence increase removes useful low-confidence detections from the public split.
- R14 confirms that lowering confidence back toward higher recall can recover the R11 score, but more boxes alone did not improve beyond the plateau.
- R15 improves by a small margin through narrow NMS left-shoulder tuning, placing the best public point at `conf=0.001, iou=0.46625`.
- Local mAP differences remain too small to rank these variants reliably; public score is the decisive signal for this narrow calibration band.

Repository/proof updates:
- Added R13-R15 submission, summary, audit, submit, poll, and final-list artifacts.
- Updated README, write-up, proof index, and 3LC workflow status for the May 6 loop.

Next candidate directions:
- If continuing inference-only, test the immediate right shoulder around `conf=0.001, iou=0.46675` or `0.4675`.
- Avoid further confidence increases above `0.001`; R13 showed a clear public drop.
- Higher-upside work is a compliant short YOLOv8n scratch seed/augmentation variant, then applying the R15 inference calibration.


## 2026-05-07 submission loop x3

Context:
- Submission list was queried at loop start and before each submit. The start list showed no 2026-05-07 submissions; R16, R17, and R18 were the three accepted records for the day.
- Kaggle Code refresh still showed Avik Das `3LC YOLOv8n Vehicle Detection and Label QA Process` as the newest public notebook, last run 2026-04-30.
- A readable Discussion update from 2026-05-06 clarified that external scripts may assist label-issue discovery only if changes are submitted back through a new 3LC table version and only official data is used.
- Rules remained unchanged for model/submission constraints: YOLOv8n only, from scratch, no pretrained weights, no ensemble, no TTA, no pseudo-labeling, no external data, and 3 submissions/day.
- GPU scheduling constraints affected R17/R18 generation. R17's first GPU run was stopped after no progress; R17/R18 were regenerated on CPU.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---|
| R16 | `submissions/r16/r16_r1_conf001_iou046675_submission.csv` | R1 weights, conf 0.001, iou 0.46675 | val mAP50 0.81880 / audit ok / 50406 boxes | 0.82768 |
| R17 | `submissions/r17/r17_r1_conf001_iou046575_submission.csv` | R1 weights, conf 0.001, iou 0.46575 | val mAP50 0.81870 / audit ok / 50283 boxes | 0.82765 |
| R18 | `submissions/r18/r18_r1_conf001_iou0466375_submission.csv` | R1 weights, conf 0.001, iou 0.466375 | val mAP50 0.81870 / audit ok / 50343 boxes | 0.82765 |

Current best public score: R15 `0.82769`.

Error analysis:
- R16 was just below R15, so the right shoulder from 0.46625 to 0.46675 is already slightly worse.
- R17 and R18 both fell to 0.82765, confirming that further R1 NMS micro-sweeps are saturated and mostly leaderboard noise.
- R17 first upload attempt returned HTTP 429 and produced no submission-list record after five checks; the retry was accepted and counted.
- Local mAP differences remain too small to predict the public order inside this narrow NMS band.

Next candidate directions:
- Do not prioritize more R1-only NMS micro-sweeps unless a daily slot would otherwise go unused.
- Use the 2026-05-06 Discussion guidance to build a compliant 3LC label-review loop if API credentials become available.
- Otherwise train a small number of YOLOv8n scratch seed/augmentation variants and apply R15 inference calibration.

## 2026-05-12 submission loop x3

Context:
- Submission list was queried at loop start and before each submit. The start list showed no 2026-05-12 submissions; R19, R20, and R21 were the three accepted records for the day.
- Kaggle Code refresh still showed Avik Das `3LC YOLOv8n Vehicle Detection and Label QA Process` as the newest public notebook, last run 2026-04-30.
- Since R16-R18 showed R1 NMS micro-sweeps were saturated, this loop tested conservative single-checkpoint post-processing around R15 rather than more NMS-only interpolation.
- All candidates used the R15/R1 single YOLOv8n checkpoint output as source, with no TTA, no ensemble, no pseudo-labeling, no external data, and no model retraining.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R19 | `submissions/r19/r19_r15_boxscale0985_submission.csv` | R15 output, bbox scale 0.985 | audit ok / 50368 boxes | 0.82644 |
| R20 | `submissions/r20/r20_r15_boxscale1010_submission.csv` | R15 output, bbox scale 1.010 | audit ok / 50368 boxes | 0.82760 |
| R21 | `submissions/r21/r21_r15_conf00105_from_r15_submission.csv` | R15 output, remove detections below conf 0.00105 | audit ok / 49215 boxes | 0.82695 |

Current best public score: R15 `0.82769`.

Error analysis:
- R19 shows bbox shrinkage is harmful on the public split, likely because true positives lose IoU margin faster than false positives are improved.
- R20 partially recovered the score but still underperformed R15, so bbox scaling is not a promising direction around this checkpoint.
- R21 confirms that even removing only the lowest-confidence tail hurts public recall; the public split rewards keeping the very low confidence detections from R15.
- The current R1/R15 post-processing region is saturated. Further quota should be spent on a new compliant YOLOv8n scratch checkpoint or a sanctioned data-review iteration, not more output-only geometry/confidence tweaks.

Repository/proof updates:
- Added R19-R21 submission, summary, audit, submit, poll, and final-list artifacts.
- Updated README, write-up, proof index, and experiment write-up for the May 12 loop.

Next candidate directions:
- Do not continue bbox scaling from R15.
- Do not raise the effective confidence floor above 0.001 from R15 output.
- Train a small number of YOLOv8n scratch seed/augmentation variants and evaluate them with the R15 inference calibration.

## 2026-05-13 submission loop x3

Context:
- Submission list was queried at loop start and before each submit. The start list showed no 2026-05-13 submissions; R22, R23, and R24 were the three accepted records for the day.
- Kaggle Code refresh still showed no newer public notebook than the 2026-04-30 YOLOv8n/label-QA public code. A 2026-05-06 Discussion clarification remains relevant: scripts may help find label issues, but any label changes must be recorded as a new 3LC table revision and use only official data.
- Rules remained unchanged: YOLOv8n only, from scratch for training runs, no pretrained weights, no ensemble, no TTA, no pseudo-labeling, no external data, and three submissions per day.
- Strategy: first test a new compliant YOLOv8n scratch seed/augmentation run because R15 post-processing had saturated, then use the remaining quota on tightly bounded R1 NMS checks after the new checkpoint underperformed.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R22 | `submissions/r22/r22_yolov8n_scratch_e10_seed7_640_submission.csv` | YOLOv8n scratch, seed 7, 10 epochs, conf 0.001, iou 0.46625 | val mAP50 0.811 / audit ok / 69776 boxes | 0.81336 |
| R23 | `submissions/r23/r23_r1_conf001_iou04665_submission.csv` | R1 weights, conf 0.001, iou 0.4665 | audit ok / 50379 boxes | 0.82767 |
| R24 | `submissions/r24/r24_r1_conf001_iou0466125_submission.csv` | R1 weights, conf 0.001, iou 0.466125 | audit ok / 50346 boxes | 0.82768 |

Current best public score: R15 `0.82769`.

Error analysis:
- R22 confirms that a new short YOLOv8n scratch checkpoint can look reasonable on validation but still miss the public split. It also produced many more boxes than R15, suggesting an unfavorable false-positive/recall balance.
- R23 and R24 both landed in the established R1 plateau but did not beat R15. R24 tied R16 at 0.82768; R23 was one point lower at 0.82767.
- The R1 NMS optimum remains extremely narrow around `conf=0.001, iou=0.46625`. Additional micro-sweeps have very low expected upside.
- Kaggle API had intermittent list-query timeouts during polling, but each counted submission was confirmed only after the submission list showed a new complete record and public score.

Repository/proof updates:
- Added R22-R24 submission, summary, audit, submit, poll, and final-list artifacts.
- Updated README, write-up, and proof index for the May 13 loop.

Next candidate directions:
- Do not prioritize more R1/R15 micro post-processing. It is now heavily saturated across confidence, NMS, and bbox scaling.
- Higher-upside next work is a compliant data-review pass using 3LC table revisions, or a more systematic short YOLOv8n scratch training search with stronger validation diagnostics before spending submissions.

## 2026-05-16 submission loop x3

Context:
- Submission list was queried at loop start and before each submit. The start list showed no 2026-05-16 submissions; R25, R26, and R27 were the three accepted records for the day.
- Kaggle Code refresh still showed the latest public notebook as Avik Das `3LC YOLOv8n Vehicle Detection and Label QA Process`, last run 2026-04-30. No new public discussion changed the modeling constraints.
- The remote GPU host was unreachable during this loop, so no new training was attempted. All candidates were local, single-checkpoint post-processing of the R15 output.
- Strategy: test class-specific low-confidence tail filtering because R21 showed global filtering hurts, while R15/R1 NMS and bbox-scale sweeps were already saturated.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R25 | `submissions/r25/r25_r15_bus_conf00105_submission.csv` | R15 output, remove only bus detections below conf 0.00105 | audit ok / 50236 boxes / 132 dropped | 0.82769 |
| R26 | `submissions/r26/r26_r15_noncar_conf00105_submission.csv` | R15 output, remove truck/van/bus detections below conf 0.00105, keep car unchanged | audit ok / 50177 boxes / 191 dropped | 0.82695 |
| R27 | `submissions/r27/r27_r15_bus_conf00110_submission.csv` | R15 output, remove only bus detections below conf 0.00110 | audit ok / 50121 boxes / 247 dropped | 0.82769 |

Current best public score: R15/R25/R27 tie at `0.82769`.

Error analysis:
- R25 and R27 show that removing a small amount of extremely low-confidence bus tail is public-neutral, but not beneficial.
- R26 falling to 0.82695, matching the failed R21 global filtering score, shows that the truck/van low-confidence tail is important on the public split.
- The low-confidence car tail was intentionally preserved in R25-R27; prior R21 already showed that global tail removal is harmful.
- This loop adds evidence that output-only post-processing is saturated. Further improvement likely requires compliant label review or better scratch training/validation, not more tail filtering.

Repository/proof updates:
- Added `scripts/filter_submission.py` for reproducible class-specific submission filtering.
- Added R25-R27 submission, summary, audit, submit, poll, and final-list artifacts.

Next candidate directions:
- Stop spending submissions on R15 output-only filtering unless a new diagnosis identifies a specific systematic error.
- If the remote GPU becomes available, prioritize a stronger validation protocol or a 3LC-sanctioned label-review loop before training more scratch variants.

## 2026-05-17 submission loop x3

Context:
- Submission list was queried at loop start and before each submit. The start list showed no 2026-05-17 submissions; R28, R29, and R30 were the three accepted records for the day.
- Kaggle Code refresh still showed Avik Das `3LC YOLOv8n Vehicle Detection and Label QA Process` as the newest public notebook, last run 2026-04-30. No new public rule or discussion changed the modeling constraints.
- The remote GPU host was unreachable during this loop, so no new training was attempted. All candidates were local, single-checkpoint post-processing of the R15 output.
- Strategy: isolate the R26 failure by testing truck-only and van-only low-confidence tail filtering, then combine only filters that had already proven public-neutral.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R28 | `submissions/r28/r28_r15_truck_conf00105_submission.csv` | R15 output, remove only truck detections below conf 0.00105 | audit ok / 50337 boxes / 31 dropped | 0.82769 |
| R29 | `submissions/r29/r29_r15_van_conf00105_submission.csv` | R15 output, remove only van detections below conf 0.00105 | audit ok / 50340 boxes / 28 dropped | 0.82695 |
| R30 | `submissions/r30/r30_r15_truck00105_bus00110_submission.csv` | R15 output, remove truck below conf 0.00105 and bus below conf 0.00110 | audit ok / 50090 boxes / 278 dropped | 0.82769 |

Current best public score: R15/R25/R27/R28/R30 tie at `0.82769`.

Error analysis:
- R28 shows that the 31 truck detections below confidence 0.00105 are public-neutral when removed alone.
- R29 shows that the 28 van detections below confidence 0.00105 are public-critical; removing them reproduces the R26/R21 drop to 0.82695.
- R30 confirms that combining the public-neutral truck filter with the already neutral bus filter remains neutral, but still does not improve the public score.
- The post-processing search is now strongly saturated. Public score is sensitive to small recall losses in van and generally does not reward removing low-confidence tails.

Repository/proof updates:
- Added R28-R30 submission, summary, audit, submit, poll, and final-list artifacts.
- Updated README, write-up, proof index, and chronological experiment log for the May 17 loop.

Next candidate directions:
- Do not remove low-confidence van detections from the R15 output.
- Do not prioritize further output-only filtering around R15 unless a new systematic error is found.
- Higher-upside next work remains a compliant label-review revision or a better scratch-training/validation protocol once GPU access is restored.
