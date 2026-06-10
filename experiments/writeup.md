# Experiment Write-up

## Method

All scored experiments use only competition-provided data and keep the model budget fixed to YOLOv8n. Training runs start from `yolov8n.yaml` random initialization with 640 px input size unless explicitly recorded as a historical diagnostic. Inference submissions use one checkpoint at a time with no ensemble, no TTA, no pseudo-labeling, no distillation, and no external data.

The official 3LC starter code is retained. The dashboard-based 3LC process was not available in this runtime because a usable 3LC API key was not configured, so the reproducible fallback path uses Ultralytics YOLOv8n from scratch and records audit/submit/poll evidence for every submitted CSV.

## Final Results

| Scope | Run(s) | Public | Private | Notes |
|---|---|---:|---:|---|
| Downloaded final leaderboard snapshot | Kun Zhang / beicicc | 0.87382 | n/a | Rank 19/97, submission count 93. |
| Best post-competition submissions view | R113/R114/R116 | 0.87382 | 0.85648 | Train+val YOLOv8n scratch checkpoint. |
| Previous active 640 px baseline | R93/R101/R110 | 0.83235 | 0.82001 | R62/R93 low-confidence line. |
| Earlier 640 px plateau | R46a/R49/R50/R51/R53/R54/R55/R60-R67/R77 | 0.82864 | <=0.80223 | R1/R49 low-confidence plateau. |

## Key Findings

The decisive improvement came from training one YOLOv8n scratch checkpoint on the provided train+val images at 640 px. R112-R116 all scored 0.87382 publicly, and R113/R114/R116 tied at privateScore 0.85648. This was a large improvement over the R93/R101/R110 public baseline of 0.83235 and private 0.82001.

Earlier experiments showed that local validation was useful for rejecting weak runs but not sufficient for ranking public-best checkpoints. R2, R34, R42, and the June 5 R62 reproduction had reasonable local signals but materially worse leaderboard results.

The train+val checkpoint formed a broad displayed-score plateau across confidence thresholds `0.000075`, `0.000060`, and `0.000050`, plus a small NMS move from `0.46625` to `0.466125`. R116 is the latest tied-best private result.

## Final Archive

Primary proof files are `experiments/final_summary_2026-06-10.md`, `logs/final_2026-06-10/submissions_final_2026-06-10.txt`, `logs/final_2026-06-10/final_leaderboard_kun_zhang_2026-06-10.txt`, and `logs/final_2026-06-10/final_leaderboard_public_snapshot_2026-06-10.csv`. The competition is closed and no further submissions are planned.
