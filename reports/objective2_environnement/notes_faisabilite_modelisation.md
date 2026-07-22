# Faisabilité d'un modèle intégré - Objectif 2, Tâche 2.2

## Verdict

Un modèle activité-environnement est faisable. Un modèle incluant les comportements observés comme covariables principales n'est pas robuste avec seulement huit jours de scan.

## Résultats de sensibilité

- Modèle mixte avec vache et heure : effet THI positif, +0,198 pas par unité THI.
- Analyse du troupeau par timestamp avec contrôle de l'heure : +0,221, p = 6,15e-08.
- Même analyse avec contrôle explicite du jour : +0,061, IC 95 % [-0,070; 0,192], p = 0,364.
- Motion Index avec heure et jour : +0,091, p = 0,752.
- Le terme quadratique du THI n'est plus concluant après contrôle du jour, p = 0,224.

## Contrôle complet de l'effet THI

Les estimations `+0,221` et `+0,061` répondent à deux questions différentes :

- **Association globale** : `+0,221` pas par unité THI, p = 6,15e-08. Elle combine les variations entre jours et les variations à l'intérieur des jours.
- **Association au niveau de 62 unités journalières** : `+0,273`, p = 9,20e-08, avec des erreurs HAC tenant compte de leur succession temporelle. Avec une tendance calendaire linéaire, l'estimation reste positive (`+0,162`, p = 0,030).
- **Effet intra-jour strict** : `+0,061`, IC 95 % [-0,070; 0,192], p = 0,364. Avec des erreurs regroupées par jour, la conclusion demeure non concluante (p = 0,291).

Les contrôles d'intégrité confirment 5 795 timestamps uniques, aucun doublon vache-timestamp et une valeur THI commune aux vaches présentes au même timestamp. L'association globale reste positive lorsque l'analyse est limitée aux jours ayant au moins 80 timestamps ou aux timestamps comptant au moins 14 vaches.

L'association positive globale est donc reproductible et ne résulte pas de la simple duplication des vaches. Elle est principalement portée par les différences entre jours. Le contrôle par jour retire toute cette composante et pose une question plus stricte : à heure et journée identiques, la variation résiduelle du THI explique-t-elle l'activité? La réponse actuelle est non concluante.

La progression saisonnière, le protocole d'exercice ou d'autres caractéristiques journalières peuvent encore expliquer une partie de l'association entre jours. Les données montrent une association positive, mais elles ne démontrent pas un effet thermique causal indépendant.

## Recommandations

1. Conserver le contrôle de l'heure et du jour dans l'analyse principale.
2. Présenter séparément les associations entre jours et les variations intra-jour.
3. Densifier les scans comportementaux avant de les utiliser comme covariables.
4. Tester les effets décalés lorsque davantage de jours indépendants seront disponibles.
5. Étendre au froid hivernal après validation McGill de la correspondance des éthogrammes.
