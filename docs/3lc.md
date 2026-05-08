# 3LC Workflow Status

The official starter workflow expects a personal 3LC account and API key, plus 3LC table registration and dashboard inspection.

## Current Status

- 3LC dashboard exports and screenshots are not included in this public repository.
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
