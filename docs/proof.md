# Proof Index

This page indexes the reproducibility and leaderboard proof artifacts.

## Submission List Snapshots

- Start of May 5 loop: `logs/submissions_2026-05-05_start.txt`
- Final May 5 list: `logs/final_submissions_2026-05-05.txt`
- Start of May 6 loop: `logs/submissions_2026-05-06_start.txt`
- Final May 6 list: `logs/final_submissions_2026-05-06.txt`
- Start of May 7 loop: `logs/submissions_2026-05-07_start.txt`
- Final May 7 list: `logs/final_submissions_2026-05-07.txt`
- Start/before-submit May 12 lists: `logs/submissions_2026-05-12_before_r19.txt`, `logs/submissions_2026-05-12_before_r20.txt`, `logs/submissions_2026-05-12_before_r21.txt`
- Final May 12 list: `logs/final_submissions_2026-05-12.txt`
- Start/before-submit May 13 lists: `logs/submissions_2026-05-13_start.txt`, `logs/submissions_2026-05-13_before_r22.txt`, `logs/submissions_2026-05-13_before_r23.txt`, `logs/submissions_2026-05-13_before_r24_retry_1.txt`
- Final May 13 list: `logs/final_submissions_2026-05-13.txt`
- Start/before-submit May 16 lists: `logs/submissions_2026-05-16_start.txt`, `logs/submissions_2026-05-16_before_r25.txt`, `logs/submissions_2026-05-16_before_r26.txt`, `logs/submissions_2026-05-16_before_r27.txt`
- Final May 16 list: `logs/final_submissions_2026-05-16.txt`
- Start/before-submit May 17 lists: `logs/submissions_2026-05-17_start.txt`, `logs/submissions_2026-05-17_before_r28.txt`, `logs/submissions_2026-05-17_before_r29.txt`, `logs/submissions_2026-05-17_before_r30.txt`
- Final May 17 list: `logs/final_submissions_2026-05-17.txt`
- Start/before-submit May 18 lists: `logs/submissions_2026-05-18_start.txt`, `logs/submissions_2026-05-18_before_r31.txt`, `logs/submissions_2026-05-18_before_r32.txt`, `logs/submissions_2026-05-18_before_r33.txt`
- Final May 18 list: `logs/final_submissions_2026-05-18.txt`
- Start/before-submit May 19 lists: `logs/submissions_2026-05-19_start.txt`, `logs/submissions_2026-05-19_before_r34.txt`, `logs/submissions_2026-05-19_before_r35.txt`, `logs/submissions_2026-05-19_before_r36.txt`
- Final May 19 list: `logs/final_submissions_2026-05-19.txt`
- Start/before-submit May 20 lists: `logs/submissions_2026-05-20_start.txt`, `logs/submissions_2026-05-20_before_r38.txt`, `logs/submissions_2026-05-20_before_r39.txt`, `logs/submissions_2026-05-20_before_r40.txt`
- Final May 20 list: `logs/final_submissions_2026-05-20.txt`
- Start/before-submit May 21 lists: `logs/submissions_2026-05-21_start.txt`, `logs/submissions_2026-05-21_before_r42.txt`, `logs/submissions_2026-05-21_before_r44.txt`, `logs/submissions_2026-05-21_before_r45.txt`
- Final May 21 list: `logs/final_submissions_2026-05-21.txt`
- Start/before-submit May 22 lists: `logs/submissions_2026-05-22_start.txt`, `logs/submissions_2026-05-22_before_r46.txt`, `logs/submissions_2026-05-22_before_r49.txt`
- Final May 22 list: `logs/final_submissions_2026-05-22.txt`

## May 5 Submission Proof

| Run | Candidate | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---:|
| R10 | `submissions/r10/r10_r1_conf001_iou04625_submission.csv` | `logs/r10/audit_r10.txt` | `logs/r10/submit_r10.txt` | `logs/r10/submissions_poll_*.txt` | 0.82761 |
| R11 | `submissions/r11/r11_r1_conf001_iou046875_submission.csv` | `logs/r11/audit_r11.txt` | `logs/r11/submit_r11.txt` | `logs/r11/submissions_poll_*.txt` | 0.82765 |
| R12 | `submissions/r12/r12_r1_conf001_iou0470_submission.csv` | `logs/r12/audit_r12_local.txt` | `logs/r12/submit_r12.txt` | `logs/r12/submissions_poll_*.txt` | 0.82761 |

An additional local candidate `submissions/r12/r12_r1_conf001_iou0471875_submission.csv` was generated and audited, but upload was rejected by Kaggle with HTTP 400 after the daily quota was already consumed. It has no accepted submission-list record and is not counted as a completed submission.

## May 6 Submission Proof

