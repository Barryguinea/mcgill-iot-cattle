# Analyse des alertes - Objectif 1

Pipeline applique: Isolation Forest + regles metier du memoire, seuils geles.

## Synthese par saison

| season      |   n_cows |   n_intervals |   cow_days | first_T             | last_T              |   if_anomaly_points |   lameness_points |   lameness_starts |   lameness_notifs |   alerted_cows |   notifs_per_cow |   notifs_per_100_cow_days |   mean_alert_confidence |   min_alert_confidence |   max_alert_confidence |   mean_coverage_pct |   min_coverage_pct |   low_coverage_rows |   low_coverage_notifications |
|:------------|---------:|--------------:|-----------:|:--------------------|:--------------------|--------------------:|------------------:|------------------:|------------------:|---------------:|-----------------:|--------------------------:|------------------------:|-----------------------:|-----------------------:|--------------------:|-------------------:|--------------------:|-----------------------------:|
| fall_2019   |       30 |         93860 |     977.71 | 2019-11-11 18:45:00 | 2019-12-14 13:00:00 |                5711 |              1104 |               121 |               105 |             26 |             3.5  |                     10.74 |                   49.12 |                   33.1 |                   60.5 |               99.28 |                  0 |                 673 |                            0 |
| fall_2021   |       10 |          5131 |      53.45 | 2021-11-30 09:00:00 | 2021-12-06 11:00:00 |                 302 |                38 |                 5 |                 4 |              4 |             0.4  |                      7.48 |                   53.23 |                   48.1 |                   58.1 |              100    |                100 |                   0 |                            0 |
| summer_2019 |       18 |        139111 |    1449.07 | 2019-06-05 13:00:00 | 2019-09-06 12:00:00 |                8081 |              1045 |               166 |               127 |             17 |             7.06 |                      8.76 |                   46.85 |                   31.9 |                   58.8 |               98.29 |                  0 |                2385 |                            0 |
| winter_2019 |       17 |        136929 |    1426.34 | 2019-01-16 15:15:00 | 2019-04-17 11:30:00 |                6462 |              1635 |               214 |               149 |             17 |             8.76 |                     10.45 |                   48.23 |                   32.1 |                   61.2 |               94.45 |                  0 |                7606 |                            0 |

## Interpretation courte

- Les quatre saisons produisent des alertes exploitables et des taux normalises comparables.
- Fall 2019, Summer 2019 et Winter 2019 ont un volume suffisant pour analyse par vache.
- Fall 2021 est exploitable techniquement mais court: 10 vaches, environ 53 vache-jours.
- Les lignes a faible couverture ne generent aucune notification; elles doivent etre documentees mais ne gonflent pas les alertes.
- Les alertes restent des episodes compatibles avec perturbation locomotrice; elles ne sont pas des diagnostics cliniques confirmes.

## Top 10 vaches par saison

### fall_2019
|   Cow |   n_bins |   lameness_notifs |   notifs_per_100_cow_days |   lameness_starts |   lameness_points |   coverage_mean |   coverage_min |
|------:|---------:|------------------:|--------------------------:|------------------:|------------------:|----------------:|---------------:|
|  8517 |     3072 |                 8 |                     25    |                 8 |                92 |             100 |            100 |
|  2062 |     3144 |                 8 |                     24.43 |                10 |                78 |             100 |            100 |
|  5879 |     3141 |                 7 |                     21.39 |                 7 |                72 |             100 |            100 |
|  2066 |     3142 |                 6 |                     18.33 |                 7 |                34 |             100 |            100 |
|  5865 |     3144 |                 6 |                     18.32 |                 6 |                47 |             100 |            100 |
|  8525 |     3072 |                 5 |                     15.62 |                 5 |                69 |             100 |            100 |
|  8527 |     3072 |                 5 |                     15.62 |                 5 |                34 |             100 |            100 |
|  2081 |     3141 |                 5 |                     15.28 |                 6 |                47 |             100 |            100 |
|  5871 |     3144 |                 5 |                     15.27 |                 7 |                74 |             100 |            100 |
|  2041 |     3145 |                 5 |                     15.26 |                 6 |                56 |             100 |            100 |

### summer_2019
|   Cow |   n_bins |   lameness_notifs |   notifs_per_100_cow_days |   lameness_starts |   lameness_points |   coverage_mean |   coverage_min |
|------:|---------:|------------------:|--------------------------:|------------------:|------------------:|----------------:|---------------:|
|  2062 |     8922 |                17 |                     18.29 |                18 |               224 |        100      |            100 |
|  5258 |     7492 |                11 |                     14.1  |                19 |                92 |        100      |            100 |
|   419 |     8920 |                11 |                     11.84 |                13 |                89 |        100      |            100 |
|  8536 |     8921 |                10 |                     10.76 |                15 |                47 |        100      |            100 |
|  5871 |     8921 |                10 |                     10.76 |                13 |                97 |        100      |            100 |
|  8520 |     8920 |                10 |                     10.76 |                12 |                53 |        100      |            100 |
|  5313 |     8921 |                 9 |                      9.69 |                12 |                96 |        100      |            100 |
|  5857 |     8920 |                 9 |                      9.69 |                10 |                58 |         97.7242 |              0 |
|  5322 |     8920 |                 7 |                      7.53 |                10 |                26 |         92.6233 |              0 |
|  8515 |     8925 |                 7 |                      7.53 |                10 |                74 |        100      |            100 |

