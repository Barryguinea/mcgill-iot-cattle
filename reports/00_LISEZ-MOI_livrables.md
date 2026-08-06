# Livrables - Projet IoT Vaches Laitières (WELL-E)

**Auteur :** Aliou Barry (UQAM)
**Projet :** Well-E - Integrated Analysis of IoT, Behavioral and Environmental Data in Dairy Cattle
**Collaboration :** UQAM (A. B. Diallo) x McGill (Pr Elsa Vasseur, WELL-E)
**Période du contrat :** 1er juin - 31 août 2026

Ce dossier rassemble les livrables : rapports, tables de résultats agrégées (CSV), données traitées avec alertes, et présentations.

---

## Comment naviguer

```
00_contexte_projet/                 Audit et inventaire des données (mise en contexte)

Objectif1_Pipeline_detection_boiterie/
    NOTES_SOW/                      Note technique + rapport de validation (livrables SOW)
    DONNEES_TRAITEES_ALERTES/       Jeux de données traités : alertes, résumés, prédictions
    TABLEAUX_CSV/                   Table de concordance + tableaux du renforcement
    RAPPORTS/                       Rapport de livraison Word + présentation
    ANNEXE_pipeline_actuelle_HYPO_instabilite_hybride/   Extension comparative (approche du mémoire)

Objectif2_Environnement_x_comportement/
    NOTES_SOW/                      Documentation synchro + notes de faisabilité
    DONNEES_SYNCHRONISEES/          Tables vache-15 min et trimodale vache-jour
    TABLEAUX_CSV/                   Résultats du modèle mixte + analyses
    RAPPORTS/                       Rapport de livraison Word + présentation
    FIGURES/                        Figures
    code/                           Notebook final 11 + deux scripts d'analyse

Objectif3_Notebook_demonstration/
    RAPPORTS/                       Guide Word + présentation détaillée
    DOCUMENTATION/                  Documentation d'exécution
    DONNEES_DEMO/                   Données compactes de démonstration
    RESULTATS/                      Figures et synthèse du notebook
    code/                           Notebook (12), pipeline et paramètres

Objectif4_Support_outils_WELL-E/
    01_RAPPORTS_WORD/               Revue annotée, note Mira et guide de dépannage
    02_SCRIPTS_PYTHON/              Scripts nettoyés et exécutables en ligne de commande
    03_TESTS/                       Tests unitaires et comparaison reproductible
    04_RESULTATS_VALIDATION/        Résumés numériques de validation
```

Pour une lecture rapide : ouvrir `Objectif1_Pipeline_detection_boiterie/RAPPORTS/Objectif1_rapport_livraison.docx`.

---

## Objectif 1 - Appliquer et évaluer le pipeline de détection de boiterie

**À lire en premier :** `RAPPORTS/Objectif1_rapport_livraison.docx`

**Ce qui a été livré**
- **Pipeline appliqué aux 4 corpus IceTag** (Fall / Summer / Winter 2019, Fall 2021) : environ 375 000 intervalles de 15 min traités, **385 alertes** produites, paramètres gelés, exécution reproductible.
- **Note technique de reproductibilité** : `NOTES_SOW/note_technique_reproductibilite.md`.
- **Concordance alertes / observations comportementales** (Tâche 1.2), sur un dénominateur corrigé : 396 scans datés dont 133 réellement couverts par IceTag à plus ou moins un jour, 38 concordants soit 28,6 %. Le contrôle du niveau attendu donne 29,9 % observé contre 27,8 % attendu, p = 0,324 : l'écart n'est pas concluant. `NOTES_SOW/rapport_validation_concordance.md` + `TABLEAUX_CSV/table_concordance.csv`.
- **Renforcement scientifique** : requalification des 385 alertes par normalisation troupeau et filtrage des événements collectifs, en niveaux de confiance A/B/C/D (**A = 37** individuelles prioritaires, **B = 195** à vérifier, **C = 153** contexte collectif). Tables : `TABLEAUX_CSV/objective1_reinforced_*.csv`, `objective1_collective_days.csv`.
- **Présentation** : `RAPPORTS/Objectif1_presentation_detaillee.pptx`.
- **Annexe** : `ANNEXE_pipeline_actuelle_HYPO_instabilite_hybride/` documente l'approche du mémoire actuel (branches HYPO + instabilité + fusion hybride) appliquée aux mêmes données. Les deux approches y sont comparées sur un protocole strictement identique, soit les mêmes 14 vaches, le score SLS du 12 mars et la même fenêtre de sept jours : AUC 0,576 pour la pipeline initiale contre 0,924 pour l'approche actuelle. Script de calcul et fichiers sources inclus.

**Résultat clé.** Le pipeline se **transfère techniquement** aux nouvelles données. La **baseline IF + règles ne montre aucun signal** face aux scores locomoteurs, ce qui tient d'abord au **capteur** : l'IceTag mesure une quantité de mouvement, pas l'asymétrie de démarche propre à la boiterie légère. L'approche actuelle du mémoire sépare en revanche les deux groupes sur la fenêtre du score, mais sur trois cas positifs seulement : c'est un signal exploratoire, pas une validation clinique.

**Correspondance avec le SOW (Aim 1)**

