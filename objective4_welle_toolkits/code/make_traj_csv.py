"""
make_traj_csv.py
----------------
  - Etape 1 : Lit le fichier .mat produit par MATRID et genere le CSV des trajectoires.
  - Etape 2 : Affiche un resume du CSV, genere des images de verification
              par vache, detecte les erreurs de nommage, et demande si on continue.

Usage:
    python make_traj_csv.py --mat INPUT.mat --output-dir RESULTS \
        --sampling continuous --video VIDEO.mp4
"""

import argparse
import scipy.io as sio
import numpy as np
import pandas as pd
import os
import sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')   # sauvegarde les images sans avoir besoin d'un ecran
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec

# Palette de couleurs pour distinguer les vaches
def make_palette():
    nbc = 4
    dc = np.linspace(0, 1, nbc)
    palette = []
    for r in dc:
        for g in dc:
            for b in dc:
                palette.append([r, g, b])
    palette = np.array(palette)
    order = np.argsort(palette.sum(axis=1))[::-1]
    return palette[order]
 
PALETTE = make_palette()
 
 
def compute_center_BB(bb):
    """
    Calcule le centre d'une bounding box.
    bb : array de shape (N, 4) avec colonnes [left, top, width, height]
    Retourne array (N, 2) avec colonnes [center_x, center_y]
    """
    bb = np.atleast_2d(bb)
    center_x = bb[:, 0] + bb[:, 2] / 2.0
    center_y = bb[:, 1] + bb[:, 3] / 2.0
    return np.column_stack([center_x, center_y])
 
 
def load_mat_file(mat_file):
    """
    Charge le fichier .mat et retourne la liste des trajectoires.
    Gere les cas ou frames/all_frames sont des scalaires (trajectoires a 1 point).
    """
    mat = sio.loadmat(mat_file, simplify_cells=True)
    if 'new_cow_gs' not in mat:
        raise KeyError("Variable 'new_cow_gs' absente du fichier MATRID")
    data = mat['new_cow_gs']
    if isinstance(data, dict):
        data = [data]
    trajs = []
    removed = 0
    for cow in data:
        name = cow.get('name', '')
        if not name or str(name).strip() == '':
            removed += 1
            continue
        trajectory = {
            'name':       str(name),
            'frames':     np.atleast_1d(np.array(cow['frames'],     dtype=np.float64)),
            'all_frames': np.atleast_1d(np.array(cow['all_frames'], dtype=np.float64)),
            'BBl':        np.atleast_2d(np.array(cow['BBl'],        dtype=np.float64)),
            'BBf':        np.atleast_2d(np.array(cow['BBf'],        dtype=np.float64)),
        }
        if len(trajectory['all_frames']) != len(trajectory['BBl']) or len(
            trajectory['all_frames']
        ) != len(trajectory['BBf']):
            raise ValueError(
                f"Longueurs incompatibles pour {trajectory['name']}: "
                "all_frames, BBl et BBf doivent être alignés"
            )
        trajs.append(trajectory)
    if removed > 0:
        print(f'  {removed} trajectoire(s) sans nom ignoree(s).')
    return trajs
 
 
def make_csv_continuous(trajectories, video_name, res_folder, fps):
    """
    Genere le CSV pour un echantillonnage continu.
    Regroupe les morceaux de trajectoire par nom de vache,
    trie chronologiquement et ecrit le CSV.
    """
    cow_list = sorted(set(t['name'] for t in trajectories))
    print(f'  Nombre de vaches uniques : {len(cow_list)}')
    rows = []
 
    for name in cow_list:
        print(f'  Traitement de : {name}')
        pieces     = [t for t in trajectories if t['name'] == name]
        all_frames = np.concatenate([p['all_frames'] for p in pieces])
        frames     = np.concatenate([p['frames']     for p in pieces])
        BBl        = np.vstack([p['BBl'] for p in pieces])
        BBf        = np.vstack([p['BBf'] for p in pieces])
        sort_idx   = np.argsort(all_frames)
        all_frames = all_frames[sort_idx]
        BBl        = BBl[sort_idx]
        BBf        = BBf[sort_idx]
        frames_set = set(frames)
        centers    = compute_center_BB(BBf)
 
        for n in range(len(all_frames)):
            af    = int(all_frames[n])
            f_val = af if af in frames_set else np.nan
            rows.append({
                'all_frames': af,   'frames':    f_val,
                'video':      video_name,        'sampling':   'continuous',
                'name':       name,
                'BBl_left':   BBl[n,0],          'BBl_top':    BBl[n,1],
                'BBl_width':  BBl[n,2],          'BBl_height': BBl[n,3],
                'BBf_left':   BBf[n,0],          'BBf_top':    BBf[n,1],
                'BBf_width':  BBf[n,2],          'BBf_height': BBf[n,3],
                'Center_X':   centers[n,0],      'Center_Y':   centers[n,1],
            })
 
    tbl = pd.DataFrame(rows)
    os.makedirs(res_folder, exist_ok=True)
    csv_path = os.path.join(res_folder, f'traj_{video_name}.csv')
    tbl.to_csv(csv_path, index=False)
    print(f'  Fichier CSV sauvegarde : {csv_path}')
    print(f'  Total de lignes : {len(tbl)}')
    return tbl
 
 
