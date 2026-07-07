# Visibilité complète des données McGill

Date: 2026-06-02

## Lecture rapide

- Données brutes McGill: `Données completes` (~4.1 Go), 2 414 fichiers inventoriés.
- Brutes avec IceTag disponibles: Fall 2019, Summer 2019, Winter 2019, Fall 2021.
- Données agrégées article: 6 CSV dans `data-movement-behavior-main/dataset` pour Fall2019, Summer2019, Winter2019, Summer2020, Winter2020, Summer2021.
- Données produites par notre travail: `reports/objective1_pipeline_icetag` pour inputs 15 min, features/prédictions, résumés, alertes, alignement comportemental.

## Vue par couche de données

| layer | season | files |
| --- | --- | --- |
| derived_or_analysis_output | Fall 2019 | 4 |
| derived_or_analysis_output | Fall 2021 | 4 |
| derived_or_analysis_output | Other / unknown | 2 |
| derived_or_analysis_output | Summer 2019 | 4 |
| derived_or_analysis_output | Winter 2019 | 15 |
| local_project_dataset | Fall 2019 | 1 |
| local_project_dataset | Fall 2019 / SLS labels | 1 |
| published_aggregate_dataset | Fall 2019 | 1 |
| published_aggregate_dataset | Summer 2019 | 1 |
| published_aggregate_dataset | Summer 2020 | 1 |
| published_aggregate_dataset | Summer 2021 | 1 |
| published_aggregate_dataset | Winter 2019 | 1 |
| published_aggregate_dataset | Winter 2020 | 1 |
| raw_mcgill_complete | Fall 2019 | 401 |
| raw_mcgill_complete | Fall 2021 | 49 |
| raw_mcgill_complete | Multi-season / aggregate | 1 |
| raw_mcgill_complete | Other / unknown | 2 |
| raw_mcgill_complete | Summer 2019 | 873 |
| raw_mcgill_complete | Winter 2019 | 1088 |

## Données brutes McGill: fichiers par saison et type

| season | source_type | files |
| --- | --- | --- |
| Fall 2019 | accelerometer_icetag_export_support | 124 |
| Fall 2019 | accelerometer_icetag_other | 2 |
| Fall 2019 | accelerometer_icetag_raw_csv | 248 |
| Fall 2019 | accelerometer_icetag_workbook_or_mapping | 6 |
| Fall 2019 | behavior_scan_workbook | 1 |
| Fall 2019 | environment_hobo_xlsx | 20 |
| Fall 2021 | accelerometer_icetag_raw_csv | 20 |
| Fall 2021 | accelerometer_icetag_workbook_or_mapping | 2 |
| Fall 2021 | behavior_scan_workbook | 1 |
| Fall 2021 | environment_hobo_csv | 4 |
| Fall 2021 | environment_hobo_xlsx | 22 |
| Multi-season / aggregate | behavior_scan_workbook | 1 |
| Other / unknown | behavior_scan_other | 1 |
| Other / unknown | documentation_protocol | 1 |
| Summer 2019 | accelerometer_icetag_export_support | 179 |
| Summer 2019 | accelerometer_icetag_raw_csv | 579 |
| Summer 2019 | accelerometer_icetag_workbook_or_mapping | 9 |
| Summer 2019 | behavior_scan_workbook | 1 |
| Summer 2019 | environment_hobo_graph_png | 35 |
| Summer 2019 | environment_hobo_raw_hobo | 34 |
| Summer 2019 | environment_hobo_xlsx | 36 |
| Winter 2019 | accelerometer_icetag_export_support | 351 |
| Winter 2019 | accelerometer_icetag_other | 2 |
| Winter 2019 | accelerometer_icetag_raw_csv | 726 |
| Winter 2019 | accelerometer_icetag_workbook_or_mapping | 7 |
| Winter 2019 | behavior_scan_workbook | 1 |
| Winter 2019 | clinical_sls_labels | 1 |

## Données brutes McGill: extensions par saison

