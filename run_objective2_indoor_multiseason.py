#!/usr/bin/env python3
"""Objectif 2, extension : environnement INTERIEUR et activite, trois corpus.

Question posee
--------------
L'analyse principale de l'Objectif 2 porte sur Summer 2019 et les sondes
exterieures (indice THI). Elle conclut a une association positive entre les
journees, qui n'est plus concluante apres controle du jour. Cette extension
verifie si ce comportement se reproduit sur d'autres corpus.

Choix de la mesure
------------------
Seul Summer 2019 dispose de sondes exterieures. Pour comparer trois corpus, on
utilise donc la temperature INTERIEURE, seule mesure commune aux trois. Cette
analyse complete l'analyse THI exterieure, elle ne la remplace pas.

Winter 2019 est absent : ce corpus ne comporte aucune donnee environnementale.

Sorties : TABLEAUX_CSV/objective2_indoor_multiseason_*.csv
"""
from __future__ import annotations

import glob
import os
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

warnings.filterwarnings("ignore")

RACINE = Path(__file__).resolve().parent
DONNEES = RACINE / "Données completes" / "Données accelerometres"
PREDICTIONS = RACINE / "reports" / "objective1_pipeline_icetag"
# Les sorties vont dans reports/, source unique du paquet de livraison.
# make_objective2_clean_deliverables.py les copie ensuite dans TABLEAUX_CSV/.
LIVRAISON = RACINE / "reports" / "objective2_environnement"

# Les sondes de Summer sont rangees dans Inside/Outside ; celles des automnes ne
# le sont pas, mais leurs releves (autour de 11 a 13 °C en novembre au Quebec)
# correspondent a des sondes de batiment.
CORPUS = [
    ("Summer 2019", [str(DONNEES / "Summer 2019" / "Hobo" / "*" / "Inside" / "*")], "summer_2019"),
    ("Fall 2019", [str(DONNEES / "Fall 2019" / "HOBO data" / "*" / "*.xlsx")], "fall_2019"),
    (
        "Fall 2021",
        [
            str(DONNEES / "Fall 2021" / "Hobos" / "*" / "*.xlsx"),
            str(DONNEES / "Fall 2021" / "Hobos" / "*" / "*.csv"),
        ],
        "fall_2021",
    ),
]


def _lire_hobo(chemin: str) -> pd.DataFrame | None:
    """Lit un releve HOBO, quel que soit son format (entetes FR ou EN)."""
    try:
        if chemin.lower().endswith((".xlsx", ".xls")):
            brut = pd.read_excel(chemin, skiprows=1)
        else:
            brut = pd.read_csv(chemin, skiprows=1)
    except Exception:
        return None

    colonnes = {str(c): c for c in brut.columns}
    date = next((v for k, v in colonnes.items() if "Date" in k), None)
    temp = next(
        (
            v
            for k, v in colonnes.items()
            if k.startswith("Temp")
            and not any(x in k for x in ["Max", "Min", "Moy", "Éct", "StdDev", "Avg"])
        ),
        None,
    )
    if date is None or temp is None:
        return None

    sortie = pd.DataFrame(
        {
            "T": pd.to_datetime(brut[date], errors="coerce"),
            "temp": pd.to_numeric(brut[temp], errors="coerce"),
        }
    ).dropna()
    return sortie if len(sortie) else None


def charger_environnement(motifs: list[str]) -> pd.DataFrame:
    frames = [
        frame
        for motif in motifs
        for chemin in sorted(glob.glob(motif))
        if not os.path.isdir(chemin) and (frame := _lire_hobo(chemin)) is not None
    ]
    if not frames:
        return pd.DataFrame(columns=["T", "temp"])
    env = pd.concat(frames, ignore_index=True)
    env["T"] = env["T"].dt.floor("15min")
    return env.groupby("T", as_index=False).agg(temp=("temp", "mean")).sort_values("T")