def make_csv_sparse(trajectories, video_name, res_folder, fps):
    """
    Genere le CSV pour un echantillonnage sparse.
    Ne garde que le premier frame de chaque morceau de trajectoire.
    """
    cow_list = sorted(set(t['name'] for t in trajectories))
    print(f'  Nombre de vaches uniques : {len(cow_list)}')
    rows = []
 
    for name in cow_list:
        print(f'  Traitement de : {name}')
        pieces = [t for t in trajectories if t['name'] == name]
        piece_frames = np.array([p['frames'][0]  for p in pieces])
        piece_BB     = np.vstack([p['BBl'][0]    for p in pieces])
        sort_idx     = np.argsort(piece_frames)
        piece_frames = piece_frames[sort_idx]
        piece_BB     = piece_BB[sort_idx]
        centers      = compute_center_BB(piece_BB)
 
        for n in range(len(piece_frames)):
            f        = int(piece_frames[n])
            time_min = round(f / (fps * 60))
            rows.append({
                'frames':      f,            'video':      video_name,
                'sampling':    'sparse',     'name':       name,
                'time_in_min': time_min,
                'BB_left':     piece_BB[n,0],'BB_top':     piece_BB[n,1],
                'BB_width':    piece_BB[n,2],'BB_height':  piece_BB[n,3],
                'Center_X':    centers[n,0], 'Center_Y':   centers[n,1],
            })
 
    tbl = pd.DataFrame(rows)
    os.makedirs(res_folder, exist_ok=True)
    csv_path = os.path.join(res_folder, f'traj_{video_name}.csv')
    tbl.to_csv(csv_path, index=False)
    print(f'  Fichier CSV sauvegarde : {csv_path}')
    print(f'  Total de lignes : {len(tbl)}')
    return tbl
 
 
def get_first_video_frame(video_file):
    """
    Lit le premier frame de la video comme image numpy (H x W x 3).
    Retourne None si la video n'est pas disponible.
    """
    if video_file is None or not os.path.exists(video_file):
        return None
    try:
        import cv2
        cap = cv2.VideoCapture(video_file)
        ret, frame = cap.read()
        cap.release()
        if ret:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    except Exception as e:
        print(f'  Impossible de lire la video : {e}')
    return None
 
 
def get_video_dimensions(video_file):
    """
    Lit la resolution d'une video. Retourne (width, height) ou None si indisponible.
    """
    if video_file is None or not os.path.exists(video_file):
        return None, None
    try:
        import cv2
        cap   = cv2.VideoCapture(video_file)
        vid_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        vid_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        return vid_w, vid_h
    except Exception:
        return None, None


def get_video_metadata(video_file):
    """Retourne largeur, hauteur, fps et nombre de frames si OpenCV est disponible."""
    if video_file is None or not os.path.exists(video_file):
        return None
    try:
        import cv2
        cap = cv2.VideoCapture(video_file)
        metadata = {
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': float(cap.get(cv2.CAP_PROP_FPS)),
            'frames': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        }
        cap.release()
        return metadata
    except Exception as exc:
        print(f'  Métadonnées vidéo indisponibles : {exc}')
        return None
 
 
