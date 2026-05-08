# Proof Index

This page indexes the reproducibility and leaderboard proof artifacts.

## Submission List Snapshots

- Start of May 5 loop: `logs/submissions_2026-05-05_start.txt`
- Final May 5 list: `logs/final_submissions_2026-05-05.txt`
- Start of May 6 loop: `logs/submissions_2026-05-06_start.txt`
- Final May 6 list: `logs/final_submissions_2026-05-06.txt`
- Start of May 7 loop: `logs/submissions_2026-05-07_start.txt`
- Final May 7 list: `logs/final_submissions_2026-05-07.txt`

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

R15 is the current best public submission. All three May 6 candidates passed strict local submission audits before upload.

## May 7 Submission Proof

| Run | Candidate | Summary | Audit | Submit log | Poll logs | Public LB |
|---|---|---|---|---|---|---:|
| R16 | `submissions/r16/r16_r1_conf001_iou046675_submission.csv` | `submissions/r16/r16_r1_conf001_iou046675_summary.json` | `logs/r16/audit_r16.txt` | `logs/r16/submit_r16.txt` | `logs/r16/submissions_poll_*.txt` | 0.82768 |
| R17 | `submissions/r17/r17_r1_conf001_iou046575_submission.csv` | `submissions/r17/r17_r1_conf001_iou046575_summary.json` | `logs/r17/audit_r17.txt` | `logs/r17/submit_r17_retry1.txt` | `logs/r17/submissions_poll_*.txt` | 0.82765 |
| R18 | `submissions/r18/r18_r1_conf001_iou0466375_submission.csv` | `submissions/r18/r18_r1_conf001_iou0466375_summary.json` | `logs/r18/audit_r18.txt` | `logs/r18/submit_r18.txt` | `logs/r18/submissions_poll_*.txt` | 0.82765 |

R17's first upload attempt returned `429 Too Many Requests`; five subsequent submission-list checks showed no R17 record, so it was not counted. The retry was accepted and produced the R17 row above. R15 remains the current best public submission.

## Training and Inference Proof

- R1 training artifacts: `competition_starter/runs/detect/r1_yolov8n_scratch_e10_640/`
- R2 training artifacts: `competition_starter/runs/detect/r2_yolov8n_scratch_e30_b32_640/`
- Inference summaries: `submissions/r*/r*_summary.json`
- Chronological experiment log: `experiments/run_log.md`
