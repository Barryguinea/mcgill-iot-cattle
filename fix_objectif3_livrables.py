#!/usr/bin/env python3
"""Corrections de l'audit de l'Objectif 3.

Deux défauts relevés sur un paquet par ailleurs solide :

1. Les sorties enregistrées dans le notebook affichaient le chemin absolu du
   poste de travail, /Users/... Ce chemin part chez McGill sans rien apporter.
   Le notebook affiche désormais des chemins relatifs à la racine détectée.
2. Vingt et un cadratins subsistaient dans les textes générés, contrairement à
   la règle de mise en forme du projet.

Les corrections vont dans make_objective3_deliverables.py, qui produit le
notebook, le guide, la documentation et le README. Le script est idempotent.
"""
from __future__ import annotations

from pathlib import Path

GENERATEUR = Path(__file__).resolve().parent / "make_objective3_deliverables.py"

# Les cadratins jouent trois rôles distincts : séparateur de titre, connecteur
# de relation entre deux variables, et borne d'intervalle. Chacun appelle un
# remplacement different.
REMPLACEMENTS = [
    # titres et libellés
    ("## Objectif 3 du SOW — Tâche 3.1", "## Objectif 3 du SOW, tâche 3.1"),
    ('"Profil journalier moyen — vache 2062"', '"Profil journalier moyen, vache 2062"'),
    ('"Comportements observés et THI — huit jours indépendants"',
     '"Comportements observés et THI, huit jours indépendants"'),
    ("OBJECTIF 3 — NOTEBOOK DE DÉMONSTRATION IoT", "OBJECTIF 3 - NOTEBOOK DE DÉMONSTRATION IoT"),
    ("# Documentation du notebook — Objectif 3", "# Documentation du notebook - Objectif 3"),
    # niveaux de confiance
    ('"A — prioritaire"', '"A prioritaire"'),
    ('"B — à vérifier"', '"B à vérifier"'),
    ('"C — contexte collectif"', '"C contexte collectif"'),
    # bornes d'intervalle
    ('"Léger (68–71,9)"', '"Léger (68 à 71,9)"'),
    ('"Modéré (72–79,9)"', '"Modéré (72 à 79,9)"'),
    # relations entre variables
    ("environnement–activité", "environnement-activité"),
    ("environnement–comportement", "environnement-comportement"),
    ("Environnement–comportement", "Environnement-comportement"),
    ("THI–activité", "THI-activité"),
    ("THI–comportements", "THI-comportements"),
    ("alimentation–THI", "alimentation-THI"),
]

# Les chemins absolus n'ont aucune valeur pour le lecteur et exposent
# l'arborescence du poste. On affiche le chemin relatif à la racine détectée.
CHEMINS_AVANT = '''print(f"Mode d'exécution : {CTX['mode']}")
print(f"Données de démonstration : {DATA}")
print(f"Résultats : {OUT}")'''

CHEMINS_APRES = '''print(f"Mode d'exécution : {CTX['mode']}")
print(f"Données de démonstration : {DATA.relative_to(CTX['root'])}")
print(f"Résultats : {OUT.relative_to(CTX['root'])}")'''


def main() -> None:
    source = GENERATEUR.read_text(encoding="utf-8")
    avant = source

    appliques = 0
    for ancien, nouveau in REMPLACEMENTS:
        if ancien in source:
            appliques += source.count(ancien)
            source = source.replace(ancien, nouveau)

    chemins = "déjà corrigés"
    if CHEMINS_AVANT in source:
        source = source.replace(CHEMINS_AVANT, CHEMINS_APRES)
        chemins = "corrigés"

    restants = source.count("—") + source.count("–")

    if source != avant:
        GENERATEUR.write_text(source, encoding="utf-8")

    print(f"  cadratins remplaces : {appliques}")
    print(f"  cadratins restants  : {restants}")
    print(f"  chemins absolus     : {chemins}")
    if restants:
        for numero, ligne in enumerate(source.splitlines(), 1):
            if "—" in ligne or "–" in ligne:
                print(f"     ligne {numero} : {ligne.strip()[:100]}")


if __name__ == "__main__":
    main()
