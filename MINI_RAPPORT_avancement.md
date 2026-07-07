# Mini-rapport d'avancement — Projet IoT bovins McGill
**Aliou Barry — UQAM — 4 juin 2026**

*Note : suivi interne, structuré selon les tâches du SOW. McGill n'attend pas de livrable à ce stade.*

---

## Objectif 1 — Appliquer et évaluer le pipeline sur les nouvelles données IoT

**Tâche 1.1 — Appliquer le pipeline aux nouvelles données accélérométriques**
- Pipeline exécuté sur les 4 corpus IceTag (Fall 2019, Summer 2019, Winter 2019, Fall 2021),
  sans modification, de façon reproductible.
- Livrables prévus : dataset traité avec alertes (produit) + note technique de
  reproductibilité (produite).
- Statut : **fait.**

**Tâche 1.2 — Comparer les alertes aux observations comportementales**
- Comparaison réalisable directement pour Summer 2019 et Winter 2019 (vaches identifiées
  par Cow_ID).
- Bloquée pour Fall 2019 et Fall 2021 : scans identifiés par couleur de collier, en attente
  de la correspondance couleur → Cow_ID de McGill.
- Livrables prévus : table de concordance + court rapport de validation.
- Statut : **en cours** (partiel, en attente McGill pour 2 corpus sur 4).

---

## Objectif 2 — Relation entre conditions environnementales et comportement locomoteur

**Tâche 2.1 — Synchroniser données environnementales et accélérométriques**
- Dataset multimodal créé pour Summer 2019 : IceTag (activité) + HOBO (température, humidité)
  alignés en bins de 15 min.
- Livrables prévus : dataset intégré (produit) + documentation de la synchronisation (produite).
- Statut : **fait pour Summer 2019**, à étendre aux autres saisons.

**Tâche 2.2 — Analyses exploratoires environnement-comportement**
- Premières analyses produites : activité vs température/THI ; comportement vs conditions
  d'exercice (taille de paddock, durée).
- Livrables prévus : visualisations (produites) + rapport exploratoire (à finaliser).
- Statut : **en cours.**

---

## Objectif 3 — Notebook de démonstration IoT
- Non commencé. Planifié pour août (semaines 10 à 12).

---

## Objectif 4 — Support technique WELL-E
- Non commencé. En attente des scripts WELL-E et du contexte de Mira (nécessaires avant le
  3 août pour tenir le calendrier).

---

## Synthèse
Avancement conforme au calendrier du SOW. Objectif 1 réalisé (Tâche 1.1) et en cours pour la
partie comportementale (Tâche 1.2, partiellement bloquée). Objectif 2 amorcé avec un premier
corpus traité. Objectifs 3 et 4 à venir selon le planning.

## En attente de McGill
1. Correspondance couleur → Cow_ID pour Fall 2019 et Fall 2021 (Tâche 1.2).
2. Scripts WELL-E + description du projet de Mira, avant le 3 août (Objectif 4).