| Run | Candidate | Summary | Audit | Submit/list evidence | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R13 | `submissions/r13/r13_r1_conf0011_iou046875_submission.csv` | `submissions/r13/r13_r1_conf0011_iou046875_summary.json` | `logs/r13/audit_r13.txt` | `logs/r13/submit_r13.txt` | `logs/r13/submissions_poll_*.txt` | 0.82691 |
| R14 | `submissions/r14/r14_r1_conf0009_iou046875_submission.csv` | `submissions/r14/r14_r1_conf0009_iou046875_summary.json` | `logs/r14/audit_r14.txt` | `logs/r14/submit_r14.txt` | `logs/r14/submissions_poll_*.txt` | 0.82765 |
| R15 | `submissions/r15/r15_r1_conf001_iou046625_submission.csv` | `submissions/r15/r15_r1_conf001_iou046625_summary.json` | `logs/r15/audit_r15.txt` | `logs/r15/submit_r15.txt` | `logs/r15/submissions_poll_*.txt` | 0.82769 |

R15 became the best public submission at that time. All three May 6 candidates passed strict local submission audits before upload.

## May 7 Submission Proof

| Run | Candidate | Summary | Audit | Submit/list evidence | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R16 | `submissions/r16/r16_r1_conf001_iou046675_submission.csv` | `submissions/r16/r16_r1_conf001_iou046675_summary.json` | `logs/r16/audit_r16.txt` | `logs/r16/submit_r16.txt` | `logs/r16/submissions_poll_*.txt` | 0.82768 |
| R17 | `submissions/r17/r17_r1_conf001_iou046575_submission.csv` | `submissions/r17/r17_r1_conf001_iou046575_summary.json` | `logs/r17/audit_r17.txt` | `logs/r17/submit_r17_retry1.txt` | `logs/r17/submissions_poll_*.txt` | 0.82765 |
| R18 | `submissions/r18/r18_r1_conf001_iou0466375_submission.csv` | `submissions/r18/r18_r1_conf001_iou0466375_summary.json` | `logs/r18/audit_r18.txt` | `logs/r18/submit_r18.txt` | `logs/r18/submissions_poll_*.txt` | 0.82765 |

R17's first upload attempt returned `429 Too Many Requests`; five subsequent submission-list checks showed no R17 record, so it was not counted. The retry was accepted and produced the R17 row above. R15 remained the best public submission at that time.

## Training and Inference Proof

- R1 training artifacts: `competition_starter/runs/detect/r1_yolov8n_scratch_e10_640/`
- R2 training artifacts: `competition_starter/runs/detect/r2_yolov8n_scratch_e30_b32_640/`
- Inference summaries: `submissions/r*/r*_summary.json`
- Chronological experiment log: `experiments/run_log.md`

## May 12 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R19 | `submissions/r19/r19_r15_boxscale0985_submission.csv` | `submissions/r19/r19_r15_boxscale0985_summary.json` | `logs/r19/audit_r19.txt` | `logs/r19/submit_r19.txt` | `logs/r19/submissions_poll_*.txt` | 0.82644 |
| R20 | `submissions/r20/r20_r15_boxscale1010_submission.csv` | `submissions/r20/r20_r15_boxscale1010_summary.json` | `logs/r20/audit_r20.txt` | `logs/r20/submit_r20.txt` | `logs/r20/submissions_poll_*.txt` | 0.82760 |
| R21 | `submissions/r21/r21_r15_conf00105_from_r15_submission.csv` | `submissions/r21/r21_r15_conf00105_from_r15_summary.json` | `logs/r21/audit_r21.txt` | `logs/r21/submit_r21.txt` | `logs/r21/submissions_poll_*.txt` | 0.82695 |

Final May 12 submission list snapshot: `logs/final_submissions_2026-05-12.txt`. R15 remained the best public submission at that time.

## May 13 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R22 | `submissions/r22/r22_yolov8n_scratch_e10_seed7_640_submission.csv` | `submissions/r22/r22_yolov8n_scratch_e10_seed7_640_summary.json` | `logs/r22/audit_r22.txt` | `logs/r22/submit_r22.txt` | `logs/r22/submissions_poll_*.txt` | 0.81336 |
| R23 | `submissions/r23/r23_r1_conf001_iou04665_submission.csv` | `submissions/r23/r23_r1_conf001_iou04665_summary.json` | `logs/r23/audit_r23.txt` | `logs/r23/submit_r23.txt` | `logs/r23/submissions_poll_*.txt` | 0.82767 |
| R24 | `submissions/r24/r24_r1_conf001_iou0466125_submission.csv` | `submissions/r24/r24_r1_conf001_iou0466125_summary.json` | `logs/r24/audit_r24.txt` | `logs/r24/submit_r24.txt` | `logs/r24/submissions_poll_*.txt` | 0.82768 |

Final May 13 submission list snapshot: `logs/final_submissions_2026-05-13.txt`. R15 remained the best public submission at that time.

