# Objectif 4.2 - Guide de dépannage et FAQ WELL-E

## Le script ne trouve pas le fichier MAT ou la vidéo

Utiliser des chemins complets ou lancer la commande depuis le dossier du projet. Éviter de modifier le code. Les chemins se donnent avec `--mat`, `--video`, `--traj-csv` et `--output-dir`.

## La variable `new_cow_gs` est absente

Le fichier `.mat` n'est pas la sortie attendue de MATRID. Vérifier que le fichier transmis est bien le fichier agrégé `*_new_cow_gs.mat`, et non un fichier individuel `position_cow_*.mat`.

## Le mode sparse signale des colonnes manquantes

Vérifier que le CSV a été généré avec `--sampling sparse` et qu'il contient `BB_left`, `BB_top`, `BB_width`, `BB_height` et `time_in_min`. Ne pas réutiliser un CSV continu sous un autre mode.

## Comment saisir l'orientation sparse ?

Lancer le calcul avec `--sampling sparse --metrics orientation --sparse-orientation interactive --video VIDEO.mp4`. Cliquer dans la direction de la tête à partir du centre de la boîte, puis appuyer sur Entrée. Q ou Échap annule la session sans remplacer le fichier existant.

## Les boîtes ne coïncident pas avec la vidéo

Confirmer que la vidéo correspond au fichier MAT et qu'elle n'a pas été recadrée. Le script peut estimer un facteur d'échelle uniforme, mais un recadrage ou un changement de rapport d'image nécessite une correction explicite des coordonnées.

## La validation signale des doublons vache-frame

Deux observations portent le même identifiant et la même frame. Il faut résoudre le conflit dans les trajectoires amont; conserver arbitrairement une ligne pourrait masquer une erreur d'identité.

## Une frame dépasse la fin de la vidéo

Le MAT et la vidéo ne sont probablement pas alignés, ou la vidéo a été raccourcie. Vérifier le nombre de frames et ne pas contourner le contrôle strict avant d'avoir expliqué l'écart.

## Pourquoi la matrice de distances est-elle vide sous la diagonale ?

C'est intentionnel. Chaque paire de vaches est calculée une seule fois dans le triangle supérieur, comme dans la procédure de référence. Une matrice symétrique peut être reconstruite pour l'affichage, mais ne doit pas être confondue avec une seconde mesure.

## Les unités sont-elles des mètres, m/s et m/s² ?

Non. Sans calibration spatiale, les unités sont le pixel, le pixel/seconde et le pixel/seconde². Une conversion physique nécessite une calibration adaptée à la perspective de la caméra.

## Pourquoi générer trois fichiers d'occupation par vache ?

La heatmap JPG sert au contrôle visuel sur le fond vidéo. Le PNG normalisé sans fond facilite la comparaison visuelle. Le fichier NPY conserve les comptes bruts et doit être utilisé pour les analyses quantitatives.

## La vidéo complète est longue à produire

Générer d'abord un aperçu avec `--preview-minutes 1`. La lecture est séquentielle et seules les frames suivies sont décodées, mais la durée finale dépend de la longueur de la vidéo, du codec et du stockage.

## L'aperçu vidéo est vide

La copie nettoyée compte l'aperçu à partir de la première frame suivie. Si aucun frame n'apparaît encore, vérifier le mode d'échantillonnage, la colonne de frames et la concordance entre le CSV et la vidéo.

## Peut-on affirmer que Python reproduit exactement MATLAB ?

La revue confirme la correspondance des étapes et les tests indépendants confirment les formules principales. Le cas du 27 mars reproduit exactement les résultats de la version Python reçue. Une affirmation catégorique d'identité MATLAB/Python exige toutefois des sorties MATLAB de référence calculées sur le même fichier.

## Où est l'« identity map » de l'étape 3.7 ?

Elle n'est pas définie dans la SOP de travail et n'est pas implémentée dans le script MATLAB de référence. Le besoin doit être précisé avant d'ajouter une fonctionnalité qui n'a pas de comportement de référence.

## Que fournir pour obtenir du support sur Mira ?

Fournir le MAT agrégé, la vidéo correspondante, le mode d'échantillonnage, le FPS attendu, les identifiants valides et la commande exécutée. Joindre le message d'erreur complet et le résumé de validation, sans transmettre uniquement une capture partielle.