| Livrable SOW | Fichier(s) |
|---|---|
| Jeux de données traités avec alertes (4 corpus) | `DONNEES_TRAITEES_ALERTES/` |
| Note technique de reproductibilité | `NOTES_SOW/note_technique_reproductibilite.md` |
| Table de concordance (alertes vs comportement) | `TABLEAUX_CSV/table_concordance.csv` |
| Rapport de validation (Tâche 1.2) | `NOTES_SOW/rapport_validation_concordance.md` |
| Rapport de livraison de l'objectif | `RAPPORTS/Objectif1_rapport_livraison.docx` |

---

## Objectif 2 - Conditions environnementales x comportement locomoteur

**À lire en premier :** `RAPPORTS/Objectif2_rapport_livraison.docx`

**Ce qui a été livré**
- Synchronisation IceTag + HOBO extérieur (indice THI) + scans comportementaux (Summer 2019) : 87 501 intervalles de 15 minutes, 17 vaches et 62 jours. La table trimodale `DONNEES_SYNCHRONISEES/summer2019_multimodal_cow_day.csv` contient 49 scans complets sur 51.
- **Analyses de sensibilité activité x THI** : association globale positive (+0,221 pas/unité THI au niveau troupeau-timestamp, p=6,15e-8), encore positive après contrôle d'une tendance calendaire linéaire (+0,129; p=0,020), mais plus faible et non concluante dans la comparaison stricte à l'intérieur d'un même jour (+0,061; p=0,364). Tables : `TABLEAUX_CSV/objective2_thi_controle_complet.csv`, `objective2_mixed_model_summary.csv`, `objective2_profil_par_thi.csv`.
- Analyse comportement x THI : exploratoire sur 8 jours; l'alimentation présente un signal quotidien positif (rho=0,738; p=0,037), à confirmer sur davantage de jours.
- **Extension à d'autres corpus** : la même méthode appliquée à Fall 2019 et Fall 2021 sur la température intérieure, seule mesure commune aux trois. L'effet intra-jour reste non concluant dans les trois cas. Le placement des sondes des deux automnes est déduit des relevés et reste à confirmer par McGill; les défauts de qualité de Fall 2021 sont documentés. Tables : `TABLEAUX_CSV/objective2_indoor_multiseason_*.csv`.
- Notes de faisabilité d'un modèle intégré : `NOTES_SOW/notes_faisabilite_modelisation.md`.
- Code : notebook final 11 + `build_objective2_trimodal_dataset.py` + `run_objective2_mixed_model.py` + `run_objective2_indoor_multiseason.py`.

**Résultat clé.** Une association positive THI-activité est observée globalement et demeure positive après contrôle d'une tendance calendaire linéaire. Toutefois, la comparaison stricte à l'intérieur d'un même jour n'est pas concluante. Le stress sévère (THI >= 80) est rare, soit 1,1 % des intervalles. Les résultats restent exploratoires : ils ne démontrent ni un effet thermique causal indépendant ni une baisse d'activité attribuable au stress sévère.

**Correspondance SOW (Aim 2)**

| Livrable SOW | Fichier(s) |
|---|---|
| Jeu de données intégré | `DONNEES_SYNCHRONISEES/summer2019_multimodal_cow_day.csv` |
| Documentation de la synchronisation | `NOTES_SOW/documentation_synchronisation.md` |
| Rapport d'analyse exploratoire | `RAPPORTS/Objectif2_rapport_livraison.docx` |
| Notes sur la faisabilité d'un modèle intégré | `NOTES_SOW/notes_faisabilite_modelisation.md` |

---

## Objectif 3 - Notebook de démonstration IoT

**À lire en premier :** `RAPPORTS/Objectif3_guide_utilisation.docx`

**Ce qui a été livré**
- **Notebook final exécuté** (`code/12_objectif3_notebook_demonstration.ipynb`) couvrant le chargement, le prétraitement, l'exécution réelle de la pipeline IceTag et les analyses environnement-comportement.
- **Documentation d'utilisation** et données compactes permettant de relancer la démonstration de façon autonome.
- **Guide d'interprétation** distinguant dépistage comportemental, association exploratoire et preuve clinique ou causale.
- **Présentation détaillée** de 12 diapositives avec notes : `RAPPORTS/Objectif3_presentation_detaillee.pptx`.

---

## Objectif 4 - Support technique aux boîtes à outils WELL-E

**À lire en premier :** `Objectif4_Support_outils_WELL-E/01_RAPPORTS_WORD/Objectif4_revue_annotee_scripts.docx`

- **Tâche 4.1 terminée** : revue de la conversion MATLAB vers Python, scripts nettoyés, six corrections documentées et tests sur l'exemple du 27 mars.
- La conversion et les métriques numériques principales reproduisent exactement la version Python reçue sur 314 715 lignes et 13 vaches.
- **Tâche 4.2 préparée** : note d'application à Mira et guide de dépannage livrés.
- **Application Mira en attente** : aucun jeu de données ni fichier de configuration Mira n'est présent; aucun résultat Mira n'est revendiqué.

---

## Confidentialité

Les **données brutes McGill** sont **confidentielles** et **ne font pas partie** de ce dossier. Le paquet ne contient que le code, les rapports et les résultats agrégés (les prédictions par vache sont incluses car elles appartiennent à McGill).
