# Rapport final - Objectif 1
## Appliquer et évaluer le pipeline de détection de boiterie sur les nouvelles données IoT

**Auteur :** Aliou Barry (UQAM)
**Mise à jour :** 2026-06-08
**Périmètre :** Tâche 1.1 (application du pipeline) et Tâche 1.2 (concordance avec les
observations comportementales), conformément au Statement of Work.

---

## Résumé exécutif

Le pipeline initial convenu pour le projet McGill (Isolation Forest + règles métier, intervalles de 15 min) a été appliqué
aux **quatre corpus IceTag de McGill** (Tâche 1.1) : exécution réussie, reproductible, sans
modification. La comparaison des alertes avec les observations comportementales (Tâche 1.2)
montre une **concordance temporelle** (24-44 % des scans ont une alerte à ±1 jour) mais **aucune
différence comportementale robuste** une fois le confondant « expérience » contrôlé : un contraste
groupé apparent (« Idle ») s'est révélé être un artefact de Simpson. Le faible nombre de scans
alertés par expérience limite la puissance de cette comparaison.

Une analyse complémentaire (hors livrables SOW) a confronté les alertes aux scores cliniques
SLS : aucune concordance avec la boiterie clinique, parce que les cas disponibles sont légers et
que le capteur IceTag mesure la quantité de mouvement, non l'asymétrie de démarche.

---

## 1. Tâche 1.1 - Appliquer le pipeline aux nouvelles données accélérométriques

### 1.1 Données traitées (notebooks 02, 05)

| Corpus | Vaches | Intervalles 15 min | Période | Couverture moy. |
|---|---|---|---|---|
| Fall 2019 | 30 | 93 860 | nov-déc 2019 | 99.3 % |
| Summer 2019 | 18 | 139 111 | juin-sept 2019 | 98.3 % |
| Winter 2019 | 17 | 136 929 | janv-avr 2019 | 94.4 % |
| Fall 2021 | 10 | 5 131 | 30 nov-6 déc 2021 | 100 % |

### 1.2 Résultats

| Corpus | Notifications | Notif. / 100 cow-jours |
|---|---|---|
| Fall 2019 | 105 | 10.74 |
| Summer 2019 | 127 | 8.76 |
| Winter 2019 | 149 | 10.45 |
| Fall 2021 | 4 | 7.48 |

### 1.3 Vérifications de qualité
- Conversion per-minute → bins de 15 min validée (bins exactement de 15 min, continuité temporelle).
- Reproductibilité confirmée (exécutions répétées identiques sur Fall 2019).
- Paramètres du pipeline initial appliqués sans modification.

**Livrables 1.1 (conformes au SOW) :** jeux de données traités avec alertes + note technique
de reproductibilité.

---

## 2. Tâche 1.2 - Comparer les alertes aux observations comportementales

### 2.1 Données et méthode (notebook 10)

Source comportementale : `Scan_Tot_newVersion_SMN.xlsx` (fourni par McGill), qui apporte
l'identifiant vache, la couleur de collier et la date des scans. Pour chaque scan (vache, date),
on vérifie la présence d'une alerte du pipeline dans une fenêtre de ±1 jour, puis on compare la
composition comportementale des scans avec et sans alerte.

### 2.2 Concordance temporelle par expérience

| Expérience | Scans alignés | Avec alerte (±1 j) | Taux |
|---|---|---|---|
| Fall 2019 | 27 | 12 | 44 % |
| Winter 2019 | 41 | 11 | 27 % |
| Summer 2019 | 58 | 14 | 24 % |
| Fall 2021 | 270 | 1 | 0.4 % |

(396 scans alignables au total, 38 avec alerte concurrente.)

### 2.3 Comportement des scans avec vs sans alerte (analyse intra-expérience)

L'analyse est conduite **à l'intérieur de chaque expérience**, car les expériences diffèrent à
la fois par leur codage comportemental et par leur taux d'alerte (contrôle du confondant).

