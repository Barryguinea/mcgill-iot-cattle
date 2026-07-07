# Analyse comparative — memoirev3 vs ancien pipeline McGill

Date: 2026-06-15

## Conclusion courte

La V3 a été appliquée aux quatre saisons McGill sans modifier le dossier `memoirev3`. Le comparateur IF historique recalculé par V3 reproduit exactement les anciennes notifications: 385/385. La différence observée vient donc de la nouvelle logique V3 HYPO/INSTABILITÉ/HYBRIDE, pas d’un problème d’entrée.

L’ancien pipeline produit 385 notifications (9.86/100 cow-days). La sortie principale V3 hybride produit 1179 notifications (30.18/100 cow-days), soit 3.1 fois plus. Cette V3 est donc nettement plus sensible sur McGill, mais elle change aussi la définition: elle signale une alerte comportementale à vérifier, pas une boiterie clinique.

## Résumé par saison

| season | n_cows | n_bins | old_lameness_notifs | v3_legacy_if_lameness_notifs | v3_behavioral_hypo_notifs | v3_instability_notifs | v3_hybrid_notifs | old_rate_per_100_cow_days | v3_hybrid_rate_per_100_cow_days |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fall_2019 | 30 | 93860 | 105 | 105 | 198 | 197 | 299 | 10.739 | 30.582 |
| summer_2019 | 18 | 139111 | 127 | 127 | 254 | 324 | 421 | 8.764 | 29.053 |
| winter_2019 | 17 | 136929 | 149 | 149 | 279 | 320 | 441 | 10.446 | 30.918 |
| fall_2021 | 10 | 5131 | 4 | 4 | 15 | 13 | 18 | 7.484 | 33.678 |

## Composition des alertes hybrides V3

| hybrid_warning_type | n | pct |
| --- | --- | --- |
| SEQUENCE | 645 | 54.7 |
| MIXTE | 330 | 28.0 |
| HYPO | 204 | 17.3 |

## Chevauchement temporel old vs V3 hybride

Le chevauchement exact au même timestamp est nul. Le tableau ci-dessous mesure une proximité temporelle par même vache, avec tolérance autour de chaque notification.

| season | tolerance_hours | old_alerts | hybrid_alerts | old_alerts_with_hybrid_nearby | old_alerts_with_hybrid_nearby_pct | hybrid_alerts_with_old_nearby | hybrid_alerts_with_old_nearby_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fall_2019 | 24 | 105 | 299 | 37 | 35.2 | 57 | 19.1 |
| fall_2019 | 48 | 105 | 299 | 45 | 42.9 | 96 | 32.1 |
| summer_2019 | 24 | 127 | 421 | 42 | 33.1 | 59 | 14.0 |
| summer_2019 | 48 | 127 | 421 | 47 | 37.0 | 93 | 22.1 |
| winter_2019 | 24 | 149 | 441 | 21 | 14.1 | 38 | 8.6 |
| winter_2019 | 48 | 149 | 441 | 24 | 16.1 | 68 | 15.4 |
| fall_2021 | 24 | 4 | 18 | 0 | 0.0 | 0 | 0.0 |
| fall_2021 | 48 | 4 | 18 | 2 | 50.0 | 2 | 11.1 |

## Corrélation par vache

| season | n_cows | pearson_old_vs_hybrid_by_cow | spearman_old_vs_hybrid_by_cow | old_total | hybrid_total |
| --- | --- | --- | --- | --- | --- |
| GLOBAL | 75 | 0.726 | 0.746 | 385 | 1179 |
| fall_2019 | 30 | 0.072 | -0.001 | 105 | 299 |
| summer_2019 | 18 | 0.458 | 0.319 | 127 | 421 |
| winter_2019 | 17 | 0.551 | 0.521 | 149 | 441 |
| fall_2021 | 10 | 0.491 | 0.525 | 4 | 18 |

## Top vaches selon la V3 hybride

