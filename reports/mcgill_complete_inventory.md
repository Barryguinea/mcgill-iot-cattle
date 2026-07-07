# Inventaire Complet Des Donnees McGill

Date: 2026-04-16

## Resume

- Nombre total de fichiers inventories: 2414
- Cet inventaire couvre le dossier `Données completes` et vise a identifier les sources accelerometres, environnementales, comportementales et documentaires.
- L'objectif est de preparer la phase d'integration multi-sources du projet McGill sans repartir de zero a chaque exploration.

## Repartition Par Type De Source

- accelerometer_icetag: 2256
- behavior_aggregate: 1
- behavior_scan: 5
- documentation: 1
- environment_hobo: 151

## Repartition Par Saison / Bloc D'etude

- fall 2019: 401
- fall 2021: 49
- other: 3
- summer 2019: 873
- winter 2019: 1088

## Priorites De Travail Recommandees

- Winter 2019: meilleur point de depart pour une analyse integree, car `cow_scan_long-format_7.12.19.xlsx` contient deja comportement + environnement + mesures IceTag synchrones.
- Fall 2019: tres riche pour une integration multi-source, avec IceTag minute, HOBO et scans comportementaux, mais necessite davantage de fusion entre fichiers.
- Summer 2019: riche egalement, avec scans, THI/HOBO et tableaux IceTag avant/apres/trajets, mais structure plus heterogene.
- Fall 2021: semble surtout contenir des scans comportementaux; a confirmer si d'autres sources existent hors de ce dossier.
- Documentation: le fichier `Étapes pour nettoyer les données.docx` explicite deja plusieurs regles de nettoyage utilisees pour les analyses de l'article.

## Extrait De La Documentation De Nettoyage

Le document de nettoyage confirme deja plusieurs decisions de pretraitement importantes pour les analyses de l'article:

```text
É
tapes pour nettoyer les données : 
Pour Winter2020, on supprime les semaines 7 et 8 car elles ne sont pas complètes pou
r
 cause COVID
. Pour Summer 2021, on ne garde que la période 3 (dire initialement 3 périodes, mais problèmes techniques donc on ne garde que la dernière période)
On supprime les jours où les données ne sont pas complètes, où il manque des heures ou des minutes (si le nombre de lignes par jours est &lt; à 1440 (minutes car les enregistrements des 
icetags
 sont par minute)
Summer 2021 : 
ca
 enlève 6 
observations (=jours) sur 206 
au total (pour combien de vaches ?)
Summer 2020 : ça enlève 30 
observations sur 374 au total
Winter
 
2020 : 
ca
 enlève 101 
observations sur 1377 
au total
Fall 2019 : 
ca
 enlève 47 observations sur 998 au
 total
Summer 2019 : 
ca
 enlève 17 observations sur 759 au total
Winter 2019 : 
ca
 enlève 22 observations sur 721 au total
On supprime les weekends et les jours où les vaches ne sont pas en traitement/ne sont pas sorties
 pour diverses raisons (météo, chaleur, pb quelconque)
On considère comme 
outlier
 les jours où le nombre de pas d’une vache
 est &lt;&gt; à 3 SD de la moyenne de cette vache (voir explication dans article ch
```

## Tables A Privilegier Des Maintenant

- `Données completes/Données accelerometres/Winter 2019/cow_scan_long-format_7.12.19.xlsx`
- `Données completes/Données accelerometres/Fall 2019/Icetag/IceTags/@IceTag_Compiled_Lameness.xlsx`
- `Données completes/Données accelerometres/Fall 2019/HOBO data/.../*.xlsx`
- `Données completes/Données accelerometres/Fall 2019/Behavioral scans - Amir's lameness project.xlsx`
- `Données completes/Données accelerometres/Summer 2019/Behavioral scans - Catherine.xlsx`
- `Données completes/Données accelerometres/Summer 2019/Hobo/THI per day of observation.xlsx`
- `Données completes/Scan_Tot.xlsx`

## Prochaine Etape Conseillee

Construire une table d'integration cible par saison, en commencant par Winter 2019, car c'est la source la plus directement synchrone pour relier comportement, environnement et locomotion.
