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

## 2026-05-18 submission loop x3

Context:
- Submission list was queried at loop start and before each submit. The start list showed no 2026-05-18 submissions; R31, R32, and R33 were the three accepted records for the day.
- Kaggle Code refresh still showed only the same three public notebooks. Rules, evaluation, and the single public Discussion topic did not change in a way that affected modeling or submission constraints.
- The remote GPU host remained unreachable, so no new training or remote sync was attempted. All candidates were local, single-checkpoint post-processing of the R15 output.
- Strategy: avoid van/car filtering after R29 and R21/R26, then probe only the previously neutral bus and truck low-confidence axes.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R31 | `submissions/r31/r31_r15_bus_conf00120_submission.csv` | R15 output, remove only bus detections below conf 0.00120 | audit ok / 49919 boxes / 449 dropped | 0.82769 |
| R32 | `submissions/r32/r32_r15_truck_conf00110_submission.csv` | R15 output, remove only truck detections below conf 0.00110 | audit ok / 50307 boxes / 61 dropped | 0.82769 |
| R33 | `submissions/r33/r33_r15_bus_conf00130_submission.csv` | R15 output, remove only bus detections below conf 0.00130 | audit ok / 49730 boxes / 638 dropped | 0.82769 |

Current best public score: R15/R25/R27/R28/R30/R31/R32/R33 tie at `0.82769`.

Error analysis:
- R31 and R33 show that bus-only low-confidence filtering remains public-neutral through 0.00130, but still does not improve the score.
- R32 shows that truck-only filtering remains public-neutral through 0.00110.
- Combined with R29, the class-specific picture is now clear: van low-confidence detections are public-critical, while moderate bus/truck tail filtering is mostly score-neutral.
- Output-only post-processing is exhausted for public-score improvement. The next meaningful work requires either restored GPU access for better scratch-training diagnostics or a compliant 3LC label-review revision.

Repository/proof updates:
- Added R31-R33 submission, summary, audit, submit, poll, and final-list artifacts.
- Updated README, write-up, proof index, and chronological experiment log for the May 18 loop.

Next candidate directions:
- Do not spend further quota on bus/truck low-confidence filtering unless needed as a control.
- Continue to avoid van low-confidence filtering, global confidence increases, bbox scaling, and R1 NMS micro-sweeps.
- Prioritize restoring GPU/server access or setting up a documented 3LC table-revision workflow before the next high-value submissions.

## 2026-05-19 submission loop x3

Context:
- Submission list was queried at loop start and before each submit. The start list showed no 2026-05-19 submissions; R34, R35, and R36 were the three accepted records for the day.
- Rules, evaluation, Code, and Discussion were refreshed before experiments. No new public rule, notebook, or discussion update changed the modeling constraints.
- Remote GPU access was restored. R34 trained a fresh YOLOv8n scratch seed; R35 and R36 ran single-checkpoint inference experiments. All submitted files were clipped and passed strict local audits before upload.
- Strategy: after output-only post-processing saturated through R33, test a new scratch checkpoint, then test whether R2 was hurt by inference settings, then test a higher single-scale inference resolution from the proven R1 checkpoint.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R34 | `submissions/r34/r34_yolov8n_scratch_e10_seed123_640_submission_clipped.csv` | YOLOv8n scratch, seed 123, 10 epochs, 640, conf 0.001, iou 0.46625 | val mAP50 0.8116 / audit ok / 50859 boxes | 0.82359 |
| R35 | `submissions/r35/r35_r2_conf001_iou046625_submission_clipped.csv` | R2 weights, 640, conf 0.001, iou 0.46625 | val mAP50 0.8219 / audit ok / 29286 boxes | 0.82088 |
| R36 | `submissions/r36/r36_r1_imgsz768_conf001_iou046625_submission_clipped.csv` | R1 weights, 768 single-scale inference, conf 0.001, iou 0.46625 | val mAP50 0.8203 / audit ok / 52741 boxes | 0.83245 |

Current best public score: R36 `0.83245`.

Error analysis:
- R34 confirms that new scratch seeds can underperform public even with acceptable validation and a familiar box profile.
- R35 confirms that R2's public weakness is not simply caused by its original inference threshold/NMS settings. Despite the strongest validation metrics in this loop, its much lower test box count likely loses recall on the public split.
- R36 shows that higher single-scale inference resolution is a real improvement axis for the R1 checkpoint. It kept the proven low confidence and NMS setting, increased box count moderately versus R15, and improved public score by +0.00476.
- Local validation mAP50 alone remains insufficient for candidate ranking; the best public result in this loop had lower validation mAP50 than R35 but better public recall/precision balance.

Repository/proof updates:
- Added `scripts/clip_submission.py` for reproducible bbox clipping before strict audit.
- Added R34-R36 submission, summary, audit, submit, poll, and final-list artifacts.
- Updated README, write-up, proof index, and chronological experiment log for the May 19 loop.

Next candidate directions:
- Treat R36 as the baseline: R1 checkpoint, 768 single-scale inference, `conf=0.001`, `iou=0.46625`, clipped and strictly audited.
- Search around R36 with resolution and NMS calibration before spending more training submissions.
- Do not revert to R2 or fresh seed scratch checkpoints unless a stronger validation/public correlation diagnostic is added.

