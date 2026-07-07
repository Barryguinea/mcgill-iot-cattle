#!/usr/bin/env python3
"""
Construire le jeu Winter 2019 synchrone exploitable pour le projet McGill.

Source:
  Données completes/Données accelerometres/Winter 2019/cow_scan_long-format_7.12.19.xlsx

Sorties:
  reports/winter2019_sync_enriched.csv
  reports/winter2019_sync_by_cow.csv
  reports/winter2019_sync_by_context.csv
  reports/winter2019_sync_correlations.csv
  reports/winter2019_sync_report.txt
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
WINTER_XLSX = (
    ROOT
    / "Données completes"
    / "Données accelerometres"
    / "Winter 2019"
    / "cow_scan_long-format_7.12.19.xlsx"
)
REPORTS_DIR = ROOT / "reports"


SCAN_CATEGORY_MAP = {
    "Scan_SI": "immobile",
    "Scan_SR": "rumination",
    "Scan_SA": "immobile",
    "Scan_SW": "immobile",
    "Scan_SWR": "rumination",
    "Scan_PMH": "active_mobile",
    "Scan_SP": "active_immobile",
    "Scan_SN": "active_mobile",
    "Scan_W": "active_mobile",
    "Scan_EXI": "active_immobile",
    "Scan_EXW": "active_mobile",
    "Scan_SG": "active_immobile",
    "Scan_AG": "active_immobile",
    "Scan_ES": "active_immobile",
    "Scan_EW": "active_immobile",
    "Scan_KW": "active_immobile",
    "Scan_LD": "immobile",
    "Scan_EG": "active_immobile",
    "Scan_OT": "other",
}

CATEGORY_WEIGHTS = {
    "active_mobile": 1.0,
    "active_immobile": 0.5,
    "rumination": 0.25,
    "immobile": 0.0,
    "other": 0.0,
}


def load_source() -> pd.DataFrame:
    df = pd.read_excel(WINTER_XLSX, sheet_name="all scans FINAL")
    df["Date"] = pd.to_datetime(df["Date"])
    return df


def add_behavior_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    for cat in sorted(set(SCAN_CATEGORY_MAP.values())):
        cols = [c for c, mapped in SCAN_CATEGORY_MAP.items() if mapped == cat]
        df[f"count_{cat}"] = df[cols].sum(axis=1)

    category_cols = [f"count_{cat}" for cat in sorted(set(SCAN_CATEGORY_MAP.values()))]
    df["total_scans"] = df[category_cols].sum(axis=1)

    for cat in sorted(set(SCAN_CATEGORY_MAP.values())):
        df[f"pct_{cat}"] = np.where(
            df["total_scans"] > 0,
            df[f"count_{cat}"] / df["total_scans"],
            np.nan,
        )

    weighted_sum = sum(df[f"count_{cat}"] * weight for cat, weight in CATEGORY_WEIGHTS.items())
    df["behavior_activity_score"] = np.where(
        df["total_scans"] > 0,
        weighted_sum / df["total_scans"],
        np.nan,
    )

    return df


def add_icetag_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["icetag_steps_session_total"] = np.where(
        df["Treatment_hour"] == 1,
        df["Icetag_steps_per_treatment_hour1"],
        df["Icetag_steps_2hours_total"],
    )

    df["icetag_steps_per_hour_norm"] = np.where(
        df["Treatment_hour"] == 1,
        df["Icetag_steps_per_treatment_hour1"],
        df["Icetag_steps_2hours_total"] / df["Treatment_hour"],
    )
    return df


def build_summaries(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    by_cow = df.groupby("Cow_ID").agg(
        n_obs=("Cow_ID", "size"),
        mean_steps_per_hour=("icetag_steps_per_hour_norm", "mean"),
        mean_behavior_score=("behavior_activity_score", "mean"),
        mean_pct_active_mobile=("pct_active_mobile", "mean"),
        mean_pct_immobile=("pct_immobile", "mean"),
        mean_distance_index=("Distance_index_per_treatment_hour", "mean"),
    ).sort_values("mean_steps_per_hour", ascending=False)

    by_context = df.groupby(
        ["Treatment_hour", "Treatment_pad_size(m2)", "Weather_conditions"]
    ).agg(
        n_obs=("Cow_ID", "size"),
        mean_steps_per_hour=("icetag_steps_per_hour_norm", "mean"),
        mean_behavior_score=("behavior_activity_score", "mean"),
        mean_pct_active_mobile=("pct_active_mobile", "mean"),
        mean_pct_immobile=("pct_immobile", "mean"),
    ).reset_index().sort_values(["Treatment_hour", "Treatment_pad_size(m2)", "Weather_conditions"])

    corr_cols = [
        "icetag_steps_per_hour_norm",
        "icetag_steps_session_total",
        "count_active_mobile",
        "count_active_immobile",
        "count_rumination",
        "count_immobile",
        "pct_active_mobile",
        "pct_active_immobile",
        "pct_rumination",
        "pct_immobile",
        "behavior_activity_score",
        "Distance_index_per_treatment_hour",
        "Treatment_hour",
        "Treatment_pad_size(m2)",
        "Temp_7:15am_(C)",
        "Gov_CAN_Temp_10am_(C)",
        "Gov_CAN_rel_humidity_10am_(%)",
    ]
    corr = df[corr_cols].corr(numeric_only=True)
    step_corr = corr["icetag_steps_per_hour_norm"].sort_values(ascending=False).to_frame(
        "corr_with_icetag_steps_per_hour_norm"
    )

    return by_cow, by_context, step_corr


def write_report(df: pd.DataFrame, by_cow: pd.DataFrame, by_context: pd.DataFrame, corr: pd.DataFrame) -> None:
    report_path = REPORTS_DIR / "winter2019_sync_report.txt"
    top_corr = corr.head(8).to_string()
    top_cows = by_cow.head(8).to_string()
    top_contexts = by_context.head(12).to_string(index=False)

    text = f"""RAPPORT - WINTER 2019 SYNCHRONE REPRODUCTIBLE
