"""
compute_metrics.py
------------------
Traduit l'etape 3 du script MATLAB post-processing.
  - 3.1 : Orientation des vaches (mode continu = tangente a la trajectoire)
  - 3.2 : Matrice de distances inter-vaches
  - 3.3 : Distance totale parcourue
  - 3.4 : Vitesse moyenne
  - 3.5 : Acceleration moyenne
  - 3.6 : Cartes d'occupation (heatmaps)
  - 3.8 : Video complete avec BB, noms et orientations

Usage:
    python compute_metrics.py --traj-csv TRAJ.csv --output-dir RESULTS \
        --sampling continuous --fps 30
"""

import argparse
import numpy as np
import pandas as pd
import os
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def compute_center_BB(bb):
    """
    Centre d'une bounding box.
    bb : array (N, 4) -> [left, top, width, height]
    Retourne (N, 2) -> [center_x, center_y]
    """
    bb = np.atleast_2d(bb)
    return np.column_stack([bb[:, 0] + bb[:, 2] / 2,
                            bb[:, 1] + bb[:, 3] / 2])


def make_palette():
    """Palette de couleurs pour distinguer les vaches."""
    nbc = 4
    dc  = np.linspace(0, 1, nbc)
    palette = []
    for r in dc:
        for g in dc:
            for b in dc:
                palette.append([r, g, b])
    palette = np.array(palette)
    order   = np.argsort(palette.sum(axis=1))[::-1]
    return palette[order]

PALETTE = make_palette()


def validate_metric_table(tbl, sampling_type):
    """Valide le schéma et l'ordre temporel avant tout calcul."""
    common = {'frames', 'video', 'sampling', 'name'}
    continuous = {
        'all_frames', 'BBl_left', 'BBl_top', 'BBl_width', 'BBl_height',
        'BBf_left', 'BBf_top', 'BBf_width', 'BBf_height',
    }
    sparse = {'time_in_min', 'BB_left', 'BB_top', 'BB_width', 'BB_height'}
    required = common | (continuous if sampling_type == 'continuous' else sparse)
    missing = sorted(required.difference(tbl.columns))
    if missing:
        raise ValueError(f"Colonnes manquantes pour {sampling_type}: {missing}")
    if not tbl['sampling'].dropna().astype(str).eq(sampling_type).all():
        raise ValueError("La colonne sampling ne correspond pas au mode demandé")
    if tbl['name'].isna().any() or tbl['name'].astype(str).str.strip().eq('').any():
        raise ValueError("Au moins un identifiant de vache est vide")

    frame_col = 'all_frames' if sampling_type == 'continuous' else 'frames'
    duplicated = int(tbl.duplicated(['name', frame_col]).sum())
    if duplicated:
        raise ValueError(f"{duplicated} doublons vache-frame empêchent une parité fiable")
    for name, sub in tbl.groupby('name', sort=False):
        if not sub[frame_col].is_monotonic_increasing:
            raise ValueError(f"Frames non triées pour {name}")
    return {
        'rows': int(len(tbl)),
        'cows': int(tbl['name'].nunique()),
        'sampled_frames': int(tbl[frame_col].nunique()),
    }


# =========================================================================
# bb2orientation : calcul de l'orientation par tangente a la trajectoire
# =========================================================================

def _smooth_trajectory(original, bb, bb_scale=0.5):
    """
    Etape 1 : lissage spatial de la trajectoire.
    Pour chaque point i, on moyenne tous les points qui tombent
    dans une boite reduite (bb_scale * BB) autour du point i.
    """
    Nf = len(original)
    xy = np.zeros((Nf, 2))

    for i in range(Nf):
        cx, cy = original[i]
        W = bb[i, 2]
        H = bb[i, 3]
        bx = cx - bb_scale * W / 2
        by = cy - bb_scale * H / 2
        bw = bb_scale * W
        bh = bb_scale * H

        inbox = (
            (original[:, 0] >= bx) & (original[:, 0] <= bx + bw) &
            (original[:, 1] >= by) & (original[:, 1] <= by + bh)
        )
        changes = np.diff(np.concatenate([[False], inbox, [False]]).astype(int))
        starts = np.where(changes == 1)[0]
        ends = np.where(changes == -1)[0]
        block = next(
            ((start, end) for start, end in zip(starts, ends)
             if start <= i < end),
            (i, i + 1),
        )
        xy[i] = original[block[0]:block[1]].mean(axis=0)

    return xy


