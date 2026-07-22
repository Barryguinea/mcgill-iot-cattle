"""Assemble le paquet de livraison de l'objectif 4 sur le Bureau."""

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEST_ROOT = Path.home() / 'Desktop' / 'Livrables_McGill_WellE'
DEST = DEST_ROOT / 'Objectif4_Support_outils_WELL-E'


def copy_file(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def main():
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)

    copy_file(ROOT / 'README.md', DEST / '00_LISEZ-MOI.md')

    report_names = [
        'Objectif4_revue_annotee_scripts.docx',
        'Objectif4_note_application_Mira.docx',
        'Objectif4_guide_depannage_FAQ.docx',
    ]
    for name in report_names:
        copy_file(ROOT / 'reports' / name, DEST / '01_RAPPORTS_WORD' / name)

    for name in ['make_traj_csv.py', 'compute_metrics.py']:
        copy_file(ROOT / 'code' / name, DEST / '02_SCRIPTS_PYTHON' / name)

    for name in ['test_welle_conversion.py', 'run_example_validation.py']:
        copy_file(ROOT / 'tests' / name, DEST / '03_TESTS' / name)

    validation_dir = ROOT / 'results' / 'validation'
    for source in sorted(validation_dir.glob('*')):
        if source.is_file():
            copy_file(source, DEST / '04_RESULTATS_VALIDATION' / source.name)

    archive = DEST_ROOT / 'Objectif4_Support_outils_WELL-E.zip'
    if archive.exists():
        archive.unlink()
    shutil.make_archive(str(archive.with_suffix('')), 'zip', DEST_ROOT, DEST.name)
    print(DEST)
    print(archive)


if __name__ == '__main__':
    main()
