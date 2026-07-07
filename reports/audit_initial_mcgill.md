# Audit des donnees — Projet McGill IoT Cattle

**Date**: 2 avril 2026
**Auteur**: Aliou Barry (UQAM)

## Resume

Le depot contient 6 fichiers CSV correspondant aux 6 essais de l'article Cellier et al. (2025):
- **2214 observations** au total
- **90 vaches uniques** (article: 141 — ecart a clarifier)
- **110 presences-vache** (somme des identifiants distincts par essai)
- Certaines vaches participent a plusieurs essais

Les donnees sont agregees autour de `Sum_Steps` (pas par jour). Aucun signal brut n'est disponible dans ce depot.

## 1. Structure des fichiers

| Essai | Lignes | Vaches | Semaines | Sum_Steps (moy) | Min | Max |
|---|---|---|---|---|---|---|
| Summer2019 | 506 | 15 | 8 | 910.8 | 123 | 2471 |
| Fall2019 | 708 | 30 | 5 | 666.7 | 6 | 2510 |
| Winter2019 | 410 | 14 | 8 | 682.2 | 45 | 2049 |
| Summer2020 | 243 | 18 | 3 | 1048.7 | 293 | 3268 |
| Winter2020 | 286 | 27 | 6 | 729.6 | 155 | 1989 |
| Summer2021 | 61 | 6 | 3 | 873.4 | 131 | 1882 |

## 2. Heterogeneite des schemas

Les 6 fichiers ne partagent pas le meme schema:
- `Fall2019`: pas de `Trt_details` ni `Trt_order`, double colonne `Block`/`Block.1`
- `Size` et `Duration_per_day`: seulement Summer2019 et Winter2019
- `Period`: seulement dans les essais 2020-2021
- `Week_Period`: seulement Winter2020
- `Trt` et `Trt_details` changent de semantique entre essais

## 3. Codage des traitements (non homogene)

- **Summer/Winter 2019**: `Trt` = Exercise/No_Exercise, `Trt_details` = Outdoor
- **Fall2019**: `Trt` = Outdoor/Stall, pas de Trt_details
- **Summer/Winter 2020**: `Trt` = Exercise/No_Exercise, `Trt_details` = Indoor/Outdoor/Stall
- **Summer2021**: `Trt` = Outdoor, `Trt_details` = Alternatif/Conventionnel/Stall

## 4. Design experimental

- **Summer/Winter 2019**: latin square avec Size (20-80 m2) x Duration (1-2h)
- **Winter 2020**: crossover 2 periodes (I-O, O-I, I-S, S-I)
- **Summer 2020**: crossover 3 periodes (O-I-S, I-S-O, S-O-I)
- **Summer 2021**: crossover 3 periodes (A-C-S, C-A-S, S-A-C)
- **Fall 2019**: design different? Pas de Trt_order

## 5. Qualite des donnees

- **0 valeur manquante** dans les CSV
- **13 doublons exacts**: Fall2019 (9), Winter2019 (3), Summer2020 (1)
- Quelques valeurs extremes basses (Sum_Steps = 6 dans Fall2019)
- Desequilibre variable du nombre d'observations par vache

## 6. Coherence avec l'article

Les contrastes descriptifs sont coherents:
- Exercise: ~944 pas/jour vs Stall: ~612 pas/jour (+54%)
- Outdoor > Indoor > Stall (952 > 899 > 612)
- Effet visible de Size et Duration dans les essais 2019

## 7. Questions pour Tania et Marjorie

### Donnees manquantes
1. 90 vaches dans les CSV vs 141 dans l'article — ou sont les 51 manquantes?
2. Chaque ligne = un jour d'observation?
3. Criteres d'exclusion appliques?

### Structure des variables
4. Pourquoi Fall2019 est-il structure differemment?
5. Summer2021: que signifient "Alternatif" et "Conventionnel"?
6. Size = 2.6 et 2.9 dans Summer2021: surface de la stall?
7. Week = semaine experimentale ou calendaire?

### Design experimental
8. Latin square complet pour les essais 2019?
9. Duree de chaque periode dans les crossovers 2020-2021?
10. Periode de washout entre traitements?
11. Criteres d'appariement des Block?

### Doublons et valeurs extremes
12. Les 13 doublons exacts sont-ils normaux?
13. Les Sum_Steps tres bas (ex: 6) representent-ils un capteur non porte?

### Donnees complementaires
14. Donnees environnementales: frequence et format?
15. Observations comportementales: ethogramme code? Video?
16. Signaux accelerometres bruts (IceTag 1-min) disponibles?
17. Autres variables reponses mesurees?

### Objectifs
18. Objectif explicatif ou predictif?
19. Public cible du notebook?
20. Quelles decouvertes nouvelles espere l'equipe?

## Notebook associe

`notebooks/01_audit_donnees_mcgill.ipynb` — contient toutes les analyses, visualisations et tables de cet audit.
