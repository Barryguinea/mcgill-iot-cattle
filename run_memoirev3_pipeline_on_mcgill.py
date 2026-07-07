#!/usr/bin/env python3
"""Apply the read-only memoirev3 pipeline to McGill IceTag outputs.

This script deliberately does not write inside ``/Users/alioubarry/PROJECT/memoirev3``.
Outputs are written under ``mcgill_iot_cattle/reports``.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
MEMOIREV3_ROOT = PROJECT_ROOT / "memoirev3"
OBJECTIVE1_DIR = ROOT / "reports" / "objective1_pipeline_icetag"
DEFAULT_OUTPUT_DIR = OBJECTIVE1_DIR / "memoirev3_comparison"

SEASONS = {
    "fall_2019": {
        "input": OBJECTIVE1_DIR / "fall_2019_pipeline_input_15min.csv",
        "old_summary": OBJECTIVE1_DIR / "fall_2019_pipeline_summary.csv",
        "old_alerts": OBJECTIVE1_DIR / "fall_2019_pipeline_alerts_only.csv",
    },
    "summer_2019": {
        "input": OBJECTIVE1_DIR / "summer_2019_pipeline_input_15min.csv",
        "old_summary": OBJECTIVE1_DIR / "summer_2019_pipeline_summary.csv",
        "old_alerts": OBJECTIVE1_DIR / "summer_2019_pipeline_alerts_only.csv",
    },
    "winter_2019": {
        "input": OBJECTIVE1_DIR / "winter_2019_pipeline_input_15min.csv",
        "old_summary": OBJECTIVE1_DIR / "winter_2019_pipeline_summary.csv",
        "old_alerts": OBJECTIVE1_DIR / "winter_2019_pipeline_alerts_only.csv",
    },
    "fall_2021": {
        "input": OBJECTIVE1_DIR / "fall_2021_pipeline_input_15min.csv",
        "old_summary": OBJECTIVE1_DIR / "fall_2021_pipeline_summary.csv",
        "old_alerts": OBJECTIVE1_DIR / "fall_2021_pipeline_alerts_only.csv",
    },
}

CORE_PREDICTION_COLUMNS = [
    "T",
    "Cow",
    "coverage_pct",
    "dataset_split",
    "notif_lameness",
    "lame_confidence",
    "behavioral_warning_score",
    "behavioral_warning_cusum",
    "behavioral_warning_families",
    "behavioral_warning_episode",
    "behavioral_warning_start",
    "behavioral_warning_notification",
    "instability_warning_score",
    "instability_warning_cusum",
    "instability_warning_families",
    "instability_warning_episode",
    "instability_warning_start",
    "instability_warning_notification",
    "hybrid_warning_score",
    "hybrid_warning_episode",
    "hybrid_warning_surveillance",
    "hybrid_warning_sequence_start",
    "hybrid_warning_start",
    "hybrid_warning_notification",
    "hybrid_warning_type",
    "hybrid_warning_priority",
    "hybrid_warning_fusion_mode",
]


def import_memoirev3() -> tuple[Any, Any, Any]:
    """Import memoirev3 code without writing bytecode in that project."""
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(MEMOIREV3_ROOT))

    from core.io import normalize_columns  # type: ignore
    from core.pipeline import run_pipeline_herd  # type: ignore
    from revalidation_v3.campaign import final_params  # type: ignore

    return normalize_columns, run_pipeline_herd, final_params


def _notification_set(frame: pd.DataFrame, flag_col: str) -> set[tuple[str, pd.Timestamp]]:
    if frame.empty or flag_col not in frame.columns:
        return set()
    tmp = frame.loc[pd.to_numeric(frame[flag_col], errors="coerce").fillna(0).astype(int) == 1, ["Cow", "T"]].copy()
    tmp["Cow"] = tmp["Cow"].astype(str)
    tmp["T"] = pd.to_datetime(tmp["T"], errors="coerce")
    tmp = tmp.dropna(subset=["T"])
    return set(zip(tmp["Cow"], tmp["T"]))


def _rate_per_100_cow_days(n_notifs: int, n_bins: int) -> float:
    cow_days = n_bins / 96.0
    return float(n_notifs / cow_days * 100.0) if cow_days else 0.0


def _select_core_predictions(predictions: pd.DataFrame) -> pd.DataFrame:
    keep = [col for col in CORE_PREDICTION_COLUMNS if col in predictions.columns]
    return predictions[keep].copy()


def run_one_season(season: str, paths: dict[str, Path], output_dir: Path, *, full_predictions: bool) -> dict[str, Any]:
    normalize_columns, run_pipeline_herd, final_params = import_memoirev3()

    raw = pd.read_csv(paths["input"])
    normalized = normalize_columns(raw)
    normalized["Cow"] = normalized["Cow"].astype(str)

    params = final_params()
    v3_summary, v3_pred = run_pipeline_herd(normalized, **params)
    v3_summary["Cow"] = v3_summary["Cow"].astype(str)
    v3_pred["Cow"] = v3_pred["Cow"].astype(str)
    v3_pred["T"] = pd.to_datetime(v3_pred["T"], errors="coerce")

    old_summary = pd.read_csv(paths["old_summary"])
    old_summary["Cow"] = old_summary["Cow"].astype(str)
    old_alerts = pd.read_csv(paths["old_alerts"])
    old_alerts["Cow"] = old_alerts["Cow"].astype(str)
    old_alerts["T"] = pd.to_datetime(old_alerts["T"], errors="coerce")

    season_dir = output_dir / season
    season_dir.mkdir(parents=True, exist_ok=True)

    v3_summary_path = season_dir / f"{season}_memoirev3_summary.csv"
    v3_core_pred_path = season_dir / f"{season}_memoirev3_predictions_core.csv"
    v3_alerts_path = season_dir / f"{season}_memoirev3_alerts_only.csv"
    v3_summary.to_csv(v3_summary_path, index=False)
    _select_core_predictions(v3_pred).to_csv(v3_core_pred_path, index=False)

    alert_flags = [
        col
        for col in [
            "notif_lameness",
            "behavioral_warning_notification",
            "instability_warning_notification",
            "hybrid_warning_notification",
        ]
        if col in v3_pred.columns
    ]
    alert_mask = pd.Series(False, index=v3_pred.index)
    for col in alert_flags:
        alert_mask = alert_mask | (pd.to_numeric(v3_pred[col], errors="coerce").fillna(0).astype(int) == 1)
    v3_alerts = _select_core_predictions(v3_pred.loc[alert_mask])
    v3_alerts.to_csv(v3_alerts_path, index=False)

    full_path = None
    if full_predictions:
        full_path = season_dir / f"{season}_memoirev3_predictions_full.csv"
        v3_pred.to_csv(full_path, index=False)

    old_n = int(old_summary["lameness_notifs"].sum())
    v3_if_n = int(v3_summary.get("lameness_notifs", pd.Series(dtype=int)).sum())
    hypo_n = int(v3_summary.get("behavioral_warning_notifs", pd.Series(dtype=int)).sum())
    instability_n = int(v3_summary.get("instability_warning_notifs", pd.Series(dtype=int)).sum())
    hybrid_n = int(v3_summary.get("hybrid_warning_notifs", pd.Series(dtype=int)).sum())
    n_bins = int(v3_summary["n_bins"].sum())

    old_set = _notification_set(old_alerts, "notif_lameness")
    v3_if_set = _notification_set(v3_pred, "notif_lameness")
    hybrid_set = _notification_set(v3_pred, "hybrid_warning_notification")
    hypo_set = _notification_set(v3_pred, "behavioral_warning_notification")
    instability_set = _notification_set(v3_pred, "instability_warning_notification")

    old_hybrid_overlap = len(old_set & hybrid_set)
    old_v3_if_overlap = len(old_set & v3_if_set)
    type_counts = (
        v3_pred.loc[pd.to_numeric(v3_pred["hybrid_warning_notification"], errors="coerce").fillna(0).astype(int) == 1, "hybrid_warning_type"]
        .value_counts(dropna=False)
        .to_dict()
        if "hybrid_warning_type" in v3_pred
        else {}
    )

    by_cow = old_summary[["Cow", "lameness_notifs", "n_bins", "coverage_mean"]].rename(
        columns={
            "lameness_notifs": "old_lameness_notifs",
            "n_bins": "old_n_bins",
            "coverage_mean": "old_coverage_mean",
        }
    )
    v3_cols = [
        col
        for col in [
            "Cow",
            "n_bins",
            "coverage_mean",
            "lameness_notifs",
            "behavioral_warning_notifs",
            "instability_warning_notifs",
            "hybrid_warning_notifs",
        ]
        if col in v3_summary.columns
    ]
    by_cow = by_cow.merge(
        v3_summary[v3_cols].rename(
            columns={
                "n_bins": "v3_n_bins",
                "coverage_mean": "v3_coverage_mean",
                "lameness_notifs": "v3_legacy_if_lameness_notifs",
            }
        ),
        on="Cow",
        how="outer",
    )
    by_cow["season"] = season
    for col in [
        "old_lameness_notifs",
        "v3_legacy_if_lameness_notifs",
        "behavioral_warning_notifs",
        "instability_warning_notifs",
        "hybrid_warning_notifs",
    ]:
        if col in by_cow.columns:
            by_cow[col] = pd.to_numeric(by_cow[col], errors="coerce").fillna(0).astype(int)
    by_cow.to_csv(season_dir / f"{season}_comparison_by_cow.csv", index=False)

    return {
        "season": season,
        "n_cows": int(v3_summary["Cow"].nunique()),
        "n_bins": n_bins,
        "old_lameness_notifs": old_n,
        "v3_legacy_if_lameness_notifs": v3_if_n,
        "v3_behavioral_hypo_notifs": hypo_n,
        "v3_instability_notifs": instability_n,
        "v3_hybrid_notifs": hybrid_n,
        "old_rate_per_100_cow_days": round(_rate_per_100_cow_days(old_n, n_bins), 3),
        "v3_hybrid_rate_per_100_cow_days": round(_rate_per_100_cow_days(hybrid_n, n_bins), 3),
        "old_vs_v3_legacy_if_exact_overlap": old_v3_if_overlap,
        "old_vs_hybrid_exact_overlap": old_hybrid_overlap,
        "old_only_vs_hybrid": len(old_set - hybrid_set),
        "hybrid_only_vs_old": len(hybrid_set - old_set),
        "hypo_exact_notifs": len(hypo_set),
        "instability_exact_notifs": len(instability_set),
        "hybrid_type_counts": json.dumps(type_counts, ensure_ascii=False),
        "v3_summary_path": str(v3_summary_path.relative_to(ROOT)),
        "v3_core_predictions_path": str(v3_core_pred_path.relative_to(ROOT)),
        "v3_alerts_path": str(v3_alerts_path.relative_to(ROOT)),
        "v3_full_predictions_path": str(full_path.relative_to(ROOT)) if full_path else "",
    }


def write_report(summary: pd.DataFrame, output_dir: Path) -> None:
    total = {
        "season": "TOTAL",
        "n_cows": int(summary["n_cows"].sum()),
        "n_bins": int(summary["n_bins"].sum()),
        "old_lameness_notifs": int(summary["old_lameness_notifs"].sum()),
        "v3_legacy_if_lameness_notifs": int(summary["v3_legacy_if_lameness_notifs"].sum()),
        "v3_behavioral_hypo_notifs": int(summary["v3_behavioral_hypo_notifs"].sum()),
        "v3_instability_notifs": int(summary["v3_instability_notifs"].sum()),
        "v3_hybrid_notifs": int(summary["v3_hybrid_notifs"].sum()),
        "old_rate_per_100_cow_days": round(_rate_per_100_cow_days(int(summary["old_lameness_notifs"].sum()), int(summary["n_bins"].sum())), 3),
        "v3_hybrid_rate_per_100_cow_days": round(_rate_per_100_cow_days(int(summary["v3_hybrid_notifs"].sum()), int(summary["n_bins"].sum())), 3),
        "old_vs_v3_legacy_if_exact_overlap": int(summary["old_vs_v3_legacy_if_exact_overlap"].sum()),
        "old_vs_hybrid_exact_overlap": int(summary["old_vs_hybrid_exact_overlap"].sum()),
        "old_only_vs_hybrid": int(summary["old_only_vs_hybrid"].sum()),
        "hybrid_only_vs_old": int(summary["hybrid_only_vs_old"].sum()),
    }
    display = pd.concat([summary, pd.DataFrame([total])], ignore_index=True, sort=False)

    lines = [
        "# Comparaison McGill — ancien pipeline vs memoirev3",
        "",
        "## Protocole",
        "",
        "- Entrées: fichiers McGill déjà convertis en intervalles de 15 minutes (`*_pipeline_input_15min.csv`).",
        "- Ancien pipeline: sorties existantes de l'objectif 1 (`notif_lameness`).",
        "- Nouveau pipeline: code importé depuis `memoirev3` en lecture seule; sorties principales HYPO, INSTABILITÉ et HYBRIDE.",
        "- Interprétation V3: alerte comportementale à vérifier, non diagnostic clinique de boiterie.",
        "",
        "## Résumé par saison",
        "",
        display[
            [
                "season",
                "n_cows",
                "n_bins",
                "old_lameness_notifs",
                "v3_legacy_if_lameness_notifs",
                "v3_behavioral_hypo_notifs",
                "v3_instability_notifs",
                "v3_hybrid_notifs",
                "old_rate_per_100_cow_days",
                "v3_hybrid_rate_per_100_cow_days",
                "old_vs_hybrid_exact_overlap",
                "old_only_vs_hybrid",
                "hybrid_only_vs_old",
            ]
        ].to_markdown(index=False),
        "",
        "## Lecture",
        "",
        "- `v3_legacy_if_lameness_notifs` est le comparateur IF historique recalculé par le code V3.",
        "- `v3_behavioral_hypo_notifs` est la branche primaire MemoireV3: baisse comportementale persistante.",
        "- `v3_instability_notifs` est la branche exploratoire d'instabilité comportementale.",
        "- `v3_hybrid_notifs` est la fusion hiérarchique utilisée comme sortie V3 principale.",
        "- Le chevauchement exact compare les notifications au même couple `(Cow, T)`; un faible chevauchement ne signifie pas forcément contradiction clinique, car les définitions d'alerte ont changé.",
        "",
        "## Fichiers produits",
        "",
        "- `comparison_summary_by_season.csv`",
        "- `comparison_by_cow_all_seasons.csv`",
        "- `<season>/<season>_memoirev3_summary.csv`",
        "- `<season>/<season>_memoirev3_predictions_core.csv`",
        "- `<season>/<season>_memoirev3_alerts_only.csv`",
    ]
    (output_dir / "README_comparison.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--season", choices=sorted(SEASONS), action="append", help="Season to run; can be repeated.")
    parser.add_argument("--full-predictions", action="store_true", help="Also export full V3 prediction tables.")
    args = parser.parse_args()

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    seasons = args.season or list(SEASONS)

    rows: list[dict[str, Any]] = []
    for season in seasons:
        print(f"[memoirev3-mcgill] running {season}", flush=True)
        rows.append(run_one_season(season, SEASONS[season], output_dir, full_predictions=args.full_predictions))

    summary = pd.DataFrame(rows)
    summary.to_csv(output_dir / "comparison_summary_by_season.csv", index=False)

    by_cow_frames = []
    for season in seasons:
        p = output_dir / season / f"{season}_comparison_by_cow.csv"
        if p.exists():
            by_cow_frames.append(pd.read_csv(p))
    if by_cow_frames:
        pd.concat(by_cow_frames, ignore_index=True).to_csv(output_dir / "comparison_by_cow_all_seasons.csv", index=False)

    write_report(summary, output_dir)
    print(f"[memoirev3-mcgill] wrote {output_dir}", flush=True)


if __name__ == "__main__":
    main()