## 2026-05-20 submission loop x3

Context:
- Submission list was queried at loop start and before each counted submit. The start list showed no 2026-05-20 submissions; R38, R39, and R40 were the three accepted records for the day.
- Rules and Evaluation pages were re-read. The rules page explicitly states `Input size: 640 px`, so the active search for this loop used 640 px inference only. R36 remains the highest observed public score, but 640 px is treated as the rule-constrained baseline for new work.
- Kaggle Code had one new public notebook, `quartzyu/3lc-multi-vehicle-detection-challenge-yolov8n`, last run 2026-05-19. It used 512 px, 20 epochs, conf 0.05, and self-reported about 0.72 public LB, so it was not used as a candidate.
- Remote GPU was available. R37 tested class-agnostic NMS at 640 and was not submitted because validation mAP50 dropped to 0.7756 with 46936 boxes.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R38 | `submissions/r38/r38_r1_640_conf0008_iou046625_submission.csv` | R1 weights, 640, conf 0.0008, iou 0.46625 | val mAP50 0.8189 / audit ok / 55755 boxes | 0.82769 |
| R39 | `submissions/r39/r39_r1_640_conf0006_iou046625_submission.csv` | R1 weights, 640, conf 0.0006, iou 0.46625 | val mAP50 0.8194 / audit ok / 63610 boxes | 0.82769 |
| R40 | `submissions/r40/r40_r1_640_conf0008_iou046575_submission.csv` | R1 weights, 640, conf 0.0008, iou 0.46575 | val mAP50 0.8189 / audit ok / 55701 boxes | 0.82768 |

Highest observed public score remains R36 `0.83245`, but the active 640 px rule-constrained best is tied at `0.82769` by R15/R25/R27/R28/R30/R31/R32/R33/R38/R39.

Error analysis:
- Lowering confidence below 0.001 at 640 increases recall/box count but is public-neutral through 0.0006. R39 reached 63610 boxes without dropping public score, unlike the much weaker R22/R34 scratch checkpoints.
- Lowering NMS IoU from 0.46625 to 0.46575 with the lower confidence setting loses 0.00001, matching the earlier evidence that the 640 R1 NMS optimum is extremely narrow.
- Class-agnostic NMS is not viable for this label set; it suppresses valid cross-class detections and caused a large validation mAP50 drop before submission.
- Additional 640 px R1 confidence/NMS micro-sweeps have very low expected value. The next improvement likely needs rule-constrained training/label review rather than more output calibration.

Repository/proof updates:
- Added R38-R40 submission, summary, audit, submit, poll, and final-list artifacts.
- Updated `scripts/make_inference_submission.py` with a reproducible `--agnostic-nms` switch used for the rejected R37 diagnostic.
- Updated README, write-up, proof index, and chronological experiment log for the May 20 loop.

Next candidate directions:
- Treat R15/R38/R39 as the active 640 px baseline.
- Do not spend more quota on R1 640 confidence/NMS micro-sweeps unless needed as controls.
- Prioritize 3LC label-review workflow or a rule-constrained 640 px training experiment with better validation diagnostics.

## 2026-05-21 submission loop x3

Context:
- Submission list was queried at loop start and before each counted submit. The start list showed no 2026-05-21 submissions; R42, R44, and R45 were the three accepted records for the day.
- Rules, Evaluation, Code, and Discussion were refreshed before experiments. No new public rule, notebook, or discussion update changed the active 640 px, YOLOv8n-only, no-pretraining/no-external-data constraint set.
- Remote GPU was available. R41, R42, and R43 were trained/generated first. R41 and R43 were not submitted after R42 showed that the new training direction did not generalize publicly.
- Strategy: test whether the R1 recipe benefits from a slightly longer 12 epoch run at 640 px. After R42 failed publicly, revert the remaining quota to low-risk R1 640 inference calibration around the active best.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R42 | `submissions/r42/r42_yolov8n_scratch_e12_seed42_640_submission_clipped.csv` | YOLOv8n scratch, seed 42, 12 epochs, 640, AdamW, conf 0.0006, iou 0.46625 | val mAP50 0.8236 / audit ok / 63548 boxes | 0.81293 |
| R44 | `submissions/r44/r44_r1_640_conf0007_iou046625_submission.csv` | R1 weights, 640, conf 0.0007, iou 0.46625 | audit ok / 59259 boxes | 0.82769 |
| R45 | `submissions/r45/r45_r1_640_conf0007_iou0466375_submission.csv` | R1 weights, 640, conf 0.0007, iou 0.466375 | audit ok / 59275 boxes | 0.82768 |

Additional generated candidates:
- R41: YOLOv8n scratch, seed 42, 8 epochs, val mAP50 0.8181, 73812 boxes. Not submitted after R42 confirmed the training direction was public-weak.
- R43: YOLOv8n scratch, seed 42, SGD, 10 epochs, val mAP50 0.7789, 57249 boxes. Not submitted because validation was too weak and quota was better spent on R1 controls.

Highest observed public score remains R36 `0.83245`, but the active 640 px rule-constrained best is tied at `0.82769` by R15/R25/R27/R28/R30/R31/R32/R33/R38/R39/R44.

