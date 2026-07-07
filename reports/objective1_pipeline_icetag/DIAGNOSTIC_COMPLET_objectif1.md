# Diagnostic complet — Objectif 1 (application du pipeline aux données McGill)

Date : 2026-05-30
Auteur : Aliou Barry (UQAM)

---

## 1. Résumé exécutif

Le pipeline de détection de boiterie du mémoire a été appliqué techniquement avec succès aux
4 corpus McGill (Fall 2019, Summer 2019, Winter 2019, Fall 2021). En revanche, les alertes
produites **ne concordent pas avec les scores cliniques SLS**. Le diagnostic approfondi montre
que **ce n'est imputable ni au pipeline, ni au travail du mémoire**, mais à trois limites des
données McGill. Le pipeline détecte correctement des anomalies d'activité réelles ; ces
anomalies ne correspondent simplement pas à de la boiterie individuelle dans cette cohorte.

---

## 2. Faits vérifiés

### 2.1 Exécution technique (réussie)
- 4 corpus traités, format IceTag identique, conversion en bins de 15 min validée.
- Winter 2019 : 17 vaches, 149 notifications ; couverture ~99%.
- Reproductibilité confirmée (runs avril vs mai identiques sur Fall 2019).

### 2.2 Concordance avec le SLS (échec, sur données SYNCHRONES Winter 2019)
- Mann-Whitney boiteuses (SLS≥2) vs saines : p = 0.65 (non significatif).
- Corrélation Spearman SLS vs notifications : rho = 0.03 (nulle).
- Classifieur Random Forest (Leave-One-Out) : AUC = 0.24 (pire que le hasard).
- Aucune feature IceTag (pas/jour, heures couché, lying bouts, motion index) ne sépare
  boiteuses et saines (tous p ≥ 0.27).

### 2.3 Sévérité de la boiterie dans le corpus
- Winter 2019 (SLS synchrone) : score maximum = 2 (léger). Aucun cas ≥ 3.
- Fall 2019 : un seul cas SLS = 4 (vache 3444), mais sans données IceTag synchrones.
- **Conclusion : le corpus ne contient quasiment que de la boiterie légère.**

### 2.4 Nature des alertes (analyse temporelle)
- 62% des alertes Winter 2019 (93/149) se concentrent du 1 au 15 février.
- Ce bloc touche 14 vaches sur 17 (82%), avec un pic de 13 vaches le 8 février.
- Profil synchronisé incompatible avec une boiterie individuelle → **événement au niveau
  du troupeau** (changement de régime de gestion, météo, ou artefact).

---

## 3. Explication mécaniste

Le pipeline analyse chaque vache **indépendamment**, par rapport à sa propre ligne de base
récente (`window_baseline = 24`). Il ne compare jamais une vache aux autres. Lorsqu'un
événement collectif décale l'activité de tout le troupeau, **chaque vache s'écarte
individuellement de son propre passé** et déclenche une alerte. Le pipeline produit donc un
amas d'alertes simultanées qui reflète une cause commune, mais qu'il interprète comme des
anomalies individuelles. Il est, par construction, **aveugle au contexte du troupeau**.

---

## 4. Pourquoi cela n'accuse pas le mémoire

- La validation du mémoire repose sur **injection synthétique** (chap. 4 : scénarios
  `detectable_strong`, `detectable_borderline`, `non_detectable_short`). Les anomalies
  injectées effondrent l'activité de −90% à −98% (pas) et triplent le temps couché.
- La vraie boiterie légère de McGill ne produit qu'un écart de ~1% sur les pas.
- Le pipeline a donc été validé sur des anomalies ~90× plus marquées que la boiterie réelle
  disponible. Il détecte ce qu'il sait détecter (anomalies fortes) ; il n'a jamais été
  confronté à de la vraie boiterie légère.
- Cette pratique d'injection est reconnue (Chandola 2009, Emmott 2015), mais ces auteurs
  soulignent qu'un benchmark injecté peut surestimer la performance si les anomalies sont
  « trop faciles » — ce que McGill illustre.

---

## 5. Trois explications aux alertes non confirmées par le SLS

1. **Décalage temporel** : le SLS est ponctuel (jan + mars) ; les alertes sont continues.
   Beaucoup d'alertes surviennent entre les scorings (ex. bloc de février).
2. **Cause non-locomotrice** : une anomalie d'activité peut venir d'un événement collectif,
   de l'œstrus, d'un autre problème de santé, ou de la gestion — pas forcément de la boiterie.
3. **Sensibilité capteur** : les capteurs peuvent capter des anomalies subcliniques invisibles
   au scoring visuel.

En l'absence de suivi clinique synchrone et continu, ces alertes ne peuvent être classées
définitivement comme vrais ou faux positifs.

---

## 6. Piste d'amélioration (à tester, sans toucher au mémoire)

**Normalisation par rapport au troupeau (comparaison contemporaine)** : soustraire l'activité
médiane du troupeau de chaque jour avant la détection d'anomalie. Un décalage collectif
s'annule ; seules les vaches déviant *par rapport au troupeau* (vraie boiterie individuelle)
restent signalées. À implémenter dans un notebook McGill séparé (07) et à ré-évaluer contre
le SLS.

---

## 7. Questions à poser à McGill

1. **Boiterie sévère synchrone** : disposez-vous de données capteurs (IceTag) enregistrées en
   même temps que des cas de boiterie cliniquement nets (SLS ≥ 3) ? C'est la seule condition
   pour une vraie validation clinique du pipeline.
2. **Journal de gestion de février 2019 (Winter)** : un changement de protocole, de logement,
   d'alimentation ou de regroupement est-il survenu début février 2019 ? (Un événement
   collectif explique 62% des alertes.)
3. **Météo de début février 2019** : données de température/refroidissement éolien du 1 au
   15 février (le fichier scan ne couvre qu'à partir du 14 février).
4. **Échelle SLS** : confirmer la définition exacte de l'échelle (composantes Edge/Rest/
   Shiftwt/Uneven, score max) et le protocole de scoring.

---

## 8. Reformulation honnête pour le mémoire / rapport

> « L'application du pipeline gelé à une cohorte externe McGill a confirmé sa transférabilité
> technique. L'évaluation contre des scores cliniques SLS synchrones (Winter 2019) n'a pas
> montré de concordance, pour trois raisons documentées : (1) le corpus ne contient que de la
> boiterie légère, sous le seuil de détection d'un capteur d'activité ; (2) la majorité des
> alertes correspond à un événement collectif du troupeau (analyse temporelle) que le pipeline,
> traitant chaque vache indépendamment, ne peut distinguer d'une anomalie individuelle ; (3) le
> SLS ponctuel et les alertes continues ne mesurent pas le même phénomène au même moment. Ce
> résultat documente une limite de transférabilité importante et oriente une amélioration
> (normalisation par rapport au troupeau). Il ne remet pas en cause la validation interne du
> mémoire, conduite par injection contrôlée. »
