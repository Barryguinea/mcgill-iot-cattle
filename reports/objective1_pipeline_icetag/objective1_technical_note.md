# Note technique - Objectif 1

Pipeline applique: Isolation Forest + regles metier.
Resolution temporelle: bins de 15 minutes.
Seuils et parametres: configuration existante du pipeline appliquee de facon identique aux quatre corpus.

Parametres utilises:
- interval: 15T
- window_baseline: 24
- contamination: 0.06
- baseline_ratio: 0.6
- random_state: 42
- persist_hours: 7
- alert_min: 2
- mix_mode: MIX
- mix_rate_thr: 0.24
- z_low_thr: -2.0
- z_high_thr: 2.0
- cooldown_hours: 12
- mi_z_high_thr: 2.2
- coverage_min_pct: 25.0

Sorties generees:

## fall_2019
- vaches: 30
- intervalles predits: 93860
- notifications boiterie: 105
- resume: fall_2019_pipeline_summary.csv
- predictions: fall_2019_pipeline_predictions.csv

## summer_2019
- vaches: 18
- intervalles predits: 139111
- notifications boiterie: 127
- resume: summer_2019_pipeline_summary.csv
- predictions: summer_2019_pipeline_predictions.csv

## winter_2019
- vaches: 17
- intervalles predits: 136929
- notifications boiterie: 149
- resume: winter_2019_pipeline_summary.csv
- predictions: winter_2019_pipeline_predictions.csv

## fall_2021
- vaches: 10
- intervalles predits: 5131
- notifications boiterie: 4
- resume: fall_2021_pipeline_summary.csv
- predictions: fall_2021_pipeline_predictions.csv

## Synthese multi-saisons
- fall_2019: 30 vaches, 93860 intervalles, 105 notifications, 10.74 notifications / 100 vache-jours
- fall_2021: 10 vaches, 5131 intervalles, 4 notifications, 7.48 notifications / 100 vache-jours
- summer_2019: 18 vaches, 139111 intervalles, 127 notifications, 8.76 notifications / 100 vache-jours
- winter_2019: 17 vaches, 136929 intervalles, 149 notifications, 10.45 notifications / 100 vache-jours