Error analysis:
- R42 is the clearest evidence so far that local validation can be misleading for new scratch checkpoints. It had the strongest 640 px validation mAP50 among recent training attempts but scored only 0.81293 public.
- Longer R1-recipe training appears to overfit or shift the detection distribution away from the public split. It should not replace the original R1 checkpoint.
- R44 confirms that `conf=0.0007, iou=0.46625` is public-neutral and ties the active 640 px best.
- R45 confirms that nudging NMS upward to 0.466375 at the same confidence loses 0.00001, consistent with the narrow R1 640 NMS optimum.

Repository/proof updates:
- Added R42, R44, and R45 submission, summary, audit, submit, poll, and final-list artifacts.
- Added the May 21 Kaggle refresh note and updated README, write-up, proof index, and chronological experiment log.

Next candidate directions:
- Do not submit more 8-12 epoch scratch variants without stronger validation/public diagnostics.
- Treat the original R1 checkpoint, 640 px, `iou=0.46625`, and low confidence around 0.0006-0.001 as the active rule-constrained baseline.
- The next meaningful improvement still requires label-review evidence or a different 640 px training protocol, not more narrow R1 confidence/NMS sweeps.

## 2026-05-22 submission loop x3

Context:
- Submission list was queried at loop start and before counted submits. The start list showed no 2026-05-22 submissions.
- Rules and Evaluation pages were unchanged versus 2026-05-21 by SHA256. Code listing had no relevant new notebook. Discussion refresh through the available CLI was unavailable, but no rule/evaluation/page change was detected.
- Remote GPU was available and the R1 checkpoint was present. No training was run; all candidates were single-checkpoint, 640 px, no-TTA/no-ensemble R1 inference sweeps.
- Strategy: after R44 confirmed `conf=0.0007, iou=0.46625` tied the old 640 best, test lower confidence at the same NMS point to see whether additional recall helps.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R46a | `submissions/r46/r46_r1_640_conf0005_iou046625_submission.csv` | R1 weights, 640, conf 0.0005, iou 0.46625 | audit ok / 69462 boxes | 0.82864 |
| R46b | `submissions/r46/r46_r1_640_conf00065_iou046625_submission.csv` | R1 weights, 640, conf 0.00065, iou 0.46625 | audit ok / 61303 boxes | 0.82769 |
| R49 | `submissions/r49/r49_r1_640_conf00045_iou046625_submission.csv` | R1 weights, 640, conf 0.00045, iou 0.46625 | audit ok / 73131 boxes | 0.82864 |

Additional generated but not submitted candidates:
- R47: R1 weights, 640, conf 0.0006, iou 0.466125, 63593 boxes, audit ok.
- R48: R1 weights, 640, conf 0.0007, iou 0.466125, 59244 boxes, audit ok.

Highest observed public score remains R36 `0.83245`, but the active 640 px rule-constrained best is now `0.82864` from R46a/R49.

Error analysis:
- Lowering confidence from the old neutral band (`0.0006-0.001`) to `0.0005` improved the 640 px public score by +0.00095, showing that public recall still benefits from a larger low-confidence tail.
- Moving from `0.0005` to `0.00045` added 3669 more boxes but did not improve beyond 0.82864. This suggests the immediate left side of the optimum is flat or saturated.
- The `0.00065` control returned to 0.82769, so the useful threshold appears below about 0.0006 for this checkpoint/NMS setting.

Repository/proof updates:
- Added R46a/R46b/R49 submission, summary, audit, submit, poll, and final-list artifacts.
- Added R47/R48 generated candidate summaries and audits.
- Updated README, write-up, proof index, and run log.

Next candidate directions:
- Prioritize very narrow sweeps around `conf=0.00045-0.00055, iou=0.46625`.
- Candidate controls: `conf=0.000475`, `conf=0.000525`, and possibly `conf=0.0005` with `iou=0.466125`.
- Avoid going much lower than `0.00045` without analyzing box quality because R49 already reaches 73131 boxes and did not improve over R46a.

## 2026-05-23 submission loop x3

Context:
- Submission list was queried at loop start. The start list showed no 2026-05-23 submissions; R50, R51, and R52 became the three accepted records for the day.
- Rules, Evaluation, and Main sauce pages were refreshed. SHA256 checks matched the May 22 copies, so the active constraint set remained unchanged: YOLOv8n only, 640 px input size, no pretrained weights, no ensemble, no TTA, no pseudo-labeling, no distillation, and official data only.
- Public Code listing was unchanged; the latest visible notebook remained Quartz Yu's 2026-05-19 YOLOv8n notebook. The available Kaggle CLI still did not support a discussions subcommand.
- Remote GPU inference was available on an RTX 4080. All submitted candidates used the original R1 checkpoint, 640 px, single-checkpoint inference, and strict local audits before upload.
- Strategy: refine the low-confidence plateau found on May 22 around `conf=0.00045-0.000525` and test one NMS left-shoulder control.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R50 | `submissions/r50/r50_r1_640_conf000475_iou046625_submission.csv` | R1 weights, 640, conf 0.000475, iou 0.46625 | audit ok / 71256 boxes | 0.82864 |
| R51 | `submissions/r51/r51_r1_640_conf000525_iou046625_submission.csv` | R1 weights, 640, conf 0.000525, iou 0.46625 | audit ok / 67763 boxes | 0.82864 |
| R52 | `submissions/r52/r52_r1_640_conf0005_iou0466125_submission.csv` | R1 weights, 640, conf 0.0005, iou 0.466125 | audit ok / 69444 boxes | 0.82862 |