def make_summary_and_plots(tbl, sampling_type, res_folder, Nframes, video_file):
    """
    Etape 2 : resume console + images de verification par vache.
    Equivalent du Step 2 MATLAB.
    """
    print()
    print('---------------------------------------')
    print('Resume du contenu du fichier CSV :')
    print('---------------------------------------')
    print()
 
    cow_list = sorted(tbl['name'].unique())
    Ncows    = len(cow_list)
 
    # --- Resume console ---
    if sampling_type == 'continuous':
        print('Type echantillonnage : continu')
        n_instants = tbl['all_frames'].nunique()
        print(f'Instants echantillonnes : {n_instants} frames')
        print()
        print('Vaches et nombre de frames :')
        for name in cow_list:
            n = len(tbl[tbl['name'] == name])
            too_many = (Nframes is not None) and (n > Nframes)
            flag = '  <<<<< TROP DE FRAMES !' if too_many else ''
            print(f'  {name} : {n} frames{flag}')
 
    else:  # sparse
        print('Type echantillonnage : sparse')
        instants = sorted(tbl['time_in_min'].unique())
        print(f'Instants : {instants} (min)')
        print()
        print('Vaches et instants traces :')
        for name in cow_list:
            sub  = tbl[tbl['name'] == name]
            mins = sorted(sub['time_in_min'].tolist())
            n    = len(sub)
            too_many = (Nframes is not None) and (n > Nframes)
            flag = '  <<<<< TROP DE FRAMES !' if too_many else ''
            print(f'  {name} : {mins} (min){flag}')
 
    # --- Images de verification ---
    print()
    print('Generation des images de verification des trajectoires...')
    os.makedirs(res_folder, exist_ok=True)
 
    # Lire le premier frame de la video et les dimensions reelles
    bg_frame       = get_first_video_frame(video_file)
    vid_w, vid_h   = get_video_dimensions(video_file)
 
    # Estimer la resolution originale du tracking depuis les BB du CSV
    if sampling_type == 'continuous':
        orig_w = (tbl['BBl_left'] + tbl['BBl_width']).max()
        orig_h = (tbl['BBl_top']  + tbl['BBl_height']).max()
    else:
        orig_w = (tbl['BB_left'] + tbl['BB_width']).max()
        orig_h = (tbl['BB_top']  + tbl['BB_height']).max()
 
    # Facteur d'echelle si la video actuelle est differente
    if vid_w is not None and abs(vid_w / orig_w - 1.0) > 0.05:
        scale_xy = vid_w / orig_w
        print(f'  Resolution tracking : {orig_w:.0f}x{orig_h:.0f}')
        print(f'  Resolution video    : {vid_w}x{vid_h}')
        print(f'  Facteur echelle     : {scale_xy:.3f}')
    else:
        scale_xy = 1.0
 
    # Rapport hauteur/largeur pour les figures
    if vid_w is not None and vid_w > 0:
        fig_ratio = vid_h / vid_w
    elif orig_w > 0:
        fig_ratio = orig_h / orig_w
    else:
        fig_ratio = 9 / 16
 
    for c, name in enumerate(cow_list):
        sub = tbl[tbl['name'] == name].copy()
 
        # Garder seulement les frames traces manuellement (frames non NaN)
        sub_manual = sub.dropna(subset=['frames'])
 
        if len(sub_manual) == 0:
            print(f'  {name} : aucun frame manuel, image ignoree.')
            continue
 
        frames_n  = sub_manual['frames'].values
        centers_n = sub_manual[['Center_X', 'Center_Y']].values
        if sampling_type == 'continuous':
            bb_cols = ['BBl_left', 'BBl_top', 'BBl_width', 'BBl_height']
        else:
            bb_cols = ['BB_left', 'BB_top', 'BB_width', 'BB_height']
        bbn = sub_manual[bb_cols].values
 
        # Detecter les morceaux de trajectoire (sauts dans les frames)
        if len(frames_n) > 1:
            dfr      = frames_n[1] - frames_n[0]
            dframes  = np.diff(frames_n)
            pieces   = np.zeros(len(frames_n), dtype=int)
            pieces[0] = 0
            p = 0
            for ff in range(len(frames_n) - 1):
                if dframes[ff] > dfr:
                    p += 1
                pieces[ff + 1] = p
        else:
            pieces = np.array([0])
 
        n_pieces = pieces.max() + 1
 
        # --- Figure ---
        fig = plt.figure(figsize=(16, 16 * fig_ratio + 3))
        gs  = gridspec.GridSpec(5, 6, figure=fig)
 
        # Graphe X(t)
        ax1 = fig.add_subplot(gs[0, 0:3])
        for p in range(n_pieces):
            idx = np.where(pieces == p)[0]
            color = PALETTE[(p + 1) % len(PALETTE)]
            ax1.plot(frames_n[idx], centers_n[idx, 0], 'o',
                     color=color, markersize=3)
        ax1.set_xlabel('Frames')
        ax1.set_ylabel('X(t)')
        ax1.set_title(f'{name} - position X')
 
        # Graphe Y(t)
        ax2 = fig.add_subplot(gs[0, 3:6])
        for p in range(n_pieces):
            idx = np.where(pieces == p)[0]
            color = PALETTE[(p + 1) % len(PALETTE)]
            ax2.plot(frames_n[idx], centers_n[idx, 1], 'o',
                     color=color, markersize=3)
        ax2.set_xlabel('Frames')
        ax2.set_ylabel('Y(t)')
        ax2.set_title(f'{name} - position Y')
 
        # Vue 2D avec image de fond
        ax3 = fig.add_subplot(gs[1:5, 0:6])
        if bg_frame is not None:
            ax3.imshow(bg_frame)
        else:
            # Fond gris si pas de video
            ax3.set_facecolor('#cccccc')
 
        for p in range(n_pieces):
            idx   = np.where(pieces == p)[0]
            color = PALETTE[(p + 1) % len(PALETTE)]
            # Trajectoire (avec scale si necessaire)
            ax3.plot(centers_n[idx, 0] * scale_xy,
                     centers_n[idx, 1] * scale_xy,
                     'x-', color='red', linewidth=1.5, markersize=4)
            # Bounding boxes (avec scale si necessaire)
            for i in idx:
                left = bbn[i, 0] * scale_xy
                top  = bbn[i, 1] * scale_xy
                w    = bbn[i, 2] * scale_xy
                h    = bbn[i, 3] * scale_xy
                rect = patches.Rectangle(
                    (left, top), w, h,
                    linewidth=1.5, edgecolor=color, facecolor='none'
                )
                ax3.add_patch(rect)
 
        ax3.set_xlabel(f'{c+1}) Vache : {name}')
 
        plt.tight_layout()
        img_path = os.path.join(res_folder, f'cow_trajectory_{c+1}.png')
        plt.savefig(img_path, dpi=80)
        plt.close(fig)
        print(f'  [{c+1}/{Ncows}] Image sauvegardee : {img_path}')
 
    print('Images generees.')
 
 