def charger_activite(cle: str) -> pd.DataFrame:
    ice = pd.read_csv(
        PREDICTIONS / f"{cle}_pipeline_predictions.csv",
        usecols=["T", "Cow", "Steps_sum"],
    )
    ice["T"] = pd.to_datetime(ice["T"], errors="coerce")
    ice["Cow"] = ice["Cow"].astype(str).str.replace(r"\.0$", "", regex=True)
    return ice.dropna(subset=["T"])


def analyser(nom: str, env: pd.DataFrame, ice: pd.DataFrame) -> tuple[dict, list[dict]]:
    fusion = ice.merge(env, on="T", how="inner").dropna(subset=["temp", "Steps_sum"])
    if fusion.empty:
        return {}, []

    troupeau = (
        fusion.groupby("T", as_index=False)
        .agg(Steps=("Steps_sum", "mean"), temp=("temp", "first"))
        .sort_values("T")
    )
    troupeau["Heure"] = troupeau["T"].dt.hour
    troupeau["Jour"] = troupeau["T"].dt.strftime("%Y-%m-%d")
    jour = troupeau.groupby("Jour", as_index=False).agg(
        Steps=("Steps", "mean"), temp=("temp", "mean")
    )

    descriptif = {
        "corpus": nom,
        "intervalles_apparies": len(fusion),
        "pct_corpus_icetag": round(100 * len(fusion) / len(ice), 1),
        "vaches": fusion["Cow"].nunique(),
        "jours": fusion["T"].dt.date.nunique(),
        "temp_min": round(float(fusion["temp"].min()), 1),
        "temp_max": round(float(fusion["temp"].max()), 1),
        "temp_moy": round(float(fusion["temp"].mean()), 1),
        "debut": str(fusion["T"].min().date()),
        "fin": str(fusion["T"].max().date()),
    }

    lignes = []
    specifications = [
        ("Global, ajusté pour l'heure", "Steps ~ temp + C(Heure)", troupeau, 96,
         "Association globale, melangeant variations entre jours et intra-jour."),
        ("Intra-jour strict (jour fixe)", "Steps ~ temp + C(Heure) + C(Jour)", troupeau, 96,
         "Effet a l'interieur des journees, apres controle du jour."),
        ("Entre journées (unité jour)", "Steps ~ temp", jour, 3,
         "Comparaison des moyennes journalieres entre elles."),
    ]
    for libelle, formule, donnees, lags, lecture in specifications:
        if len(donnees) <= 3:
            continue
        ajuste = smf.ols(formule, donnees).fit(cov_type="HAC", cov_kwds={"maxlags": lags})
        bas, haut = ajuste.conf_int().loc["temp"]
        lignes.append(
            {
                "corpus": nom,
                "modele": libelle,
                "coefficient_temp": round(float(ajuste.params["temp"]), 4),
                "ic95_bas": round(float(bas), 4),
                "ic95_haut": round(float(haut), 4),
                "p": float(ajuste.pvalues["temp"]),
                "n": int(ajuste.nobs),
                "interpretation": lecture,
            }
        )
    return descriptif, lignes


def main() -> None:
    descriptifs, modeles = [], []
    for nom, motifs, cle in CORPUS:
        env = charger_environnement(motifs)
        ice = charger_activite(cle)
        descriptif, lignes = analyser(nom, env, ice)
        if descriptif:
            descriptifs.append(descriptif)
            modeles.extend(lignes)
            print(f"  {nom:14} {descriptif['intervalles_apparies']:>7} intervalles, "
                  f"{descriptif['vaches']:>2} vaches, {descriptif['jours']:>2} jours, "
                  f"{descriptif['temp_min']:.1f}-{descriptif['temp_max']:.1f} °C")

    LIVRAISON.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(descriptifs).to_csv(
        LIVRAISON / "objective2_indoor_multiseason_descriptifs.csv", index=False
    )
    pd.DataFrame(modeles).to_csv(
        LIVRAISON / "objective2_indoor_multiseason_modeles.csv", index=False
    )
    print(f"\n  Ecrit dans {LIVRAISON}")
    print(pd.DataFrame(modeles)[["corpus", "modele", "coefficient_temp", "p"]].to_string(index=False))


if __name__ == "__main__":
    main()
