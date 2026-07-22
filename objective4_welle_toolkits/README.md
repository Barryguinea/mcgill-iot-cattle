# Objectif 4 - Support aux outils WELL-E

## État au 22 juillet 2026

- **Tâche 4.1 terminée** : les deux scripts Python reçus ont été revus, corrigés et testés sans modifier les originaux.
- **Tâche 4.2 préparée, application en attente** : la procédure Mira et le guide de dépannage sont prêts, mais aucun jeu de données ni fichier de configuration Mira n'est présent dans le projet. Aucun résultat Mira n'est donc revendiqué.

## Contenu

- `code/make_traj_csv.py` : conversion MATRID `.mat` vers CSV, contrôles et figures de vérification.
- `code/compute_metrics.py` : orientations, distances, distance totale, vitesse, accélération, cartes d'occupation et vidéo annotée.
- `tests/test_welle_conversion.py` : tests unitaires des formules, des schémas et des modes continu/sparse.
- `tests/run_example_validation.py` : comparaison reproductible entre les scripts reçus et les scripts nettoyés sur l'exemple du 27 mars.
- `reports/` : livrables Word et sources techniques.
- `results/validation/` : résultats légers de la comparaison numérique.

Les fichiers reçus dans `UQAM - Matlab vers Python (Aliou)` restent inchangés et servent de référence d'audit.

## Exécution rapide

Environnement testé : Python 3.11 avec `numpy`, `pandas`, `scipy`, `matplotlib` et `opencv-python`.

```bash
python code/make_traj_csv.py \
  --mat INPUT_new_cow_gs.mat \
  --video INPUT.mp4 \
  --output-dir results/run \
  --sampling continuous \
  --strict

python code/compute_metrics.py \
  --traj-csv results/run/traj_INPUT.csv \
  --video INPUT.mp4 \
  --output-dir results/run \
  --sampling continuous \
  --fps 30 \
  --metrics all
```

Pour le mode sparse, utiliser `--sampling sparse`. La saisie d'orientation manuelle se lance avec `--sparse-orientation interactive`.

## Limite de validation

La comparaison sur l'exemple du 27 mars démontre une identité numérique avec la version Python reçue pour la conversion, la matrice de distances, la distance totale, la vitesse moyenne et l'accélération moyenne. La correspondance fonctionnelle avec le script MATLAB a été revue ligne par ligne. Une équivalence noire-boîte MATLAB/Python complète nécessite toutefois des sorties MATLAB de référence produites sur le même fichier, qui n'ont pas été fournies.