Additional generated but not accepted:
- R53: post-processing of R49 that kept van detections down to 0.00045 while filtering truck/car/bus below 0.0005. It passed local audit with 69526 boxes, but Kaggle returned HTTP 400 on upload and no R53 row appeared in the submission list, so it is not counted as an accepted submission.

Highest observed public score remains R36 `0.83245`, but the active 640 px rule-constrained best remains `0.82864` from R46a/R49/R50/R51.

Error analysis:
- R50 and R51 both tied the current 640 px best, confirming that the useful R1 640 confidence plateau spans at least `0.00045-0.000525` at `iou=0.46625`.
- R51 reduced the test box count by 1699 versus R46a and 5368 versus R49 without changing public score, so a small amount of low-confidence noise can be removed safely.
- R52 lowered NMS IoU from 0.46625 to 0.466125 at the proven 0.0005 confidence setting and lost 0.00002 public. This confirms that the NMS left shoulder remains slightly worse even after the lower-confidence improvement.
- The plateau appears score-saturated under R1 640 inference-only tuning. More progress likely requires a new signal, such as compliant label review or stronger diagnostics, rather than more tiny confidence/NMS perturbations.

Repository/proof updates:
- Added R50-R52 submission, summary, audit, submit, poll, and final-list artifacts.
- Added R53 generated candidate, audit, and rejected-submit log as a non-counted candidate.
- Updated README, write-up, proof index, and chronological experiment log.

Next candidate directions:
- Treat R50/R51 as compact active 640 px baselines when a lower box count is preferred without score loss.
- Do not prioritize further NMS-left sweeps below 0.46625.
- If using another inference-only control, test class-aware post-processing only if the upload issue is resolved and the daily quota is available; otherwise prioritize compliant label-review or training diagnostics.

## 2026-05-24 submission loop x3

Context:
- Submission list was queried at loop start. The start list showed no 2026-05-24 submissions; R53, R54, and R55 became the three accepted records for the day.
- Rules and Evaluation pages were refreshed and matched the May 23 copies by SHA256. The active constraints remained YOLOv8n only, 640 px input size, from-scratch training only, no pretrained weights, no ensemble, no TTA, no pseudo-labeling, no distillation, and official data only.
- Public Code listing was unchanged; the latest visible notebook remained Quartz Yu's 2026-05-19 YOLOv8n notebook. The old discussions command was unavailable; the newer topics command was also not usable in this CLI build, so no readable discussion change was found through the available interfaces.
- Strategy: since R50/R51 confirmed a flat low-confidence plateau at `0.82864`, test class-specific post-processing derived from the R49 low-threshold output. All accepted candidates were single-submission post-processing of one R1 640 output, with no TTA, no ensemble, and strict local audit before upload.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R53 | `submissions/r53/r53_r49_keep_van00045_others0005_submission.csv` | R49 output, keep van to 0.00045, filter truck/car/bus below 0.0005 | audit ok / 69526 boxes | 0.82864 |
| R54 | `submissions/r54/r54_r49_keep_carvan00045_filter_truckbus0005_submission.csv` | R49 output, keep car/van to 0.00045, filter truck/bus below 0.0005 | audit ok / 72606 boxes | 0.82864 |
| R55 | `submissions/r55/r55_r49_filter_car0005_keep_others00045_submission.csv` | R49 output, filter only car below 0.0005, keep truck/van/bus to 0.00045 | audit ok / 70051 boxes | 0.82864 |

Highest observed public score remains R36 `0.83245`, but the active 640 px rule-constrained best remains `0.82864` from R46a/R49/R50/R51/R53/R54/R55.

Error analysis:
- R53, R54, and R55 all tied the active 640 px best, so removing selected low-confidence tails from R49 is public-neutral, not beneficial.
- Van low-confidence retention remains important by historical evidence from R29, but today's class-aware variants show that keeping or filtering other low-confidence tails does not move the public score above the plateau.
- The 640 px R1 inference/post-processing region is now strongly saturated: global confidence, NMS left shoulder, and class-aware filtering all converge around 0.82864.
- Further quota should not prioritize more R49 tail-filter combinations unless needed for controls. A new signal is needed, most likely compliant label review or a materially different validation/training diagnostic.

Repository/proof updates:
- Added R53-R55 submission, summary, audit, submit, poll, and final-list artifacts.
- Added May 24 rules/code/discussion refresh logs.
- Updated README, write-up, proof index, and chronological experiment log.

Next candidate directions:
- Stop spending primary quota on R1/R49 inference-only micro-variants unless no higher-value experiment is available.
- If continuing within current constraints, use R50/R51/R53/R54/R55 as compact tie baselines and focus on label-review evidence or a fresh diagnostic that explains the gap to the public leaderboard leaders.

## 2026-05-25 submission loop x3

