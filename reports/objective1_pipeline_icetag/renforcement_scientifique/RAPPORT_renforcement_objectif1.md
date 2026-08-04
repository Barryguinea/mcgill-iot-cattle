# Renforcement scientifique - Objectif 1

Date: 2026-07-13

## Perimetre

- Base conservee: pipeline initiale McGill deja livree (Isolation Forest + regles metier).
- Objectif: requalifier les 385 notifications existantes avec un contexte troupeau, un filtre d'evenements collectifs et des niveaux de confiance.
- Interpretation: alertes comportementales compatibles avec une perturbation locomotrice, pas diagnostics cliniques confirmes.

## Methode ajoutee

1. Normalisation troupeau: chaque vache est comparee a la mediane contemporaine du troupeau au meme timestamp de 15 min.
2. Contexte valide si au moins 50% du troupeau et au moins 5 vaches ont une couverture >= 75%.
3. Evenement collectif si une alerte survient avec >= 30% des vaches alertees dans +/-1 jour ou >= 50% dans +/-3 jours.
4. Niveaux de confiance:
   - A_individuelle_prioritaire: alerte non collective, bonne couverture, deviation propre a la vache.
   - B_individuelle_a_verifier: alerte non collective mais support troupeau moins net.
   - C_probable_evenement_collectif: alerte dans un episode de troupeau, interpretation clinique prudente.
   - D_qualite_ou_contexte_insuffisant: donnees insuffisantes pour renforcer l'interpretation.

## Synthese par saison

| season      |   n_cows |   n_intervals | first_T    | last_T     |   initial_notifications |   alerted_cows |   collective_flagged |   herd_specific_signal |   mean_lame_confidence |   mean_coverage_pct |   A_individuelle_prioritaire |   B_individuelle_a_verifier |   C_probable_evenement_collectif |   D_qualite_ou_contexte_insuffisant | collective_flagged_pct   | herd_specific_signal_pct   |
|:------------|---------:|--------------:|:-----------|:-----------|------------------------:|---------------:|---------------------:|-----------------------:|-----------------------:|--------------------:|-----------------------------:|----------------------------:|---------------------------------:|------------------------------------:|:-------------------------|:---------------------------|
| fall_2019   |       30 |         93860 | 2019-11-11 | 2019-12-14 |                     105 |             26 |                   47 |                     26 |                49.1171 |                 100 |                            7 |                          51 |                               47 |                                   0 | 44.8%                    | 24.8%                      |
| fall_2021   |       10 |          5131 | 2021-11-30 | 2021-12-06 |                       4 |              4 |                    0 |                      0 |                53.225  |                 100 |                            0 |                           4 |                                0 |                                   0 | 0.0%                     | 0.0%                       |
| summer_2019 |       18 |        139111 | 2019-06-05 | 2019-09-06 |                     127 |             17 |                   17 |                     28 |                46.848  |                 100 |                           16 |                          94 |                               17 |                                   0 | 13.4%                    | 22.0%                      |
| winter_2019 |       17 |        136929 | 2019-01-16 | 2019-04-17 |                     149 |             17 |                   89 |                     34 |                48.2282 |                 100 |                           14 |                          46 |                               89 |                                   0 | 59.7%                    | 22.8%                      |

## Synthese par niveau de confiance

| season      | reinforced_confidence_level    |   notifications |   cows |   mean_lame_confidence |   mean_coverage_pct |   collective_alerts |   herd_specific_signals |
|:------------|:-------------------------------|----------------:|-------:|-----------------------:|--------------------:|--------------------:|------------------------:|
| fall_2019   | A_individuelle_prioritaire     |               7 |      4 |                49.9571 |                 100 |                   0 |                       7 |
| fall_2019   | B_individuelle_a_verifier      |              51 |     24 |                47.9392 |                 100 |                   0 |                       2 |
| fall_2019   | C_probable_evenement_collectif |              47 |     21 |                50.2702 |                 100 |                  47 |                      17 |
| fall_2021   | B_individuelle_a_verifier      |               4 |      4 |                53.225  |                 100 |                   0 |                       0 |
| summer_2019 | A_individuelle_prioritaire     |              16 |      8 |                49.975  |                 100 |                   0 |                      16 |
| summer_2019 | B_individuelle_a_verifier      |              94 |     16 |                45.9819 |                 100 |                   0 |                       6 |
| summer_2019 | C_probable_evenement_collectif |              17 |     10 |                48.6941 |                 100 |                  17 |                       6 |
| winter_2019 | A_individuelle_prioritaire     |              14 |      6 |                51.1857 |                 100 |                   0 |                      14 |
| winter_2019 | B_individuelle_a_verifier      |              46 |     15 |                47.1043 |                 100 |                   0 |                       1 |
| winter_2019 | C_probable_evenement_collectif |              89 |     14 |                48.3438 |                 100 |                  89 |                      19 |

