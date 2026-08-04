# Documentation du notebook - Objectif 3

## Livrables SOW

- Notebook final : `code/12_objectif3_notebook_demonstration.ipynb`
- Documentation : `RAPPORTS/Objectif3_guide_utilisation.docx` et ce fichier
- Support de présentation additionnel : `RAPPORTS/Objectif3_presentation_detaillee.pptx`

## Exécution

1. Ouvrir le notebook dans Jupyter.
2. Vérifier que le noyau Python possède pandas, numpy, matplotlib, scipy et scikit-learn.
3. Choisir **Restart Kernel and Run All**.
4. Vérifier le message final « Toutes les sorties attendues ont été générées ».

Le notebook détecte automatiquement s'il est exécuté depuis le dépôt ou depuis le paquet
de livraison. Le paquet contient un échantillon IceTag, les tables nécessaires, les modules
du pipeline et les paramètres gelés.

## Résultats attendus

- 8 922 intervalles pour la vache 2062;
- 582 points atypiques Isolation Forest;
- 17 alertes brutes après règles métier;
- 385 alertes brutes dans les quatre saisons, requalifiées en 37 A, 195 B et 153 C;
- association THI-activité globale positive, mais effet intra-jour non concluant;
- huit jours indépendants pour l'analyse comportementale.

## Interprétation

Une alerte signale une anomalie comportementale à vérifier. Elle ne constitue ni un
diagnostic de boiterie ni une preuve causale d'un effet thermique. Les résultats THI et
comportement restent exploratoires.
