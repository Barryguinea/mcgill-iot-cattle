# Projet McGill — IoT Bovins Laitiers

Analyse de données IoT (capteurs IceTag + HOBO) pour bovins laitiers en stabulation entravée,
dans le cadre du projet Well-E (collaboration UQAM × McGill).

## Équipe
- **Elsa Vasseur** (PI, McGill) — conceptualisation, supervision
- **Tania Wolfe** (McGill) — collecte et préparation des données
- **Marjorie Cellier** (McGill) — analyse accéléromètres, auteure principale de l'article de référence
- **Abdoulaye Baniré Diallo** (UQAM) — direction académique
- **Aliou Barry** (UQAM) — analyse de données, pipeline, notebook de démonstration

## Objectifs (Statement of Work, 1er juin – 31 août 2026)

| # | Objectif | Statut |
|---|---|---|
| 1 | Appliquer et évaluer le pipeline de détection de boiterie sur les données IoT | ✅ Fait |
| 2 | Analyser la relation entre conditions environnementales et comportement locomoteur | ✅ Fait (Summer 2019) |
| 3 | Développer un notebook de démonstration IoT | ✅ Fait |
| 4 | Support technique aux boîtes à outils WELL-E | 🔜 En attente des scripts |

## Résultats clés

- **Objectif 1** : le pipeline (Isolation Forest + règles) est **techniquement transférable** aux 4 corpus
  McGill (385 alertes), mais la **boiterie légère n'est pas détectable** — limite du capteur (mesure la
  quantité de mouvement, pas l'asymétrie de démarche), confirmée par McGill (peu/pas de vaches
  cliniquement boiteuses). Voir `reports/objective1_pipeline_icetag/RAPPORT_FINAL_objectif1.md`.
- **Comparaison V3** : la V3 (HYPO + INSTABILITÉ, approche du mémoire actuel) produit 1179 alertes (×3,1),
  définition élargie, à recalibrer. Voir `.../memoirev3_comparison/CADRAGE_pipeline_initiale_vs_V3.md`.
- **Objectif 2** : effet du stress thermique (THI) sur l'activité et le comportement, sur données synchronisées
  IceTag + HOBO + scans. Voir `reports/objective2_environnement/`.

## Structure du dépôt

```
notebooks/              12 notebooks (audit → pipeline → diagnostic → env×comportement → démonstration)
  01  audit des données          07  features de couchage
  02  conversion IceTag          08  environnement × comportement
  03  pipeline + SLS [superseded] 09  comportement × condition [superseded]
  04  synchro Winter 2019        10  concordance alertes/comportement (Tâche 1.2)
  05  pipeline 4 saisons (Obj 1) 11  Objectif 2 final (fichier daté)
  06  diagnostic séparabilité    12  notebook de démonstration (Obj 3)
reports/                rapports, figures, tables de résultats agrégés (par objectif)
Données completes/      données brutes (NON versionnées — confidentiel, voir .gitignore)
SOW Alliou - Complété.docx, presentation_travaux_mcgill.pptx
```

## Données & confidentialité

- Corpus : 4 essais IceTag (Fall/Summer/Winter 2019, Fall 2021) + capteurs environnementaux HOBO.
- **Les données brutes McGill sont confidentielles et ne sont pas versionnées** (exclues via `.gitignore`,
  ainsi que les gros fichiers régénérables : prédictions, séries 15 min). Le dépôt ne contient que le code,
  les rapports, les figures et les résultats agrégés.

## Reproduction

Les notebooks se réexécutent dans l'ordre après avoir replacé `Données completes/` en local
(fichiers non diffusables). Chaque notebook écrit ses sorties dans `reports/`.

## Article de référence
Cellier, M., Shepley, E., Aigueperse, N. et al. (2025). *Enhancing movement opportunity
to support behavioral needs for movement-restricted cattle through different conditions
of access to exercise.* Sci Rep 15, 5917. https://doi.org/10.1038/s41598-025-89891-4
