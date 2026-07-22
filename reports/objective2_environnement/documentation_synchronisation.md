# Documentation de la synchronisation - Objectif 2, Tâche 2.1

## Sources et résolution

- Activité locomotrice : accéléromètres IceTag, agrégés en intervalles de 15 minutes.
- Environnement : sondes HOBO **extérieures** (`Outside`), température et humidité.
- Comportements : scans d'observation datés, interprétés au niveau du jour.

Les deux sondes HOBO extérieures disponibles pour chaque période sont concaténées puis agrégées par intervalle de 15 minutes. Le THI est calculé à partir de la température et de l'humidité. L'environnement est commun au troupeau et est joint à chaque vache par timestamp.

## Tables livrées

1. `summer2019_icetag_environnement_15min.csv` : activité + environnement, au niveau vache-15 minutes.
2. `summer2019_comportement_environnement.csv` : comportements + environnement journalier.
3. `summer2019_multimodal_cow_day.csv` : table trimodale au niveau vache-jour-scan.

La table trimodale conserve les 51 scans. Quarante-neuf disposent des trois modalités. Deux scans de la vache 5169, datés du 16 et du 23 août 2019, sont conservés avec le statut `activité IceTag absente pour cette vache et ce jour`.

## Contrôles de qualité

- 87 501 intervalles vache-15 minutes, 17 vaches et 62 jours.
- 51 scans comportementaux, 8 vaches et 8 jours.
- 49 scans trimodaux complets; 2 scans incomplets documentés.
- Le comportement n'a pas une résolution de 15 minutes : aucune interpolation artificielle n'est effectuée.
- La période du 2 au 9 août ne comporte pas de fichiers HOBO `Outside`; seules les périodes réellement disponibles sont utilisées.

## Périmètre de l'analyse (écart avec l'Objectif 1)

Le corpus Summer 2019 traité à l'Objectif 1 compte **139 111 intervalles et 18 vaches** (5 juin au 6 septembre 2019).
Les sondes environnementales HOBO ne couvrent la période qu'**à partir du 1er juillet 2019**. L'analyse
environnement-activité porte donc sur le **sous-ensemble apparié** :

| | Objectif 1 (corpus complet) | Objectif 2 (apparié environnement) |
|---|---|---|
| Intervalles 15 min | 139 111 | 87 501 (62,9 %) |
| Vaches | 18 | 17 |
| Période | 5 juin - 6 sept 2019 | 1er juillet - 6 sept 2019 |

La vache 2067 est absente du sous-ensemble, faute de mesure environnementale concomitante.
Cet écart est **attendu** et ne traduit pas une perte de données : il reflète la couverture des sondes HOBO.