## Principaux jours avec contexte collectif

| season      | Day        |   n_alerts |   alerted_cows |   collective_alerts | cows                                                                         | alerted_cow_frac   |
|:------------|:-----------|-----------:|---------------:|--------------------:|:-----------------------------------------------------------------------------|:-------------------|
| winter_2019 | 2019-02-08 |         14 |             13 |                  14 | 2047, 2056, 2063, 2069, 2081, 3437, 3443, 5221, 5246, 5250, 8506, 8508, 8510 | 76.5%              |
| winter_2019 | 2019-02-07 |         13 |             12 |                  13 | 2047, 2056, 2069, 2081, 3437, 3443, 5246, 5250, 8500, 8506, 8508, 8510       | 70.6%              |
| winter_2019 | 2019-02-04 |         11 |             11 |                  11 | 2047, 2056, 2069, 2081, 3437, 3443, 5250, 8500, 8506, 8508, 8510             | 64.7%              |
| winter_2019 | 2019-02-05 |         11 |              9 |                  11 | 2047, 2056, 2063, 3443, 5246, 5250, 8506, 8508, 8510                         | 52.9%              |
| winter_2019 | 2019-02-03 |         10 |              9 |                  10 | 2047, 2063, 2069, 3437, 3443, 5246, 5250, 8500, 8506                         | 52.9%              |
| winter_2019 | 2019-02-01 |          8 |              8 |                   8 | 2047, 2063, 2069, 2081, 3437, 8500, 8506, 8508                               | 47.1%              |
| winter_2019 | 2019-02-06 |          8 |              7 |                   8 | 2047, 2063, 2081, 5221, 5246, 5250, 8508                                     | 41.2%              |
| fall_2019   | 2019-11-12 |          8 |              8 |                   7 | 2041, 2057, 2066, 5327, 5865, 5875, 8517, 8527                               | 26.7%              |
| fall_2019   | 2019-11-25 |          6 |              6 |                   6 | 2041, 2081, 3437, 3444, 5865, 5879                                           | 20.0%              |
| fall_2019   | 2019-12-11 |          6 |              6 |                   6 | 2066, 5870, 5871, 5874, 8525, 8527                                           | 20.0%              |
| winter_2019 | 2019-02-02 |          6 |              6 |                   6 | 2047, 2063, 3443, 5246, 8506, 8508                                           | 35.3%              |
| winter_2019 | 2019-02-11 |          6 |              6 |                   6 | 2056, 2081, 3437, 3443, 8506, 8508                                           | 35.3%              |
| fall_2019   | 2019-11-21 |          5 |              5 |                   5 | 2041, 2062, 2066, 2081, 5879                                                 | 16.7%              |
| fall_2019   | 2019-11-29 |          4 |              4 |                   4 | 2062, 5865, 5879, 8527                                                       | 13.3%              |
| summer_2019 | 2019-07-17 |          4 |              4 |                   4 | 5313, 5854, 5857, 8536                                                       | 22.2%              |
| summer_2019 | 2019-07-18 |          4 |              4 |                   4 | 419, 5857, 8520, 8536                                                        | 22.2%              |
| summer_2019 | 2019-07-19 |          4 |              4 |                   4 | 5214, 5854, 5865, 5871                                                       | 22.2%              |
| fall_2019   | 2019-12-13 |          6 |              6 |                   3 | 2062, 2063, 5865, 5872, 5875, 8525                                           | 20.0%              |
| fall_2019   | 2019-11-20 |          4 |              4 |                   3 | 5870, 821, 8517, 8525                                                        | 13.3%              |
| fall_2019   | 2019-11-22 |          3 |              3 |                   3 | 2062, 3437, 8527                                                             | 10.0%              |

## Lecture scientifique

Cette analyse renforce l'Objectif 1 parce qu'elle separe les alertes individuelles prioritaires des alertes probablement liees a un contexte partage. Elle ne transforme pas les alertes en verite-terrain clinique: la sensibilite et la specificite a la boiterie restent non mesurables sans labels synchrones et cas cliniquement nets.

## Fichiers produits

- `objective1_reinforced_alerts.csv`
- `objective1_reinforced_summary_by_season.csv`
- `objective1_reinforced_summary_by_confidence.csv`
- `objective1_reinforced_summary_by_cow.csv`
- `objective1_collective_days.csv`
