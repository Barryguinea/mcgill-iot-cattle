from __future__ import annotations

import math
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT = Path(__file__).resolve().parent
REPORTS = PROJECT / "reports" / "objective1_pipeline_icetag"
OUTDIR = REPORTS / "renforcement_scientifique"

SEASONS = ("fall_2019", "summer_2019", "winter_2019", "fall_2021")

FEATURES = [
    "Steps_sum",
    "Motion Index_sum",
    "Lying Time_sum",
    "Standing Time_sum",
    "Transitions_sum",
]

COVERAGE_MIN_PCT = 75.0
HERD_MIN_FRAC = 0.50
COLLECTIVE_3D_MIN_FRAC = 0.30
COLLECTIVE_7D_MIN_FRAC = 0.50
CONFIDENCE_MIN_FOR_PRIORITY = 45.0


def _required_columns(path: Path) -> list[str]:
    cols = pd.read_csv(path, nrows=0).columns.tolist()
    wanted = [
        "Cow",
        "T",
        "Day",
        "coverage_pct",
        "notif_lameness",
        "lame_confidence",
        "if_anomaly_point",
        "pred_problem_episode",
        "pred_problem_start",
        "pred_lameness_episode",
        "pred_lameness_start",
        *FEATURES,
    ]
    return [col for col in wanted if col in cols]


def _format_pct(value: float) -> str:
    if pd.isna(value):
        return ""
    return f"{100 * value:.1f}%"


