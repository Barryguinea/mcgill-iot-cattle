import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd


TOOLKIT_ROOT = Path(__file__).resolve().parents[1]
CODE_DIR = TOOLKIT_ROOT / 'code'
if not CODE_DIR.exists():
    CODE_DIR = TOOLKIT_ROOT / '02_SCRIPTS_PYTHON'
sys.path.insert(0, str(CODE_DIR))

import compute_metrics as metrics
import make_traj_csv as converter


def continuous_table():
    rows = []
    trajectories = {
        'A': [(0.0, 0.0), (3.0, 4.0), (6.0, 8.0)],
        'B': [(0.0, 4.0), (3.0, 8.0), (6.0, 12.0)],
    }
    for name, centers in trajectories.items():
        for frame, (cx, cy) in enumerate(centers, start=1):
            rows.append({
                'all_frames': frame,
                'frames': frame,
                'video': 'synthetic',
                'sampling': 'continuous',
                'name': name,
                'BBl_left': cx - 1,
                'BBl_top': cy - 1,
                'BBl_width': 2,
                'BBl_height': 2,
                'BBf_left': cx - 1,
                'BBf_top': cy - 1,
                'BBf_width': 2,
                'BBf_height': 2,
                'Center_X': cx,
                'Center_Y': cy,
            })
    return pd.DataFrame(rows)


class TestConversion(unittest.TestCase):
    def test_center_of_bounding_box(self):
        centers = metrics.compute_center_BB(np.array([[1, 2, 4, 6]]))
        np.testing.assert_allclose(centers, [[3, 5]])

    def test_continuous_core_metrics(self):
        table = continuous_table()
        distances = metrics.compute_distance_matrix_continuous(table)
        self.assertAlmostEqual(distances.loc['A', 'B'], 4.0)
        self.assertTrue(np.isnan(distances.loc['B', 'A']))

        total = metrics.compute_total_distance(table, 'continuous', fps=1)
        velocity = metrics.compute_mean_velocity(table, 'continuous', fps=1)
        acceleration = metrics.compute_mean_acceleration(
            table, 'continuous', fps=1)
        self.assertAlmostEqual(total['A'], 10.0)
        self.assertAlmostEqual(velocity['A'], 5.0)
        self.assertAlmostEqual(acceleration['A'], 0.0)

    def test_sparse_summary_uses_sparse_bounding_boxes(self):
        trajectories = [{
            'name': 'Cow1',
            'frames': np.array([30]),
            'all_frames': np.array([30]),
            'BBl': np.array([[10, 20, 8, 6]], dtype=float),
            'BBf': np.array([[10, 20, 8, 6]], dtype=float),
        }]
        with tempfile.TemporaryDirectory() as tmp:
            table = converter.make_csv_sparse(
                trajectories, 'sparse_test', tmp, fps=30)
            converter.make_summary_and_plots(
                table, 'sparse', tmp, Nframes=100, video_file=None)
            self.assertTrue((Path(tmp) / 'cow_trajectory_1.png').exists())

    def test_validation_rejects_duplicate_cow_frame(self):
        table = continuous_table()
        duplicated = pd.concat([table, table.iloc[[0]]], ignore_index=True)
        with self.assertRaisesRegex(ValueError, 'doublons'):
            metrics.validate_metric_table(duplicated, 'continuous')

    def test_occupancy_exports_visual_normalized_and_raw_maps(self):
        table = continuous_table().query("name == 'A'")
        with tempfile.TemporaryDirectory() as tmp:
            outputs = metrics.compute_occupancy_maps(
                table, 'continuous', tmp, 'synthetic', video_file=None)
            self.assertEqual(len(outputs), 1)
            for key in ('heatmap', 'normalized_map', 'raw_counts'):
                self.assertTrue(Path(outputs[0][key]).exists(), key)
            raw = np.load(outputs[0]['raw_counts'])
            self.assertGreater(raw.max(), 0)

    def test_optimized_smoothing_matches_contiguous_reference(self):
        original = np.array([
            [0.0, 0.0], [0.2, 0.1], [0.3, 0.2], [5.0, 5.0], [5.2, 5.1]
        ])
        bb = np.column_stack([
            original[:, 0] - 1,
            original[:, 1] - 1,
            np.full(len(original), 4.0),
            np.full(len(original), 4.0),
        ])

        expected = []
        for i, (cx, cy) in enumerate(original):
            inside = (
                (original[:, 0] >= cx - 1)
                & (original[:, 0] <= cx + 1)
                & (original[:, 1] >= cy - 1)
                & (original[:, 1] <= cy + 1)
            )
            indices = np.flatnonzero(inside)
            blocks = np.split(indices, np.where(np.diff(indices) != 1)[0] + 1)
            block = next(block for block in blocks if i in block)
            expected.append(original[block].mean(axis=0))

        actual = metrics._smooth_trajectory(original, bb, bb_scale=0.5)
        np.testing.assert_allclose(actual, expected)


if __name__ == '__main__':
    unittest.main()