Date : 2026-04-16

Source :
{WINTER_XLSX}

1. Taille du jeu
- lignes : {len(df)}
- vaches : {df['Cow_ID'].nunique()}
- periode : {df['Date'].min().date()} a {df['Date'].max().date()}

2. Variables derivees creees
- comptes comportementaux par categorie
- pourcentages comportementaux par categorie
- behavior_activity_score
- icetag_steps_session_total
- icetag_steps_per_hour_norm

3. Correlations les plus utiles avec les pas IceTag normalises
{top_corr}

4. Resume par vache
{top_cows}

5. Resume par contexte
{top_contexts}

Conclusion :
Winter 2019 reste le meilleur point de depart pour une analyse integree McGill, car
les dimensions comportement, environnement et locomotion y sont deja alignees dans
une meme table exploitable.
"""
    report_path.write_text(text, encoding="utf-8")


def main() -> None:
    REPORTS_DIR.mkdir(exist_ok=True)
    df = load_source()
    df = add_behavior_features(df)
    df = add_icetag_features(df)
    by_cow, by_context, corr = build_summaries(df)

    enriched_csv = REPORTS_DIR / "winter2019_sync_enriched.csv"
    by_cow_csv = REPORTS_DIR / "winter2019_sync_by_cow.csv"
    by_context_csv = REPORTS_DIR / "winter2019_sync_by_context.csv"
    corr_csv = REPORTS_DIR / "winter2019_sync_correlations.csv"

    df.to_csv(enriched_csv, index=False)
    by_cow.to_csv(by_cow_csv)
    by_context.to_csv(by_context_csv, index=False)
    corr.to_csv(corr_csv)
    write_report(df, by_cow, by_context, corr)

    print(f"Enriched : {enriched_csv}")
    print(f"By cow   : {by_cow_csv}")
    print(f"By ctx   : {by_context_csv}")
    print(f"Corr     : {corr_csv}")
    print(f"Report   : {REPORTS_DIR / 'winter2019_sync_report.txt'}")


if __name__ == "__main__":
    main()
