# Rapport court de validation - Objectif 1.2

Objet: comparer les alertes produites avec les observations comportementales disponibles.

## Concordance temporelle
Les fichiers contiennent 396 scans datés. Un scan est considéré comme comparable seulement si la même vache dispose de données IceTag dans une fenêtre de ±1 jour. Cette vérification laisse 133 scans réellement couverts.

| Expérience | Scans couverts IceTag (±1 j) | Avec alerte (±1 j) | Taux descriptif |
|---|---:|---:|---:|
| Winter 2019 | 41 | 11 | 26.8% |
| Summer 2019 | 55 | 14 | 25.5% |
| Fall 2019 | 27 | 12 | 44.4% |
| Fall 2021 | 10 | 1 | 10.0% |
| **Total** | **133** | **38** | **28.6%** |

## Contrôle du niveau attendu
Dans l'analyse de sensibilité limitée aux 127 scans couverts le jour même, 38 concordances sont observées (29.9%), contre 35.31 attendues (27.8%) d'après la fréquence d'alerte propre à chaque vache. L'écart est de +2.1 points et n'est pas statistiquement concluant (test unilatéral de Poisson-binomial, p = 0.324).

## Interprétation
Les taux décrivent une proximité temporelle entre certains scans et certaines alertes. Ils ne démontrent pas un enrichissement au-delà de ce qui est attendu compte tenu de la fréquence des alertes, et ne constituent ni une sensibilité, ni une spécificité, ni une validation clinique. Le faible dénominateur de Fall 2021 (10 scans couverts) impose une prudence particulière.

## Concordance exploratoire avec les scores SLS
Les deux pipelines sont comparées sur un protocole strictement identique : les mêmes 14 vaches de Winter 2019, le score McGill du 12 mars 2019 comme référence, et les notifications produites dans les sept jours précédant ce score.

| Pipeline | Cohorte | AUC | Mann-Whitney p | Spearman rho |
|---|---|---:|---:|---:|
| Initiale IF + règles | 14 vaches, 3 avec SLS >= 2 | 0,576 | 0,695 | 0,241 |
| HYPO + instabilité + hybride | 14 vaches, 3 avec SLS >= 2 | 0,924 | 0,031 | 0,504 |

Le fichier McGill contient deux séances de notation : une au 15 janvier 2019 et une au 12 mars 2019. Les données IceTag de Winter 2019 débutent le 16 janvier, soit après la première séance : aucune fenêtre capteur ne précède le score de janvier, alors que 54 jours de données précèdent celui du 12 mars. La comparaison retient donc le score du 12 mars, seul compatible avec un protocole de détection.

Lecture antérieure conservée pour mémoire : un premier diagnostic comparait le nombre d'alertes de toute la saison au score du 15 janvier, sur 16 vaches dont 5 avec SLS >= 2, et ne trouvait aucune concordance (p = 0,649; rho = 0,033). Cette lecture répond à une question de persistance et non de détection : trois des cinq vaches boiteuses en janvier ne l'étaient plus au 12 mars. Elle n'est pas comparable au tableau ci-dessus.

Avec trois cas positifs seulement et un traitement Exercise confondu avec le statut SLS, ces résultats ne permettent aucune estimation clinique de sensibilité ou de spécificité.

Sources : reports/objective1_sls_comparaison_equitable.csv et objective1_sls_comparaison_cohorte.csv, livrés dans ANNEXE_pipeline_actuelle_HYPO_instabilite_hybride/TABLEAUX_CSV/.

## Conclusion
La comparaison documente une cohérence temporelle descriptive entre certaines alertes et les observations disponibles, sans enrichissement statistiquement démontré par rapport au niveau attendu. Les SLS ajoutent une validation observationnelle exploratoire limitée, mais ne permettent pas de calculer une sensibilité ou une spécificité robuste.
