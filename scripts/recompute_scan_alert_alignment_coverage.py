#!/usr/bin/env python3
"""Recalcule la concordance scans-alertes en contrôlant la couverture IceTag."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd


MCGILL = Path(__file__).resolve().parents[1]
REPORTS = MCGILL / "reports" / "objective1_pipeline_icetag"
SCANS_PATH = MCGILL / "Données completes" / "Scan_Tot_newVersion_SMN.xlsx"
CONCORDANCE_DIR = REPORTS / "tache1_2_concordance"
DELIVERY_TABLES = (
    Path.home()
    / "Desktop"
    / "Livrables_McGill_WellE"
    / "Objectif1_Pipeline_detection_boiterie"
    / "TABLEAUX_CSV"
)

EXPERIMENTS = {
    "Winter2019": ("Winter 2019", "winter_2019"),
    "Summer2019": ("Summer 2019", "summer_2019"),
    "Fall2019": ("Fall 2019", "fall_2019"),
    "Fall 2021": ("Fall 2021", "fall_2021"),
}

BEHAVIOURS = [
    "Pct_locomotion",
    "Pct_lying",
    "Pct_Idle",
    "Pct_Vigilance",
    "Pct_Explo",
    "Pct_eating",
    "Pct_Social",
    "Pct_Maintenance",
    "Pct_Other",
]


def normalize_cow(values: pd.Series) -> pd.Series:
    return values.astype(str).str.replace(".0", "", regex=False).str.strip()


def load_coverage_days(path: Path) -> dict[str, set[pd.Timestamp]]:
    days: dict[str, set[pd.Timestamp]] = defaultdict(set)
    for chunk in pd.read_csv(
        path,
        usecols=["T", "Cow", "coverage_pct"],
        chunksize=300_000,
    ):
        chunk["T"] = pd.to_datetime(chunk["T"], errors="coerce").dt.normalize()
        chunk["Cow"] = normalize_cow(chunk["Cow"])
        coverage = pd.to_numeric(chunk["coverage_pct"], errors="coerce")
        chunk = chunk[chunk["T"].notna() & (coverage > 0)]
        for cow, group in chunk.groupby("Cow"):
            days[cow].update(group["T"].tolist())
    return days


def load_alerts(path: Path) -> tuple[dict[str, set[pd.Timestamp]], pd.DataFrame]:
    alerts = pd.read_csv(path, usecols=["T", "Cow"])
    alerts["T"] = pd.to_datetime(alerts["T"], errors="coerce").dt.normalize()
    alerts["Cow"] = normalize_cow(alerts["Cow"])

    days: dict[str, set[pd.Timestamp]] = defaultdict(set)
    for cow, group in alerts.groupby("Cow"):
        days[cow].update(group["T"].dropna().tolist())
    return days, alerts


def window_days(date: pd.Timestamp) -> set[pd.Timestamp]:
    return {date + pd.Timedelta(days=offset) for offset in (-1, 0, 1)}


def poisson_binomial_upper_tail(probabilities: list[float], observed: int) -> float:
    distribution = np.array([1.0])
    for probability in probabilities:
        distribution = np.convolve(
            distribution,
            np.array([1.0 - probability, probability]),
        )
    return float(distribution[observed:].sum())


def write_outputs(
    detailed: pd.DataFrame,
    summary: pd.DataFrame,
    expected: pd.DataFrame,
    global_control: pd.DataFrame,
) -> None:
    CONCORDANCE_DIR.mkdir(parents=True, exist_ok=True)
    output_dirs = [CONCORDANCE_DIR]
    if DELIVERY_TABLES.parent.exists():
        DELIVERY_TABLES.mkdir(parents=True, exist_ok=True)
        output_dirs.append(DELIVERY_TABLES)

    for output_dir in output_dirs:
        detailed.to_csv(output_dir / "table_concordance.csv", index=False)
        summary.to_csv(output_dir / "concordance_par_experience.csv", index=False)
        expected.to_csv(
            output_dir / "concordance_controle_niveau_attendu.csv",
            index=False,
        )
        global_control.to_csv(
            output_dir / "concordance_controle_global.csv",
            index=False,
        )


def main() -> None:
    scans = pd.read_excel(SCANS_PATH, sheet_name="Feuil1")
    scans["Cow"] = normalize_cow(scans["Cow"])
    scans["Date"] = pd.to_datetime(scans["Date"], errors="coerce").dt.normalize()

    detailed_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    expected_rows: list[dict[str, object]] = []
    all_probabilities: list[float] = []
    total_observed_exact = 0

    for source_experiment, (display_experiment, stem) in EXPERIMENTS.items():
        experiment_scans = scans[
            (scans["Experiment"] == source_experiment) & scans["Date"].notna()
        ].copy()
        coverage_days = load_coverage_days(
            REPORTS / f"{stem}_pipeline_predictions.csv"
        )
        alert_days, alert_rows = load_alerts(
            REPORTS / f"{stem}_pipeline_alerts_only.csv"
        )

        covered_pm1_count = 0
        observed_pm1_count = 0
        exact_count = 0
        observed_exact_count = 0
        probabilities: list[float] = []

        for _, scan in experiment_scans.iterrows():
            cow = scan["Cow"]
            scan_date = scan["Date"]
            window = window_days(scan_date)
            cow_coverage = coverage_days.get(cow, set())
            cow_alerts = alert_days.get(cow, set())

            covered_pm1 = bool(window & cow_coverage)
            covered_same_day = scan_date in cow_coverage
            alert_present = covered_pm1 and bool(window & cow_alerts)
            alert_count = int(
                (
                    (alert_rows["Cow"] == cow)
                    & (alert_rows["T"].isin(window))
                ).sum()
            )

            covered_pm1_count += int(covered_pm1)
            observed_pm1_count += int(alert_present)

            if covered_same_day:
                exact_count += 1
                observed_exact = bool(window & cow_alerts)
                observed_exact_count += int(observed_exact)

                eligible_days = list(cow_coverage)
                expected_hits = sum(
                    bool(window_days(day) & cow_alerts) for day in eligible_days
                )
                probability = expected_hits / len(eligible_days)
                probabilities.append(probability)
                all_probabilities.append(probability)

            row = {
                "Experiment": display_experiment,
                "Cow": cow,
                "scan_date": scan_date.date(),
                "icetag_covered_pm1j": int(covered_pm1),
                "icetag_covered_same_day": int(covered_same_day),
                "alert_present_pm1j": int(alert_present),
                "n_alerts_pm1j": alert_count,
            }
            row.update(
                {
                    behaviour: scan.get(behaviour, np.nan)
                    for behaviour in BEHAVIOURS
                }
            )
            detailed_rows.append(row)

        summary_rows.append(
            {
                "Experiment": display_experiment,
                "scans_dates": len(experiment_scans),
                "scans_couverts_icetag_pm1j": covered_pm1_count,
                "scans_avec_alerte_pm1j": observed_pm1_count,
                "taux_concordance_pm1j_pct": round(
                    100 * observed_pm1_count / covered_pm1_count,
                    1,
                )
                if covered_pm1_count
                else np.nan,
            }
        )

        expected_count = float(sum(probabilities))
        expected_rows.append(
            {
                "Experiment": display_experiment,
                "scans_couverts_meme_jour": exact_count,
                "scans_avec_alerte_pm1j_observes": observed_exact_count,
                "taux_observe_pct": round(
                    100 * observed_exact_count / exact_count,
                    1,
                )
                if exact_count
                else np.nan,
                "scans_avec_alerte_attendus": round(expected_count, 2),
                "taux_attendu_pct": round(100 * expected_count / exact_count, 1)
                if exact_count
                else np.nan,
                "ratio_observe_attendu": round(
                    observed_exact_count / expected_count,
                    2,
                )
                if expected_count
                else np.nan,
            }
        )
        total_observed_exact += observed_exact_count

    detailed = pd.DataFrame(detailed_rows)
    summary = pd.DataFrame(summary_rows)
    expected = pd.DataFrame(expected_rows)

    total_exact = len(all_probabilities)
    total_expected = float(sum(all_probabilities))
    p_upper = poisson_binomial_upper_tail(
        all_probabilities,
        total_observed_exact,
    )
    global_control = pd.DataFrame(
        [
            {
                "scans_couverts_meme_jour": total_exact,
                "scans_avec_alerte_pm1j_observes": total_observed_exact,
                "taux_observe_pct": round(
                    100 * total_observed_exact / total_exact,
                    1,
                ),
                "scans_avec_alerte_attendus": round(total_expected, 2),
                "taux_attendu_pct": round(100 * total_expected / total_exact, 1),
                "difference_points": round(
                    100
                    * (total_observed_exact - total_expected)
                    / total_exact,
                    1,
                ),
                "p_unilateral_observe_superieur_attendu": round(p_upper, 3),
            }
        ]
    )

    write_outputs(detailed, summary, expected, global_control)
    print(summary.to_string(index=False))
    print()
    print(global_control.to_string(index=False))


if __name__ == "__main__":
    main()
