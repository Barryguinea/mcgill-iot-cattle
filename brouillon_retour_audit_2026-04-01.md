# Brouillon — Retour d'audit initial a Elsa, Tania et Marjorie

**À :** Elsa Vasseur  
**Cc :** Tania Wolfe, Abdoulaye Diallo, Marjorie Cellier

---

Bonjour Elsa,

Comme convenu, j'ai pris le temps de parcourir l'article de Marjorie ainsi que les donnees qui m'ont ete transmises.

A ce stade, mon premier retour est le suivant.

Les donnees actuellement disponibles correspondent bien au socle de l'article de reference et comprennent 6 fichiers CSV, soit les 6 experiences du papier. Au total, cela represente 2214 lignes. En fusionnant les fichiers, on observe 90 identifiants `Cow_ID` uniques dans les CSV actuellement disponibles, ce qui n'est pas directement equivalent a l'effectif global rapporte dans l'article. Les variables disponibles permettent deja une premiere lecture descriptive centree sur `Sum_Steps`, ce qui fournit une bonne base pour demarrer un audit methodique des donnees et envisager une reproduction initiale des resultats publies.

J'observe cependant que les 6 fichiers ne partagent pas exactement le meme schema. Certaines colonnes ne sont presentes que dans certains essais (`Period`, `Week_Period`, `Duration_per_day`, `Size`) et le codage des traitements varie selon les jeux de donnees (`Trt`, `Trt_details`). J'ai aussi releve quelques doublons exacts dans certains fichiers, qu'il faudra valider avec vous avant toute decision de nettoyage. Autrement dit, la premiere etape logique n'est pas encore une modelisation avancee, mais une harmonisation rigoureuse des tables et une clarification du dictionnaire des variables.

Les premiers contrastes descriptifs que j'obtiens sont coherents avec la logique de l'article, avec davantage de pas dans les conditions d'exercice que dans la condition stall, ce qui est encourageant pour la suite. En revanche, les donnees que j'ai pour l'instant restent principalement agregees autour de `Sum_Steps`. Pour aller vers l'objectif central du projet, c'est-a-dire integrer les variables environnementales et les observations comportementales, il faudra confirmer la disponibilite, la granularite temporelle et la qualite de ces autres sources.

Compte tenu de cela, la progression que je recommande est la suivante:

1. harmoniser les 6 jeux de donnees experimentaux actuellement disponibles
2. reproduire proprement les resultats descriptifs et analytiques de base de l'article
3. clarifier avec Tania et Marjorie la structure exacte des variables, les protocoles experimentaux et la disponibilite des donnees environnementales et observationnelles
4. a partir de cette base, formaliser une offre de service avec une methodologie detaillee, progressive et realiste

Ce cadrage s'inscrit bien dans la continuite de mes travaux actuels sur les donnees IoT bovines. Le projet McGill ne me semble pas etre une simple repetition de mon memoire, mais plutot une extension naturelle: mon experience en structuration de donnees capteurs, en validation methodologique et en mise en place de pipelines reproductibles peut servir de socle robuste pour cette nouvelle question scientifique plus contextuelle et multi-source.

Je serais donc tres favorable a un echange avec Tania et Marjorie afin de discuter plus precisement:

- de la signification exacte de certaines variables selon les essais
- de la disponibilite des donnees de temperature et d'humidite
- de l'existence d'observations comportementales annotées et alignables
- et, si elles existent, de donnees accelerometres plus fines que les tables agregees actuelles

De mon cote, j'ai deja prepare un notebook d'audit initial qui me servira de base pour la suite du travail et pour la construction de l'offre methodologique.

Si cela vous convient, je peux vous envoyer dans un second temps une proposition de methodologie structuree en phases, appuyee sur cet audit preliminaire.

Cordialement,  
Aliou Barry
