# Note technique de reproductibilité - Objectif 1

Cette note confirme que le pipeline de détection a été appliqué aux quatre corpus IceTag fournis pour l'Objectif 1.

## Données traitées
- Saisons: Winter 2019, Summer 2019, Fall 2019, Fall 2021
- Total analysé: 375 031 intervalles de 15 minutes
- Alertes produites: 385
- Fall 2021: 10 profils traités, dont 8 couvrent la fenêtre complète du SOW et 2 sont partiels.

## Traitement appliqué
- Harmonisation des timestamps et des identifiants de vaches.
- Construction de séries régulières par vache en intervalles de 15 minutes.
- Application du pipeline de détection sur chaque saison.
- Export des prédictions, alertes seules et résumés par saison.
- Ajout d'une lecture troupeau pour séparer les alertes individuelles des épisodes collectifs.

## Sorties
- DONNEES_TRAITEES_ALERTES/: prédictions, alertes et résumés par saison.
- TABLEAUX_CSV/: synthèses et tables de concordance.

## Où trouver le code
Le code du pipeline n'est pas dupliqué dans ce paquet. Il accompagne le livrable de l'Objectif 3, dans `code/core/`, avec un notebook qui l'exécute sur un échantillon et vérifie ses sorties par assertion.

Le présent paquet contient en revanche le script qui reproduit la comparaison des deux approches sur les scores SLS : `ANNEXE_pipeline_actuelle_HYPO_instabilite_hybride/code/run_objective1_sls_comparaison_equitable.py`.

## Limite
Les sorties sont reproductibles comme alertes comportementales. Des scores SLS synchronisés sont disponibles pour une sous-cohorte Winter 2019, mais le faible nombre de cas SLS >= 2 ne permet pas une validation clinique complète.
