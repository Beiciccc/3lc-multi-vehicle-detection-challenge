# 3LC Workflow Status

The official starter process expects a personal 3LC account and API key, plus 3LC table registration and dashboard inspection.

## Current Status

- The 3LC API key was not configured for the runtime used for these submissions.
- Because of that, `register_tables.py` and the full dashboard-based data-centric loop could not be completed.
- No 3LC project export or Dashboard screenshot is currently available. This was rechecked for the May 7 loop; the fallback proof is therefore the reproducible code, summaries, audit logs, Kaggle submit logs, and leaderboard submission-list snapshots.

## Fallback Used

The fallback pipeline uses the competition data directly in YOLO format with YOLOv8n only. It preserves the competition restrictions:

- YOLOv8n architecture only.
- No pretrained weights.
- No external data.
- No TTA, ensemble, distillation, or pseudo-labeling.
- Single-checkpoint inference.

If a valid 3LC API key becomes available, rerun the official flow:

```bash
cd competition_starter
python verify_setup.py
python register_tables.py
python train.py
python predict.py
```

Then add any 3LC dashboard screenshots or project export paths to this document.

## 2026-06-05 Update

The 3LC credential/dashboard path is still unavailable in this runtime. The June 5 refresh noted updated 3LC package-index installation instructions in the competition discussion, but no dashboard export or screenshot was produced. The documented fallback evidence remains reproducible code, training/inference summaries, audits, Kaggle kernel logs, submission logs, and submission-list snapshots.
