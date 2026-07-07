# Synthèse — Cellier et al. (2025)

**Titre:** Enhancing movement opportunity to support behavioral needs for movement-restricted
cattle through different conditions of access to exercise

**Revue:** Scientific Reports 15, 5917 (Open Access)
**DOI:** https://doi.org/10.1038/s41598-025-89891-4

**Auteurs:** Cellier M., Shepley E., Aigueperse N., Robichaud M.V., Vasseur E.

---

## Contexte

L'intensification de la production animale a augmenté le confinement intérieur des vaches,
limitant les besoins comportementaux (exploration, locomotion). L'étude examine comment
l'accès à un espace d'exercice peut atténuer ces restrictions chez les vaches en stabulation
entravée (tie-stall).

## Méthodologie

- **Sujets:** 141 vaches Holstein en lactation, logées en stabulation entravée
- **Période:** 2019–2021, sur été/hiver/automne
- **Design:** 6 essais avec différentes conditions d'accès à l'exercice :
  - Intérieur vs extérieur
  - Durée de sortie (1h vs 2h)
  - Taille de l'aire d'exercice (20 m² vs 80 m²)
  - Type de surface au sol
- **Mesures:** Nombre de pas quotidiens via pédomètres à accéléromètres (validés pour tie-stall)
- **Analyse:** Méta-analyse comparant pas quotidiens (exercice vs non-exercice) +
  modèles linéaires mixtes généralisés (GLMM) pour les effets des conditions d'exercice

## Résultats clés

| Facteur | Effet |
|---------|-------|
| Accès exercice vs pas d'accès | +300 pas/jour (+50%) |
| Extérieur vs intérieur | +167 pas/jour (+20%) |
| Grande aire (80m²) vs petite (20m²) | +146 pas/jour (+16%) |
| 2h vs 1h de sortie | +84 pas/jour (+9%) |

### Budget temps dans l'aire d'exercice
- **~68% du temps** passé en inactivité (idle)
- **~32% du temps** en activités locomotrices (exploration, comportement social)
- Les vaches tendent à retourner à l'étable plus rapidement après la 2e heure

## Points importants pour notre projet

1. **Capteurs utilisés:** Pédomètres à accéléromètres sur les pattes — même type de données
   que nous allons analyser
2. **L'article ne traite PAS** de l'impact des variables environnementales (température, humidité)
   sur le comportement → c'est exactement notre valeur ajoutée
3. **Modèles statistiques classiques** (GLMM) → opportunité d'apporter des approches ML/deep learning
4. **Classification comportementale** non abordée en détail → possibilité d'enrichir avec
   nos méthodes de classification IoT
5. **Budget temps** montre que 68% du temps est en inactivité → question intéressante :
   est-ce que les conditions environnementales influencent ce ratio ?

## Limites identifiées

- Données limitées à la stabulation entravée (tie-stall)
- Pas de croisement avec des variables environnementales
- Pas de modélisation prédictive avancée (ML)
- Pas de classification automatique fine des comportements