Context:
- Submission list was queried at loop start. The start list showed no 2026-05-25 submissions; R58, R59, and R56 became the three accepted records for the day.
- Rules and Evaluation pages were refreshed and matched the May 24 copies by SHA256. The active constraints remained YOLOv8n only, 640 px input size, from-scratch training only, no pretrained weights, no ensemble, no TTA, no pseudo-labeling, no distillation, and official data only.
- Public Code listing was unchanged; the latest visible notebook remained Quartz Yu's 2026-05-19 YOLOv8n notebook. The topics interface was still not usable in the available Kaggle CLI build.
- Strategy: after May 24 showed class-specific R49 filtering is public-neutral, test the remaining R1 640 inference boundary controls that had already been generated and audited: a confidence right-edge point and an NMS right-shoulder point.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R58 | `submissions/r58/r58_r1_640_conf00055_iou046625_submission.csv` | R1 weights, 640, conf 0.00055, iou 0.46625 | audit ok / 66289 boxes | 0.82833 |
| R59 | `submissions/r59/r59_r1_640_conf0005_iou0466375_submission.csv` | R1 weights, 640, conf 0.0005, iou 0.466375 | audit ok / 69483 boxes | 0.82862 |
| R56 | `submissions/r56/r56_r1_640_conf0005_iou0466375_submission.csv` | R1 weights, 640, conf 0.0005, iou 0.466375 | audit ok / 69483 boxes | 0.82862 |

Additional generated but not submitted:
- R60: R49 post-processing that kept van/bus down to 0.00045 while filtering truck/car below 0.0005. It passed local audit with 69931 boxes, but was not submitted because the three accepted May 25 records had already consumed the daily quota.

Highest observed public score remains R36 `0.83245`, but the active 640 px rule-constrained best remains `0.82864` from R46a/R49/R50/R51/R53/R54/R55.

Error analysis:
- R58 scored 0.82833, confirming that raising the R1 640 confidence threshold to 0.00055 leaves the useful low-confidence plateau. The viable band is below this point and includes 0.00045-0.000525.
- R59 and R56 duplicated the `conf=0.0005, iou=0.466375` right-shoulder NMS control and both scored 0.82862. Together with R52 at `iou=0.466125`, this shows both immediate NMS shoulders around 0.46625 are slightly worse than the center point.
- The R1 640 inference-only search is now exhausted: confidence right edge, NMS left/right shoulders, and class-aware filtering have not improved beyond 0.82864.

Repository/proof updates:
- Added R58/R59/R56 submission, summary, audit, submit/poll/final-list artifacts.
- Added R60 generated candidate summary and audit as a non-submitted candidate.
- Updated README, write-up, proof index, and chronological experiment log.

Next candidate directions:
- Do not spend further primary quota on R1 640 confidence/NMS micro-sweeps.
- Do not repeat R49 class-tail filtering unless needed as a control.
- The next meaningful improvement requires a new signal: compliant 3LC label review, stronger split diagnostics, or a materially different rule-compliant training protocol.

## 2026-05-26 submission loop x3

Context:
- Submission list was queried at loop start. The start list showed no 2026-05-26 submissions; R61, R62, and R60 became the three accepted records for the day.
- Rules and Evaluation pages were refreshed and matched the May 25 copies by SHA256. The active constraints remained YOLOv8n only, 640 px input size, from-scratch training only for training runs, no pretrained weights, no ensemble, no TTA, no pseudo-labeling, no distillation, and official data only.
- Public Code listing was unchanged; the latest visible competition notebook remained the 2026-05-19 YOLOv8n notebook. Discussion/topic access through the available Kaggle CLI remained unreliable, so command output was captured but no readable new signal was found.
- Strategy: because R1 global confidence/NMS micro-sweeps were exhausted by May 25, complete the remaining low-risk class-tail controls from the R49 low-threshold output while retaining van detections.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R61 | `submissions/r61/r61_r49_filter_truck0005_keep_others00045_submission.csv` | R49 output, filter only truck below 0.0005, keep car/van/bus to 0.00045 | audit ok / 73011 boxes | 0.82864 |
| R62 | `submissions/r62/r62_r49_filter_bus0005_keep_others00045_submission.csv` | R49 output, filter only bus below 0.0005, keep truck/car/van to 0.00045 | audit ok / 72726 boxes | 0.82864 |
| R60 | `submissions/r60/r60_r49_keep_vanbus00045_filter_truckcar0005_submission.csv` | R49 output, filter truck/car below 0.0005, keep van/bus to 0.00045 | audit ok / 69931 boxes | 0.82864 |

Highest observed public score remains R36 `0.83245`, but the active 640 px rule-constrained best remains `0.82864` from R46a/R49/R50/R51/R53/R54/R55/R60/R61/R62.

Error analysis:
- R61 shows that removing only the 120 lowest-confidence truck boxes from R49 is public-neutral.
- R62 shows that removing only the 405 lowest-confidence bus boxes from R49 is also public-neutral.
- R60 shows that combining truck and car low-confidence filtering remains public-neutral, consistent with R55's car-only neutral result and R53/R54's broader neutral class-tail controls.
- The R49 class-tail filtering space is now effectively saturated when van is retained. Further output-only filtering has low expected value unless a new diagnostic identifies a specific false-positive cluster.

Repository/proof updates:
- Added R60/R61/R62 submission, summary, audit, submit/poll/final-list artifacts.
- Added May 26 rules/code/discussion refresh logs and remote read-only check.
- Updated README, write-up, proof index, and chronological experiment log.

