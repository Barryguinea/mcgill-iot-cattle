# Cadrage - Renforcement scientifique de l'Objectif 2

**Projet :** Well-E (IoT vaches laitières, UQAM x McGill)
**Auteur :** Aliou Barry
**Objet :** Passer l'Objectif 2 (environnement x comportement) d'un résultat « suggestif » à un résultat défendable.
**Statut :** proposition de plan, à valider avec McGill avant exécution.

---

## 1. Point de départ (état actuel)

L'analyse comportement x THI de l'Objectif 2 repose sur **Summer 2019 uniquement**, avec **51 scans sur 8 jours** : la puissance est faible et les conclusions sont, à juste titre, qualifiées de **suggestives**. L'analyse activité (pas) x THI, elle, s'appuie sur ~51 000 intervalles de 15 min et donne un effet faible mais robuste (rho ~0,10).

**But :** augmenter la puissance et la portée sans surinterpréter, en exploitant une deuxième saison et un modèle statistique adapté.

## 2. Constats vérifiés sur les données

- **Winter 2019** (`cow_scan_long-format_7.12.19.xlsx`) : une seule table déjà synchronisée (environnement + comportement + IceTag), **42 observations, 7 jours, 8 vaches**, 14 fév - 5 avr 2019. Variable thermique pertinente : **le froid** (température, windchill, humidité), pas le THI.
- **Summer 2019** : comportement dans un fichier brut hétérogène (feuilles par semaine, feuilles « don't use it »), THI dans des fichiers HOBO séparés. Déjà partiellement traité par les notebooks 08/09/11. Variable thermique : **la chaleur** (THI).
- **Éthogrammes différents** entre saisons. Codes Winter (SI, SR, EG, EXI...) vs Summer (IM, IRu, EAT, EXPL...). Seuls **W** et **EW** sont communs à la lettre ; les autres comportements existent dans les deux mais sous des codes distincts.

## 3. Deux options

**Option A (recommandée) - Analyses parallèles par saison.**
Modéliser chaque saison séparément avec la même méthode, puis comparer : « en été, la chaleur (THI) est liée au comportement X ; en hiver, le froid (windchill) est lié à Y ». On ne rapproche que les catégories **clairement communes** (manger, marcher, debout inactif, couché).
*Avantages :* évite le risque d'un mauvais appariement d'éthogramme ; deux saisons ; vrais modèles ; résultat honnête.

**Option B - Fusion complète multi-saisons.**
Construire une table de correspondance (crosswalk) complète Summer <-> Winter et empiler les données.
*Avantages :* un seul modèle, plus de puissance. *Risque :* un crosswalk erroné introduit des **erreurs silencieuses** ; à ne faire qu'avec validation McGill.

## 4. Plan méthodologique (commun aux deux options)

1. **Modèle à effets mixtes (LMM/GLMM)** : variable thermique en effet fixe ; **vache** et **jour** (et **saison** en Option B) en effets aléatoires. Exploite toutes les observations sans réduire à 8 points, tout en respectant la structure hiérarchique (corrige la pseudo-réplication).
2. **Non-linéarité / seuil** : tester un point de rupture thermique (modèle segmenté ou GAM), le stress n'étant pas linéaire.
3. **Effets décalés (lags)** : tester la charge thermique de la veille et le cumul de jours extrêmes.
4. **Covariables** : moment de la journée, stade de lactation, parité, ligne de base individuelle.
5. **Rapporter les tailles d'effet et intervalles de confiance**, pas seulement les p-values.
6. **Borne de portée** : le stress sévère (THI >= 80) est rare au Québec ; conclusions limitées à la plage observée.

## 5. Crosswalk d'éthogramme (si Option B, ou pour les catégories communes de l'Option A)

Établir une table Summer -> Winter comportement par comportement, en s'appuyant sur les légendes (`Code used` de Summer, `references` de Winter). Catégories cœur, a priori sans ambiguïté :
manger, marcher, debout inactif, debout ruminant, explorer, couché.
**Cette table doit être validée par McGill** (voir section 7).

## 6. Effort estimé

| Option | Effort (avec IA) | Sans IA |
|---|---|---|
| A - Winter seul (modèle mixte froid x comportement) | 2-3 jours | ~1 semaine |
| A - Summer + Winter en parallèle | ~1 semaine | ~1,5-2 semaines |
| B - Fusion complète (crosswalk validé) | ~1,5-2,5 semaines | ~3 semaines |

## 7. Questions à valider avec McGill (avant de commencer)

1. **Périmètre attendu** de l'Objectif 2 : Summer 2019 suffit-il, ou une analyse multi-saisons est-elle souhaitée ?
2. **Validation de l'éthogramme** : confirmer la correspondance Summer <-> Winter (Marjorie / Catherine).
3. **Comparabilité des contextes** : le comportement Winter est mesuré pendant des séances d'exercice de 1-2 h ; est-ce comparable au protocole Summer ?
4. **Extension éventuelle à Fall 2019** (riche mais nécessitant une fusion de fichiers) : pertinent ou hors périmètre ?

## 8. Recommandation

Commencer par **l'Option A sur Winter 2019 seul** (données déjà synchronisées) : un **modèle mixte froid x comportement** est un gain rapide et sûr, qui montre déjà un cadre méthodologique solide. Décider ensuite de l'extension (Summer en parallèle, puis éventuellement fusion) **en fonction du retour de McGill** sur le périmètre et l'éthogramme.

---

*Note : ce document est un plan. Aucune donnée brute McGill n'y figure. Les données brutes restent confidentielles et non versionnées.*
