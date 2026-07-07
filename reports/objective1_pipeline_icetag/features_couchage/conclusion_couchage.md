# Features de couchage vs boiterie — Winter 2019

Vaches : 16 (boiteuses : 5, saines/légères : 11)

## Séparabilité univariée (couchage)
Features significatives (p<0.05) : 0 / 7

                   feature  moy_boiteuses  moy_saines  p_value  spearman_rho signif_5pct
      Heures couché / jour          14.87       14.54   0.5833         0.000         non
      Heures debout / jour          11.21       10.76   0.9130         0.195         non
        Nb couchers / jour          83.00       63.46   0.2674         0.249         non
  Durée moy. coucher (min)          25.07       24.74   0.6612        -0.139         non
Agitation (trans/h couché)           9.61        7.01   0.2674         0.284         non
Fragmentation (couchers/h)           5.46        4.18   0.2674         0.284         non
  Ratio couchage jour/nuit           0.83        0.80   0.7427        -0.014         non

## Plafond multivarié
AUC features de couchage = 0.182 | features de pas (nb 06) = 0.24 | hasard = 0.5

## Conclusion
Le comportement de couchage ne sépare pas non plus les vaches boiteuses des saines. Le signal de boiterie légère est absent de TOUTES les variables IceTag disponibles (activité ET couchage). 

=> Confirmation finale : la limite n'est pas l'algorithme ni les features choisies, mais le CAPTEUR. L'IceTag mesure la quantité de mouvement, pas l'asymétrie de démarche (le vrai marqueur de boiterie légère). Recommandation : capteurs de symétrie de démarche ou analyse vidéo pour les cas légers.