## May 16 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R25 | `submissions/r25/r25_r15_bus_conf00105_submission.csv` | `submissions/r25/r25_r15_bus_conf00105_summary.json` | `logs/r25/audit_r25.txt` | `logs/r25/submit_r25.txt` | `logs/r25/submissions_poll_*.txt` | 0.82769 |
| R26 | `submissions/r26/r26_r15_noncar_conf00105_submission.csv` | `submissions/r26/r26_r15_noncar_conf00105_summary.json` | `logs/r26/audit_r26.txt` | `logs/r26/submit_r26.txt` | `logs/r26/submissions_poll_*.txt` | 0.82695 |
| R27 | `submissions/r27/r27_r15_bus_conf00110_submission.csv` | `submissions/r27/r27_r15_bus_conf00110_summary.json` | `logs/r27/audit_r27.txt` | `logs/r27/submit_r27.txt` | `logs/r27/submissions_poll_*.txt` | 0.82769 |

Final May 16 submission list snapshot: `logs/final_submissions_2026-05-16.txt`. R15, R25, and R27 were tied at the best public score of 0.82769 at that time.

## May 17 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R28 | `submissions/r28/r28_r15_truck_conf00105_submission.csv` | `submissions/r28/r28_r15_truck_conf00105_summary.json` | `logs/r28/audit_r28.txt` | `logs/r28/submit_r28.txt` | `logs/r28/submissions_poll_*.txt` | 0.82769 |
| R29 | `submissions/r29/r29_r15_van_conf00105_submission.csv` | `submissions/r29/r29_r15_van_conf00105_summary.json` | `logs/r29/audit_r29.txt` | `logs/r29/submit_r29.txt` | `logs/r29/submissions_poll_*.txt` | 0.82695 |
| R30 | `submissions/r30/r30_r15_truck00105_bus00110_submission.csv` | `submissions/r30/r30_r15_truck00105_bus00110_summary.json` | `logs/r30/audit_r30.txt` | `logs/r30/submit_r30.txt` | `logs/r30/submissions_poll_*.txt` | 0.82769 |

Final May 17 submission list snapshot: `logs/final_submissions_2026-05-17.txt`. R15, R25, R27, R28, and R30 were tied at the best public score of 0.82769 at that time.

## May 18 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R31 | `submissions/r31/r31_r15_bus_conf00120_submission.csv` | `submissions/r31/r31_r15_bus_conf00120_summary.json` | `logs/r31/audit_r31.txt` | `logs/r31/submit_r31.txt` | `logs/r31/submissions_poll_*.txt` | 0.82769 |
| R32 | `submissions/r32/r32_r15_truck_conf00110_submission.csv` | `submissions/r32/r32_r15_truck_conf00110_summary.json` | `logs/r32/audit_r32.txt` | `logs/r32/submit_r32.txt` | `logs/r32/submissions_poll_*.txt` | 0.82769 |
| R33 | `submissions/r33/r33_r15_bus_conf00130_submission.csv` | `submissions/r33/r33_r15_bus_conf00130_summary.json` | `logs/r33/audit_r33.txt` | `logs/r33/submit_r33.txt` | `logs/r33/submissions_poll_*.txt` | 0.82769 |

Final May 18 submission list snapshot: `logs/final_submissions_2026-05-18.txt`. R15, R25, R27, R28, R30, R31, R32, and R33 were tied at the best public score of 0.82769 before the May 19 loop.

## May 19 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R34 | `submissions/r34/r34_yolov8n_scratch_e10_seed123_640_submission_clipped.csv` | `submissions/r34/r34_yolov8n_scratch_e10_seed123_640_summary.json` | `logs/r34/audit_r34_clipped.txt` | `logs/r34/submit_r34.txt` | `logs/r34/submissions_poll_*.txt` | 0.82359 |
| R35 | `submissions/r35/r35_r2_conf001_iou046625_submission_clipped.csv` | `submissions/r35/r35_r2_conf001_iou046625_summary.json` | `logs/r35/audit_r35_clipped.txt` | `logs/r35/submit_r35.txt` | `logs/r35/submissions_poll_*.txt` | 0.82088 |
| R36 | `submissions/r36/r36_r1_imgsz768_conf001_iou046625_submission_clipped.csv` | `submissions/r36/r36_r1_imgsz768_conf001_iou046625_summary.json` | `logs/r36/audit_r36_clipped.txt` | `logs/r36/submit_r36.txt` | `logs/r36/submissions_poll_*.txt` | 0.83245 |

Final May 19 submission list snapshot: `logs/final_submissions_2026-05-19.txt`. R36 is the highest observed public submission at 0.83245; after the May 20 rules refresh, 640 px is treated as the active input-size constraint for new submissions.