| season | extension | files |
| --- | --- | --- |
| Fall 2019 | .csv | 248 |
| Fall 2019 | .rtf | 2 |
| Fall 2019 | .ses | 124 |
| Fall 2019 | .xlsx | 27 |
| Fall 2021 | .csv | 24 |
| Fall 2021 | .xlsx | 25 |
| Multi-season / aggregate | .xlsx | 1 |
| Other / unknown | .docx | 1 |
| Other / unknown | .pdf | 1 |
| Summer 2019 | .csv | 579 |
| Summer 2019 | .hobo | 34 |
| Summer 2019 | .png | 35 |
| Summer 2019 | .ses | 179 |
| Summer 2019 | .xlsx | 46 |
| Winter 2019 | .csv | 726 |
| Winter 2019 | .docx | 1 |
| Winter 2019 | .pdf | 1 |
| Winter 2019 | .raw_bin | 23 |
| Winter 2019 | .ses | 327 |
| Winter 2019 | .txt | 1 |
| Winter 2019 | .xlsx | 9 |

## IceTag brut par saison

| season | icetag_files_total | main_csv | lying_bout_lb_csv | xlsx_mapping_or_compiled | support_files_ses_rawbin_txt |
| --- | --- | --- | --- | --- | --- |
| Fall 2019 | 380 | 124 | 124 | 6 | 124 |
| Fall 2021 | 22 | 10 | 10 | 2 | 0 |
| Summer 2019 | 767 | 289 | 290 | 9 | 179 |
| Winter 2019 | 1086 | 363 | 363 | 7 | 351 |

## Données agrégées publiques / article

| season | relative_path | rows | cols | n_cows | columns_preview |
| --- | --- | --- | --- | --- | --- |
| Fall 2019 | data-movement-behavior-main/dataset/Fall2019.csv | 708 | 7 | 30 | Cow_ID, Trt, Week, Block, Block.1, Sum_Steps, Experiment |
| Summer 2019 | data-movement-behavior-main/dataset/Summer2019.csv | 506 | 10 | 15 | Cow_ID, Trt_details, Trt, Trt_order, Week, Block, Size, Duration_per_day, Sum_Steps, Experiment |
| Summer 2020 | data-movement-behavior-main/dataset/Summer2020.csv | 243 | 9 | 18 | Cow_ID, Trt_details, Trt, Trt_order, Week, Period, Block, Sum_Steps, Experiment |
| Summer 2021 | data-movement-behavior-main/dataset/Summer2021.csv | 61 | 10 | 6 | Cow_ID, Trt, Trt_details, Trt_order, Week, Period, Block, Size, Sum_Steps, Experiment |
| Winter 2019 | data-movement-behavior-main/dataset/Winter2019.csv | 410 | 10 | 14 | Cow_ID, Trt_details, Trt, Trt_order, Week, Block, Size, Duration_per_day, Sum_Steps, Experiment |
| Winter 2020 | data-movement-behavior-main/dataset/Winter2020.csv | 286 | 10 | 27 | Cow_ID, Trt_details, Trt, Trt_order, Week, Period, Week_Period, Block, Sum_Steps, Experiment |

## Données locales déjà intégrées

| season | source_type | relative_path | rows | cols | n_cows | date_min | date_max | columns_preview |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Fall 2019 | csv_other | mcgill_brut.csv | 93187 | 10 | 30 | 2019-11-11 18:45:00 | 2019-12-14 13:00:00 | Cow, Start, End, Steps, Motion Index, Lying Time, Standing Time, Transitions, Transitions Up, Transitions Down |
| Fall 2019 / SLS labels | clinical_sls_labels | mcgill_sls_labels.csv | 30 | 8 | 30 |  |  | Cow, SLS_Baseline_Jan2019, SLS_Midway_Mar2019, Statut, Bins_15min, Jours, Debut, Fin |

## Principales sources brutes à connaître

