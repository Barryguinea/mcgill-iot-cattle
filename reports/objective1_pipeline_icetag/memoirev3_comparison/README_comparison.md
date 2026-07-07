# Comparaison McGill — ancien pipeline vs memoirev3

## Protocole

- Entrées: fichiers McGill déjà convertis en intervalles de 15 minutes (`*_pipeline_input_15min.csv`).
- Ancien pipeline: sorties existantes de l'objectif 1 (`notif_lameness`).
- Nouveau pipeline: code importé depuis `memoirev3` en lecture seule; sorties principales HYPO, INSTABILITÉ et HYBRIDE.
- Interprétation V3: alerte comportementale à vérifier, non diagnostic clinique de boiterie.

## Résumé par saison

| season      |   n_cows |   n_bins |   old_lameness_notifs |   v3_legacy_if_lameness_notifs |   v3_behavioral_hypo_notifs |   v3_instability_notifs |   v3_hybrid_notifs |   old_rate_per_100_cow_days |   v3_hybrid_rate_per_100_cow_days |   old_vs_hybrid_exact_overlap |   old_only_vs_hybrid |   hybrid_only_vs_old |
|:------------|---------:|---------:|----------------------:|-------------------------------:|----------------------------:|------------------------:|-------------------:|----------------------------:|----------------------------------:|------------------------------:|---------------------:|---------------------:|
| fall_2019   |       30 |    93860 |                   105 |                            105 |                         198 |                     197 |                299 |                      10.739 |                            30.582 |                             0 |                  105 |                  299 |
| summer_2019 |       18 |   139111 |                   127 |                            127 |                         254 |                     324 |                421 |                       8.764 |                            29.053 |                             0 |                  127 |                  421 |
| winter_2019 |       17 |   136929 |                   149 |                            149 |                         279 |                     320 |                441 |                      10.446 |                            30.918 |                             0 |                  149 |                  441 |
| fall_2021   |       10 |     5131 |                     4 |                              4 |                          15 |                      13 |                 18 |                       7.484 |                            33.678 |                             0 |                    4 |                   18 |
| TOTAL       |       75 |   375031 |                   385 |                            385 |                         746 |                     854 |               1179 |                       9.855 |                            30.18  |                             0 |                  385 |                 1179 |

## Lecture

- `v3_legacy_if_lameness_notifs` est le comparateur IF historique recalculé par le code V3.
- `v3_behavioral_hypo_notifs` est la branche primaire MemoireV3: baisse comportementale persistante.
- `v3_instability_notifs` est la branche exploratoire d'instabilité comportementale.
- `v3_hybrid_notifs` est la fusion hiérarchique utilisée comme sortie V3 principale.
- Le chevauchement exact compare les notifications au même couple `(Cow, T)`; un faible chevauchement ne signifie pas forcément contradiction clinique, car les définitions d'alerte ont changé.

## Fichiers produits

- `comparison_summary_by_season.csv`
- `comparison_by_cow_all_seasons.csv`
- `<season>/<season>_memoirev3_summary.csv`
- `<season>/<season>_memoirev3_predictions_core.csv`
- `<season>/<season>_memoirev3_alerts_only.csv`