## May 20 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R38 | `submissions/r38/r38_r1_640_conf0008_iou046625_submission.csv` | `submissions/r38/r38_r1_640_conf0008_iou046625_summary.json` | `logs/r38/audit_r38.txt` | `logs/r38/submit_r38.txt` | `logs/r38/submissions_poll_*.txt` | 0.82769 |
| R39 | `submissions/r39/r39_r1_640_conf0006_iou046625_submission.csv` | `submissions/r39/r39_r1_640_conf0006_iou046625_summary.json` | `logs/r39/audit_r39.txt` | `logs/r39/submit_r39.txt` | `logs/r39/submissions_poll_*.txt` | 0.82769 |
| R40 | `submissions/r40/r40_r1_640_conf0008_iou046575_submission.csv` | `submissions/r40/r40_r1_640_conf0008_iou046575_summary.json` | `logs/r40/audit_r40.txt` | `logs/r40/submit_r40.txt` | `logs/r40/submissions_poll_*.txt` | 0.82768 |

Final May 20 submission list snapshot: `logs/final_submissions_2026-05-20.txt`. R38 and R39 tied the active 640 px public best at 0.82769; R36 remains the highest observed public score at 0.83245.

## May 21 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R42 | `submissions/r42/r42_yolov8n_scratch_e12_seed42_640_submission_clipped.csv` | `submissions/r42/r42_yolov8n_scratch_e12_seed42_640_summary.json` | `logs/r42/audit_r42_clipped.txt` | `logs/r42/submit_r42.txt` | `logs/r42/submissions_poll_r42.txt` | 0.81293 |
| R44 | `submissions/r44/r44_r1_640_conf0007_iou046625_submission.csv` | `submissions/r44/r44_r1_640_conf0007_iou046625_summary.json` | `logs/r44/audit_r44.txt` | `logs/r44/submit_r44.txt` | `logs/r44/submissions_poll_r44.txt` | 0.82769 |
| R45 | `submissions/r45/r45_r1_640_conf0007_iou0466375_submission.csv` | `submissions/r45/r45_r1_640_conf0007_iou0466375_summary.json` | `logs/r45/audit_r45.txt` | `logs/r45/submit_r45.txt` | `logs/r45/submissions_poll_r45.txt` | 0.82768 |

Final May 21 submission list snapshot: `logs/final_submissions_2026-05-21.txt`. R44 tied the active 640 px public best at 0.82769; R36 remains the highest observed public score at 0.83245.

## May 22 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R46a | `submissions/r46/r46_r1_640_conf0005_iou046625_submission.csv` | `submissions/r46/r46_r1_640_conf0005_iou046625_summary.json` | `logs/r46/audit_r46.txt` | `logs/r46/submit_r46.txt` | `logs/r46/submissions_poll_r46.txt` | 0.82864 |
| R46b | `submissions/r46/r46_r1_640_conf00065_iou046625_submission.csv` | `submissions/r46/r46_r1_640_conf00065_iou046625_summary.json` | `logs/r46/audit_r46_conf00065.txt` | `logs/r46/submit_r46_conf00065.txt` | `logs/r46/submissions_poll_r46.txt` | 0.82769 |
| R49 | `submissions/r49/r49_r1_640_conf00045_iou046625_submission.csv` | `submissions/r49/r49_r1_640_conf00045_iou046625_summary.json` | `logs/r49/audit_r49.txt` | `logs/r49/submit_r49.txt` | `logs/r49/submissions_poll_r49.txt` | 0.82864 |

Final May 22 submission list snapshot: `logs/final_submissions_2026-05-22.txt`. R46a and R49 are tied as the active 640 px public best at 0.82864; R36 remains the highest observed public score at 0.83245.

## May 23 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R50 | `submissions/r50/r50_r1_640_conf000475_iou046625_submission.csv` | `submissions/r50/r50_r1_640_conf000475_iou046625_summary.json` | `logs/r50/audit_r50.txt` | `logs/r50/submit_r50.txt` | `logs/r50/submissions_poll_r50_1.txt` | 0.82864 |
| R51 | `submissions/r51/r51_r1_640_conf000525_iou046625_submission.csv` | `submissions/r51/r51_r1_640_conf000525_iou046625_summary.json` | `logs/r51/audit_r51.txt` | `logs/r51/submit_r51.txt` | `logs/r51/submissions_poll_r51_1.txt` | 0.82864 |
| R52 | `submissions/r52/r52_r1_640_conf0005_iou0466125_submission.csv` | `submissions/r52/r52_r1_640_conf0005_iou0466125_summary.json` | `logs/r52/audit_r52.txt` | `logs/r52/submit_r52.txt` | `logs/r52/submissions_poll_r52.txt` | 0.82862 |

Final May 23 submission list snapshot: `logs/final_submissions_2026-05-23.txt`. R50 and R51 tied the active 640 px public best at 0.82864; R52 scored 0.82862. R36 remains the highest observed public score at 0.83245, but it is not the active 640 px baseline for new submissions.