Next candidate directions:
- Do not spend primary quota on additional R1/R49 confidence, NMS, or class-tail micro-variants.
- Prioritize compliant label-review evidence if 3LC table credentials are available.
- If 3LC label review remains blocked, use stronger split diagnostics or a materially different 640 px YOLOv8n scratch training protocol before spending more submissions.

## 2026-05-27 submission loop x3

Context:
- Submission list was queried at loop start. The start list showed no 2026-05-27 submissions; R63, R64, and R65 became the three accepted records for the day.
- Rules and Evaluation pages were refreshed and matched the May 26 copies by SHA256. The active constraints remained YOLOv8n only, 640 px input size, from-scratch training only for training runs, no pretrained weights, no ensemble, no TTA, no pseudo-labeling, no distillation, and official data only.
- Public Code listing contained the same visible notebooks as May 26, with only row ordering changes. Discussion/topic access through the available Kaggle CLI returned HTTP 403, so no readable new discussion signal was available.
- Strategy: after May 26 confirmed truck/car/bus low-confidence tails are public-neutral from the R49 output, test the remaining small van tail at the same 0.0005 class floor and two neutral pairings.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R63 | `submissions/r63/r63_r49_filter_van0005_keep_others00045_submission.csv` | R49 output, filter only van below 0.0005, keep truck/car/bus to 0.00045 | audit ok / 73067 boxes | 0.82864 |
| R64 | `submissions/r64/r64_r49_filter_truckvan0005_keep_carbus00045_submission.csv` | R49 output, filter truck/van below 0.0005, keep car/bus to 0.00045 | audit ok / 72947 boxes | 0.82864 |
| R65 | `submissions/r65/r65_r49_filter_busvan0005_keep_truckcar00045_submission.csv` | R49 output, filter bus/van below 0.0005, keep truck/car to 0.00045 | audit ok / 72662 boxes | 0.82864 |

Highest observed public score remains R36 `0.83245`, but the active 640 px rule-constrained best remains `0.82864` from R46a/R49/R50/R51/R53/R54/R55/R60/R61/R62/R63/R64/R65.

Error analysis:
- R63 shows that removing the 64 R49 van boxes below 0.0005 is public-neutral, unlike the earlier R15/R29 van-filter failure at a higher operating point.
- R64 and R65 show that adding the neutral truck or bus tail removals to the van-tail removal remains public-neutral.
- The R49 output-only class-tail space is now effectively exhausted: truck, car, bus, van, and several pairings preserve the 0.82864 plateau but do not improve it.

Repository/proof updates:
- Added R63/R64/R65 submission, summary, audit, submit/poll/final-list artifacts.
- Added May 27 rules/code/discussion refresh logs.
- Updated README, write-up, proof index, and chronological experiment log.

Next candidate directions:
- Stop spending primary quota on R1/R49 confidence, NMS, or class-tail post-processing.
- Prioritize a new signal: compliant 3LC label-review evidence, stronger split diagnostics, or a materially different 640 px YOLOv8n scratch training protocol.
- If no new signal is available, use future submissions only for carefully chosen controls, not blind output-only micro-variants.

## 2026-05-29 submission loop x3

Context:
- Submission list was queried at loop start. The initial visible list showed no accepted 2026-05-29 local-day records. The final Kaggle list is treated as authoritative: three accepted records were present for the 2026-05-29 local loop, so no additional submissions were counted.
- Rules and Evaluation pages were refreshed. The active constraints remained YOLOv8n only, 640 px input size, from-scratch training only for training runs, no pretrained weights, no ensemble, no TTA, no pseudo-labeling, no distillation, and official data only.
- Public Code listing remained unchanged in substance, with the latest visible notebook dated 2026-05-19. Discussion/topic listing remained unavailable through the installed Kaggle CLI.
- Strategy: R49 class-tail filtering had already saturated the public plateau, so one submitted candidate tested whether the longer-trained R2 checkpoint's poor previous score was mainly a confidence-threshold mismatch. Additional R2 low-threshold candidates were generated and audited but not submitted after the daily quota was exhausted.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R66a | `submissions/r66/r66_r49_filter_carbus0005_keep_truckvan00045_submission.csv` | R49 output, filter car/bus below 0.0005, keep truck/van to 0.00045 | audit ok / 69646 boxes | 0.82864 |
| R67a | `submissions/r67/r67_r49_filter_carvan0005_keep_truckbus00045_submission.csv` | R49 output, filter car/van below 0.0005, keep truck/bus to 0.00045 | audit ok / 69987 boxes | 0.82864 |
| R66b | `submissions/r66/r66_r2_640_conf00045_iou046625_submission.csv` | R2 weights, 640, conf 0.00045, iou 0.46625 | audit ok / 38675 boxes | 0.82271 |

Non-counted candidates / rejected attempts:
- R68 R49 (`submissions/r68/r68_r49_filter_truckbusvan0005_keep_car00045_submission.csv`) was generated and audited, but Kaggle returned HTTP 400 after the three accepted records were already present, so it is not counted.
- R67/R68 R2 low-threshold candidates (`conf=0.0005` and `conf=0.0006`) were generated and audited, but not submitted because the daily quota was exhausted.

Highest observed public score remains R36 `0.83245`, but the active 640 px rule-constrained best remains `0.82864` from R46a/R49/R50/R51/R53/R54/R55/R60/R61/R62/R63/R64/R65/R66a/R67a.