### winter_2019
|   Cow |   n_bins |   lameness_notifs |   notifs_per_100_cow_days |   lameness_starts |   lameness_points |   coverage_mean |   coverage_min |
|------:|---------:|------------------:|--------------------------:|------------------:|------------------:|----------------:|---------------:|
|  8508 |     8718 |                19 |                     20.92 |                27 |               170 |         99.9541 |              0 |
|  2056 |     8718 |                17 |                     18.72 |                22 |               144 |         99.9541 |              0 |
|  5250 |     8718 |                13 |                     14.32 |                19 |               141 |         99.9541 |              0 |
|  3443 |     8718 |                12 |                     13.21 |                19 |               110 |         92.3492 |              0 |
|  8506 |     8718 |                11 |                     12.11 |                19 |               145 |         99.9541 |              0 |
|  2081 |     8722 |                11 |                     12.11 |                15 |               148 |         99.9541 |              0 |
|  2047 |     6219 |                 9 |                     13.89 |                17 |               134 |         99.9357 |              0 |
|  3437 |     8718 |                 9 |                      9.91 |                11 |               114 |         92.2689 |              0 |
|  5246 |     8055 |                 8 |                      9.53 |                10 |                57 |         99.9503 |              0 |
|  2063 |     8718 |                 8 |                      8.81 |                 9 |                98 |         99.9541 |              0 |

### fall_2021
|   Cow |   n_bins |   lameness_notifs |   notifs_per_100_cow_days |   lameness_starts |   lameness_points |   coverage_mean |   coverage_min |
|------:|---------:|------------------:|--------------------------:|------------------:|------------------:|----------------:|---------------:|
|  8557 |      457 |                 1 |                     21.01 |                 2 |                15 |             100 |            100 |
|  8562 |      582 |                 1 |                     16.49 |                 1 |                 6 |             100 |            100 |
|  2041 |      582 |                 1 |                     16.49 |                 1 |                10 |             100 |            100 |
|  8089 |      584 |                 1 |                     16.44 |                 1 |                 7 |             100 |            100 |
|  8057 |      583 |                 0 |                      0    |                 0 |                 0 |             100 |            100 |
|  8056 |      584 |                 0 |                      0    |                 0 |                 0 |             100 |            100 |
|  8080 |      585 |                 0 |                      0    |                 0 |                 0 |             100 |            100 |
|  8537 |      582 |                 0 |                      0    |                 0 |                 0 |             100 |            100 |
|  2208 |      583 |                 0 |                      0    |                 0 |                 0 |             100 |            100 |
|  8539 |        9 |                 0 |                      0    |                 0 |                 0 |             100 |            100 |

## Transition vers objectif 1.2

Objectif 1.2 = comparer les alertes automatisees avec les observations comportementales.

Sources comportementales a aligner:

| season      | behavior_source                                                                                                                                | status_for_alignment                                                                                 | priority   |
|:------------|:-----------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------------------------------------------------|:-----------|
| fall_2019   | /Users/alioubarry/PROJECT/mcgill_iot_cattle/Données completes/Données accelerometres/Fall 2019/Behavioral scans - Amir's lameness project.xlsx | needs collar/color-to-Cow_ID mapping for some scans; dates likely align with Fall 2019 IceTag period | high       |
| summer_2019 | /Users/alioubarry/PROJECT/mcgill_iot_cattle/Données completes/Données accelerometres/Summer 2019/Behavioral scans - Catherine.xlsx             | direct scan workbook present; inspect columns and Cow_ID/date granularity next                       | high       |
| winter_2019 | /Users/alioubarry/PROJECT/mcgill_iot_cattle/Données completes/Données accelerometres/Winter 2019/cow_scan_long-format_7.12.19.xlsx             | best candidate; already long-format and includes behavior/context variables                          | highest    |
| fall_2021   | /Users/alioubarry/PROJECT/mcgill_iot_cattle/Données completes/Données accelerometres/Fall 2021/Scan Sampling.xlsx                              | small dataset; likely needs tag/collar/group mapping confirmation                                    | medium     |

Etapes recommandees:

1. Inspecter les colonnes et unites temporelles des quatre fichiers de scans.
2. Construire une table standardisee `season, Cow, scan_time/date, behavior_category, raw_code`.
3. Aligner chaque notification avec les scans dans une fenetre temporelle definie, par exemple +/- 24 h et meme jour.
4. Produire une table de concordance: alertes avec comportement actif/reduit/immobile, alertes sans scan, scans suspects sans alerte.
5. Rapporter les limites: mapping Cow_ID/couleurs, granularite temporelle, scans non continus, contexte experimental.