def check_errors(tbl):
    """
    Verifie les erreurs courantes dans les noms de vaches.
    Retourne True s'il y a des erreurs, False sinon.
    """
    errors = 0
    names = tbl['name']

    # Noms manquants
    missing_names = names.isna() | names.fillna('').astype(str).str.strip().eq('')
    if missing_names.any():
        print('ATTENTION : au moins une vache a un nom manquant.')
        errors += 1

    # Problemes de casse (ex: "Alexandra" et "alexandra")
    cow_list = sorted(names[~missing_names].astype(str).unique())
    lower_list = [n.lower() for n in cow_list]
    if len(set(lower_list)) != len(cow_list):
        seen = {}
        for name in cow_list:
            key = name.lower()
            seen.setdefault(key, []).append(name)
        duplicates = [v for v in seen.values() if len(v) > 1]
        print('ATTENTION : noms en double (probleme de majuscules/minuscules) :')
        for dup in duplicates:
            print(f'  {dup}')
        errors += 1
 
    return errors > 0


def validate_table(tbl, sampling_type, nframes=None):
    """Valide le schéma et les invariants nécessaires aux métriques."""
    common = {'frames', 'video', 'sampling', 'name', 'Center_X', 'Center_Y'}
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

    frame_col = 'all_frames' if sampling_type == 'continuous' else 'frames'
    duplicated = int(tbl.duplicated(['name', frame_col]).sum())
    box_cols = (
        ['BBl_width', 'BBl_height', 'BBf_width', 'BBf_height']
        if sampling_type == 'continuous'
        else ['BB_width', 'BB_height']
    )
    invalid_boxes = int(
        ((tbl[box_cols] <= 0) | tbl[box_cols].isna()).any(axis=1).sum()
    )
    too_long = 0
    if nframes is not None:
        too_long = int((tbl[frame_col] > nframes).fillna(False).sum())

    return {
        'rows': int(len(tbl)),
        'cows': int(tbl['name'].nunique(dropna=True)),
        'sampled_frames': int(tbl[frame_col].nunique(dropna=True)),
        'manual_frames': int(tbl['frames'].notna().sum()),
        'duplicate_cow_frame': duplicated,
        'invalid_boxes': invalid_boxes,
        'frames_after_video_end': too_long,
    }
 
 