| season | source_type | relative_path | rows | cols | sheet_count | sheet_names_preview | columns_preview |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fall 2019 | behavior_scan_workbook | Données completes/Données accelerometres/Fall 2019/Behavioral scans - Amir's lameness project.xlsx | 27 | 2 | 6 | Code used, SCAN template, SCAN week 4, SCAN week 5 , SCAN week 5.2, Focus | Distance Code, Distance Definition |
| Fall 2019 | accelerometer_icetag_workbook_or_mapping | Données completes/Données accelerometres/Fall 2019/Icetag/IceTags/@IceTag_Compiled_Lameness.xlsx | 47177 | 11 | 30 | 821, 2041, 2057, 2062, 2063, 2066, 2078, 2081, 3435, 3437 | Cow, Block, Treatment, Week, Date, Time, Motion Index, Standing [t], Lying [t], Steps, Lying Bouts |
| Fall 2019 | accelerometer_icetag_workbook_or_mapping | Données completes/Données accelerometres/Fall 2019/Icetag/IceTags/AllinOne_IceTag_Compiled_Lameness+LB.xlsx | 454 | 7 | 30 | 5871, 5865, 5857, 5327, 2062, 2041, 5854, 5870, 5862, 3437 | CowID, Start Date, Start Time, End Date, End Time, Duration, Second |
| Fall 2019 | accelerometer_icetag_workbook_or_mapping | Données completes/Données accelerometres/Fall 2019/Icetag/IceTags/AllinOne_IceTag_Compiled_Lameness.xlsx | 6 | 4 | 8 | Sheet4, Summary, Summary_NoWeekend, Summary_NoWkEnd_NoWeird, Sheet2, Compiled_LB, Compiled_1, Compiled_2 | Row Labels, Average of LT, Average of LB, Average of STEP |
| Fall 2021 | accelerometer_icetag_workbook_or_mapping | Données completes/Données accelerometres/Fall 2021/Icetag/IceTags/Copy of Ice tag download Notes1.xlsx | 18 | 8 | 1 | Sheet1 | Cow Name, Cow_ID, Group#, IceTag#, 2021-11-09 00:00:00, 2021-11-16 00:00:00, 2021-11-23 00:00:00, 2021-11-30 00:00:00 |
| Fall 2021 | accelerometer_icetag_workbook_or_mapping | Données completes/Données accelerometres/Fall 2021/Icetag/IceTags/Ice tag download Notes.xlsx | 18 | 6 | 1 | Sheet1 | Cow Name, Cow_ID, Group#, IceTag#, 2021-11-09 00:00:00, 2021-11-16 00:00:00 |
| Fall 2021 | behavior_scan_workbook | Données completes/Données accelerometres/Fall 2021/Scan Sampling.xlsx | 62 | 30 | 17 | Nov 1, Nov 3, Nov 4, Nov 5, Nov 8, Nov 11, Nov 15, Nov 12, Nov 18, Nov 19 | Date: Nov 1, , , , 11:22am, , , , Observer: Jazzy, , ,  |
| Summer 2019 | behavior_scan_workbook | Données completes/Données accelerometres/Summer 2019/Behavioral scans - Catherine.xlsx | 32 | 2 | 15 | Code used, SCAN template, Week 1, Week 1.2, Week 2, Week 3, Week 4, Week 5 (don't use it), Week 5.2 (the good one), Week 6 | Distance Code, Distance Definition |
| Summer 2019 | environment_hobo_xlsx | Données completes/Données accelerometres/Summer 2019/Hobo/Excel sheet of THI for all summer's exercise project.xlsx | 181 | 11 | 20 | General data, Semaine 1 Inside, Semaine 2 Inside , Semaine 3 Inside, Semaine 4 Inside , Semaine 5 - Inside, Semaine 6 - Inside, Semaine 7 - Inside, Semaine 8 - Inside, Indoor (Mean + SD) | , , Day 1, Duration of treatment, Starting/ending  time, Mean THI, Min THI, Max THI, Mean THI, Min THI, Max THI |
| Summer 2019 | environment_hobo_xlsx | Données completes/Données accelerometres/Summer 2019/Hobo/THI per day of observation.xlsx | 181 | 11 | 18 | General data, Semaine 1 Inside, Semaine 2 Inside , Semaine 3 Inside, Semaine 4 Inside , Semaine 5 - Inside, Semaine 6 - Inside, Semaine 7 - Inside, Semaine 8 - Inside, Semaine 1 - Outside | , , Day 1, Duration of treatment, Starting/ending  time, Mean THI, Min THI, Max THI, Mean THI, Min THI, Max THI |
| Winter 2019 | clinical_sls_labels | Données completes/Données accelerometres/Winter 2019/Icetag/IceTags_Data/IceTags-issues and reports/Exercise Study - SLS Scores.xlsx | 35 | 9 | 3 | Baseline - 15JAN19, Midway - 12MAR19, Sheet1 | Cow, Block, Edge, Rest, Shiftwt, Uneven, , , * 2 videos for 2063 showing different blocks, both were scored |
| Winter 2019 | behavior_scan_workbook | Données completes/Données accelerometres/Winter 2019/cow_scan_long-format_7.12.19.xlsx | 38 | 4 | 5 | references, all scans FINAL, all scans, data summary by trt, data summary by cow | Distance Code, Distance Definition, ,  |
| Multi-season / aggregate | behavior_scan_workbook | Données completes/Scan_Tot.xlsx | 160 | 13 | 2 | Feuil1, Behaviours regroupment | Experiment, Paddock, Week, Cows, Trt, Pct_locomotion, Pct_rest, Pct_lying, Pct_Explo, Pct_eating, Pct_Ruminating, Pct_Social |

## Sorties objectif 1: inputs convertis 15 min

| season | relative_path | rows | cols | n_cows | date_min | date_max |
| --- | --- | --- | --- | --- | --- | --- |
| Fall 2019 | reports/objective1_pipeline_icetag/fall_2019_pipeline_input_15min.csv | 93187 | 10 | 30 | 2019-11-11 18:45:00 | 2019-12-14 13:00:00 |
| Fall 2021 | reports/objective1_pipeline_icetag/fall_2021_pipeline_input_15min.csv | 5131 | 10 | 10 | 2021-11-30 09:00:00 | 2021-12-06 11:00:00 |
| Summer 2019 | reports/objective1_pipeline_icetag/summer_2019_pipeline_input_15min.csv | 136726 | 10 | 18 | 2019-06-05 13:00:00 | 2019-09-06 12:00:00 |
| Winter 2019 | reports/objective1_pipeline_icetag/winter_2019_pipeline_input_15min.csv | 129323 | 10 | 17 | 2019-01-16 15:15:00 | 2019-04-17 11:30:00 |

## Sorties objectif 1: prédictions/features pipeline

| season | relative_path | rows | cols | n_cows | date_min | date_max |
| --- | --- | --- | --- | --- | --- | --- |
| Fall 2019 | reports/objective1_pipeline_icetag/fall_2019_pipeline_predictions.csv | 93860 | 139 | 30 | 2019-11-11 18:45:00 | 2019-12-14 13:00:00 |
| Fall 2021 | reports/objective1_pipeline_icetag/fall_2021_pipeline_predictions.csv | 5131 | 139 | 10 | 2021-11-30 09:00:00 | 2021-12-06 11:00:00 |
| Summer 2019 | reports/objective1_pipeline_icetag/summer_2019_pipeline_predictions.csv | 139111 | 139 | 18 | 2019-06-05 13:00:00 | 2019-09-06 12:00:00 |
| Winter 2019 | reports/objective1_pipeline_icetag/winter_2019_pipeline_predictions.csv | 136929 | 139 | 17 | 2019-01-16 15:15:00 | 2019-04-17 11:30:00 |

## Sorties objectif 1: résumés pipeline

| season | relative_path | rows | cols | n_cows | columns_preview |
| --- | --- | --- | --- | --- | --- |
| Fall 2019 | reports/objective1_pipeline_icetag/fall_2019_pipeline_summary.csv | 30 | 11 | 30 | n_bins, if_anomaly_points, problem_points, lameness_points, problem_starts, lameness_starts, lameness_notifs, critique_points, coverage_mean, coverage_min, Cow |
| Fall 2021 | reports/objective1_pipeline_icetag/fall_2021_pipeline_summary.csv | 10 | 11 | 10 | n_bins, if_anomaly_points, problem_points, lameness_points, problem_starts, lameness_starts, lameness_notifs, critique_points, coverage_mean, coverage_min, Cow |
| Summer 2019 | reports/objective1_pipeline_icetag/summer_2019_pipeline_summary.csv | 18 | 11 | 18 | n_bins, if_anomaly_points, problem_points, lameness_points, problem_starts, lameness_starts, lameness_notifs, critique_points, coverage_mean, coverage_min, Cow |
| Winter 2019 | reports/objective1_pipeline_icetag/winter_2019_pipeline_summary.csv | 17 | 11 | 17 | n_bins, if_anomaly_points, problem_points, lameness_points, problem_starts, lameness_starts, lameness_notifs, critique_points, coverage_mean, coverage_min, Cow |

## Sorties objectif 1: alertes seulement

| season | relative_path | rows | cols | n_cows | date_min | date_max |
| --- | --- | --- | --- | --- | --- | --- |
| Fall 2019 | reports/objective1_pipeline_icetag/fall_2019_pipeline_alerts_only.csv | 105 | 10 | 26 | 2019-11-12 03:00:00 | 2019-12-14 07:15:00 |
| Fall 2021 | reports/objective1_pipeline_icetag/fall_2021_pipeline_alerts_only.csv | 4 | 10 | 4 | 2021-12-01 10:15:00 | 2021-12-03 12:15:00 |
| Summer 2019 | reports/objective1_pipeline_icetag/summer_2019_pipeline_alerts_only.csv | 127 | 10 | 17 | 2019-06-05 21:00:00 | 2019-09-04 22:45:00 |
| Winter 2019 | reports/objective1_pipeline_icetag/winter_2019_pipeline_alerts_only.csv | 149 | 10 | 17 | 2019-01-17 22:15:00 | 2019-04-11 00:15:00 |

## Lecture par saison

### Fall 2019
Brut complet: IceTag CSV minute + LB, workbooks compilés, HOBO, scans comportementaux. Déjà converti en 15 min et passé dans le pipeline. Labels SLS locaux disponibles, mais synchronisation clinique limitée.

### Summer 2019
Brut complet: IceTag CSV minute + LB, HOBO/THI très riche, scans comportementaux. Déjà converti en 15 min et passé dans le pipeline. L’objectif 1.2 demande un mapping précis des scans.

### Winter 2019
Brut complet: IceTag CSV minute + LB, SLS, et workbook long-format `cow_scan_long-format_7.12.19.xlsx`. C’est la saison la plus intégrable pour comportement/environnement/SLS, même si les SLS ne valident pas les alertes comme boiterie clinique.

### Fall 2021
Brut plus court: IceTag CSV + mapping tag-vache, HOBO, Scan Sampling. Déjà converti en 15 min et passé dans le pipeline, mais fenêtre courte.

### Summer 2020
Présent dans les CSV agrégés de l’article seulement; pas de brut IceTag complet trouvé dans `Données completes`.

### Winter 2020
Présent dans les CSV agrégés de l’article seulement; pas de brut IceTag complet trouvé dans `Données completes`.

### Summer 2021
Présent dans les CSV agrégés de l’article seulement; pas de brut IceTag complet trouvé dans `Données completes`.

## Fichier catalogue

Catalogue détaillé CSV: `reports/mcgill_data_visibility_2026-06-02_catalog.csv`

## Priorité pratique

1. Objectif 1: travailler sur `*_pipeline_input_15min.csv`, `*_pipeline_predictions.csv`, `*_pipeline_alerts_only.csv`.
2. Objectif 1.2: commencer par Winter 2019, puis Summer 2019, Fall 2019, Fall 2021.
3. Analyse article/design expérimental: utiliser les 6 CSV agrégés dans `data-movement-behavior-main/dataset`.
4. Analyse météo/THI: utiliser les fichiers HOBO/THI, surtout Summer 2019 et Fall 2021.