def _decimate_trajectory(original, smoothed, bb, bb_scale=0.5):
    """
    Etape 2 : decimation de la trajectoire lissee.
    On ne retient un nouveau point que lorsqu'on sort de la BB courante.
    """
    Nf    = len(original)
    traj  = original.copy().astype(float)
    Ctraj = smoothed.copy()

    Pstart = Ctraj[0]
    dist   = np.linalg.norm(Pstart - traj, axis=1)
    v      = int(np.argmin(dist))

    cx, cy = compute_center_BB(bb[v:v+1])[0]
    W, H   = bb[v, 2], bb[v, 3]
    bx = cx - bb_scale * W / 2
    by = cy - bb_scale * H / 2
    bw = bb_scale * W
    bh = bb_scale * H

    outbox  = ~((Ctraj[:, 0] >= bx) & (Ctraj[:, 0] <= bx + bw) &
                (Ctraj[:, 1] >= by) & (Ctraj[:, 1] <= by + bh))
    pos_arr = np.where(outbox)[0]

    if len(pos_arr) == 0 or np.any(np.isnan(Ctraj[pos_arr[0]])):
        return np.array([[0,      Ctraj[0, 0],  Ctraj[0, 1]],
                         [Nf - 1, Ctraj[-1, 0], Ctraj[-1, 1]]])

    nnew      = int(pos_arr[0])
    Pnew      = Ctraj[nnew]
    decimated = np.array([[0, Ctraj[0, 0], Ctraj[0, 1]],
                          [nnew, Pnew[0], Pnew[1]]])

    last_original = v
    stopit        = False

    while not stopit:
        Pstart = Pnew
        n      = nnew

        if last_original >= Nf - 1:
            break

        traj_tmp = traj.copy()
        traj_tmp[:last_original + 1] = np.inf
        dist = np.linalg.norm(Pstart - traj_tmp, axis=1)

        if np.all(~np.isfinite(dist)):
            break

        v_new = int(np.nanargmin(dist))

        if v_new <= last_original:
            break

        last_original = v_new

        cx, cy = compute_center_BB(bb[v_new:v_new+1])[0]
        W, H   = bb[v_new, 2], bb[v_new, 3]
        bx = cx - bb_scale * W / 2
        by = cy - bb_scale * H / 2
        bw = bb_scale * W
        bh = bb_scale * H

        outbox_mask = ~((Ctraj[:, 0] >= bx) & (Ctraj[:, 0] <= bx + bw) &
                        (Ctraj[:, 1] >= by) & (Ctraj[:, 1] <= by + bh))
        outbox_mask[:n] = False
        pos_arr = np.where(outbox_mask)[0]

        if len(pos_arr) == 0:
            break

        nnew = int(pos_arr[0])
        Pnew = Ctraj[nnew]

        if np.any(np.isnan(Pnew)):
            break

        new_row = np.array([nnew, Pnew[0], Pnew[1]])

        if np.allclose(new_row, decimated[-1]):
            stopit = True
        else:
            decimated = np.vstack([decimated, new_row])

    last_valid = Nf - 1
    while last_valid > 0 and np.any(np.isnan(Ctraj[last_valid])):
        last_valid -= 1
    last_row = np.array([last_valid, Ctraj[last_valid, 0], Ctraj[last_valid, 1]])
    if not np.allclose(last_row, decimated[-1]):
        decimated = np.vstack([decimated, last_row])

    return decimated


def _compute_orientations_from_decim(original, smoothed, decim, all_frames):
    """
    Etape 3 : tangente locale de la trajectoire decimee comme direction.
    """
    Nf        = len(original)
    decim_idx = decim[:, 0].astype(int)
    decim_xy  = decim[:, 1:3]
    decim_tg  = np.diff(decim_xy, axis=0)
    decim_tg  = np.vstack([decim_tg, decim_tg[-1]])
    cow_dir   = np.zeros((Nf, 2))

    for n in range(Nf):
        f  = all_frames[n]
        pt = original[n]

        frames_decim = all_frames[decim_idx]
        before = np.where(frames_decim <= f)[0]
        after  = np.where(frames_decim >= f)[0]

        if len(before) == 0:
            idx_section = [0]
        elif len(after) == 0:
            idx_section = [len(decim_idx) - 1]
        else:
            idx_section = list(set([before[-1], after[0]]))

        section_xy  = decim_xy[idx_section]
        dist_section = np.linalg.norm(pt - section_xy, axis=1)
        best        = idx_section[int(np.argmin(dist_section))]
        cow_dir[n]  = decim_tg[best]

    return cow_dir


def bb2orientation(tbl):
    """
    Calcule l'orientation de chaque vache frame par frame.
    Retourne un dict {nom_vache: array (Nf, 2)} de vecteurs unitaires.
    """
    cow_list = sorted(tbl['name'].unique())
    results  = {}

    for c, name in enumerate(cow_list):
        print(f'  [{c+1}/{len(cow_list)}] Calcul orientation : {name}')

        sub = tbl[tbl['name'] == name].copy()
        sub = sub.dropna(subset=['BBf_left'])

        if len(sub) < 3:
            print(f'    Pas assez de frames ({len(sub)}), orientation = NaN.')
            results[name] = np.full((len(sub), 2), np.nan)
            continue

        all_frames = sub['all_frames'].values
        bb         = sub[['BBf_left', 'BBf_top', 'BBf_width', 'BBf_height']].values
        original   = compute_center_BB(bb)
        Nf         = len(original)

        print(f'    {Nf} frames. Lissage...')
        smoothed = _smooth_trajectory(original, bb, bb_scale=0.5)

        print(f'    Decimation...')
        decim = _decimate_trajectory(original, smoothed, bb, bb_scale=0.5)
        print(f'    {len(decim)} points decimaux. Tangentes...')

        cow_dir = _compute_orientations_from_decim(original, smoothed,
                                                    decim, all_frames)

        # Normaliser
        norms = np.linalg.norm(cow_dir, axis=1)

        # Fallback si la vache ne bouge pas (tangente decimee nulle)
        if (norms < 1e-10).all():
            print(f'    Tangente nulle -> fallback sur trajectoire originale.')
            cow_dir = np.diff(original, axis=0)
            cow_dir = np.vstack([cow_dir, cow_dir[-1]])
            norms   = np.linalg.norm(cow_dir, axis=1)

        norms_2d = norms[:, np.newaxis]
        norms_2d[norms_2d < 1e-10] = 1
        results[name] = cow_dir / norms_2d

    return results


