# Tache 1.2 - Rapport de validation : alertes vs observations comportementales

Scans alignables (date + vache appariee) : 396
Scans avec alerte concurrente (pm1 jour) : 38

## Concordance temporelle par experience
Experiment  n_scans  scans_avec_alerte  taux_concurrence_%
 Fall 2021      270                  1                 0.4
  Fall2019       27                 12                44.4
Summer2019       58                 14                24.1
Winter2019       41                 11                26.8

## Comportement avec vs sans alerte (analyse intra-experience)
Experiment comportement  moy_avec  moy_sans  p_value signif  n_avec  n_sans
Summer2019        Explo     0.074     0.148    0.017    OUI     NaN     NaN

## Point methodologique important
Une comparaison GROUPEE (toutes experiences confondues) suggerait faussement que les scans avec alerte ont plus de comportement "Idle" (p<0.0001). Ce resultat est un ARTEFACT de confusion (paradoxe de Simpson) : Fall 2021 a un codage comportemental different et quasiment aucune alerte, ce qui domine le groupe "sans alerte". Apres controle par experience, cette concordance disparait.

## Conclusion
La concordance temporelle existe (24-44%% des scans de Fall2019/Summer/Winter ont une alerte a pm1 jour), mais la composition comportementale des scans avec et sans alerte ne differe pas significativement une fois le confondant "experience" controle. Le faible nombre de scans avec alerte par experience (11-14) limite la puissance.

## Limites
- Scans ponctuels (quelques jours/essai) vs alertes continues : peu de coincidences exactes.
- Fall 2021 : fenetre IceTag de 7 jours -> 1 seul scan avec alerte ; codage comportemental distinct.
- La concordance mesure une coincidence temporelle alerte/comportement, non un diagnostic de boiterie.