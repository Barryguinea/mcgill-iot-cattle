# -*- coding: utf-8 -*-
"""Analyse de sensibilité de l'Objectif 2 : THI et activité locomotrice.

Le THI est commun à toutes les vaches observées au même timestamp. Le script
rapporte donc plusieurs niveaux d'analyse : mesures répétées par vache,
agrégation du troupeau par timestamp, puis contrôle explicite du jour.

Entrée : reports/objective2_environnement/
         summer2019_icetag_environnement_15min.csv
Sorties : reports/objective2_environnement/mixed_model/*.csv
"""
from __future__ import annotations

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

warnings.filterwarnings("ignore")

SCRIPT_DIR = Path(__file__).resolve().parent
DELIVERY_ROOT = SCRIPT_DIR.parent
if (DELIVERY_ROOT / "DONNEES_SYNCHRONISEES").is_dir():
    SRC = (
        DELIVERY_ROOT
        / "DONNEES_SYNCHRONISEES"
        / "summer2019_icetag_environnement_15min.csv"
    )
    OUTDIR = DELIVERY_ROOT / "TABLEAUX_CSV"
else:
    SRC = (
        SCRIPT_DIR
        / "reports"
        / "objective2_environnement"
        / "summer2019_icetag_environnement_15min.csv"
    )
    OUTDIR = SCRIPT_DIR / "reports" / "objective2_environnement" / "mixed_model"
USECOLS = ["Cow", "Start", "Steps", "Motion Index", "THI"]


def _load() -> pd.DataFrame:
    df = pd.read_csv(SRC, usecols=USECOLS).rename(columns={"Motion Index": "MI"})
    df["Start"] = pd.to_datetime(df["Start"], errors="coerce")
    df["Day"] = df["Start"].dt.strftime("%Y-%m-%d")
    df["Hour"] = df["Start"].dt.hour
    for column in ["Steps", "MI", "THI"]:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df = df.dropna(subset=["Start", "Steps", "MI", "THI", "Cow", "Hour"])
    df["Cow"] = df["Cow"].astype(str).str.replace(r"\.0$", "", regex=True)
    df["THI_cat"] = pd.cut(
        df["THI"],
        bins=[-np.inf, 68, 72, 80, np.inf],
        labels=["1_aucun", "2_leger", "3_modere", "4_severe"],
        right=False,
    )
    return df


def _row(
    label: str,
    unit: str,
    controls: str,
    coef: float,
    ci_low: float | None,
    ci_high: float | None,
    p_value: float,
    n: int,
    interpretation: str,
) -> dict:
    return {
        "modele": label,
        "unite_analyse": unit,
        "controles": controls,
        "coef_THI": round(float(coef), 4),
        "ic95_bas": "" if ci_low is None else round(float(ci_low), 4),
        "ic95_haut": "" if ci_high is None else round(float(ci_high), 4),
        "p": float(p_value),
        "n": int(n),
        "interpretation": interpretation,
    }


def _mixed_cow(df: pd.DataFrame, outcome: str, rhs: str) -> tuple:
    model = smf.mixedlm(f"{outcome} ~ {rhs}", df, groups=df["Cow"]).fit(
        method="lbfgs"
    )
    coef = model.params["THI"]
    ci_low, ci_high = model.conf_int().loc["THI"]
    return coef, ci_low, ci_high, model.pvalues["THI"], int(model.nobs)


def _ols_hac(
    df: pd.DataFrame, outcome: str, rhs: str, maxlags: int = 96
) -> tuple:
    model = smf.ols(f"{outcome} ~ {rhs}", df).fit(
        cov_type="HAC", cov_kwds={"maxlags": maxlags}
    )
    coef = model.params["THI"]
    ci_low, ci_high = model.conf_int().loc["THI"]
    return coef, ci_low, ci_high, model.pvalues["THI"], int(model.nobs)