| season | Cow | old_lameness_notifs | hybrid_warning_notifs | behavioral_warning_notifs | instability_warning_notifs | delta_hybrid_minus_old |
| --- | --- | --- | --- | --- | --- | --- |
| fall_2019 | 3437 | 4 | 14 | 6 | 13 | 10 |
| fall_2019 | 3435 | 0 | 13 | 2 | 11 | 13 |
| fall_2019 | 8526 | 2 | 13 | 6 | 13 | 11 |
| fall_2019 | 5865 | 6 | 13 | 9 | 11 | 7 |
| fall_2019 | 2062 | 8 | 13 | 7 | 7 | 5 |
| fall_2019 | 5857 | 2 | 12 | 6 | 12 | 10 |
| fall_2019 | 2041 | 5 | 12 | 6 | 8 | 7 |
| fall_2019 | 8525 | 5 | 12 | 9 | 2 | 7 |
| summer_2019 | 5871 | 10 | 34 | 15 | 34 | 24 |
| summer_2019 | 5313 | 9 | 31 | 18 | 17 | 22 |
| summer_2019 | 5865 | 4 | 28 | 19 | 23 | 24 |
| summer_2019 | 5862 | 5 | 28 | 16 | 16 | 23 |
| summer_2019 | 5330 | 4 | 27 | 14 | 28 | 23 |
| summer_2019 | 8520 | 10 | 27 | 16 | 26 | 17 |
| summer_2019 | 5258 | 11 | 27 | 17 | 24 | 16 |
| summer_2019 | 5854 | 6 | 26 | 13 | 20 | 20 |
| winter_2019 | 5221 | 6 | 35 | 17 | 33 | 29 |
| winter_2019 | 2081 | 11 | 32 | 20 | 23 | 21 |
| winter_2019 | 3443 | 12 | 32 | 15 | 31 | 20 |
| winter_2019 | 5250 | 13 | 32 | 21 | 19 | 19 |
| winter_2019 | 8508 | 19 | 32 | 20 | 24 | 13 |
| winter_2019 | 8510 | 7 | 30 | 18 | 24 | 23 |
| winter_2019 | 3437 | 9 | 30 | 19 | 23 | 21 |
| winter_2019 | 2056 | 17 | 30 | 20 | 21 | 13 |
| fall_2021 | 2041 | 1 | 3 | 2 | 2 | 2 |
| fall_2021 | 2208 | 0 | 2 | 1 | 2 | 2 |
| fall_2021 | 8056 | 0 | 2 | 2 | 1 | 2 |
| fall_2021 | 8057 | 0 | 2 | 2 | 1 | 2 |
| fall_2021 | 8080 | 0 | 2 | 2 | 1 | 2 |
| fall_2021 | 8089 | 1 | 2 | 2 | 2 | 1 |
| fall_2021 | 8557 | 1 | 2 | 1 | 1 | 1 |
| fall_2021 | 8562 | 1 | 2 | 2 | 2 | 1 |

## Interprétation

1. La compatibilité technique est validée: les mêmes inputs McGill peuvent alimenter la V3.
2. La continuité avec l’ancien pipeline est validée pour le comparateur IF: mêmes alertes, mêmes volumes.
3. La sortie principale V3 n’est pas une simple version “meilleure” de `notif_lameness`; elle répond à une autre question: anomalie comportementale persistante à vérifier.
4. Sur McGill, la V3 hybride augmente fortement la charge d’alertes. Avant toute conclusion clinique, il faut la comparer aux scans comportementaux et aux SLS selon le même protocole que l’objectif 1.2.

## Fichiers associés

- `comparison_summary_by_season.csv`
- `comparison_by_cow_all_seasons.csv`
- `comparison_temporal_overlap_tolerance.csv`
- `comparison_by_cow_correlations.csv`
- `top_hybrid_cows_by_season.csv`
- `<season>/<season>_memoirev3_predictions_core.csv`
- `<season>/<season>_memoirev3_alerts_only.csv`