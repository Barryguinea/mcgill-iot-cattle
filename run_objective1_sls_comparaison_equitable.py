#!/usr/bin/env python3
"""Comparaison des deux pipelines sur un protocole strictement identique.

Problème traité
---------------
Le rapport de l'Objectif 1 mettait deux évaluations SLS côte à côte sans qu'elles
partagent la même référence de boiterie. La ligne « IF + règles » classait les
vaches d'après le score McGill du 15 janvier; la ligne « HYPO » d'après celui du
12 mars. Quatre vaches sur quatorze changeaient de groupe d'une lecture à
l'autre, ce qui interdisait toute comparaison.

Pourquoi le score du 12 mars
----------------------------
Le fichier « Exercise Study - SLS Scores.xlsx » contient deux séances : Baseline
au 15 janvier 2019 et Midway au 12 mars 2019. Les données IceTag de Winter 2019
commencent le 16 janvier à 15 h 15, soit APRÈS la séance de janvier. Aucune
fenêtre capteur ne précède ce score : le protocole des sept jours avant le score
n'y est pas applicable. Le 12 mars dispose lui de 54 jours de données en amont.

Ce que fait ce script
---------------------
Il applique aux deux pipelines la même cohorte (les 14 vaches évaluables), la
même référence (score du 12 mars) et la même fenêtre (7 jours avant le score),
puis écrit la comparaison et la cohorte détaillée.

Sorties, dans reports/objective1_pipeline_icetag/ :
  objective1_sls_comparaison_equitable.csv
  objective1_sls_comparaison_cohorte.csv
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
from scipy.stats import mannwhitneyu, spearmanr

RACINE = Path(__file__).resolve().parent
SORTIES = RACINE / "reports" / "objective1_pipeline_icetag"
SCORES = (
    RACINE
    / "Données completes"
    / "Données accelerometres"
    / "Winter 2019"
    / "Icetag"
    / "IceTags_Data"
    / "IceTags-issues and reports"
    / "Exercise Study - SLS Scores.xlsx"
)
COHORTE_HYPO = (
    Path.home()
    / "Desktop"
    / "Livrables_McGill_WellE"
    / "Objectif1_Pipeline_detection_boiterie"
    / "ANNEXE_pipeline_actuelle_HYPO_instabilite_hybride"
    / "TABLEAUX_CSV"
    / "pipeline_actuelle_validation_sls_cohorte.csv"
)

DATE_SCORE = pd.Timestamp("2019-03-12")
FENETRE_JOURS = 7
CRITERES = ["Edge", "Rest", "Shiftwt", "Uneven"]


def charger_scores(feuille: str) -> pd.DataFrame:
    """Le score SLS est la somme des quatre critères observés en vidéo.

    Certaines vaches ont deux vidéos notées; on retient le score le plus élevé,
    conformément à la note laissée dans le fichier McGill.
    """
    brut = pd.read_excel(SCORES, sheet_name=feuille)
    brut["SLS"] = brut[CRITERES].sum(axis=1)
    return brut.groupby("Cow", as_index=False)["SLS"].max()


def notifications_initiales(debut: pd.Timestamp, fin: pd.Timestamp) -> pd.Series:
    """Compte les alertes de la pipeline IF + règles dans la fenêtre."""
    alertes = pd.read_csv(SORTIES / "winter_2019_pipeline_alerts_only.csv")
    colonne_vache = next(c for c in alertes.columns if c.lower() == "cow")
    colonne_temps = next(c for c in alertes.columns if c.upper() == "T")
    alertes[colonne_vache] = (
        alertes[colonne_vache].astype(str).str.replace(r"\.0$", "", regex=True).astype(int)
    )
    alertes[colonne_temps] = pd.to_datetime(alertes[colonne_temps], errors="coerce")
    fenetre = alertes[(alertes[colonne_temps] >= debut) & (alertes[colonne_temps] < fin)]
    return fenetre.groupby(colonne_vache).size()


def evaluer(valeurs: pd.Series, positif: pd.Series, score: pd.Series) -> dict:
    boiteuses = valeurs[positif == 1]
    saines = valeurs[positif == 0]
    test = mannwhitneyu(boiteuses, saines, alternative="two-sided")
    correlation = spearmanr(valeurs, score)
    return {
        "n_vaches": int(len(valeurs)),
        "n_sls_ge_2": int(len(boiteuses)),
        "n_sls_lt_2": int(len(saines)),
        "moyenne_sls_ge_2": round(float(boiteuses.mean()), 3),
        "moyenne_sls_lt_2": round(float(saines.mean()), 3),
        "auc": round(float(test.statistic / (len(boiteuses) * len(saines))), 3),
        "mann_whitney_p": round(float(test.pvalue), 4),
        "spearman_rho": round(float(correlation.statistic), 3),
        "spearman_p": round(float(correlation.pvalue), 4),
    }


def main() -> None:
    mars = charger_scores("Midway - 12MAR19").rename(
        columns={"Cow": "vache", "SLS": "sls_12_mars"}
    )
    janvier = charger_scores("Baseline - 15JAN19").rename(
        columns={"Cow": "vache", "SLS": "sls_15_janvier"}
    )

    hypo = pd.read_csv(COHORTE_HYPO)[
        ["vache", "notifications_hybrides_pre7", "sls_ge_2", "traitement"]
    ]
    debut = DATE_SCORE - pd.Timedelta(days=FENETRE_JOURS)
    pre7 = notifications_initiales(debut, DATE_SCORE)

    cohorte = hypo.copy()
    cohorte["notifications_initiales_pre7"] = (
        cohorte["vache"].map(pre7).fillna(0).astype(int)
    )
    cohorte = cohorte.merge(mars, on="vache", how="left")
    cohorte = cohorte.merge(janvier, on="vache", how="left")
    cohorte = cohorte[
        [
            "vache",
            "sls_15_janvier",
            "sls_12_mars",
            "sls_ge_2",
            "traitement",
            "notifications_initiales_pre7",
            "notifications_hybrides_pre7",
        ]
    ].sort_values("vache")

    lignes = []
    for libelle, colonne in [
        ("Pipeline initiale IF + règles", "notifications_initiales_pre7"),
        ("Pipeline HYPO + instabilité + hybride", "notifications_hybrides_pre7"),
    ]:
        mesures = evaluer(
            cohorte[colonne], cohorte["sls_ge_2"], cohorte["sls_12_mars"]
        )
        lignes.append(
            {
                "pipeline": libelle,
                "reference_boiterie": "score McGill du 12 mars 2019",
                "fenetre_capteur": f"{FENETRE_JOURS} jours avant le score",
                **mesures,
            }
        )

    comparaison = pd.DataFrame(lignes)
    SORTIES.mkdir(parents=True, exist_ok=True)
    comparaison.to_csv(SORTIES / "objective1_sls_comparaison_equitable.csv", index=False)
    cohorte.to_csv(SORTIES / "objective1_sls_comparaison_cohorte.csv", index=False)

    print(f"  Cohorte : {len(cohorte)} vaches, "
          f"{int(cohorte['sls_ge_2'].sum())} avec SLS >= 2 au 12 mars")
    print(f"  Fenetre : {debut.date()} -> {DATE_SCORE.date()}\n")
    print(comparaison[
        ["pipeline", "n_vaches", "n_sls_ge_2", "auc", "mann_whitney_p", "spearman_rho"]
    ].to_string(index=False))
    print(f"\n  Ecrit dans {SORTIES}")


if __name__ == "__main__":
    main()