def save_orientation_csv(tbl, cow_directions, res_folder):
    """Sauvegarde les orientations dans cow_orientations.csv."""
    os.makedirs(res_folder, exist_ok=True)
    csv_path = os.path.join(res_folder, 'cow_orientations.csv')
    rows = []
    for name, orientations in cow_directions.items():
        sub    = tbl[tbl['name'] == name].dropna(subset=['BBf_left'])
        frames = sub['all_frames'].values
        for n in range(len(frames)):
            rows.append({
                'frame':         int(frames[n]),
                'sampling':      'continuous',
                'name':          name,
                'orientation_x': orientations[n, 0],
                'orientation_y': orientations[n, 1],
            })
    pd.DataFrame(rows).to_csv(csv_path, index=False)
    print(f'  Orientations sauvegardees : {csv_path} ({len(rows)} lignes)')
    return csv_path


def create_sparse_orientation_csv(tbl, video_file, res_folder, overwrite=False):
    """Saisie interactive des orientations sparse, comme dans Matlab.

    Clic gauche: définir la direction depuis le centre de la BB.
    Entrée: confirmer le point courant. Q ou Échap: interrompre sans écraser.
    """
    import cv2

    if not video_file or not os.path.exists(video_file):
        raise FileNotFoundError("La saisie sparse nécessite la vidéo source")
    os.makedirs(res_folder, exist_ok=True)
    csv_path = os.path.join(res_folder, 'cow_orientations.csv')
    if os.path.exists(csv_path) and not overwrite:
        existing = pd.read_csv(csv_path)
        required = {'frame', 'sampling', 'name', 'orientation_x', 'orientation_y'}
        if required.issubset(existing.columns):
            print(f'  Orientations existantes réutilisées : {csv_path}')
            return csv_path
        raise ValueError(f"Schéma invalide dans {csv_path}")

    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        raise RuntimeError(f"Impossible d'ouvrir la vidéo : {video_file}")

    window = 'Orientation sparse - clic, puis Entree; Q pour annuler'
    rows = []
    ordered = tbl.sort_values(['name', 'frames']).reset_index(drop=True)
    try:
        for index, row in ordered.iterrows():
            frame_number = int(row['frames'])
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
            ok, frame = cap.read()
            if not ok:
                raise RuntimeError(f"Frame {frame_number} illisible")

            left, top, width, height = [
                int(round(row[col]))
                for col in ['BB_left', 'BB_top', 'BB_width', 'BB_height']
            ]
            center = (left + width // 2, top + height // 2)
            selected = {'point': None}

            def on_mouse(event, x, y, flags, param):
                if event == cv2.EVENT_LBUTTONDOWN:
                    selected['point'] = (x, y)

            cv2.namedWindow(window, cv2.WINDOW_NORMAL)
            cv2.setMouseCallback(window, on_mouse)
            while True:
                shown = frame.copy()
                cv2.rectangle(shown, (left, top), (left + width, top + height), (0, 255, 255), 2)
                cv2.circle(shown, center, 5, (0, 255, 255), -1)
                if selected['point'] is not None:
                    cv2.arrowedLine(shown, center, selected['point'], (0, 0, 255), 3, tipLength=0.2)
                label = f"{index + 1}/{len(ordered)} {row['name']} frame {frame_number}"
                cv2.putText(shown, label, (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.imshow(window, shown)
                key = cv2.waitKey(30) & 0xFF
                if key in (13, 10) and selected['point'] is not None:
                    break
                if key in (27, ord('q')):
                    raise KeyboardInterrupt("Saisie d'orientation annulée")

            vector = np.array(selected['point'], dtype=float) - np.array(center, dtype=float)
            norm = np.linalg.norm(vector)
            if norm == 0:
                raise ValueError(f"Orientation nulle pour {row['name']} frame {frame_number}")
            vector /= norm
            rows.append({
                'frame': frame_number,
                'sampling': 'sparse',
                'name': row['name'],
                'orientation_x': float(vector[0]),
                'orientation_y': float(vector[1]),
            })
    finally:
        cap.release()
        cv2.destroyAllWindows()

    pd.DataFrame(rows).to_csv(csv_path, index=False)
    print(f'  Orientations sparse sauvegardées : {csv_path} ({len(rows)} lignes)')
    return csv_path


# =========================================================================
# 3.2 Matrice de distances
# =========================================================================

def compute_distance_matrix_continuous(tbl):
    """Distance moyenne inter-vaches sur toute la video (mode continu)."""
    cow_list  = sorted(tbl['name'].unique())
    Ncows     = len(cow_list)
    distances = np.full((Ncows, Ncows), np.nan)

    for i, name1 in enumerate(cow_list):
        sub1  = tbl[tbl['name'] == name1].dropna(subset=['BBf_left'])
        frs1  = sub1['all_frames'].values
        traj1 = compute_center_BB(
            sub1[['BBf_left', 'BBf_top', 'BBf_width', 'BBf_height']].values)

        for j, name2 in enumerate(cow_list):
            if j <= i:
                continue
            sub2  = tbl[tbl['name'] == name2].dropna(subset=['BBf_left'])
            frs2  = sub2['all_frames'].values
            traj2 = compute_center_BB(
                sub2[['BBf_left', 'BBf_top', 'BBf_width', 'BBf_height']].values)

            common, idx1, idx2 = np.intersect1d(frs1, frs2, return_indices=True)
            if len(common) > 0:
                diff = traj1[idx1] - traj2[idx2]
                distances[i, j] = np.sqrt((diff**2).sum(axis=1)).mean()

    return pd.DataFrame(distances, index=cow_list, columns=cow_list)


def compute_distance_matrix_sparse(tbl):
    """Distance inter-vaches par instant d'echantillonnage (mode sparse)."""
    cow_list     = sorted(tbl['name'].unique())
    Ncows        = len(cow_list)
    instant_list = sorted(tbl['time_in_min'].unique())
    results      = {}

    for t in instant_list:
        print(f'  Distance matrix instant {t} min...')
        distances = np.full((Ncows, Ncows), np.nan)
        sub_t     = tbl[tbl['time_in_min'] == t]

        for i, name1 in enumerate(cow_list):
            sub1 = sub_t[sub_t['name'] == name1]
            if len(sub1) == 0:
                continue
            frs1  = sub1['frames'].values
            traj1 = compute_center_BB(
                sub1[['BB_left', 'BB_top', 'BB_width', 'BB_height']].values)

            for j, name2 in enumerate(cow_list):
                if j <= i:
                    continue
                sub2 = sub_t[sub_t['name'] == name2]
                if len(sub2) == 0:
                    continue
                frs2  = sub2['frames'].values
                traj2 = compute_center_BB(
                    sub2[['BB_left', 'BB_top', 'BB_width', 'BB_height']].values)

                common, idx1, idx2 = np.intersect1d(frs1, frs2,
                                                     return_indices=True)
                if len(common) > 0:
                    diff = traj1[idx1] - traj2[idx2]
                    distances[i, j] = np.sqrt((diff**2).sum(axis=1)).mean()

        results[t] = pd.DataFrame(distances, index=cow_list, columns=cow_list)

    return results


def save_distance_matrix(dist_results, res_folder, video_name, sampling_type):
    """Sauvegarde la ou les matrices de distances en CSV."""
    os.makedirs(res_folder, exist_ok=True)
    if sampling_type == 'continuous':
        csv_path = os.path.join(res_folder, f'{video_name}_distance_matrix.csv')
        dist_results.to_csv(csv_path)
        print(f'  Matrice sauvegardee : {csv_path}')
    else:
        for t, df in dist_results.items():
            csv_path = os.path.join(res_folder,
                                    f'{video_name}_distance_matrix_{t}min.csv')
            df.to_csv(csv_path)
            print(f'  Matrice sauvegardee : {csv_path}')


# =========================================================================
# 3.3 Distance totale
# =========================================================================

def compute_total_distance(tbl, sampling_type, fps):
    """Distance totale parcourue par chaque vache (en pixels)."""
    cow_list = sorted(tbl['name'].unique())
    results  = {}

    for name in cow_list:
        sub = tbl[tbl['name'] == name]
        if sampling_type == 'continuous':
            sub     = sub.dropna(subset=['BBf_left'])
            bb_cols = ['BBf_left', 'BBf_top', 'BBf_width', 'BBf_height']
        else:
            bb_cols = ['BB_left', 'BB_top', 'BB_width', 'BB_height']

        if len(sub) < 2:
            results[name] = np.nan
            continue

        traj  = compute_center_BB(sub[bb_cols].values)
        dpos  = np.diff(traj, axis=0)
        results[name] = float(np.sqrt((dpos**2).sum(axis=1)).sum())

    return results


# =========================================================================
# 3.4 Vitesse moyenne
# =========================================================================

def compute_mean_velocity(tbl, sampling_type, fps):
    """Vitesse moyenne de chaque vache (px/s)."""
    cow_list = sorted(tbl['name'].unique())
    results  = {}

    for name in cow_list:
        sub = tbl[tbl['name'] == name]
        if sampling_type == 'continuous':
            sub     = sub.dropna(subset=['BBf_left'])
            bb_cols = ['BBf_left', 'BBf_top', 'BBf_width', 'BBf_height']
            fr_col  = 'all_frames'
        else:
            bb_cols = ['BB_left', 'BB_top', 'BB_width', 'BB_height']
            fr_col  = 'frames'

        if len(sub) < 2:
            results[name] = np.nan
            continue

        traj   = compute_center_BB(sub[bb_cols].values)
        frames = sub[fr_col].values
        dpos   = np.diff(traj, axis=0)
        dtime  = np.diff(frames) / fps
        dtime[dtime == 0] = np.nan
        vel    = dpos / dtime[:, None]
        results[name] = float(np.nanmean(np.sqrt((vel**2).sum(axis=1))))

    return results


# =========================================================================
# 3.5 Acceleration moyenne
# =========================================================================

def compute_mean_acceleration(tbl, sampling_type, fps):
    """Acceleration moyenne de chaque vache (px/s2)."""
    cow_list = sorted(tbl['name'].unique())
    results  = {}

    for name in cow_list:
        sub = tbl[tbl['name'] == name]
        if sampling_type == 'continuous':
            sub     = sub.dropna(subset=['BBf_left'])
            bb_cols = ['BBf_left', 'BBf_top', 'BBf_width', 'BBf_height']
            fr_col  = 'all_frames'
        else:
            bb_cols = ['BB_left', 'BB_top', 'BB_width', 'BB_height']
            fr_col  = 'frames'

        if len(sub) < 3:
            results[name] = np.nan
            continue

        traj   = compute_center_BB(sub[bb_cols].values)
        frames = sub[fr_col].values
        dpos   = np.diff(traj, axis=0)
        dtime  = np.diff(frames) / fps
        dtime[dtime == 0] = np.nan
        vel    = dpos / dtime[:, None]
        dvel   = np.diff(vel, axis=0)
        acc    = dvel / dtime[:-1, None]
        results[name] = float(np.nanmean(np.sqrt((acc**2).sum(axis=1))))

    return results


def save_scalar_metric(results, res_folder, video_name, sampling_type,
                       filename_suffix, col_name):
    """Sauvegarde un dict {nom: valeur} dans un CSV."""
    os.makedirs(res_folder, exist_ok=True)
    csv_path = os.path.join(res_folder, f'{video_name}_{filename_suffix}.csv')
    rows = [{'name': name, 'video': video_name,
              'sampling': sampling_type, col_name: val}
            for name, val in results.items()]
    pd.DataFrame(rows).to_csv(csv_path, index=False)
    print(f'  Sauvegarde : {csv_path}')
    return csv_path


# =========================================================================
# 3.6 Cartes d'occupation
# =========================================================================

def compute_occupancy_maps(tbl, sampling_type, res_folder, video_name,
                           video_file):
    """Cartes d'occupation visuelles et cartes normalisees par vache."""
    cow_list = sorted(tbl['name'].unique())
    out_dir  = os.path.join(res_folder, 'occupancy_maps')
    os.makedirs(out_dir, exist_ok=True)

    # Lire le premier frame de la video comme fond
    bg_frame = None
    video_h, video_w = None, None
    if video_file and os.path.exists(video_file):
        try:
            import cv2
            cap     = cv2.VideoCapture(video_file)
            ret, fr = cap.read()
            video_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            video_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            cap.release()
            if ret:
                bg_frame = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(f'  Impossible de lire la video : {e}')

    # Si pas de video, estimer les dimensions depuis les bounding boxes
    if video_h is None:
        if sampling_type == 'continuous':
            video_w = int(tbl[['BBf_left','BBf_width']].sum(axis=1).max()) + 50
            video_h = int(tbl[['BBf_top','BBf_height']].sum(axis=1).max()) + 50
        else:
            video_w = int(tbl[['BB_left','BB_width']].sum(axis=1).max()) + 50
            video_h = int(tbl[['BB_top','BB_height']].sum(axis=1).max()) + 50
        print(f'  Dimensions estimees depuis les BB : {video_w}x{video_h}')

    outputs = []
    for c, name in enumerate(cow_list):
        print(f'  [{c+1}/{len(cow_list)}] Carte occupation : {name}')

        sub = tbl[tbl['name'] == name]
        if sampling_type == 'continuous':
            sub     = sub.dropna(subset=['frames'])
            bb_cols = ['BBl_left', 'BBl_top', 'BBl_width', 'BBl_height']
        else:
            bb_cols = ['BB_left', 'BB_top', 'BB_width', 'BB_height']

        if len(sub) == 0:
            continue

        bb      = sub[bb_cols].values
        sqarea  = np.round(np.sqrt(bb[:, 2] * bb[:, 3]) / 2).astype(int)
        centers = np.round(compute_center_BB(bb)).astype(int)

        h = video_h if bg_frame is None else bg_frame.shape[0]
        w = video_w if bg_frame is None else bg_frame.shape[1]
        occ_map = np.zeros((h, w), dtype=float)

        for n in range(len(sub)):
            cx, cy = centers[n]
            r      = sqarea[n]
            y1, y2 = max(0, cy - r), min(h, cy + r + 1)
            x1, x2 = max(0, cx - r), min(w, cx + r + 1)
            yy, xx = np.ogrid[y1:y2, x1:x2]
            disk   = (xx - cx)**2 + (yy - cy)**2 <= r**2
            occ_map[y1:y2, x1:x2][disk] += 1

        if occ_map.max() == 0:
            print(f'    Carte vide pour {name}, ignoree.')
            continue

        ratio = video_h / video_w if video_w > 0 else 9/16
        fig, ax = plt.subplots(figsize=(16, 16 * ratio))

        if bg_frame is not None:
            bg_gray = bg_frame.mean(axis=2) / 255.0
            ax.imshow(bg_gray, cmap='gray', vmin=0, vmax=1)
        else:
            ax.set_facecolor('#555555')
            ax.set_xlim(0, w)
            ax.set_ylim(h, 0)

        masked = np.ma.masked_where(occ_map == 0, occ_map)
        im     = ax.imshow(masked, cmap='hot', alpha=0.6,
                           vmin=masked.min(), vmax=masked.max())

        cbar = fig.colorbar(im, ax=ax, fraction=0.02, pad=0.01)
        cbar.set_label('Nombre de passages', color='white')
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color='white')

        name_ns    = name.replace(' ', '')
        samp_label = 'continu' if sampling_type == 'continuous' else 'sparse'
        ax.set_title(f'{name} — {video_name} ({samp_label})',
                     color='white', fontsize=12)
        ax.axis('off')
        fig.patch.set_facecolor('#222222')

        img_path = os.path.join(out_dir,
                                f'heatmap_{video_name}_{name_ns}_{samp_label}.jpg')
        plt.savefig(img_path, dpi=80, bbox_inches='tight',
                    facecolor=fig.get_facecolor())
        plt.close(fig)

        # La SOP demande aussi une carte de donnees sans image de fond.
        # Le PNG normalise est directement visualisable; le NPY conserve les
        # comptes bruts afin de permettre une reutilisation quantitative.
        normalized = occ_map / occ_map.max()
        data_path = os.path.join(
            out_dir, f'data_{video_name}_{name_ns}_{samp_label}_normalized.png')
        raw_path = os.path.join(
            out_dir, f'data_{video_name}_{name_ns}_{samp_label}_counts.npy')
        plt.imsave(data_path, normalized, cmap='gray', vmin=0, vmax=1)
        np.save(raw_path, occ_map)
        outputs.append({
            'name': name,
            'heatmap': img_path,
            'normalized_map': data_path,
            'raw_counts': raw_path,
            'max_count': float(occ_map.max()),
        })

    print(f'  Cartes sauvegardees dans : {out_dir}')
    return outputs


# =========================================================================
# 3.8 Video complete
# =========================================================================

def make_complete_video(tbl, orient_csv, video_file, res_folder,
                        sampling_type, fps,
                        preview_minutes=None, scale=None):
    """
    Video complete avec BB, nom et fleche d'orientation par vache.

    preview_minutes : si specifie (ex: 2), genere seulement les N premieres
                      minutes de video pour verification rapide.
                      Mettre None pour la video complete.

    Optimisation : lecture sequentielle avec grab() au lieu de set()
                   -> ~100x plus rapide sur les grandes videos.
    """
    import cv2
    import time

    if not video_file or not os.path.exists(video_file):
        print('  Video source introuvable. Generation ignoree.')
        return

    if not os.path.exists(orient_csv):
        print(f'  Fichier orientations introuvable : {orient_csv}')
        return

    orient_tbl = pd.read_csv(orient_csv)
    if 'frame' in orient_tbl.columns:
        orient_idx = orient_tbl.set_index(['frame', 'name'])
    else:
        orient_idx = None

    cow_list = sorted(tbl['name'].unique())
    palette  = (PALETTE * 255).astype(np.uint8)

    cap   = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        raise ValueError(f'Impossible d ouvrir la video : {video_file}')
    vid_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    vid_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if vid_w <= 0 or vid_h <= 0:
        cap.release()
        raise ValueError('Dimensions video invalides')

    if sampling_type == 'continuous':
        frame_col = 'all_frames'
        bb_cols   = ['BBf_left', 'BBf_top', 'BBf_width', 'BBf_height']
    else:
        frame_col = 'frames'
        bb_cols   = ['BB_left', 'BB_top', 'BB_width', 'BB_height']

    # --- Calcul du facteur d'echelle ---
    # Les BB du CSV ont ete creees sur la video originale.
    # Si la video actuelle est de resolution differente, on recalcule.
    if scale is None:
        # Estimer la resolution originale depuis les coordonnees max du CSV
        orig_w = (tbl[bb_cols[0]] + tbl[bb_cols[2]]).max()
        orig_h = (tbl[bb_cols[1]] + tbl[bb_cols[3]]).max()
        scale_x = vid_w / orig_w
        scale_y = vid_h / orig_h
        # Prendre le plus petit pour eviter de sortir de l'image
        scale_xy = min(scale_x, scale_y)
        if abs(scale_xy - 1.0) > 0.05:
            print(f'  Resolution originale estimee : {orig_w:.0f}x{orig_h:.0f}')
            print(f'  Resolution video actuelle    : {vid_w}x{vid_h}')
            print(f'  Facteur echelle applique     : {scale_xy:.3f}')
        else:
            scale_xy = 1.0
    else:
        scale_xy = scale
        print(f'  Facteur echelle manuel : {scale_xy}')


    all_frames = sorted(tbl[frame_col].dropna().unique().astype(int))
    if not all_frames:
        cap.release()
        raise ValueError('Aucune frame a annoter')

    # Limiter aux N premieres minutes du suivi si preview demande. Le suivi
    # peut commencer tard dans la video (exemple du 27 mars: frame 23131).
    if preview_minutes is not None:
        if preview_minutes <= 0:
            cap.release()
            raise ValueError('preview_minutes doit etre strictement positif')
        max_frame = all_frames[0] + int(preview_minutes * 60 * fps)
        all_frames = [f for f in all_frames if f <= max_frame]
        suffix     = f'preview_{preview_minutes}min'
        print(f'  Mode PREVIEW : {preview_minutes} min ({len(all_frames)} frames)')
    else:
        suffix = 'continuous' if sampling_type == 'continuous' else 'sparse'

    # Choisir le codec et le format selon ce qui fonctionne sur ce systeme.
    # On essaie dans l'ordre : mp4v (MP4), XVID (AVI), MJPG (AVI).
    out_fps = fps if sampling_type == 'continuous' else 1

    def try_codec(fourcc_str, ext):
        import tempfile, os
        fourcc_test = cv2.VideoWriter_fourcc(*fourcc_str)
        tmp = tempfile.mktemp(suffix=ext)
        w = cv2.VideoWriter(tmp, fourcc_test, out_fps, (vid_w, vid_h))
        test_frame = np.zeros((vid_h, vid_w, 3), dtype=np.uint8)
        w.write(test_frame)
        w.release()
        ok = os.path.exists(tmp) and os.path.getsize(tmp) > 1000
        if os.path.exists(tmp):
            os.remove(tmp)
        return ok, fourcc_test, ext

    codec_ok = False
    for codec_str, ext in [('mp4v', '.mp4'), ('XVID', '.avi'), ('MJPG', '.avi')]:
        ok, fourcc, ext = try_codec(codec_str, ext)
        if ok:
            print(f'  Codec selectionne : {codec_str} ({ext})')
            codec_ok = True
            break
    if not codec_ok:
        print('  ATTENTION : aucun codec fiable trouve, utilisation de mp4v par defaut.')
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        ext    = '.mp4'

    # Ajuster le nom du fichier selon l'extension choisie
    out_path = os.path.join(res_folder, f'complete_video_{suffix}{ext}')
    writer   = cv2.VideoWriter(out_path, fourcc, out_fps, (vid_w, vid_h))
    if not writer.isOpened():
        cap.release()
        raise ValueError(f'Impossible de creer la video : {out_path}')

    # Construire un index {frame -> liste de lignes} pour acces rapide
    frame_index = {}
    for _, row in tbl.iterrows():
        f_val = row[frame_col]
        if pd.isna(f_val):
            continue
        f_int = int(f_val)
        if preview_minutes is not None and f_int > max_frame:
            continue
        frame_index.setdefault(f_int, []).append(row)

    Nf      = len(all_frames)
    t_start = time.time()
    print(f'  Generation video : {Nf} frames (lecture sequentielle)...')

    # Lecture sequentielle optimisee :
    # - grab() avance sans decoder (~0.5ms) -> on saute les frames inutiles
    # - read() decode seulement les frames annotes (~50ms)
    # -> gain ~100x vs cap.set() a chaque frame
    #
    # Les frames CSV sont 1-indexes : frame 1 = premiere frame de la video.
    # OpenCV est 0-indexe : set(0) = premiere frame.
    # Pour lire le frame CSV f, on se positionne a f-1 en OpenCV.

    first_frame = all_frames[0]
    # Se positionner juste avant le premier frame utile
    cap.set(cv2.CAP_PROP_POS_FRAMES, first_frame - 1)
    current_pos = first_frame - 1  # position 0-indexee courante

    for n, f in enumerate(all_frames):

        if n % 200 == 0 and n > 0:
            elapsed   = time.time() - t_start
            remaining = elapsed / n * (Nf - n)
            print(f'    {100*n/Nf:.0f}% ({n}/{Nf}) - reste ~{int(remaining//60)}m{int(remaining%60):02d}s')

        # Position 0-indexee voulue pour ce frame
        target_0idx = f - 1

        # Sauter les frames intermediaires avec grab() (sans decoder)
        while current_pos < target_0idx:
            cap.grab()
            current_pos += 1

        # Lire et decoder le frame voulu
        ret, frame = cap.read()
        current_pos += 1
        if not ret:
            continue

        # Annoter le frame
        rows_f = frame_index.get(f, [])
        for row in rows_f:
            name    = row['name']
            cow_idx = cow_list.index(name) if name in cow_list else 0
            color   = tuple(int(x) for x in palette[cow_idx % len(palette)])

            bb = [row[c] for c in bb_cols]
            if any(pd.isna(v) for v in bb):
                continue

            # Appliquer le facteur d'echelle aux coordonnees BB
            left  = int(bb[0] * scale_xy)
            top   = int(bb[1] * scale_xy)
            w_bb  = int(bb[2] * scale_xy)
            h_bb  = int(bb[3] * scale_xy)
            cx    = int(left + w_bb / 2)
            cy    = int(top  + h_bb / 2)

            cv2.rectangle(frame, (left, top),
                          (left + w_bb, top + h_bb), color, 2)
            cv2.circle(frame, (cx, cy), 5, color, -1)

            if orient_idx is not None:
                try:
                    orient_row = orient_idx.loc[(f, name)]
                    ox = float(orient_row['orientation_x'])
                    oy = float(orient_row['orientation_y'])
                    sqarea = int(np.sqrt(w_bb * h_bb))
                    cv2.arrowedLine(frame, (cx, cy),
                                    (int(cx + sqarea * ox),
                                     int(cy + sqarea * oy)),
                                    color, 2, tipLength=0.3)
                except (KeyError, TypeError):
                    pass

            cv2.putText(frame, name, (cx - 20, top - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        secs = f / fps
        ts   = f'Frame {f} | {int(secs//60):02d}:{secs%60:05.2f}'
        cv2.putText(frame, ts, (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)

        # S'assurer que le frame a exactement la bonne taille avant d'ecrire
        # (un frame de mauvaise taille cause le warning "Failed to write frame")
        if frame.shape[1] != vid_w or frame.shape[0] != vid_h:
            frame = cv2.resize(frame, (vid_w, vid_h))

        writer.write(frame)

    cap.release()
    writer.release()
    elapsed = time.time() - t_start
    print(f'  Video sauvegardee : {out_path}')
    print(f'  Temps total : {int(elapsed//60)}m{int(elapsed%60):02d}s')
    return out_path


# =========================================================================
# PROGRAMME PRINCIPAL
# =========================================================================

METRIC_NAMES = {
    'orientation', 'distance_matrix', 'total_distance', 'mean_velocity',
    'mean_acceleration', 'occupancy', 'complete_video',
}


def parse_metrics(value):
    """Transforme une liste separee par des virgules en ensemble valide."""
    selected = {item.strip() for item in value.split(',') if item.strip()}
    if 'all' in selected:
        return set(METRIC_NAMES)
    unknown = sorted(selected.difference(METRIC_NAMES))
    if unknown:
        raise argparse.ArgumentTypeError(f'Metriques inconnues : {unknown}')
    if not selected:
        raise argparse.ArgumentTypeError('Choisir au moins une metrique')
    return selected


def build_parser():
    parser = argparse.ArgumentParser(
        description='Calcule les metriques WELL-E depuis un CSV de trajectoires.')
    parser.add_argument('--traj-csv', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--sampling', required=True,
                        choices=['continuous', 'sparse'])
    parser.add_argument('--fps', type=float, default=30.0)
    parser.add_argument('--video', type=Path)
    parser.add_argument('--video-name')
    parser.add_argument(
        '--metrics', type=parse_metrics,
        default=parse_metrics('all'),
        help='Liste: orientation,distance_matrix,total_distance,'
             'mean_velocity,mean_acceleration,occupancy,complete_video ou all')
    parser.add_argument('--sparse-orientation',
                        choices=['existing', 'interactive', 'skip'],
                        default='existing')
    parser.add_argument('--overwrite-orientation', action='store_true')
    parser.add_argument('--preview-minutes', type=float)
    parser.add_argument('--video-scale', type=float)
    return parser


def run_cli(args):
    traj_csv = args.traj_csv.expanduser().resolve()
    res_folder = args.output_dir.expanduser().resolve()
    video_file = args.video.expanduser().resolve() if args.video else None
    if not traj_csv.exists():
        raise FileNotFoundError(f'CSV introuvable : {traj_csv}')
    if args.fps <= 0:
        raise ValueError('Le FPS doit etre strictement positif')

    tbl = pd.read_csv(traj_csv)
    stats = validate_metric_table(tbl, args.sampling)
    res_folder.mkdir(parents=True, exist_ok=True)
    video_name = args.video_name
    if not video_name and 'video' in tbl and tbl['video'].notna().any():
        video_name = Path(str(tbl['video'].dropna().iloc[0])).stem
    if not video_name:
        video_name = video_file.stem if video_file else traj_csv.stem

    print('=' * 60)
    print('ETAPE 3 : Calcul des metriques WELL-E')
    print('=' * 60)
    print(f'CSV : {traj_csv}')
    print(f'Lignes : {stats["rows"]}; vaches : {stats["cows"]}; '
          f'frames : {stats["sampled_frames"]}')
    print(f'Sorties : {res_folder}')

    metrics = args.metrics
    orient_csv = res_folder / 'cow_orientations.csv'

    if 'orientation' in metrics:
        print('\n--- 3.1 Orientation ---')
        if args.sampling == 'continuous':
            directions = bb2orientation(tbl)
            orient_csv = Path(save_orientation_csv(tbl, directions, res_folder))
        elif args.sparse_orientation == 'interactive':
            if video_file is None:
                raise ValueError('--video est requis pour orientation sparse interactive')
            orient_csv = Path(create_sparse_orientation_csv(
                tbl, str(video_file), res_folder,
                overwrite=args.overwrite_orientation))
        elif args.sparse_orientation == 'existing':
            if not orient_csv.exists():
                raise FileNotFoundError(
                    f'Orientations sparse absentes : {orient_csv}. '
                    'Utiliser --sparse-orientation interactive ou skip.')
            print(f'Orientation sparse existante : {orient_csv}')
        else:
            print('Orientation sparse ignoree explicitement.')

    if 'distance_matrix' in metrics:
        print('\n--- 3.2 Matrice de distances ---')
        if args.sampling == 'continuous':
            distances = compute_distance_matrix_continuous(tbl)
        else:
            distances = compute_distance_matrix_sparse(tbl)
        save_distance_matrix(distances, res_folder, video_name, args.sampling)

    scalar_specs = [
        ('total_distance', compute_total_distance, 'total_distance',
         'total distance (px)'),
        ('mean_velocity', compute_mean_velocity, 'mean_velocity',
         'mean velocity (px/s)'),
        ('mean_acceleration', compute_mean_acceleration, 'mean_acceleration',
         'mean acceleration (px/s2)'),
    ]
    for metric_name, function, suffix, column in scalar_specs:
        if metric_name not in metrics:
            continue
        print(f'\n--- {metric_name} ---')
        result = function(tbl, args.sampling, args.fps)
        save_scalar_metric(result, res_folder, video_name, args.sampling,
                           suffix, column)

    if 'occupancy' in metrics:
        print("\n--- 3.6 Cartes d'occupation ---")
        compute_occupancy_maps(tbl, args.sampling, res_folder, video_name,
                               str(video_file) if video_file else None)

    if 'complete_video' in metrics:
        print('\n--- 3.8 Video complete ---')
        if video_file is None:
            raise ValueError('--video est requis pour complete_video')
        make_complete_video(
            tbl, str(orient_csv), str(video_file), res_folder,
            args.sampling, args.fps,
            preview_minutes=args.preview_minutes, scale=args.video_scale)

    print('\nEtape 3 terminee.')


if __name__ == '__main__':
    try:
        run_cli(build_parser().parse_args())
    except (FileNotFoundError, ValueError, KeyError) as exc:
        print(f'ERREUR : {exc}', file=sys.stderr)
        sys.exit(1)
