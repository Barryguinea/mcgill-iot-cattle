# Réanalyse objectif 1 - McGill IceTag

Date: 2026-06-02

## Conclusion courte

Objectif 1 est techniquement atteint: les quatre saisons McGill ont été converties en pas de 15 minutes et passées dans le pipeline gelé du mémoire. Les sorties sont cohérentes entre résumés, prédictions et fichiers alertes.

La validation clinique de la boiterie n’est pas atteinte: les alertes détectent des anomalies d’activité, mais elles ne concordent pas avec les scores SLS disponibles. La limite vient principalement des données McGill: SLS ponctuels/asynchrones pour certaines saisons, boiterie surtout légère, et événement collectif probable en Winter 2019.

## Synthèse par saison

| season | n_cows | n_intervals | cow_days | date_min | date_max | alerts | alerts_per_100_cow_days | mean_coverage_pct | days_with_alerts | max_daily_alerts | max_daily_alert_cows | max_daily_alert_date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fall_2019 | 30 | 93860 | 977.71 | 2019-11-11 | 2019-12-14 | 105 | 10.74 | 99.28 | 30 | 8 | 8 | 2019-11-12 |
| summer_2019 | 18 | 139111 | 1449.07 | 2019-06-05 | 2019-09-06 | 127 | 8.76 | 98.29 | 69 | 4 | 4 | 2019-06-14 |
| winter_2019 | 17 | 136929 | 1426.34 | 2019-01-16 | 2019-04-17 | 149 | 10.45 | 94.45 | 52 | 14 | 13 | 2019-02-08 |
| fall_2021 | 10 | 5131 | 53.45 | 2021-11-30 | 2021-12-06 | 4 | 7.48 | 100.0 | 3 | 2 | 2 | 2021-12-01 |

## Contrôles de cohérence

| season | summary_vs_predictions_rows_match | summary_alerts | predictions_alerts | alerts_only_rows | alerts_counts_all_match | input_duplicate_cow_start | prediction_duplicate_cow_t | low_coverage_alerts |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fall_2019 | True | 105 | 105 | 105 | True | 0 | 0 | 0 |
| summer_2019 | True | 127 | 127 | 127 | True | 0 | 0 | 0 |
| winter_2019 | True | 149 | 149 | 149 | True | 0 | 0 | 0 |
| fall_2021 | True | 4 | 4 | 4 | True | 0 | 0 | 0 |

## Top vaches par saison

### fall_2019
| Cow | lameness_notifs | cow_days | alerts_per_100_cow_days | coverage_mean |
| --- | --- | --- | --- | --- |
| 8517 | 8 | 32.0 | 25.0 | 100.0 |
| 2062 | 8 | 32.75 | 24.43 | 100.0 |
| 5879 | 7 | 32.72 | 21.39 | 100.0 |
| 2066 | 6 | 32.73 | 18.33 | 100.0 |
| 5865 | 6 | 32.75 | 18.32 | 100.0 |
| 8525 | 5 | 32.0 | 15.62 | 100.0 |
| 8527 | 5 | 32.0 | 15.62 | 100.0 |
| 2081 | 5 | 32.72 | 15.28 | 100.0 |

### summer_2019
| Cow | lameness_notifs | cow_days | alerts_per_100_cow_days | coverage_mean |
| --- | --- | --- | --- | --- |
| 2062 | 17 | 92.94 | 18.29 | 100.0 |
| 5258 | 11 | 78.04 | 14.1 | 100.0 |
| 419 | 11 | 92.92 | 11.84 | 100.0 |
| 8520 | 10 | 92.92 | 10.76 | 100.0 |
| 8536 | 10 | 92.93 | 10.76 | 100.0 |
| 5871 | 10 | 92.93 | 10.76 | 100.0 |
| 5857 | 9 | 92.92 | 9.69 | 97.72 |
| 5313 | 9 | 92.93 | 9.69 | 100.0 |

### winter_2019
| Cow | lameness_notifs | cow_days | alerts_per_100_cow_days | coverage_mean |
| --- | --- | --- | --- | --- |
| 8508 | 19 | 90.81 | 20.92 | 99.95 |
| 2056 | 17 | 90.81 | 18.72 | 99.95 |
| 5250 | 13 | 90.81 | 14.32 | 99.95 |
| 3443 | 12 | 90.81 | 13.21 | 92.35 |
| 8506 | 11 | 90.81 | 12.11 | 99.95 |
| 2081 | 11 | 90.85 | 12.11 | 99.95 |
| 2047 | 9 | 64.78 | 13.89 | 99.94 |
| 3437 | 9 | 90.81 | 9.91 | 92.27 |

