"""Validation reproductible de la conversion sur l'exemple du 27 mars."""

import argparse
import importlib.util
import json
import tempfile
import time
from pathlib import Path

import numpy as np
import pandas as pd


TOOLKIT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_CODE = TOOLKIT_ROOT / 'code'
if not CLEAN_CODE.exists():
    CLEAN_CODE = TOOLKIT_ROOT / '02_SCRIPTS_PYTHON'
PROJECT_ROOT = TOOLKIT_ROOT.parent
RECEIVED_CODE = PROJECT_ROOT / 'UQAM - Matlab vers Python (Aliou)' / 'Scripts Python (post processing)'
EXAMPLE = PROJECT_ROOT / 'UQAM - Matlab vers Python (Aliou)' / '27MARS-V1(Exemple)'
DEFAULT_MAT = EXAMPLE / 'McGillWi2024SNA_SNA_OUT_27MAR2024_360V1_All_0_new_cow_gs.mat'


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def max_abs(left, right):
    left = np.asarray(left, dtype=float)
    right = np.asarray(right, dtype=float)
    both = np.isfinite(left) & np.isfinite(right)
    if not both.any():
        return 0.0
    return float(np.max(np.abs(left[both] - right[both])))


def compare_dicts(name, old_values, new_values, summary, per_cow):
    cows = sorted(set(old_values) | set(new_values))
    diffs = []
    for cow in cows:
        old = old_values.get(cow, np.nan)
        new = new_values.get(cow, np.nan)
        diff = abs(old - new) if np.isfinite(old) and np.isfinite(new) else np.nan
        diffs.append(diff)
        per_cow.append({
            'metric': name,
            'cow': cow,
            'received_python': old,
            'cleaned_python': new,
            'absolute_difference': diff,
        })
    finite = [value for value in diffs if np.isfinite(value)]
    summary.append({
        'check': name,
        'received_value': '',
        'cleaned_value': '',
        'max_absolute_difference': max(finite, default=0.0),
        'status': 'PASS' if max(finite, default=0.0) <= 1e-12 else 'FAIL',
    })


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mat', type=Path, default=DEFAULT_MAT)
    parser.add_argument('--received-code-dir', type=Path, default=RECEIVED_CODE)
    parser.add_argument('--clean-code-dir', type=Path, default=CLEAN_CODE)
    parser.add_argument(
        '--output-dir', type=Path,
        default=TOOLKIT_ROOT / 'results' / 'validation')
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)

    old_converter = load_module(
        'received_converter', args.received_code_dir / 'make_traj_csv.py')
    new_converter = load_module(
        'clean_converter', args.clean_code_dir / 'make_traj_csv.py')
    old_metrics = load_module(
        'received_metrics', args.received_code_dir / 'compute_metrics.py')
    new_metrics = load_module(
        'clean_metrics', args.clean_code_dir / 'compute_metrics.py')

    with tempfile.TemporaryDirectory() as old_tmp, tempfile.TemporaryDirectory() as new_tmp:
        old_trajectories = old_converter.load_mat_file(str(args.mat))
        new_trajectories = new_converter.load_mat_file(str(args.mat))
        old_table = old_converter.make_csv_continuous(
            old_trajectories, '27MARS_validation', old_tmp, fps=30)
        new_table = new_converter.make_csv_continuous(
            new_trajectories, '27MARS_validation', new_tmp, fps=30)

    summary = []
    per_cow = []
    keys = ['name', 'all_frames']
    old_table = old_table.sort_values(keys).reset_index(drop=True)
    new_table = new_table.sort_values(keys).reset_index(drop=True)
    numeric_columns = [
        'frames', 'BBl_left', 'BBl_top', 'BBl_width', 'BBl_height',
        'BBf_left', 'BBf_top', 'BBf_width', 'BBf_height', 'Center_X', 'Center_Y',
    ]
    conversion_diff = max_abs(
        old_table[numeric_columns].to_numpy(),
        new_table[numeric_columns].to_numpy())
    same_keys = old_table[keys].equals(new_table[keys])
    summary.append({
        'check': 'conversion_table',
        'received_value': len(old_table),
        'cleaned_value': len(new_table),
        'max_absolute_difference': conversion_diff,
        'status': 'PASS' if same_keys and conversion_diff == 0 else 'FAIL',
    })

    old_distance = old_metrics.compute_distance_matrix_continuous(old_table)
    new_distance = new_metrics.compute_distance_matrix_continuous(new_table)
    distance_diff = max_abs(old_distance.to_numpy(), new_distance.to_numpy())
    summary.append({
        'check': 'distance_matrix',
        'received_value': int(old_distance.notna().sum().sum()),
        'cleaned_value': int(new_distance.notna().sum().sum()),
        'max_absolute_difference': distance_diff,
        'status': 'PASS' if distance_diff <= 1e-12 else 'FAIL',
    })

    compare_dicts(
        'total_distance',
        old_metrics.compute_total_distance(old_table, 'continuous', 30),
        new_metrics.compute_total_distance(new_table, 'continuous', 30),
        summary, per_cow)
    compare_dicts(
        'mean_velocity',
        old_metrics.compute_mean_velocity(old_table, 'continuous', 30),
        new_metrics.compute_mean_velocity(new_table, 'continuous', 30),
        summary, per_cow)
    compare_dicts(
        'mean_acceleration',
        old_metrics.compute_mean_acceleration(old_table, 'continuous', 30),
        new_metrics.compute_mean_acceleration(new_table, 'continuous', 30),
        summary, per_cow)

    first_cow = sorted(new_table['name'].unique())[0]
    subset = new_table.query('name == @first_cow').head(2000)
    bb = subset[['BBf_left', 'BBf_top', 'BBf_width', 'BBf_height']].to_numpy()
    original = new_metrics.compute_center_BB(bb)
    start = time.perf_counter()
    old_smoothed = old_metrics._smooth_trajectory(original, bb, bb_scale=0.5)
    old_seconds = time.perf_counter() - start
    start = time.perf_counter()
    new_smoothed = new_metrics._smooth_trajectory(original, bb, bb_scale=0.5)
    new_seconds = time.perf_counter() - start
    smoothing_diff = max_abs(old_smoothed, new_smoothed)
    summary.append({
        'check': 'orientation_smoothing_2000_frames',
        'received_value': old_seconds,
        'cleaned_value': new_seconds,
        'max_absolute_difference': smoothing_diff,
        'status': 'PASS' if smoothing_diff <= 1e-12 else 'FAIL',
    })

    summary_df = pd.DataFrame(summary)
    per_cow_df = pd.DataFrame(per_cow)
    summary_df.to_csv(output / 'parity_summary.csv', index=False)
    per_cow_df.to_csv(output / 'per_cow_metrics_comparison.csv', index=False)
    report = {
        'input_mat': str(args.mat.resolve()),
        'received_code_dir': str(args.received_code_dir.resolve()),
        'clean_code_dir': str(args.clean_code_dir.resolve()),
        'rows': int(len(new_table)),
        'cows': int(new_table['name'].nunique()),
        'sampled_frames': int(new_table['all_frames'].nunique()),
        'manual_rows': int(new_table['frames'].notna().sum()),
        'all_checks_passed': bool(summary_df['status'].eq('PASS').all()),
        'matlab_runtime_comparison': (
            'Not executed: no licensed MATLAB runtime or reference MATLAB '
            'outputs were supplied. Formula-level correspondence is reviewed separately.'
        ),
    }
    (output / 'validation_report.json').write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(summary_df.to_string(index=False))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if not report['all_checks_passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
