# Cadrage — Pipeline initiale (IF + règles) vs V3 (HYPO + INSTABILITÉ + hybride)

Date : 2026-07-08
Portée : projet McGill (4 essais IceTag). Données brutes confidentielles, non versionnées.

---

## 1. Les deux pipelines et leur lien avec le mémoire

Deux approches de détection existent, correspondant à **deux versions du mémoire** :

| Pipeline | Description | Version du mémoire correspondante |
|---|---|---|
| **Initiale** | Isolation Forest + règles métier, score ponctuel | Version **antérieure** du mémoire |
| **V3** | Branches HYPO (baisse persistante) + INSTABILITÉ + fusion hiérarchique | Mémoire **actuel déposé (memoirev3)** |

> **Point important (à ne pas inverser) :** le mémoire actuellement déposé utilise la **V3** (HYPO/INSTABILITÉ),
> pas la pipeline initiale IF + règles. C'est donc la **V3** qui est directement comparable au mémoire actuel ;
> la pipeline initiale correspond à l'approche d'une version antérieure.

L'Objectif 1 du SOW McGill a toutefois été **réalisé avec la pipeline initiale** (IF + règles), qui a produit
les 385 alertes livrées. La V3 a ensuite été appliquée aux mêmes données à titre **comparatif**.

---

## 2. Résultats vérifiés sur McGill (4 essais)

| Pipeline | Notifications | Taux / 100 cow-days |
|---|---|---|
| Initiale (IF + règles) | **385** | 9,86 |
| V3 hybride | **1179** | 30,18 |

- La V3 produit **3,1× plus d'alertes** que la pipeline initiale.
- Le comparateur IF recalculé par la V3 **reproduit exactement** les 385 anciennes notifications (385/385) :
  la différence vient donc de la **nouvelle logique V3**, pas d'un changement d'entrée.
- Corrélation par vache (global) : Pearson 0,73 ; Spearman 0,75.

Détail par saison : Fall 2019 105 → 299 ; Summer 2019 127 → 421 ; Winter 2019 149 → 441 ; Fall 2021 4 → 18.

---

## 3. Quelle pipeline pour quel usage

| Objectif | Pipeline recommandée |
|---|---|
| Livrable SOW Objectif 1 / comparaison avec les résultats déjà produits | **Initiale (IF + règles)** — c'est elle qui a généré les 385 alertes livrées |
| Détection plus large d'anomalies comportementales | **V3** (plus sensible, définition élargie) |
| Diagnostic de **boiterie légère** | **Aucune des deux** — l'IceTag mesure la quantité de mouvement, pas l'asymétrie de démarche |

---

## 4. Caveat essentiel : pas de vérité-terrain boiterie sur McGill

On ne peut **pas** mesurer la sensibilité ni la spécificité *à la boiterie* sur McGill, faute de labels
cliniques valides (démontré aux notebooks 06 et 07, et confirmé par McGill : peu ou pas de vaches
cliniquement boiteuses).

En conséquence :
- Dire que la V3 est « plus sensible » signifie seulement qu'elle **produit plus d'alertes**, pas qu'elle
  détecte mieux la boiterie.
- La V3 **change la définition** de la sortie : une **alerte comportementale à vérifier**, et non une boiterie
  clinique. Sa composition sur McGill : SEQUENCE 54,7 %, MIXTE 28,0 %, HYPO 17,3 %.
- Le surcroît d'alertes (×3,1) implique une **charge de vérification plus élevée**. Sans recalibration, la V3
  n'est pas prête pour un usage opérationnel sur McGill.

---

## 5. Recommandation

- **Résultat principal livré à McGill : pipeline initiale (IF + règles)** — stable, déjà documentée, et c'est
  elle qui sous-tend les 385 alertes de l'Objectif 1.
- **V3 : présentée comme extension comparative** (= l'approche du mémoire actuel), montrant une détection
  comportementale plus large, à **recalibrer** pour réduire la charge d'alertes avant tout usage opérationnel.
- **Boiterie légère : hors de portée** des deux pipelines avec ce capteur ; nécessiterait des capteurs de
  symétrie de démarche.

---

## 6. Sources

- Rapport de comparaison : `ANALYSE_comparaison_memoirev3_vs_ancien.md`
- Tables : `comparison_summary_by_season.csv`, `comparison_by_cow_correlations.csv`,
  `comparison_temporal_overlap_tolerance.csv`
- Synthèse multi-saisons pipeline initiale : `../objective1_multi_season_summary.csv`