Non-counted May 23 candidate: R53 (`submissions/r53/r53_r49_keep_van00045_others0005_submission.csv`) passed local audit with 69526 boxes, but Kaggle returned HTTP 400 and no R53 row appeared in the submission list. It is not counted as an accepted submission.

## May 24 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R53 | `submissions/r53/r53_r49_keep_van00045_others0005_submission.csv` | `submissions/r53/r53_r49_keep_van00045_others0005_summary.json` | `logs/r53/audit_r53_2026-05-24.txt` | `logs/r53/submit_r53_2026-05-24.txt` | `logs/r53/submissions_poll_r53_2026-05-24.txt` | 0.82864 |
| R54 | `submissions/r54/r54_r49_keep_carvan00045_filter_truckbus0005_submission.csv` | `submissions/r54/r54_r49_keep_carvan00045_filter_truckbus0005_summary.json` | `logs/r54/audit_r54_pre_submit.txt` | `logs/r54/submit_r54.txt` | `logs/r54/submissions_poll_r54.txt` | 0.82864 |
| R55 | `submissions/r55/r55_r49_filter_car0005_keep_others00045_submission.csv` | `submissions/r55/r55_r49_filter_car0005_keep_others00045_summary.json` | `logs/r55/audit_r55_pre_submit.txt` | `logs/r55/submit_r55.txt` | `logs/r55/submissions_poll_r55.txt` | 0.82864 |

Final May 24 submission list snapshot: `logs/final_submissions_2026-05-24.txt`. R53, R54, and R55 all tied the active 640 px public best at 0.82864. R36 remains the highest observed public score at 0.83245, but it is not the active 640 px baseline for new submissions.

## May 25 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R58 | `submissions/r58/r58_r1_640_conf00055_iou046625_submission.csv` | `submissions/r58/r58_r1_640_conf00055_iou046625_summary.json` | `logs/r58/audit_r58_pre_submit.txt` | `logs/r58/submit_r58.txt` | `logs/r58/submissions_poll_r58.txt` | 0.82833 |
| R59 | `submissions/r59/r59_r1_640_conf0005_iou0466375_submission.csv` | `submissions/r59/r59_r1_640_conf0005_iou0466375_summary.json` | `logs/r59/audit_r59_pre_submit.txt` | `logs/r59/submit_r59.txt` | `logs/r59/submissions_poll_r59.txt` | 0.82862 |
| R56 | `submissions/r56/r56_r1_640_conf0005_iou0466375_submission.csv` | `submissions/r56/r56_r1_640_conf0005_iou0466375_summary.json` | `logs/r56/audit_r56.txt` | `logs/r56/submit_r56.txt` | `logs/final_submissions_2026-05-25.txt` | 0.82862 |

Final May 25 submission list snapshot: `logs/final_submissions_2026-05-25.txt`. R58 scored 0.82833, while R59 and R56 scored 0.82862. R36 remains the highest observed public score at 0.83245; the active 640 px public best remains 0.82864.

## May 26 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R61 | `submissions/r61/r61_r49_filter_truck0005_keep_others00045_submission.csv` | `submissions/r61/r61_r49_filter_truck0005_keep_others00045_summary.json` | `logs/r61/audit_r61.txt` | `logs/r61/submit_r61.txt` | `logs/r61/submissions_poll_r61_*.txt` | 0.82864 |
| R62 | `submissions/r62/r62_r49_filter_bus0005_keep_others00045_submission.csv` | `submissions/r62/r62_r49_filter_bus0005_keep_others00045_summary.json` | `logs/r62/audit_r62.txt` | `logs/r62/submit_r62.txt` | `logs/r62/submissions_poll_r62_*.txt` | 0.82864 |
| R60 | `submissions/r60/r60_r49_keep_vanbus00045_filter_truckcar0005_submission.csv` | `submissions/r60/r60_r49_keep_vanbus00045_filter_truckcar0005_summary.json` | `logs/r60/audit_r60_2026-05-26.txt` | `logs/r60/submit_r60.txt` | `logs/r60/submissions_poll_r60_*.txt` | 0.82864 |

Final May 26 submission list snapshot: `logs/final_submissions_2026-05-26.txt`. R60, R61, and R62 all tied the active 640 px public best at 0.82864. R36 remains the highest observed public score at 0.83245; the active 640 px public best remains 0.82864.

