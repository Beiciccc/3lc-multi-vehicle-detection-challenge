# Final Competition Archive - 2026-06-10

Competition: 3LC Multi Vehicle Detection Challenge

Final archive time: 2026-06-10T22:19Z / 2026-06-10T23:19+0100. The competition was closed, so no additional submissions were attempted.

## Final Leaderboard Snapshot

- Downloaded leaderboard snapshot contained 97 teams.
- Team: Kun Zhang (`beicicc`), TeamId `15788473`.
- Rank: `19`.
- Displayed leaderboard score: `0.87382`.
- Last submission date: `2026-06-08 13:32:39`.
- Submission count: `93`.
- Proof: `logs/final_2026-06-10/final_leaderboard_kun_zhang_2026-06-10.txt` and `logs/final_2026-06-10/final_leaderboard_public_snapshot_2026-06-10.csv`.

## Post-Competition Submission Scores

| Run | Ref | Public | Private | Notes |
|---|---:|---:|---:|---|
| R116 | 53478878 | 0.87382 | 0.85648 | Latest tied-best private submission; train+val checkpoint, conf 0.000060, iou 0.466125. |
| R115 duplicate | 53478874 | 0.87382 | 0.85637 | Duplicate accepted R115 record. |
| R115 | 53478725 | 0.87382 | 0.85637 | Train+val checkpoint, conf 0.000075, iou 0.466125. |
| R114 | 53442746 | 0.87382 | 0.85648 | Tied best private; train+val checkpoint, conf 0.000050, iou 0.46625. |
| R113 | 53442661 | 0.87382 | 0.85648 | Tied best private; train+val checkpoint, conf 0.000060, iou 0.46625. |
| R112 | 53442509 | 0.87382 | 0.85637 | First train+val submission; conf 0.000075, iou 0.46625. |

Best post-competition `privateScore`: `0.85648` from R113/R114/R116. R116 is the latest submission among the tied-best private results.

## Final Technical Summary

- The decisive improvement came from a single YOLOv8n scratch checkpoint trained on the provided train+val images at 640 px.
- This moved the public score from the R93/R101/R110 640 px baseline of `0.83235` to `0.87382`.
- Confidence thresholds from `0.000075` to `0.000050` and a small NMS move from `0.46625` to `0.466125` formed a displayed-score plateau.
- The train+val checkpoint also produced the best private scores; earlier R62/R93 and R1/R49 inference-only sweeps had materially lower private scores.

## Final Refresh Notes

- Final submissions proof is in `logs/final_2026-06-10/submissions_final_2026-06-10.txt`.
- Downloaded leaderboard proof is in `logs/final_2026-06-10/leaderboard_final_2026-06-10.txt` and the CSV snapshot.
- Public Code listing on 2026-06-10 contained one post-deadline notebook and one May 25 scratch-training notebook among the newest visible entries.
- Discussion topic list was unchanged from the final-window refreshes.

## Completion

The project archive is complete. No further experiment or submission loop remains for this competition.
