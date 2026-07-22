# -*- coding: utf-8 -*-
"""Construit le livrable trimodal Summer 2019 au niveau vache-jour-scan."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
DELIVERY_ROOT = SCRIPT_DIR.parent
if (DELIVERY_ROOT / "DONNEES_SYNCHRONISEES").is_dir():
    DATA_DIR = DELIVERY_ROOT / "DONNEES_SYNCHRONISEES"
    SUMMARY_DIR = DELIVERY_ROOT / "TABLEAUX_CSV"
else:
    DATA_DIR = SCRIPT_DIR / "reports" / "objective2_environnement"
    SUMMARY_DIR = DATA_DIR / "mixed_model"

ACTIVITY_ENV = DATA_DIR / "summer2019_icetag_environnement_15min.csv"
BEHAVIOR_ENV = DATA_DIR / "summer2019_comportement_environnement.csv"
OUT_TRIMODAL = DATA_DIR / "summer2019_multimodal_cow_day.csv"
OUT_UNMATCHED = DATA_DIR / "summer2019_multimodal_unmatched_scans.csv"
OUT_SUMMARY = SUMMARY_DIR / "objective2_trimodal_summary.csv"


def _normalize_cow(series: pd.Series) -> pd.Series:
    return series.astype(str).str.replace(r"\.0$", "", regex=True)


def run() -> None:
    activity = pd.read_csv(ACTIVITY_ENV)
    behavior = pd.read_csv(BEHAVIOR_ENV)

    activity["Cow"] = _normalize_cow(activity["Cow"])
    activity["Start"] = pd.to_datetime(activity["Start"], errors="coerce")
    activity["jour"] = activity["Start"].dt.normalize()
    behavior["Cow"] = _normalize_cow(behavior["Cow"])
    behavior["jour"] = pd.to_datetime(behavior["jour"], errors="coerce").dt.normalize()

    if "lying_h" not in activity.columns:
        activity["lying_h"] = (
            pd.to_timedelta(activity["Lying Time"], errors="coerce")
            .dt.total_seconds()
            .div(3600)
        )

    numeric_columns = [
        "Steps",
        "Motion Index",
        "lying_h",
        "Transitions",
        "temp",
        "rh",
        "THI",
    ]
    for column in numeric_columns:
        activity[column] = pd.to_numeric(activity[column], errors="coerce")

    daily = (
        activity.groupby(["Cow", "jour"], as_index=False)
        .agg(
            activite_debut=("Start", "min"),
            activite_fin=("Start", "max"),
            n_intervalles_15min=("Steps", "size"),
            pas_total_jour=("Steps", "sum"),
            pas_moyens_15min=("Steps", "mean"),
            motion_index_moyen=("Motion Index", "mean"),
            heures_couchees=("lying_h", "sum"),
            transitions_total=("Transitions", "sum"),
            temperature_moyenne=("temp", "mean"),
            humidite_moyenne=("rh", "mean"),
            THI_moyen=("THI", "mean"),
            THI_min=("THI", "min"),
            THI_max=("THI", "max"),
        )
        .sort_values(["jour", "Cow"])
    )

    behavior = behavior.reset_index(drop=True).copy()
    behavior.insert(
        0,
        "scan_id",
        [f"SUM2019_SCAN_{index:03d}" for index in range(1, len(behavior) + 1)],
    )
    merged = behavior.merge(daily, on=["Cow", "jour"], how="left", indicator=True)
    merged["statut_integration"] = np.where(
        merged["_merge"].eq("both"),
        "complet",
        "activité IceTag absente pour cette vache et ce jour",
    )
    merged = merged.drop(columns="_merge")

    numeric_output = [
        "pas_total_jour",
        "pas_moyens_15min",
        "motion_index_moyen",
        "heures_couchees",
        "transitions_total",
        "temperature_moyenne",
        "humidite_moyenne",
        "THI_moyen",
        "THI_min",
        "THI_max",
    ]
    merged[numeric_output] = merged[numeric_output].round(3)
    merged.to_csv(OUT_TRIMODAL, index=False)

    unmatched = merged[merged["statut_integration"] != "complet"].copy()
    unmatched.to_csv(OUT_UNMATCHED, index=False)

    OUT_SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    summary = pd.DataFrame(
        [
            {"indicateur": "scans_comportementaux_total", "valeur": len(merged)},
            {
                "indicateur": "scans_trimodaux_complets",
                "valeur": int((merged["statut_integration"] == "complet").sum()),
            },
            {"indicateur": "scans_sans_activite", "valeur": len(unmatched)},
            {"indicateur": "vaches_observees", "valeur": behavior["Cow"].nunique()},
            {"indicateur": "jours_de_scan", "valeur": behavior["jour"].nunique()},
        ]
    )
    summary.to_csv(OUT_SUMMARY, index=False)

    print("Table trimodale :", OUT_TRIMODAL)
    print(summary.to_string(index=False))
    if len(unmatched):
        print("\nScans sans activité correspondante :")
        print(unmatched[["scan_id", "Cow", "jour", "statut_integration"]].to_string(index=False))


if __name__ == "__main__":
    run()