## May 27 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R63 | `submissions/r63/r63_r49_filter_van0005_keep_others00045_submission.csv` | `submissions/r63/r63_r49_filter_van0005_keep_others00045_summary.json` | `logs/r63/audit_r63.txt` | `logs/r63/submit_r63.txt` | `logs/r63/submissions_poll_r63.txt` | 0.82864 |
| R64 | `submissions/r64/r64_r49_filter_truckvan0005_keep_carbus00045_submission.csv` | `submissions/r64/r64_r49_filter_truckvan0005_keep_carbus00045_summary.json` | `logs/r64/audit_r64.txt` | `logs/r64/submit_r64.txt` | `logs/r64/submissions_poll_r64.txt` | 0.82864 |
| R65 | `submissions/r65/r65_r49_filter_busvan0005_keep_truckcar00045_submission.csv` | `submissions/r65/r65_r49_filter_busvan0005_keep_truckcar00045_summary.json` | `logs/r65/audit_r65.txt` | `logs/r65/submit_r65.txt` | `logs/r65/submissions_poll_r65.txt` | 0.82864 |

Final May 27 submission list snapshot: `logs/final_submissions_2026-05-27.txt`. R63, R64, and R65 all tied the active 640 px public best at 0.82864. R36 remains the highest observed public score at 0.83245; the active 640 px public best remains 0.82864.

## May 29 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R66a | `submissions/r66/r66_r49_filter_carbus0005_keep_truckvan00045_submission.csv` | `submissions/r66/r66_r49_filter_carbus0005_keep_truckvan00045_summary.json` | `logs/r66/audit_r66_r49_carbus_pre_submit.txt` | `logs/r66/submit_r66.txt` | `logs/r66/submissions_poll_r66.txt` | 0.82864 |
| R67a | `submissions/r67/r67_r49_filter_carvan0005_keep_truckbus00045_submission.csv` | `submissions/r67/r67_r49_filter_carvan0005_keep_truckbus00045_summary.json` | `logs/r67/audit_r67_r49_carvan_pre_submit.txt` | `logs/r67/submit_r67.txt` | `logs/r67/submissions_poll_r67.txt` | 0.82864 |
| R66b | `submissions/r66/r66_r2_640_conf00045_iou046625_submission.csv` | `submissions/r66/r66_r2_640_conf00045_iou046625_summary.json` | `logs/r66/audit_r66_r2_conf00045_pre_submit.txt` | `logs/final_submissions_2026-05-29.txt` | `logs/final_submissions_2026-05-29.txt` | 0.82271 |

Final May 29 submission list snapshot: `logs/final_submissions_2026-05-29.txt`. R66a and R67a tied the active 640 px public best at 0.82864; R66b showed that R2 low-threshold inference remains below the R1/R49 plateau at 0.82271. R68 R49 was rejected with HTTP 400 and did not appear in the submission list, so it is not counted as an accepted submission.

## May 29 UTC Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R72 | `submissions/r72/r72_r34_seed123_640_conf0005_iou046625_submission.csv` | `submissions/r72/r72_r34_seed123_640_conf0005_iou046625_summary.json` | `logs/r72/audit_r72.txt` | `logs/r72/submit_r72.txt` | `logs/r72/submissions_poll_r72.txt` | 0.82548 |
| R73 | `submissions/r73/r73_r41_e8_seed42_640_conf0005_iou046625_submission.csv` | `submissions/r73/r73_r41_e8_seed42_640_conf0005_iou046625_summary.json` | `logs/r73/audit_r73.txt` | `logs/r73/submit_r73.txt` | `logs/r73/submissions_poll_r73.txt` | 0.82838 |
| R74 | `submissions/r74/r74_r2_640_conf0005_iou046625_submission.csv` | `submissions/r74/r74_r2_640_conf0005_iou046625_summary.json` | `logs/r74/audit_r74.txt` | `logs/r74/submit_r74.txt` | `logs/r74/submissions_poll_r74.txt` | 0.82271 |

Final May 29 UTC submission list snapshot: `logs/final_submissions_2026-05-29_utc.txt`. R72, R73, and R74 were all accepted on 2026-05-29 UTC. R73 was the best of these diagnostics at 0.82838, but the active 640 px public best remains 0.82864.

## May 31 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R75 | `submissions/r75/r75_r73_r41_filter_car0006_keep_others0005_submission.csv` | `submissions/r75/r75_r73_r41_filter_car0006_keep_others0005_summary.json` | `logs/r75/audit_r75_filter_actual.txt` | `logs/r75/submit_r75.txt` | `logs/r75/submissions_poll_r75.txt` | 0.82838 |
| R76 | `submissions/r76/r76_r73_r41_filter_truckcarvan0006_keep_bus0005_submission.csv` | `submissions/r76/r76_r73_r41_filter_truckcarvan0006_keep_bus0005_summary.json` | `logs/r76/audit_r76.txt` | `logs/r76/submit_r76.txt` | `logs/r76/submissions_poll_r76.txt` | 0.82838 |
| R77 | `submissions/r77/r77_r49_filter_truckbusvan0005_keep_car00045_submission.csv` | `submissions/r77/r77_r49_filter_truckbusvan0005_keep_car00045_summary.json` | `logs/r77/audit_r77.txt` | `logs/r77/submit_r77.txt` | `logs/r77/submissions_poll_r77.txt` | 0.82864 |