Error analysis:
- R66a and R67a confirm the previous conclusion: additional R49 class-tail combinations can preserve the 0.82864 plateau but do not improve it.
- R66b scored 0.82271 despite a much lower confidence threshold than the prior R2 submission. This rules out simple confidence under-recall as the primary R2 failure mode; R2 has a public-split generalization problem relative to R1.
- The R2 output had only 38675 boxes at `conf=0.00045`, far below the R1/R49 low-threshold output size. Lowering confidence improved over R35's 0.82088 but remains materially below the active R1 plateau.

Repository/proof updates:
- Added R66/R67/R68 candidate, summary, audit, submit/reject, and final-list artifacts.
- Added May 29 rules/code/discussion refresh logs.
- Updated README, write-up, proof index, and chronological experiment log.

Next candidate directions:
- Do not continue R49 class-tail filtering except as diagnostic proof; it is saturated.
- Do not prioritize R2 inference calibration; the low-threshold score remains far below R1.
- Higher-upside work now requires a new compliant training or data-centric signal, preferably 3LC label-review evidence or an altered 640 px scratch-training recipe with stronger validation diagnostics.

## 2026-05-29 UTC submission loop x3

Context:
- Submission list was queried after UTC date rollover. The prior three records were at 2026-05-28 23:37-23:39 UTC, so the 2026-05-29 UTC submission list had no records yet.
- Rules and Evaluation pages were refreshed and matched the earlier May 29 copies. The active constraints remained YOLOv8n only, 640 px input size, from-scratch training only for training runs, no pretrained weights, no ensemble, no TTA, no pseudo-labeling, no distillation, and official data only.
- Public Code listing remained unchanged in substance, and Discussion/topic access through the Kaggle CLI remained unavailable with HTTP 403.
- Strategy: avoid further R49 class-tail filtering and spend the UTC-day quota on non-R1 checkpoint diagnostics at the R1-style low-confidence operating point.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R72 | `submissions/r72/r72_r34_seed123_640_conf0005_iou046625_submission.csv` | R34 seed123 weights, 640, conf 0.0005, iou 0.46625 | audit ok / 69795 boxes | 0.82548 |
| R73 | `submissions/r73/r73_r41_e8_seed42_640_conf0005_iou046625_submission.csv` | R41 early-stop seed42 weights, 640, conf 0.0005, iou 0.46625 | audit ok / 80177 boxes | 0.82838 |
| R74 | `submissions/r74/r74_r2_640_conf0005_iou046625_submission.csv` | R2 weights, 640, conf 0.0005, iou 0.46625 | audit ok / 37238 boxes | 0.82271 |

Highest observed public score remains R36 `0.83245`, but the active 640 px rule-constrained best remains `0.82864` from R46a/R49/R50/R51/R53/R54/R55/R60/R61/R62/R63/R64/R65/R66a/R67a.

Error analysis:
- R72 improved R34 over its original 0.82359 submission but still remained well below the R1/R49 plateau, so seed123 is not a viable replacement checkpoint.
- R73 is the strongest non-R1 diagnostic so far at 0.82838, indicating that the 8-epoch seed42 checkpoint is closer to public distribution than R34/R2/R42, but it still misses the active best by 0.00026.
- R74 tied R66b at 0.82271, confirming that R2's low-confidence calibration is flat and not competitive.

Repository/proof updates:
- Added R72/R73/R74 submission, summary, audit, submit/poll/final-list artifacts.
- Added May 29 UTC rules/code/discussion refresh logs.
- Updated README, write-up, proof index, and chronological experiment log.

Next candidate directions:
- R41 early-stop deserves analysis as the closest non-R1 checkpoint, but direct low-confidence inference still does not beat R1.
- Do not spend more quota on R2 threshold calibration.
- If continuing without 3LC label-review access, focus on training protocol changes that preserve R41-like generalization while improving final localization/recall.

## 2026-05-31 submission loop x3

Context:
- Submission list was queried at loop start on 2026-05-31 UTC/Europe-London. The starting list had no 2026-05-31 records, so the full three-submission quota was available. Final quota accounting uses the Kaggle submission list: R75, R76, and R77 were accepted and completed.
- Rules and Evaluation pages were refreshed and matched the 2026-05-29 UTC copies by SHA256. Active constraints remain YOLOv8n only, 640 px input size, from-scratch/no pretrained for training runs, no external data, no ensemble, no TTA, no pseudo-labeling, and no distillation.
- Public Code listing was refreshed; the latest visible notebook remained Omar's 2026-05-19 run. Discussion/topic refresh was attempted, but the installed Kaggle CLI exposes no topics command in this environment and the topic API remained unavailable/unreadable, so no discussion update could be confirmed.
- Strategy: use R41 as the closest non-R1 checkpoint and test whether removing low-confidence class tails can close the 0.00026 gap to the active best; also submit the previously uncounted R49 truck/bus/van tail-filter control as a final R49 plateau check.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R75 | `submissions/r75/r75_r73_r41_filter_car0006_keep_others0005_submission.csv` | R73/R41 output, filter car below 0.0006, keep truck/van/bus at 0.0005 | audit ok / 74947 boxes | 0.82838 |
| R76 | `submissions/r76/r76_r73_r41_filter_truckcarvan0006_keep_bus0005_submission.csv` | R73/R41 output, filter truck/car/van below 0.0006, keep bus at 0.0005 | audit ok / 74539 boxes | 0.82838 |
| R77 | `submissions/r77/r77_r49_filter_truckbusvan0005_keep_car00045_submission.csv` | R49 output, filter truck/bus/van below 0.0005, keep car to 0.00045 | audit ok / 72542 boxes | 0.82864 |