**Résultat : après contrôle par expérience, la composition comportementale des scans avec et
sans alerte ne diffère pas significativement** (un seul test ressort, Summer 2019 « Explo »
p = 0.017, attribuable au hasard sur l'ensemble des tests).

> ⚠️ **Point méthodologique.** Une comparaison *groupée* (toutes expériences confondues)
> suggérait à tort que les scans alertés ont plus de comportement « Idle » (p < 0.0001). C'est un
> **artefact de confusion (paradoxe de Simpson)** : Fall 2021 a un codage différent et quasiment
> aucune alerte, ce qui domine le groupe « sans alerte ». L'effet disparaît après contrôle.

### 2.4 Bilan de concordance

La concordance **temporelle** existe (24-44 % des scans de Fall 2019 / Summer 2019 / Winter 2019
ont une alerte à ±1 jour), mais elle **ne se traduit pas** par une différence comportementale
robuste, le faible nombre de scans alertés par expérience (11-14) limitant la puissance.

**Livrables 1.2 (conformes au SOW) :** table de concordance + rapport de validation
(`tache1_2_concordance/`).

### 2.5 Limites de la Tâche 1.2
- Les scans sont ponctuels (quelques jours par essai) alors que les alertes sont continues :
  peu de scans ont une alerte le même jour, ce qui limite la puissance.
- Fall 2021 : fenêtre IceTag de 7 jours → recouvrement minimal.
- La concordance mesure une coïncidence temporelle entre alerte et comportement observé, non un
  diagnostic clinique de boiterie.

---

## 3. Analyse complémentaire - confrontation aux scores cliniques SLS (hors livrables SOW)

Cette analyse ne fait pas partie des livrables de la Tâche 1.2 (qui porte sur les observations
comportementales). Elle est menée pour évaluer la portée clinique du pipeline.

- **Comparaison synchrone (Winter 2019, notebook 06) :** aucune concordance entre alertes et
  scores SLS - Mann-Whitney p = 0.65, Spearman rho = 0.03, classifieur AUC = 0.24 (≈ hasard).
- **Séparabilité (notebooks 06 et 07) :** ni les features d'activité (0/5), ni les features de
  couchage (0/7) ne séparent les vaches boiteuses des saines.
- **Analyse temporelle :** 62 % des alertes Winter 2019 se concentrent du 1 au 15 février et
  touchent 14 vaches sur 17 - profil d'événement collectif (gestion ou environnement), que le
  pipeline (analyse par vache) ne distingue pas d'une anomalie individuelle.

**Lecture :** le corpus ne contient que de la boiterie légère, qui ne modifie pas suffisamment
l'activité mesurée. La limite vient surtout du type de capteur disponible : l'IceTag mesure la
quantité de mouvement et les postures, pas l'asymétrie fine de démarche. La cohorte McGill permet
donc de tester la transférabilité technique et la portée des alertes, mais pas de prouver une
performance clinique complète de détection de boiterie.

---

## 4. Portée et applications

Le pipeline se comporte comme un **détecteur d'anomalies comportementales** : il signale des
baisses d'activité réelles (confirmé par la concordance comportementale de la Tâche 1.2). En
élevage, ce type d'outil sert au dépistage d'événements à fort changement d'activité (chaleurs,
maladies aiguës, vêlage, boiterie sévère), comme les systèmes commerciaux existants. La boiterie
légère reste hors de portée d'un capteur d'activité.

---

## 5. Recommandations
1. Boiterie légère : capteurs de symétrie de démarche ou analyse vidéo, non compteurs d'activité.
2. Validation clinique : obtenir des données capteurs synchrones avec des cas de boiterie nette.
3. Spécificité : normalisation par rapport au troupeau pour filtrer les événements collectifs.

---

## 5.1 Addendum - renforcement scientifique appliqué

Un addendum reproductible a été ajouté le 2026-07-11 pour renforcer l'interprétation de
l'Objectif 1 sans modifier la pipeline initiale livrée.

Méthode ajoutée :
- normalisation de chaque vache par rapport à la médiane contemporaine du troupeau ;
- identification des épisodes collectifs (plusieurs vaches alertées dans une fenêtre courte) ;
- reclassification des 385 alertes en niveaux de confiance A/B/C/D ;
- production de tableaux courts et exploitables pour prioriser les alertes.

Résultat synthétique :
- les 385 notifications initiales sont conservées ;
- Winter 2019 est fortement marqué par un contexte collectif : 89/149 alertes reclassées en
  `C_probable_evenement_collectif`, cohérent avec l'épisode documenté du 1 au 15 février ;
- les alertes non collectives sont désormais priorisables : A = alerte individuelle prioritaire,
  B = alerte individuelle à vérifier, C = contexte collectif, D = qualité/contexte insuffisant.

Fichiers :
- notebook : `notebooks/13_objectif1_renforcement_scientifique.ipynb` ;
- script : `run_objective1_reinforcement.py` ;
- rapport : `renforcement_scientifique/RAPPORT_renforcement_objectif1.md` ;
- tableaux : `renforcement_scientifique/objective1_reinforced_*.csv`.

Lecture scientifique : cet addendum rend l'Objectif 1 plus défendable en séparant les alertes
individuelles plausibles des alertes probablement liées à un contexte de troupeau. Il ne constitue
pas une validation clinique de boiterie : la sensibilité et la spécificité restent non mesurables
sans labels synchrones et cas cliniquement nets.

---

## 6. État des demandes à McGill
1. Mapping couleur → Cow_ID : **reçu** (`Scan_Tot_newVersion_SMN.xlsx`) → Tâche 1.2 débloquée.
2. Données Fall 2021 manquantes + statut de 3 vaches et du tag 990 : en cours (Shabnaz).
3. Scripts WELL-E : annoncés pour juillet.
4. Contexte de gestion/météo de début février 2019 : non encore reçu.

---

## 7. Livrables produits
- Notebooks : 02 (conversion), 05 (pipeline 4 saisons, Tâche 1.1), 10 (concordance, Tâche 1.2),
  13 (renforcement scientifique de l'Objectif 1).
- Notebooks complémentaires : 06 et 07 (séparabilité, hors SOW).
- Note : le notebook 03 (comparaison SLS Fall 2019 non synchrone) est conservé pour traçabilité
  mais marqué comme superseded ; sa comparaison clinique n'est pas valide.
- Fichiers de résultats pipeline (4 saisons), tables de concordance, synthèse multi-saisons,
  diagnostics avec figures, et le présent rapport.