Final May 31 submission list snapshot: `logs/final_submissions_2026-05-31.txt`. R75, R76, and R77 were all accepted on 2026-05-31 UTC. R77 tied the active 640 px public best at 0.82864; R75 and R76 stayed at the R41 baseline of 0.82838.

## June 1 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R78 | `submissions/r78/r78_r49_boxscale1005_submission.csv` | `submissions/r78/r78_r49_boxscale1005_summary.json` | `logs/r78/audit_r78.txt` | `logs/r78/submissions_after_r78.txt` | `logs/r78/submissions_poll_r78.txt` | 0.82855 |
| R80 | `submissions/r80/r80_r49_boxscale10025_submission.csv` | `submissions/r80/r80_r49_boxscale10025_summary.json` | `logs/r80/audit_r80.txt` | `logs/r80/submit_r80.txt` | `logs/r80/submissions_poll_r80.txt` | 0.82862 |
| R79 | `submissions/r79/r79_r49_boxscale09975_submission.csv` | `submissions/r79/r79_r49_boxscale09975_summary.json` | `logs/r79/audit_r79.txt` | `logs/r79/submit_r79.txt` | `logs/r79/submissions_poll_r79.txt` | 0.82859 |

Final June 1 submission list snapshot: `logs/final_submissions_2026-06-01.txt`. R78, R80, and R79 were all accepted on 2026-06-01 UTC. R78's decisive accounting evidence is the new submission-list record plus completed poll result, because the local submit stdout later hit a Kaggle 429 response. None improved the active 640 px public best of 0.82864.

## June 2 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R81 | `submissions/r81/r81_r62_nomix_close3_conf0005_iou046625_submission.csv` | `submissions/r81/r81_r62_nomix_close3_conf0005_iou046625_summary_source.json` | `logs/r81/audit_r81.txt` | `logs/r81/submit_r81.txt` | `logs/r81/submissions_poll_r81.txt` | 0.82857 |
| R82 | `submissions/r82/r82_r62_nomix_close3_conf00025_iou046625_submission.csv` | `submissions/r82/r82_r62_nomix_close3_conf00025_iou046625_summary.json` | `logs/r82/audit_r82.txt` | `logs/r82/submit_r82.txt` | `logs/r82/submissions_poll_r82.txt` | 0.83015 |
| R84 | `submissions/r84/r84_r62_nomix_close3_conf0002_iou046625_submission.csv` | `submissions/r84/r84_r62_nomix_close3_conf0002_iou046625_summary.json` | `logs/r84/audit_r84.txt` | `logs/r84/submit_r84.txt` | `logs/r84/submissions_poll_r84.txt` | 0.83129 |

Final June 2 submission list snapshot: `logs/final_submissions_2026-06-02.txt`. R84 is the new active 640 px public best at 0.83129. R36 remains the highest observed public score at 0.83245, but R84 is the best result under the active 640 px constraint used for new submissions. R83 (`submissions/r83/r83_r63_lightaug_nomix_conf0005_iou046625_submission.csv`) was generated and audited, but it was not submitted and has no public score.


## June 3 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R85 | `submissions/r85/r85_r62_nomix_close3_conf000175_iou046625_submission.csv` | `submissions/r85/r85_r62_nomix_close3_conf000175_iou046625_summary.json` | `logs/r85/audit_r85.txt` | `logs/r85/submit_r85.txt` | `logs/r85/submissions_poll_r85.txt` | 0.83129 |
| R86 | `submissions/r86/r86_r62_nomix_close3_conf00015_iou046625_submission.csv` | `submissions/r86/r86_r62_nomix_close3_conf00015_iou046625_summary.json` | `logs/r86/audit_r86.txt` | `logs/r86/submit_r86.txt` | `logs/r86/submissions_poll_r86.txt` | 0.83154 |
| R89 | `submissions/r89/r89_r62_nomix_close3_conf000125_iou046625_submission.csv` | `submissions/r89/r89_r62_nomix_close3_conf000125_iou046625_summary.json` | `logs/r89/audit_r89.txt` | `logs/r89/submit_r89.txt` | `logs/r89/submissions_poll_r89.txt` | 0.83154 |

Final June 3 submission list snapshot: `logs/final_submissions_2026-06-03.txt`. R86 and R89 are the new active 640 px public best at 0.83154. R36 remains the highest observed public score at 0.83245, but R86/R89 are the best results under the active 640 px constraint used for new submissions. R87 (`conf=0.000225`) and R88 (`conf=0.0002, iou=0.466125`) were generated and audited but not submitted; they have no public score.


