# Tache 1.2 - Rapport court de validation

Objet: comparer les alertes automatisees du pipeline avec les observations comportementales
disponibles, puis documenter les concordances et les limites.

Scans alignables (date + vache appariee) : 396
Scans avec alerte concurrente (+/- 1 jour) : 38

## Concordance temporelle par experience

| Experience | Scans alignes | Scans avec alerte | Taux de concurrence |
|---|---:|---:|---:|
| Winter 2019 | 41 | 11 | 26.8% |
| Summer 2019 | 58 | 14 | 24.1% |
| Fall 2019 | 27 | 12 | 44.4% |
| Fall 2021 | 270 | 1 | 0.4% |

## Comportement avec vs sans alerte (analyse intra-experience)

Apres controle par experience, la composition comportementale des scans avec et sans alerte ne
montre pas de difference robuste. Un seul contraste ressort dans Summer 2019 pour le comportement
`Explo` (p = 0.017), mais ce signal doit etre interprete avec prudence compte tenu du nombre de
tests et du faible nombre de scans avec alerte.

## Point methodologique important
Une comparaison groupee, toutes experiences confondues, suggerait faussement que les scans avec
alerte ont plus de comportement `Idle` (p < 0.0001). Ce resultat est un artefact de confusion
(paradoxe de Simpson): Fall 2021 a un codage comportemental different et quasiment aucune alerte,
ce qui domine le groupe sans alerte. Apres controle par experience, cette concordance disparait.

## Conclusion
La concordance temporelle existe pour Winter 2019, Summer 2019 et Fall 2019: environ 24 a 44% des
scans ont une alerte a +/- 1 jour. En revanche, la composition comportementale des scans avec et
sans alerte ne differe pas significativement une fois le confondant experience controle. Le faible
nombre de scans avec alerte par experience limite la puissance.

## Limites
- Scans ponctuels (quelques jours/essai) vs alertes continues : peu de coincidences exactes.
- Fall 2021 : fenetre IceTag de 7 jours -> 1 seul scan avec alerte ; codage comportemental distinct.
- La concordance mesure une coincidence temporelle alerte/comportement, non un diagnostic de boiterie.