def _read_predictions(season: str) -> pd.DataFrame:
    path = REPORTS / f"{season}_pipeline_predictions.csv"
    if not path.exists():
        raise FileNotFoundError(path)
    df = pd.read_csv(path, usecols=_required_columns(path))
    df["season"] = season
    df["Cow"] = df["Cow"].astype(str)
    df["T"] = pd.to_datetime(df["T"])
    if "Day" not in df.columns:
        df["Day"] = df["T"].dt.date.astype(str)
    df["Day"] = pd.to_datetime(df["Day"]).dt.date
    for col in ["notif_lameness", "coverage_pct", "lame_confidence"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def _add_herd_context(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    valid = out["coverage_pct"].ge(COVERAGE_MIN_PCT)
    total_cows = out["Cow"].nunique()
    min_herd_cows = max(5, math.ceil(total_cows * HERD_MIN_FRAC))

    herd_n = out.loc[valid].groupby("T")["Cow"].nunique()
    out["herd_n_cows_at_T"] = out["T"].map(herd_n).fillna(0).astype(int)
    out["herd_context_valid"] = out["herd_n_cows_at_T"].ge(min_herd_cows)

    grouped = out.loc[valid].groupby("T")
    medians = grouped[FEATURES].median()

    for feature in FEATURES:
        median_col = f"{feature}_herd_median"
        mad_col = f"{feature}_herd_mad"
        z_col = f"{feature}_herd_z"
        pct_col = f"{feature}_vs_herd_pct"

        out[median_col] = out["T"].map(medians[feature])
        abs_dev = (out.loc[valid, feature] - out.loc[valid, median_col]).abs()
        mad = abs_dev.groupby(out.loc[valid, "T"]).median()
        out[mad_col] = out["T"].map(mad)

        denom = 1.4826 * out[mad_col].replace(0, np.nan)
        out[z_col] = ((out[feature] - out[median_col]) / denom).clip(-10, 10)

        median_abs = out[median_col].abs().replace(0, np.nan)
        out[pct_col] = 100.0 * (out[feature] - out[median_col]) / median_abs

    return out


def _window_unique_cows(alerts: pd.DataFrame, center: pd.Timestamp, radius_days: int) -> int:
    start = center - pd.Timedelta(days=radius_days)
    end = center + pd.Timedelta(days=radius_days)
    mask = alerts["T"].between(start, end, inclusive="both")
    return alerts.loc[mask, "Cow"].nunique()


def _add_collective_context(alerts: pd.DataFrame, total_cows: int) -> pd.DataFrame:
    out = alerts.copy()
    if out.empty:
        for col in [
            "herd_alerted_cows_3d",
            "herd_alerted_frac_3d",
            "herd_alerted_cows_7d",
            "herd_alerted_frac_7d",
            "collective_event_flag",
        ]:
            out[col] = []
        return out

    counts_3d = []
    counts_7d = []
    for ts in out["T"]:
        counts_3d.append(_window_unique_cows(out, ts, radius_days=1))
        counts_7d.append(_window_unique_cows(out, ts, radius_days=3))

    out["herd_alerted_cows_3d"] = counts_3d
    out["herd_alerted_cows_7d"] = counts_7d
    out["herd_alerted_frac_3d"] = out["herd_alerted_cows_3d"] / total_cows
    out["herd_alerted_frac_7d"] = out["herd_alerted_cows_7d"] / total_cows

    min_3d = max(3, math.ceil(total_cows * COLLECTIVE_3D_MIN_FRAC))
    min_7d = max(5, math.ceil(total_cows * COLLECTIVE_7D_MIN_FRAC))
    out["collective_event_flag"] = (
        out["herd_alerted_cows_3d"].ge(min_3d)
        | out["herd_alerted_cows_7d"].ge(min_7d)
    )
    return out


def _add_confidence_levels(alerts: pd.DataFrame) -> pd.DataFrame:
    out = alerts.copy()

    out["herd_hypoactivity_signal"] = (
        out["Steps_sum_herd_z"].le(-1.0)
        | out["Motion Index_sum_herd_z"].le(-1.0)
        | out["Transitions_sum_herd_z"].le(-1.0)
    )
    out["herd_posture_shift_signal"] = (
        out["Lying Time_sum_herd_z"].ge(1.0)
        | out["Standing Time_sum_herd_z"].le(-1.0)
    )
    out["herd_specific_signal"] = (
        out["herd_context_valid"]
        & (out["herd_hypoactivity_signal"] | out["herd_posture_shift_signal"])
    )

    def classify(row: pd.Series) -> str:
        if row.get("coverage_pct", np.nan) < COVERAGE_MIN_PCT or not row.get(
            "herd_context_valid", False
        ):
            return "D_qualite_ou_contexte_insuffisant"
        if bool(row.get("collective_event_flag", False)):
            return "C_probable_evenement_collectif"
        if bool(row.get("herd_specific_signal", False)) and row.get(
            "lame_confidence", 0
        ) >= CONFIDENCE_MIN_FOR_PRIORITY:
            return "A_individuelle_prioritaire"
        return "B_individuelle_a_verifier"

    out["reinforced_confidence_level"] = out.apply(classify, axis=1)

    interpretations = {
        "A_individuelle_prioritaire": (
            "Alerte individuelle prioritaire: deviation propre a la vache, bonne "
            "couverture, sans signal collectif majeur."
        ),
        "B_individuelle_a_verifier": (
            "Alerte individuelle a verifier: signal pipeline conserve, mais support "
            "troupeau moins net ou confidence moderee."
        ),
        "C_probable_evenement_collectif": (
            "Alerte en contexte collectif: interpretation clinique prudente; verifier "
            "gestion, meteo, protocole ou evenement de troupeau."
        ),
        "D_qualite_ou_contexte_insuffisant": (
            "Alerte non prioritaire: couverture ou contexte troupeau insuffisant pour "
            "renforcer l'interpretation."
        ),
    }
    out["reinforced_interpretation"] = out["reinforced_confidence_level"].map(
        interpretations
    )
    return out


def _daily_collective_summary(alerts: pd.DataFrame, total_cows: int) -> pd.DataFrame:
    if alerts.empty:
        return pd.DataFrame(
            columns=[
                "season",
                "Day",
                "n_alerts",
                "alerted_cows",
                "alerted_cow_frac",
                "collective_alerts",
                "cows",
            ]
        )

    grouped = (
        alerts.groupby(["season", "Day"])
        .agg(
            n_alerts=("notif_lameness", "size"),
            alerted_cows=("Cow", "nunique"),
            collective_alerts=("collective_event_flag", "sum"),
            cows=("Cow", lambda s: ", ".join(sorted(s.unique()))),
        )
        .reset_index()
    )
    grouped["alerted_cow_frac"] = grouped["alerted_cows"] / total_cows
    grouped["Day"] = grouped["Day"].astype(str)
    return grouped.sort_values(["season", "Day"])


def _summarize_by_season(alerts: pd.DataFrame, predictions: pd.DataFrame) -> pd.DataFrame:
    if alerts.empty:
        return pd.DataFrame()

    counts = (
        alerts.pivot_table(
            index="season",
            columns="reinforced_confidence_level",
            values="notif_lameness",
            aggfunc="size",
            fill_value=0,
        )
        .reset_index()
        .rename_axis(None, axis=1)
    )
    for col in [
        "A_individuelle_prioritaire",
        "B_individuelle_a_verifier",
        "C_probable_evenement_collectif",
        "D_qualite_ou_contexte_insuffisant",
    ]:
        if col not in counts.columns:
            counts[col] = 0

    base = (
        predictions.groupby("season")
        .agg(
            n_cows=("Cow", "nunique"),
            n_intervals=("T", "size"),
            first_T=("T", "min"),
            last_T=("T", "max"),
        )
        .reset_index()
    )
    alert_base = (
        alerts.groupby("season")
        .agg(
            initial_notifications=("notif_lameness", "size"),
            alerted_cows=("Cow", "nunique"),
            collective_flagged=("collective_event_flag", "sum"),
            herd_specific_signal=("herd_specific_signal", "sum"),
            mean_lame_confidence=("lame_confidence", "mean"),
            mean_coverage_pct=("coverage_pct", "mean"),
        )
        .reset_index()
    )
    summary = base.merge(alert_base, on="season", how="left").merge(
        counts, on="season", how="left"
    )
    summary["collective_flagged_pct"] = (
        summary["collective_flagged"] / summary["initial_notifications"]
    )
    summary["herd_specific_signal_pct"] = (
        summary["herd_specific_signal"] / summary["initial_notifications"]
    )

    v3_path = REPORTS / "memoirev3_comparison" / "comparison_summary_by_season.csv"
    if v3_path.exists():
        v3 = pd.read_csv(v3_path)
        v3_cols = [
            col
            for col in [
                "season",
                "old_lameness_notifs",
                "v3_behavioral_hypo_notifs",
                "v3_instability_notifs",
                "v3_hybrid_notifs",
                "old_rate_per_100_cow_days",
                "v3_hybrid_rate_per_100_cow_days",
            ]
            if col in v3.columns
        ]
        summary = summary.merge(v3[v3_cols], on="season", how="left")

    return summary.sort_values("season")


def _summarize_by_cow(alerts: pd.DataFrame) -> pd.DataFrame:
    if alerts.empty:
        return pd.DataFrame()

    counts = (
        alerts.pivot_table(
            index=["season", "Cow"],
            columns="reinforced_confidence_level",
            values="notif_lameness",
            aggfunc="size",
            fill_value=0,
        )
        .reset_index()
        .rename_axis(None, axis=1)
    )
    for col in [
        "A_individuelle_prioritaire",
        "B_individuelle_a_verifier",
        "C_probable_evenement_collectif",
        "D_qualite_ou_contexte_insuffisant",
    ]:
        if col not in counts.columns:
            counts[col] = 0

    totals = (
        alerts.groupby(["season", "Cow"])
        .agg(
            total_notifications=("notif_lameness", "size"),
            collective_flagged=("collective_event_flag", "sum"),
            herd_specific_signal=("herd_specific_signal", "sum"),
            mean_lame_confidence=("lame_confidence", "mean"),
        )
        .reset_index()
    )
    return totals.merge(counts, on=["season", "Cow"], how="left").sort_values(
        ["season", "total_notifications"], ascending=[True, False]
    )


def _write_report(
    summary: pd.DataFrame,
    by_confidence: pd.DataFrame,
    daily: pd.DataFrame,
) -> Path:
    report_path = OUTDIR / "RAPPORT_renforcement_objectif1.md"

    summary_display = summary.copy()
    for col in ["collective_flagged_pct", "herd_specific_signal_pct"]:
        if col in summary_display.columns:
            summary_display[col] = summary_display[col].map(_format_pct)
    for col in ["first_T", "last_T"]:
        if col in summary_display.columns:
            summary_display[col] = pd.to_datetime(summary_display[col]).dt.strftime(
                "%Y-%m-%d"
            )

    flagged = daily[daily["collective_alerts"].gt(0)].copy()
    if not flagged.empty:
        flagged = flagged.sort_values(
            ["collective_alerts", "alerted_cows"], ascending=False
        ).head(20)
        flagged["alerted_cow_frac"] = flagged["alerted_cow_frac"].map(_format_pct)

    lines = [
        "# Renforcement scientifique - Objectif 1",
        "",
        f"Date: {date.today().isoformat()}",
        "",
        "## Perimetre",
        "",
        "- Base conservee: pipeline initiale McGill deja livree (Isolation Forest + regles metier).",
        "- Aucune modification de `memoirev3`.",
        "- Objectif: requalifier les 385 notifications existantes avec un contexte troupeau, un filtre d'evenements collectifs et des niveaux de confiance.",
        "- Interpretation: alertes comportementales compatibles avec une perturbation locomotrice, pas diagnostics cliniques confirmes.",
        "",
        "## Methode ajoutee",
        "",
        "1. Normalisation troupeau: chaque vache est comparee a la mediane contemporaine du troupeau au meme timestamp de 15 min.",
        f"2. Contexte valide si au moins {int(HERD_MIN_FRAC * 100)}% du troupeau et au moins 5 vaches ont une couverture >= {COVERAGE_MIN_PCT:.0f}%.",
        f"3. Evenement collectif si une alerte survient avec >= {int(COLLECTIVE_3D_MIN_FRAC * 100)}% des vaches alertees dans +/-1 jour ou >= {int(COLLECTIVE_7D_MIN_FRAC * 100)}% dans +/-3 jours.",
        "4. Niveaux de confiance:",
        "   - A_individuelle_prioritaire: alerte non collective, bonne couverture, deviation propre a la vache.",
        "   - B_individuelle_a_verifier: alerte non collective mais support troupeau moins net.",
        "   - C_probable_evenement_collectif: alerte dans un episode de troupeau, interpretation clinique prudente.",
        "   - D_qualite_ou_contexte_insuffisant: donnees insuffisantes pour renforcer l'interpretation.",
        "",
        "## Synthese par saison",
        "",
        summary_display.to_markdown(index=False),
        "",
        "## Synthese par niveau de confiance",
        "",
        by_confidence.to_markdown(index=False),
        "",
        "## Principaux jours avec contexte collectif",
        "",
        flagged.to_markdown(index=False) if not flagged.empty else "Aucun jour collectif majeur detecte.",
        "",
        "## Lecture scientifique",
        "",
        "Cette analyse renforce l'Objectif 1 parce qu'elle separe les alertes individuelles prioritaires des alertes probablement liees a un contexte partage. Elle ne transforme pas les alertes en verite-terrain clinique: la sensibilite et la specificite a la boiterie restent non mesurables sans labels synchrones et cas cliniquement nets.",
        "",
        "La comparaison V3 reste une annexe methodologique: `../memoirev3_comparison/CADRAGE_pipeline_initiale_vs_V3.md`. Elle documente que la V3 produit plus d'alertes comportementales, mais ne prouve pas une meilleure detection clinique de boiterie sur McGill.",
        "",
        "## Fichiers produits",
        "",
        "- `objective1_reinforced_alerts.csv`",
        "- `objective1_reinforced_summary_by_season.csv`",
        "- `objective1_reinforced_summary_by_confidence.csv`",
        "- `objective1_reinforced_summary_by_cow.csv`",
        "- `objective1_collective_days.csv`",
    ]
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def run() -> dict[str, Path]:
    OUTDIR.mkdir(parents=True, exist_ok=True)

    prediction_frames = []
    alert_frames = []
    daily_frames = []

    for season in SEASONS:
        predictions = _read_predictions(season)
        predictions = _add_herd_context(predictions)
        total_cows = predictions["Cow"].nunique()

        alerts = predictions[predictions["notif_lameness"].fillna(0).astype(int).eq(1)].copy()
        alerts = _add_collective_context(alerts, total_cows=total_cows)
        alerts = _add_confidence_levels(alerts)

        prediction_frames.append(predictions[["season", "Cow", "T", "Day"]])
        alert_frames.append(alerts)
        daily_frames.append(_daily_collective_summary(alerts, total_cows=total_cows))

    all_predictions_light = pd.concat(prediction_frames, ignore_index=True)
    all_alerts = pd.concat(alert_frames, ignore_index=True)
    all_daily = pd.concat(daily_frames, ignore_index=True)

    summary = _summarize_by_season(all_alerts, all_predictions_light)
    by_cow = _summarize_by_cow(all_alerts)
    by_confidence = (
        all_alerts.groupby(["season", "reinforced_confidence_level"])
        .agg(
            notifications=("notif_lameness", "size"),
            cows=("Cow", "nunique"),
            mean_lame_confidence=("lame_confidence", "mean"),
            mean_coverage_pct=("coverage_pct", "mean"),
            collective_alerts=("collective_event_flag", "sum"),
            herd_specific_signals=("herd_specific_signal", "sum"),
        )
        .reset_index()
        .sort_values(["season", "reinforced_confidence_level"])
    )

    alert_cols = [
        "season",
        "Cow",
        "T",
        "Day",
        "notif_lameness",
        "lame_confidence",
        "coverage_pct",
        "herd_n_cows_at_T",
        "herd_context_valid",
        "Steps_sum",
        "Steps_sum_herd_median",
        "Steps_sum_herd_z",
        "Steps_sum_vs_herd_pct",
        "Motion Index_sum",
        "Motion Index_sum_herd_median",
        "Motion Index_sum_herd_z",
        "Motion Index_sum_vs_herd_pct",
        "Lying Time_sum",
        "Lying Time_sum_herd_median",
        "Lying Time_sum_herd_z",
        "Lying Time_sum_vs_herd_pct",
        "Transitions_sum",
        "Transitions_sum_herd_median",
        "Transitions_sum_herd_z",
        "Transitions_sum_vs_herd_pct",
        "herd_alerted_cows_3d",
        "herd_alerted_frac_3d",
        "herd_alerted_cows_7d",
        "herd_alerted_frac_7d",
        "collective_event_flag",
        "herd_hypoactivity_signal",
        "herd_posture_shift_signal",
        "herd_specific_signal",
        "reinforced_confidence_level",
        "reinforced_interpretation",
    ]
    alert_cols = [col for col in alert_cols if col in all_alerts.columns]

    outputs = {
        "alerts": OUTDIR / "objective1_reinforced_alerts.csv",
        "summary_by_season": OUTDIR / "objective1_reinforced_summary_by_season.csv",
        "summary_by_confidence": OUTDIR / "objective1_reinforced_summary_by_confidence.csv",
        "summary_by_cow": OUTDIR / "objective1_reinforced_summary_by_cow.csv",
        "collective_days": OUTDIR / "objective1_collective_days.csv",
    }

    all_alerts[alert_cols].to_csv(outputs["alerts"], index=False)
    summary.to_csv(outputs["summary_by_season"], index=False)
    by_confidence.to_csv(outputs["summary_by_confidence"], index=False)
    by_cow.to_csv(outputs["summary_by_cow"], index=False)
    all_daily.to_csv(outputs["collective_days"], index=False)
    outputs["report"] = _write_report(summary, by_confidence, all_daily)

    return outputs


if __name__ == "__main__":
    written = run()
    print("Objectif 1 renforce. Fichiers produits:")
    for name, path in written.items():
        print(f"- {name}: {path}")
