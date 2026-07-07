# Objectif 2 — Environnement x comportement (Summer 2019)

## Tâche 2.1 — Synchronisation
- Dataset multimodal créé : 87501 bins de 15 min, 17 vaches.
- Sources fusionnées : IceTag (activité) + HOBO (température, humidité) + THI calculé.
- Période commune : 2019-07-01 à 2019-09-06.

## Tâche 2.2 — Analyse
- Corrélation THI vs pas (jour) : rho = +0.097 (p = 1.5e-106).
- Activité moyenne par niveau de stress thermique :
          n_bins  steps_moy  mi_moy  lying_h_moy
THI_cat                                         
1_aucun    16586       8.61   24.44         0.11
2_leger    14169      11.64   36.49         0.10
3_modere   19574      11.21   32.93         0.10
4_severe     929      12.77   32.16         0.08

## Lecture
- En stress sévère, l'activité varie de +48% par rapport au confort thermique.
- Tendance : l'activité augmente avec la température (cohérent avec activité accrue par temps doux/sorties).