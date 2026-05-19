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

## May 5 Submission Proof

| Run | Candidate | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---:|
| R10 | `submissions/r10/r10_r1_conf001_iou04625_submission.csv` | `logs/r10/audit_r10.txt` | `logs/r10/submit_r10.txt` | `logs/r10/submissions_poll_*.txt` | 0.82761 |
| R11 | `submissions/r11/r11_r1_conf001_iou046875_submission.csv` | `logs/r11/audit_r11.txt` | `logs/r11/submit_r11.txt` | `logs/r11/submissions_poll_*.txt` | 0.82765 |
| R12 | `submissions/r12/r12_r1_conf001_iou0470_submission.csv` | `logs/r12/audit_r12_local.txt` | `logs/r12/submit_r12.txt` | `logs/r12/submissions_poll_*.txt` | 0.82761 |

An additional local candidate `submissions/r12/r12_r1_conf001_iou0471875_submission.csv` was generated and audited, but upload was rejected by Kaggle with HTTP 400 after the daily quota was already consumed. It has no accepted submission-list record and is not counted as a completed submission.

## May 6 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R13 | `submissions/r13/r13_r1_conf0011_iou046875_submission.csv` | `submissions/r13/r13_r1_conf0011_iou046875_summary.json` | `logs/r13/audit_r13.txt` | `logs/r13/submit_r13.txt` | `logs/r13/submissions_poll_*.txt` | 0.82691 |
| R14 | `submissions/r14/r14_r1_conf0009_iou046875_submission.csv` | `submissions/r14/r14_r1_conf0009_iou046875_summary.json` | `logs/r14/audit_r14.txt` | `logs/r14/submit_r14.txt` | `logs/r14/submissions_poll_*.txt` | 0.82765 |
| R15 | `submissions/r15/r15_r1_conf001_iou046625_submission.csv` | `submissions/r15/r15_r1_conf001_iou046625_summary.json` | `logs/r15/audit_r15.txt` | `logs/r15/submit_r15.txt` | `logs/r15/submissions_poll_*.txt` | 0.82769 |

R15 became the best public submission at that time. All three May 6 candidates passed strict local submission audits before upload.

## May 7 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
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

Final May 19 submission list snapshot: `logs/final_submissions_2026-05-19.txt`. R36 is the current best public submission at 0.83245.
