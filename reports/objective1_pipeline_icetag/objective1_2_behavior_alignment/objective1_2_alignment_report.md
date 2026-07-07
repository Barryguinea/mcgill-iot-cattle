# Objectif 1.2 - Alignement alertes et comportements

## Statut

Alignement complet produit pour Winter 2019. Les autres saisons sont preparees mais non alignees tant que le mapping date/Cow_ID n est pas confirme.

## Resume Winter 2019

| metric                             |   value |
|:-----------------------------------|--------:|
| winter_alerts_total                |     149 |
| winter_scans_total                 |      42 |
| alerts_with_matched_scan_within_1d |      16 |
| alerts_with_same_day_scan          |       7 |
| scans_with_same_day_alert          |       7 |
| scans_with_alert_within_1d         |      11 |

## Alertes Winter 2019 par etat comportemental associe

|   matched_scan_within_1d | scan_behavior_state   |   alerts |   mean_alert_confidence |   mean_behavior_activity_score |   mean_pct_immobile |   mean_pct_active_mobile |
|-------------------------:|:----------------------|---------:|------------------------:|-------------------------------:|--------------------:|-------------------------:|
|                        0 | nan                   |      133 |                 48.1489 |                     nan        |          nan        |              nan         |
|                        1 | active_mobile_present |        2 |                 52.05   |                       0.466667 |            0.133333 |                0.333333  |
|                        1 | immobile_dominant     |        1 |                 46      |                       0.125    |            0.633333 |                0.0333333 |
|                        1 | mixed_or_low_signal   |        2 |                 51.15   |                       0.266667 |            0.383333 |                0.0833333 |
|                        1 | rumination_dominant   |       11 |                 48.1636 |                       0.221212 |            0.236364 |                0.0272727 |

## Top vaches Winter 2019

|   Cow |   alerts |   matched_within_1d |   same_day |   mean_alert_confidence |   mean_matched_activity_score |   mean_matched_pct_immobile |   mean_matched_pct_active_mobile |
|------:|---------:|--------------------:|-----------:|------------------------:|------------------------------:|----------------------------:|---------------------------------:|
|  8508 |       19 |                   6 |          4 |                 48.3105 |                      0.305556 |                    0.177778 |                        0.127778  |
|  2056 |       17 |                   7 |          2 |                 49.6647 |                      0.221429 |                    0.290476 |                        0.0333333 |
|  5250 |       13 |                   0 |          0 |                 47.5077 |                    nan        |                  nan        |                      nan         |
|  3443 |       12 |                   1 |          0 |                 50.7917 |                      0.316667 |                    0.333333 |                        0.133333  |
|  2081 |       11 |                   0 |          0 |                 47.7182 |                    nan        |                  nan        |                      nan         |
|  8506 |       11 |                   0 |          0 |                 48.0909 |                    nan        |                  nan        |                      nan         |
|  2047 |        9 |                   0 |          0 |                 48.2    |                    nan        |                  nan        |                      nan         |
|  3437 |        9 |                   0 |          0 |                 47.6111 |                    nan        |                  nan        |                      nan         |
|  5246 |        8 |                   1 |          1 |                 47.3375 |                      0.125    |                    0.633333 |                        0.0333333 |
|  2063 |        8 |                   0 |          0 |                 47.5625 |                    nan        |                  nan        |                      nan         |
|  8510 |        7 |                   1 |          0 |                 45.7429 |                      0.2      |                    0.2      |                        0         |
|  2069 |        7 |                   0 |          0 |                 48.6857 |                    nan        |                  nan        |                      nan         |

## Statut par saison

| season      | alignment_status   | reason                                                                                                                             | next_action                                                                                |
|:------------|:-------------------|:-----------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------|
| winter_2019 | done               | Cow_ID and Date are available in long-format scan table.                                                                           | Interpret concordance and refine behavior categories with domain team.                     |
| summer_2019 | not_done_yet       | Scan workbook has Cow IDs and scan codes, but exact dates/times must be mapped from Week sheets before alert alignment.            | Extract week/date mapping from protocol or workbook metadata, then run same-day alignment. |
| fall_2019   | not_done_yet       | Scan workbook uses paddock/collar color labels rather than direct Cow_ID in scan rows.                                             | Obtain or reconstruct color/paddock-to-Cow_ID mapping for weeks 4, 5, 5.2.                 |
| fall_2021   | not_done_yet       | Scan workbook uses collar/color/group labels and most scan dates precede the IceTag window; mapping and overlap must be confirmed. | Use scan sheets around Nov 30-Dec 6 and map color/group labels to Cow_ID.                  |

## Interpretation

- Les concordances Winter 2019 sont temporelles et exploratoires: elles indiquent si une alerte est proche d une observation comportementale, pas une confirmation clinique.
- La fenetre utilisee est +/- 1 jour, avec indicateur separe pour meme jour.
- Les scans sont ponctuels et ne couvrent pas toute la journee; une alerte sans scan proche ne signifie pas absence de comportement anormal.
- Pour Summer/Fall, ne pas calculer de concordance tant que Cow_ID/date ne sont pas standardises.