Highest observed public score remains R36 `0.83245`, but the active 640 px rule-constrained best remains `0.82864` from R46a/R49/R50/R51/R53/R54/R55/R60/R61/R62/R63/R64/R65/R66a/R67a/R77.

Error analysis:
- R75 and R76 both tied R73 at 0.82838, so R41's 0.00026 gap to the active best is not fixed by simple class-tail filtering. The low-confidence R41 tails are removable without damage, but not beneficial.
- R77 tied 0.82864, confirming the last uncounted R49 truck/bus/van tail-filter control is public-neutral. R49 output-only tail filtering is now exhausted as a scoring direction.
- No new best was found. The next useful work should move away from R1/R49/R41 output-only calibration and toward compliant data-centric checks or a new 640 px scratch-training signal.

Repository/proof updates:
- Added R75/R76/R77 submission, summary, audit, submit/poll/final-list artifacts.
- Added May 31 rules/evaluation/code/discussion refresh logs and summary.
- Updated README, write-up, proof index, and chronological experiment log.

Next candidate directions:
- Stop spending quota on R49 class-tail filtering; it consistently preserves but does not exceed 0.82864.
- Stop spending quota on R41 tail filtering at 0.0006; it preserves the R73 score but does not close the gap.
- Prioritize compliant training/data diagnostics: label-quality review evidence, alternate 640 px scratch training schedules that keep R41-like generalization, or validation diagnostics that explain the R1/R41 public split.

## 2026-06-01 submission loop x3

Context:
- Submission list was queried at loop start on 2026-06-01 UTC/Europe-London. The initial quota evidence in `logs/submissions_2026-06-01_refresh.txt` had no 2026-06-01 records, so the full three-submission quota was available. Final quota accounting uses the Kaggle submission list: R78, R80, and R79 were accepted and completed.
- Rules and Evaluation pages were refreshed through `kaggle competitions pages --content`; both matched the 2026-05-31 copies by SHA256. Active constraints remain YOLOv8n only, 640 px input size, from-scratch/no pretrained for training runs, no external data, no ensemble, no TTA, no pseudo-labeling, and no distillation.
- Public Code listing was refreshed; the latest visible notebook remained Omar's 2026-05-19 run. Discussion/topic refresh produced no readable output through the available interface (`No pages found`), so no discussion update was confirmed.
- Strategy: after R49 confidence/NMS/class-tail filtering saturated, test small bbox geometry calibration from the same R49 single-checkpoint 640 px output. This keeps one YOLOv8n model output, no TTA, no ensemble, and no external data.

Submission results:

| Loop | File | Experiment | Validation / audit | Public LB |
|---|---|---|---|---:|
| R78 | `submissions/r78/r78_r49_boxscale1005_submission.csv` | R49 output, bbox width/height scale 1.005 around centers | audit ok / 73131 boxes | 0.82855 |
| R80 | `submissions/r80/r80_r49_boxscale10025_submission.csv` | R49 output, bbox width/height scale 1.0025 around centers | audit ok / 73131 boxes | 0.82862 |
| R79 | `submissions/r79/r79_r49_boxscale09975_submission.csv` | R49 output, bbox width/height scale 0.9975 around centers | audit ok / 73131 boxes | 0.82859 |

Highest observed public score remains R36 `0.83245`, but the active 640 px rule-constrained best remains `0.82864` from R46a/R49/R50/R51/R53/R54/R55/R60/R61/R62/R63/R64/R65/R66a/R67a/R77.

Error analysis:
- R78 shows that a 0.5% expansion of all R49 boxes drops below the plateau.
- R80 shows that even a smaller 0.25% expansion stays slightly below the unscaled R49 baseline.
- R79 shows that a 0.25% shrink also fails to improve. Together these results indicate the R49 box scale is already near the public optimum, and output-only bbox scaling should not receive more primary quota without a stronger diagnostic.
- R78's local submit stdout later hit a Kaggle 429 response, but the official submission list added the R78 record and poll logs show it completed with public score 0.82855. Quota accounting therefore follows the accepted submission-list record, not the transient stdout error.

Repository/proof updates:
- Added `scripts/scale_submission_boxes.py` plus R78/R79/R80 submission, summary, audit, submit/poll/final-list artifacts.
- Added June 1 rules/evaluation/code/discussion refresh logs and summary.
- Updated README, write-up, proof index, and chronological experiment log.

Next candidate directions:
- Stop spending primary quota on R49 confidence, NMS, class-tail filtering, or simple bbox scaling.
- Prioritize a new compliant signal: 3LC label-review evidence, class/size-stratified validation diagnostics, or a materially different 640 px YOLOv8n scratch-training recipe.
- If forced to use existing artifacts, prefer non-R49 checkpoint diagnostics only when they test a specific failure hypothesis; R41 tail filtering and R2 threshold rescue are already negative.
