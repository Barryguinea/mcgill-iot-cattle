# Proposition méthodologique — Projet IoT Vaches Laitières

## 1. Compréhension du contexte

L'article de Cellier et al. (2025) a établi l'impact de l'accès à l'exercice sur la locomotion
des vaches en stabulation entravée à l'aide de pédomètres/accéléromètres. Ce travail
a utilisé des approches statistiques classiques (GLMM) et s'est concentré sur le nombre
de pas comme indicateur principal.

**Ce que nous proposons :** Aller plus loin en croisant les données comportementales
(accéléromètres) avec les données environnementales (température, humidité) et les
observations comportementales, en utilisant des approches d'analyse de données avancées.

---

## 2. Phases du projet

### Phase 1 — Exploration et compréhension des données
- Réception et inventaire des données (expériences 2018–2023)
- Analyse exploratoire (EDA) : distributions, valeurs manquantes, temporalités
- Caractérisation des signaux accéléromètres (fréquence, axes, bruit)
- Cartographie des variables environnementales disponibles
- Alignement temporel entre sources de données (accéléromètres, capteurs environnementaux, observations)
- **Livrable :** Notebook Jupyter d'exploration + rapport de qualité des données

### Phase 2 — Prétraitement et ingénierie des features
- Nettoyage et filtrage des signaux accéléromètres
- Extraction de features temporelles et fréquentielles :
  - Domaine temporel : moyenne, écart-type, énergie, corrélation inter-axes, SMA
  - Domaine fréquentiel : FFT, puissance spectrale, entropie
  - Features statistiques par fenêtre glissante
- Agrégation des données environnementales par période
- Fusion multi-sources (capteurs + environnement + observations)
- **Livrable :** Pipeline de prétraitement reproductible

### Phase 3 — Classification comportementale
- Définition des classes comportementales avec l'équipe (en co-développement) :
  - Ex : repos, alimentation, locomotion, rumination, comportement social
- Entraînement de modèles de classification :
  - Approches classiques : Random Forest, XGBoost, SVM
  - Approches deep learning : LSTM, CNN-1D sur séries temporelles brutes
- Validation croisée adaptée aux données longitudinales (leave-one-cow-out)
- **Livrable :** Modèle de classification + métriques de performance

### Phase 4 — Analyse de l'impact environnemental
- Modélisation de la relation comportement ↔ environnement :
  - Comment température/humidité affectent la distribution des comportements ?
  - Seuils environnementaux critiques (stress thermique, etc.)
- Approches :
  - Modèles mixtes avec covariables environnementales
  - Analyse de séries temporelles multivariées
  - Modèles d'interaction (comportement × environnement × saison)
- Intégration des observations comportementales comme validation / variable additionnelle
- **Livrable :** Analyse d'impact + visualisations

### Phase 5 — Notebook interactif et transfert
- Développement du Notebook Jupyter final intégrant :
  - Chargement et visualisation des données
  - Pipeline de classification
  - Tableaux de bord d'analyse environnementale
  - Documentation pour utilisateurs non-techniques
- Formation / démonstration à l'équipe McGill
- **Livrable :** Notebook Jupyter documenté + guide utilisateur

---

## 3. Approche collaborative

Ce projet est conçu comme un **co-développement** :
- Définition des classes comportementales avec les experts terrain (Tania, Marjorie)
- Validation des résultats par les spécialistes du domaine
- Itérations régulières pour ajuster la méthodologie
- Échanges avec Tania & Marjorie pour comprendre les protocoles expérimentaux

---

## 4. Outils et technologies

| Composant | Technologie |
|-----------|-------------|
| Langage | Python |
| Analyse exploratoire | Pandas, NumPy, Matplotlib, Seaborn |
| Traitement signal | SciPy, tsfresh |
| ML classique | Scikit-learn, XGBoost |
| Deep learning | PyTorch / TensorFlow |
| Notebook | Jupyter Lab |
| Versioning | Git |

---

## 5. Prérequis / besoins

- Accès aux données brutes des accéléromètres (format, fréquence d'échantillonnage)
- Données environnementales associées (température, humidité + horodatage)
- Observations comportementales annotées (si disponibles)
- Documentation des protocoles expérimentaux (2018–2023)
- Échange initial avec Tania & Marjorie pour clarifier la structure des données