### fall_2021
| Cow | lameness_notifs | cow_days | alerts_per_100_cow_days | coverage_mean |
| --- | --- | --- | --- | --- |
| 8557 | 1 | 4.76 | 21.01 | 100.0 |
| 8562 | 1 | 6.06 | 16.49 | 100.0 |
| 2041 | 1 | 6.06 | 16.49 | 100.0 |
| 8089 | 1 | 6.08 | 16.44 | 100.0 |
| 8057 | 0 | 6.07 | 0.0 | 100.0 |
| 8056 | 0 | 6.08 | 0.0 | 100.0 |
| 8080 | 0 | 6.09 | 0.0 | 100.0 |
| 8537 | 0 | 6.06 | 0.0 | 100.0 |

## Top vaches global

| Cow | seasons | n_seasons | alerts | cow_days | alerts_per_100_cow_days | mean_coverage |
| --- | --- | --- | --- | --- | --- | --- |
| 2062 | fall_2019,summer_2019 | 2 | 25 | 125.69 | 19.89 | 100.0 |
| 8508 | winter_2019 | 1 | 19 | 90.81 | 20.92 | 99.95 |
| 2056 | winter_2019 | 1 | 17 | 90.81 | 18.72 | 99.95 |
| 2081 | fall_2019,winter_2019 | 2 | 16 | 123.57 | 12.95 | 99.98 |
| 5871 | fall_2019,summer_2019 | 2 | 15 | 125.68 | 11.94 | 100.0 |
| 5250 | winter_2019 | 1 | 13 | 90.81 | 14.32 | 99.95 |
| 3437 | fall_2019,winter_2019 | 2 | 13 | 123.57 | 10.52 | 96.13 |
| 3443 | winter_2019 | 1 | 12 | 90.81 | 13.21 | 92.35 |
| 2063 | fall_2019,winter_2019 | 2 | 12 | 123.52 | 9.71 | 99.98 |
| 5258 | summer_2019 | 1 | 11 | 78.04 | 14.1 | 100.0 |
| 8506 | winter_2019 | 1 | 11 | 90.81 | 12.11 | 99.95 |
| 419 | summer_2019 | 1 | 11 | 92.92 | 11.84 | 100.0 |

## Concentration temporelle Winter 2019

Winter 2019 concentre 94/149 alertes entre le 1er et le 15 février 2019 (63.1%), touchant 14/17 vaches. Cela indique probablement un événement collectif du troupeau plutôt qu’une série indépendante de boiteries individuelles.

| date | alerts | cows |
| --- | --- | --- |
| 2019-02-08 | 14 | 13 |
| 2019-02-07 | 13 | 12 |
| 2019-02-04 | 11 | 11 |
| 2019-02-05 | 11 | 9 |
| 2019-02-03 | 10 | 9 |
| 2019-02-01 | 8 | 8 |
| 2019-02-06 | 8 | 7 |
| 2019-02-02 | 6 | 6 |

## Fichiers ignorés pendant la compilation

| season | skipped_files | reasons |
| --- | --- | --- |
| fall_2019 | 0 | {} |
| summer_2019 | 0 | {} |
| winter_2019 | 16 | {"cow_id_introuvable": 16} |
| fall_2021 | 0 | {} |

## Validation clinique SLS

Sur Winter 2019, les labels SLS synchrones ne valident pas les alertes comme boiterie clinique. Les résultats déjà vérifiés sont: Mann-Whitney p = 0.649, Spearman rho = 0.033, Random Forest Leave-One-Out AUC = 0.236, balanced accuracy = 0.409. Les 5 features IceTag testées ne sont pas significatives (p >= 0.2674).

Interprétation: le pipeline détecte des anomalies d’activité, mais les données McGill disponibles ne montrent pas un signal de boiterie clinique séparable. Le problème principal est donc la limite des données de validation, pas l’exécution du pipeline.

## Implication pour objectif 1.2

Un premier alignement comportemental défendable existe pour Winter 2019 seulement, car cette saison dispose de scans avec Cow_ID et Date directement exploitables.

| metric | value |
| --- | --- |
| winter_alerts_total | 149 |
| winter_scans_total | 42 |
| alerts_with_matched_scan_within_1d | 16 |
| alerts_with_same_day_scan | 7 |
| scans_with_same_day_alert | 7 |
| scans_with_alert_within_1d | 11 |

Prochaine étape recommandée: garder le pipeline gelé comme résultat objectif 1, puis créer une analyse séparée pour tester une normalisation par le troupeau et poursuivre l’alignement comportemental des saisons Summer 2019, Fall 2019 et Fall 2021.