def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Convertit un fichier MATRID .mat en CSV de trajectoires."
    )
    parser.add_argument('--mat', required=True, type=Path, help="Fichier *_new_cow_gs.mat")
    parser.add_argument('--output-dir', required=True, type=Path, help="Dossier de résultats")
    parser.add_argument('--video', type=Path, help="Vidéo source, optionnelle pour les figures")
    parser.add_argument('--video-name', help="Nom de sortie sans extension")
    parser.add_argument(
        '--sampling', choices=('continuous', 'sparse'), required=True,
        help="Stratégie utilisée lors du suivi",
    )
    parser.add_argument('--fps', type=float, help="FPS; détecté depuis la vidéo si possible")
    parser.add_argument('--nframes', type=int, help="Nombre de frames; détecté si possible")
    parser.add_argument('--reuse-existing', action='store_true', help="Réutilise le CSV existant")
    parser.add_argument('--skip-plots', action='store_true', help="N'écrit pas les figures de contrôle")
    parser.add_argument('--strict', action='store_true', help="Échoue si les contrôles signalent une anomalie")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    mat_file = args.mat.expanduser().resolve()
    video_file = args.video.expanduser().resolve() if args.video else None
    res_folder = args.output_dir.expanduser().resolve()
    if not mat_file.exists():
        raise FileNotFoundError(f"Fichier .mat introuvable : {mat_file}")
    if video_file is not None and not video_file.exists():
        raise FileNotFoundError(f"Vidéo introuvable : {video_file}")

    metadata = get_video_metadata(str(video_file)) if video_file else None
    fps = args.fps or (metadata['fps'] if metadata else None)
    nframes = args.nframes or (metadata['frames'] if metadata else None)
    if not fps or fps <= 0:
        raise ValueError("FPS manquant ou invalide; fournir --fps ou --video")

    default_name = mat_file.stem.removesuffix('_new_cow_gs')
    video_name = args.video_name or (video_file.stem if video_file else default_name)
    res_folder.mkdir(parents=True, exist_ok=True)
    csv_path = res_folder / f'traj_{video_name}.csv'

    print('=' * 60)
    print('ETAPE 1 : Generation du fichier CSV des trajectoires')
    print('=' * 60)
    if args.reuse_existing and csv_path.exists():
        print(f'Lecture du CSV existant : {csv_path}')
        table = pd.read_csv(csv_path)
    else:
        trajectories = load_mat_file(str(mat_file))
        print(f'  {len(trajectories)} morceaux de trajectoires chargés.')
        if args.sampling == 'continuous':
            table = make_csv_continuous(trajectories, video_name, str(res_folder), fps)
        else:
            table = make_csv_sparse(trajectories, video_name, str(res_folder), fps)

    print()
    print('=' * 60)
    print('ETAPE 2 : Resume et verification')
    print('=' * 60)
    checks = validate_table(table, args.sampling, nframes)
    for key, value in checks.items():
        print(f'  {key}: {value}')
    has_errors = check_errors(table)
    if not args.skip_plots:
        make_summary_and_plots(
            table, args.sampling, str(res_folder), nframes,
            str(video_file) if video_file else None,
        )

    hard_failures = (
        has_errors
        or checks['duplicate_cow_frame'] > 0
        or checks['invalid_boxes'] > 0
        or checks['frames_after_video_end'] > 0
    )
    if args.strict and hard_failures:
        raise ValueError("La validation stricte a détecté des anomalies")
    print(f'CSV prêt : {csv_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