def run() -> None:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    df = _load()

    herd_time = (
        df.groupby(["Start", "Day", "Hour"], as_index=False)
        .agg(
            Steps=("Steps", "mean"),
            MI=("MI", "mean"),
            THI=("THI", "first"),
            n_cows=("Cow", "nunique"),
        )
        .sort_values("Start")
    )
    herd_time["THI_c"] = herd_time["THI"] - herd_time["THI"].mean()
    herd_time["day_index"] = (
        pd.to_datetime(herd_time["Day"]) - pd.to_datetime(herd_time["Day"]).min()
    ).dt.days

    descriptifs = pd.DataFrame(
        [
            {
                "n_bins_vache": len(df),
                "n_timestamps_troupeau": len(herd_time),
                "n_vaches": df["Cow"].nunique(),
                "n_jours": df["Day"].nunique(),
                "THI_min": round(df["THI"].min(), 1),
                "THI_moy": round(df["THI"].mean(), 1),
                "THI_max": round(df["THI"].max(), 1),
                "pct_THI_ge_68": round(100 * (df["THI"] >= 68).mean(), 1),
                "pct_THI_ge_72": round(100 * (df["THI"] >= 72).mean(), 1),
                "pct_THI_ge_80": round(100 * (df["THI"] >= 80).mean(), 1),
            }
        ]
    )
    descriptifs.to_csv(OUTDIR / "objective2_descriptifs.csv", index=False)

    rows = []
    rho, p_spearman = stats.spearmanr(df["THI"], df["Steps"])
    rows.append(
        _row(
            "Spearman naïf : Steps ~ THI",
            "bin vache-15 min",
            "aucun",
            rho,
            None,
            None,
            p_spearman,
            len(df),
            "Descriptif seulement : duplique l'exposition THI entre vaches.",
        )
    )

    coef, low, high, p_value, n_obs = _mixed_cow(df, "Steps", "THI + C(Hour)")
    rows.append(
        _row(
            "Modèle mixte vache : Steps ~ THI + heure",
            "bin vache-15 min",
            "heure; intercept aléatoire vache",
            coef,
            low,
            high,
            p_value,
            n_obs,
            "Association ajustée pour l'heure, sans contrôle propre au jour.",
        )
    )

    coef, low, high, p_value, n_obs = _ols_hac(
        herd_time, "Steps", "THI + C(Hour)"
    )
    rows.append(
        _row(
            "Troupeau-timestamp : Steps ~ THI + heure",
            "timestamp troupeau-15 min",
            "heure; erreurs HAC 24 h",
            coef,
            low,
            high,
            p_value,
            n_obs,
            "Association positive entre timestamps, encore exposée au confondant jour.",
        )
    )

    coef, low, high, p_value, n_obs = _ols_hac(
        herd_time, "Steps", "THI + C(Hour) + C(Day)"
    )
    rows.append(
        _row(
            "Troupeau-timestamp : Steps ~ THI + heure + jour",
            "timestamp troupeau-15 min",
            "heure; jour fixe; erreurs HAC 24 h",
            coef,
            low,
            high,
            p_value,
            n_obs,
            "Effet intra-jour non concluant : le signal dépend fortement des jours.",
        )
    )

    coef, low, high, p_value, n_obs = _ols_hac(
        herd_time, "MI", "THI + C(Hour) + C(Day)"
    )
    rows.append(
        _row(
            "Troupeau-timestamp : Motion Index ~ THI + heure + jour",
            "timestamp troupeau-15 min",
            "heure; jour fixe; erreurs HAC 24 h",
            coef,
            low,
            high,
            p_value,
            n_obs,
            "Analyse de sensibilité cohérente : effet intra-jour non concluant.",
        )
    )

    cow_day = (
        df.groupby(["Cow", "Day"], as_index=False)
        .agg(Steps=("Steps", "mean"), THI=("THI", "mean"))
        .dropna()
    )
    between_day = smf.ols("Steps ~ THI + C(Cow)", cow_day).fit(
        cov_type="cluster", cov_kwds={"groups": cow_day["Day"]}
    )
    coef = between_day.params["THI"]
    low, high = between_day.conf_int().loc["THI"]
    rows.append(
        _row(
            "Vache-jour : Steps ~ THI + vache",
            "vache-jour",
            "vache fixe; erreurs regroupées par jour",
            coef,
            low,
            high,
            between_day.pvalues["THI"],
            len(cow_day),
            "Association entre jours; ne démontre pas un effet thermique intra-jour.",
        )
    )
    pd.DataFrame(rows).to_csv(
        OUTDIR / "objective2_mixed_model_summary.csv", index=False
    )

    nonlinear = smf.ols(
        "Steps ~ THI_c + I(THI_c**2) + C(Hour) + C(Day)", herd_time
    ).fit(cov_type="HAC", cov_kwds={"maxlags": 96})
    nonlinear_rows = []
    for label, term in [
        ("THI centré, linéaire", "THI_c"),
        ("THI centré au carré", "I(THI_c ** 2)"),
    ]:
        low, high = nonlinear.conf_int().loc[term]
        nonlinear_rows.append(
            {
                "modele": "Steps ~ THI + THI² + heure + jour",
                "unite_analyse": "timestamp troupeau-15 min",
                "terme": label,
                "coef": round(float(nonlinear.params[term]), 5),
                "ic95_bas": round(float(low), 5),
                "ic95_haut": round(float(high), 5),
                "p": float(nonlinear.pvalues[term]),
                "n": int(nonlinear.nobs),
            }
        )
    pd.DataFrame(nonlinear_rows).to_csv(
        OUTDIR / "objective2_non_linearite.csv", index=False
    )

    profile = (
        df.groupby("THI_cat")
        .agg(
            n=("Steps", "size"),
            THI_moy=("THI", "mean"),
            Steps_moy=("Steps", "mean"),
            MI_moy=("MI", "mean"),
        )
        .reset_index()
        .sort_values("THI_moy")
    )
    profile[["THI_moy", "Steps_moy", "MI_moy"]] = profile[
        ["THI_moy", "Steps_moy", "MI_moy"]
    ].round(2)
    profile.to_csv(OUTDIR / "objective2_profil_par_thi.csv", index=False)

    # Contrôle complémentaire : distinguer l'association globale entre jours
    # de l'effet strictement identifié par les variations au sein d'un jour.
    complete_rows = []

    def add_complete(label, model, term, unit, controls, interpretation):
        low, high = model.conf_int().loc[term]
        complete_rows.append(
            {
                "modele": label,
                "unite_analyse": unit,
                "controles": controls,
                "terme": term,
                "coefficient": round(float(model.params[term]), 6),
                "erreur_standard": round(float(model.bse[term]), 6),
                "ic95_bas": round(float(low), 6),
                "ic95_haut": round(float(high), 6),
                "p": float(model.pvalues[term]),
                "n": int(model.nobs),
                "interpretation": interpretation,
            }
        )

    global_model = smf.ols(
        "Steps ~ THI + C(Hour)", herd_time
    ).fit(cov_type="HAC", cov_kwds={"maxlags": 96})
    add_complete(
        "Association globale ajustée pour l'heure",
        global_model,
        "THI",
        "timestamp troupeau-15 min",
        "heure; erreurs HAC 24 h",
        "Association globale positive, combinant variations entre jours et intra-jour.",
    )

    trend_model = smf.ols(
        "Steps ~ THI + C(Hour) + day_index", herd_time
    ).fit(cov_type="HAC", cov_kwds={"maxlags": 96})
    add_complete(
        "Association globale avec tendance calendaire",
        trend_model,
        "THI",
        "timestamp troupeau-15 min",
        "heure; tendance linéaire de date; erreurs HAC 24 h",
        "Association positive atténuée après contrôle d'une tendance saisonnière linéaire.",
    )

    herd_day = (
        herd_time.groupby("Day", as_index=False)
        .agg(Steps=("Steps", "mean"), THI=("THI", "mean"))
        .sort_values("Day")
    )
    herd_day["day_index"] = (
        pd.to_datetime(herd_day["Day"]) - pd.to_datetime(herd_day["Day"]).min()
    ).dt.days
    daily_model = smf.ols("Steps ~ THI", herd_day).fit(
        cov_type="HAC", cov_kwds={"maxlags": 3}
    )
    add_complete(
        "Association entre journées (unité jour)",
        daily_model,
        "THI",
        "jour troupeau",
        "erreurs HAC 3 jours",
        "Les journées de THI plus élevé ont une activité moyenne plus élevée.",
    )

    daily_trend_model = smf.ols(
        "Steps ~ THI + day_index", herd_day
    ).fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    add_complete(
        "Association entre jours avec tendance calendaire",
        daily_trend_model,
        "THI",
        "jour troupeau",
        "tendance linéaire de date; erreurs HAC 3 jours",
        "Association entre jours encore positive, sans démonstration causale.",
    )

    within_model = smf.ols(
        "Steps ~ THI + C(Hour) + C(Day)", herd_time
    ).fit(cov_type="HAC", cov_kwds={"maxlags": 96})
    add_complete(
        "Effet intra-jour strict",
        within_model,
        "THI",
        "timestamp troupeau-15 min",
        "heure; jour fixe; erreurs HAC 24 h",
        "Effet positif faible et non concluant à l'intérieur des jours.",
    )

    within_clustered = smf.ols(
        "Steps ~ THI + C(Hour) + C(Day)", herd_time
    ).fit(cov_type="cluster", cov_kwds={"groups": herd_time["Day"]})
    add_complete(
        "Effet intra-jour, sensibilité par grappes",
        within_clustered,
        "THI",
        "timestamp troupeau-15 min",
        "heure; jour fixe; erreurs regroupées par jour",
        "Même conclusion non concluante avec une autre estimation de l'incertitude.",
    )

    pd.DataFrame(complete_rows).to_csv(
        OUTDIR / "objective2_thi_controle_complet.csv", index=False
    )

    print("Objectif 2 : analyses écrites dans", OUTDIR)
    print(pd.DataFrame(rows).to_string(index=False))
    print("\nContrôle complet THI :")
    print(pd.DataFrame(complete_rows).to_string(index=False))


if __name__ == "__main__":
    run()