## June 4 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R91 | `submissions/r91/r91_r62_nomix_close3_conf0001125_iou046625_submission.csv` | `submissions/r91/r91_r62_nomix_close3_conf0001125_iou046625_summary.json` | `logs/r91/audit_r91.txt` | `logs/r91/submit_r91.txt` | `logs/r91/submissions_poll_r91.txt` | 0.83175 |
| R90 | `submissions/r90/r90_r62_nomix_close3_conf0001_iou046625_submission.csv` | `submissions/r90/r90_r62_nomix_close3_conf0001_iou046625_summary.json` | `logs/r90/audit_r90.txt` | `logs/r90/submit_r90.txt` | `logs/r90/submissions_poll_r90.txt` | 0.83175 |
| R93 | `submissions/r93/r93_r62_nomix_close3_conf000075_iou046625_submission.csv` | `submissions/r93/r93_r62_nomix_close3_conf000075_iou046625_summary.json` | `logs/r93/audit_r93.txt` | `logs/r93/submit_r93.txt` | `logs/r93/submissions_poll_r93.txt` | 0.83235 |

Final June 4 submission list snapshot: `logs/final_submissions_2026-06-04.txt`; final verification snapshot: `logs/final_submissions_2026-06-04_verify.txt`. R93 is the new active 640 px public best at 0.83235. R36 remains the highest observed public score at 0.83245, but R93 is the best result under the active 640 px constraint used for new submissions. R92 (`conf=0.000125, iou=0.466125`) was generated and audited but not submitted; it has no public score.

## June 5 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R99 | `submissions/r99/r99_r93_filter_truckbus0001_keep_carvan000075_submission.csv` | `submissions/r99/r99_r93_filter_truckbus0001_keep_carvan000075_summary.json` | `logs/r99/audit_r99.txt` | `logs/r99/submit_r99.txt` | `logs/r99/submissions_poll_r99_*.txt` | 0.83216 |
| R100 | `submissions/r100/r100_r93_filter_bus0001_keep_others000075_submission.csv` | `submissions/r100/r100_r93_filter_bus0001_keep_others000075_summary.json` | `logs/r100/audit_r100.txt` | `logs/r100/submit_r100.txt` | `logs/r100/submissions_poll_r100_*.txt` | 0.83216 |
| R101 | `submissions/r101/r101_r93_filter_truck0001_keep_others000075_submission.csv` | `submissions/r101/r101_r93_filter_truck0001_keep_others000075_summary.json` | `logs/r101/audit_r101.txt` | `logs/r101/submit_r101.txt` | `logs/r101/submissions_poll_r101_*.txt` | 0.83235 |

Final June 5 submission list snapshot: `logs/final_submissions_2026-06-05.txt`. R101 tied the active 640 px public best at 0.83235; R99 and R100 scored 0.83216. R36 remains the highest observed public score at 0.83245, but R93/R101 remain the best results under the active 640 px constraint used for new submissions.

Generated but not submitted on June 5: R94-R98 from the Kaggle GPU R62 reproduction were audited but not submitted because the reproduced checkpoint validated at mAP50 0.81077, below the historical R62 run. R102 was audited but not submitted after R99/R100 showed bus-tail filtering was harmful.

## June 6 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R94 | `submissions/r94/r94_r62_nomix_close3_conf000007000_iou0466250_submission.csv` | `submissions/r94/r94_r62_nomix_close3_conf000007000_iou0466250_summary.json` | `logs/r94/audit_r94.txt` | `logs/r94/submit_r94_2026-06-06.txt` | `logs/r94/submissions_poll_r94_2026-06-06_exact_*.txt` | 0.81600 |
| R108 | `submissions/r108/r108_r93_filter_van0001_keep_others000075_submission.csv` | `submissions/r108/r108_r93_filter_van0001_keep_others000075_summary.json` | `logs/r108/audit_r108.txt` | `logs/r108/submit_r108_2026-06-06.txt` | `logs/r108/submissions_poll_r108_2026-06-06_exact_*.txt` | 0.83194 |
| R110 | `submissions/r110/r110_r93_top100_per_image_per_class_submission.csv` | `submissions/r110/r110_r93_top100_per_image_per_class_summary.json` | `logs/r110/audit_r110.txt` | `logs/r110/submit_r110_2026-06-06.txt` | `logs/r110/submissions_poll_r110_2026-06-06_exact_*.txt` | 0.83235 |

Final June 6 submission list snapshot: `logs/final_submissions_2026-06-06.txt`. R110 tied the active 640 px public best at 0.83235; R108 scored 0.83194; R94 scored 0.81600. R36 remains the highest observed public score at 0.83245, but R93/R101/R110 remain the best results under the active 640 px constraint used for new submissions.

Generated but not submitted on June 6: R109 was audited at 90624 boxes but not submitted after the lower-risk R110 cap was selected. A fresh Kaggle GPU train+val kernel package was prepared but new execution was rejected by Kaggle's GPU batch session limit.
