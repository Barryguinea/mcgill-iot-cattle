# Objectif 4.2 - Note technique d'application à Mira

**Statut :** procédure prête; application non exécutée faute de données Mira dans le projet au 22 juillet 2026.

## Objet

Cette note décrit comment appliquer les scripts WELL-E nettoyés à une vidéo ou à un jeu de trajectoires provenant de Mira. Elle ne présente aucun résultat Mira, car aucun fichier vidéo, fichier `*_new_cow_gs.mat`, dictionnaire d'identités ni configuration d'échantillonnage Mira n'a été reçu.

## Entrées minimales

1. Le fichier MATRID `*_new_cow_gs.mat` contenant la variable `new_cow_gs`.
2. La vidéo source correspondante, fortement recommandée pour les contrôles visuels, les orientations sparse et la vidéo annotée.
3. Le type d'échantillonnage exact : `continuous` ou `sparse`.
4. Le FPS de la vidéo si OpenCV ne peut pas le détecter.
5. La confirmation des identifiants de vaches et de la relation frame-vidéo.

## Procédure recommandée

### 1. Convertir et valider

```bash
python make_traj_csv.py \
  --mat MIRA_new_cow_gs.mat \
  --video MIRA.mp4 \
  --output-dir resultats_mira \
  --sampling continuous \
  --strict
```

Examiner le résumé de validation. Aucun doublon vache-frame, aucune boîte invalide et aucune frame au-delà de la vidéo ne doivent être signalés.

### 2. Vérifier visuellement

Ouvrir les figures `cow_trajectory_*.png`. Les boîtes doivent entourer la bonne vache, les identifiants doivent être constants et les trajectoires ne doivent pas présenter de saut impossible. Corriger les données amont si un défaut d'identité ou de suivi est visible.

### 3. Calculer les métriques

```bash
python compute_metrics.py \
  --traj-csv resultats_mira/traj_MIRA.csv \
  --video MIRA.mp4 \
  --output-dir resultats_mira \
  --sampling continuous \
  --fps 30 \
  --metrics all
```

Pour un suivi sparse, remplacer le mode et saisir les orientations avec `--sparse-orientation interactive`.

### 4. Contrôler les sorties

Vérifier la présence des orientations, des matrices de distances, des trois métriques individuelles, des trois sorties d'occupation par vache et d'un aperçu vidéo annoté. Produire d'abord un aperçu court avec `--preview-minutes 1` avant toute vidéo complète.

## Bonnes pratiques

- Conserver les fichiers reçus en lecture seule et écrire les résultats dans un nouveau dossier.
- Garder le même nom de vidéo entre le MAT, le CSV et les résultats.
- Ne pas interpréter les distances, vitesses ou accélérations en unités physiques sans calibration pixel-mètre.
- Contrôler visuellement les identités avant d'interpréter les métriques de groupe.
- Archiver la commande exécutée, la version des scripts, le FPS et le mode d'échantillonnage.
- Pour comparer deux vidéos, confirmer qu'elles ont la même résolution, le même FPS et le même protocole.

## Critères d'acceptation Mira

L'application sera considérée terminée lorsque les données Mira auront été reçues, que la validation stricte passera sans anomalie non résolue, qu'un contrôle visuel par vache sera accepté, que les métriques seront générées et qu'un membre de l'équipe confirmera la cohérence de l'aperçu vidéo annoté.

## Limite actuelle

L'absence de données Mira est une dépendance externe. Les scripts, la procédure et les critères d'acceptation sont prêts, mais la tâche « appliquer à Mira » ne peut pas être déclarée exécutée avant réception des entrées.
