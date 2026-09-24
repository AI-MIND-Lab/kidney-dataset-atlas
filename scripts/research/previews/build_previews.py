"""Compress the Kidney-VLM quality-check figures into public/previews/ and write src/data/samples/processed-figures.json.

Input: the raw PNG figures in figures/<folder>/ (git-ignored, because they show patients; ask the project owner for
a copy). Captions were written from the Kidney-VLM figure guide, checked against each image, and are kept below;
docs/previews.md explains how the previews were made and who drew each mask. Every sample stays unapproved:
permissionApprovedBy is a curator's decision.

Requires: pip install -r scripts/research/requirements.txt
"""
import json, os, re
from pathlib import Path
from PIL import Image

REPO = str(Path(__file__).resolve().parents[3])
FIG = os.path.join(REPO, 'figures')
GUIDE = 'How these previews were made and who drew the masks: docs/previews.md.'

FOUR_PANEL = ('Four views of one scan: the whole axial slice where the centred label is largest, a zoomed axial crop, '
              'and coronal and sagittal cuts through the same point. Kidney is outlined in green, tumour in red and '
              'cyst in yellow. Window 50/500 HU; radiological orientation (patient left on viewer right).')
RMAC_PANELS = ('One panel per contrast phase at the same slice and zoom. Only phases registered to the non-contrast '
               'scan are shown. The red outline is the dataset\'s own mass annotation, drawn on the non-contrast grid.')

KITS = {
    'release': 'kits23', 'folder': 'kits23',
    'attribution': ('Images and reference labels: KiTS23, Kidney and Kidney Tumor Segmentation Challenge 2023 '
                    '(Heller et al.; kits-challenge.org/kits23), read from a Hugging Face copy of the release. '
                    'Rendered by the Kidney-VLM project: windowed, reoriented to LPS, cropped and outlined.'),
    'reuseTerms': ('CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/). This preview is an adaptation of '
                   'KiTS23 data and is shared under the same licence: non-commercial use with attribution, and '
                   'adaptations under the same terms.'),
    'sources': ['kits23-challenge-page', 'kits23-readme'],
    'alignment': 'Outlines come from the reference segmentation on the same voxel grid as the image.',
    'items': [
        ('case_00062', 'KiTS23 case_00062 (0.98 × 0.98 × 5.0 mm): a small tumour in the left kidney.', 'CT of the abdomen with a small tumour outlined in red in the left kidney, shown in axial, zoomed, coronal and sagittal views.'),
        ('case_00236', 'KiTS23 case_00236 (0.92 × 0.92 × 5.0 mm): a large, round tumour in the left kidney; the right kidney is normal. The flat upper tumour edge in the sagittal view reflects the 5 mm slices.', 'CT with a large round tumour outlined in red in the left kidney and a normal right kidney outlined in green.'),
        ('case_00242', 'KiTS23 case_00242 (0.76 × 0.76 × 5.0 mm): a large exophytic tumour on the right kidney, with small cysts in the left kidney.', 'CT with a large tumour outlined in red protruding from the right kidney, and small yellow-outlined cysts in the left kidney.'),
        ('case_00242_cyst', 'KiTS23 case_00242, the same scan centred on a left-kidney cyst: tumour and cysts in opposite kidneys.', 'CT centred on a small cyst outlined in yellow in the left kidney, with a tumour in the opposite kidney.'),
        ('case_00203_cyst', 'KiTS23 case_00203 (0.64 × 0.64 × 1.0 mm, 620 slices from chest to pelvis): a small peripheral cyst in the left kidney and a small tumour visible in the sagittal view. The kidneys fill only a small part of this long scan.', 'Thin-slice CT covering chest to pelvis, centred on a small yellow-outlined cyst in the left kidney.'),
        ('case_00433_cyst', 'KiTS23 case_00433 (0.69 × 0.69 × 2.5 mm): a large cyst at the upper pole of the left kidney, bulging beyond the kidney outline, and a tumour at the lower pole. Labels never overlap: each voxel is kidney, tumour or cyst.', 'CT with a large yellow-outlined cyst at the upper pole of the left kidney and a red-outlined tumour at its lower pole.'),
    ],
}

RMAC = {
    'release': 'ucsf-rmac-2025', 'folder': 'rmac',
    'attribution': ('Images and annotations: UCSF RMaC, the UCSF 3D Multi-Phase Renal Mass CT dataset (Larson 2025, '
                    'doi:10.58078/C2WC74; Sahin et al. 2026). Pathology from the dataset\'s key table. Rendered by the '
                    'Kidney-VLM project: cropped, windowed and outlined.'),
    'reuseTerms': ('CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). This preview is an adaptation of UCSF RMaC data; '
                   'reuse requires attribution to the dataset.'),
    'sources': ['ucsf-rmac-repo', 'ucsf-rmac-aws', 'ucsf-rmac-preprint'],
    'alignment': 'Phases shown are those the release registers to the non-contrast scan, so they share the annotation grid.',
    'items': [
        ('3LYUFVSwiY', 'RMaC exam 3LYUFVSwiY: clear cell RCC, 1.9 cm, left kidney. Non-contrast, arterial and delayed phases (no registered portal-venous volume). A small mass at the edge of the kidney, marked by a rectangle.', 'Three contrast phases of CT showing a small renal mass marked by a red rectangle.'),
        ('Mnx1XxZZPN', 'RMaC exam Mnx1XxZZPN: clear cell RCC, 5.4 cm, right kidney. All four phases: the mass is faint without contrast and enhances strongly and unevenly in the arterial phase.', 'Four contrast phases of CT of a large renal mass marked by a red rectangle, bright and heterogeneous in the arterial phase.'),
        ('WC3J7Q0yat', 'RMaC exam WC3J7Q0yat: chromophobe RCC, 6.3 cm, left kidney. All four phases: a large, round, fairly uniform mass that enhances less than the adjacent kidney cortex in the arterial phase.', 'Four contrast phases of CT of a large round renal mass marked by a red rectangle.'),
        ('YoPBh7znuG', 'RMaC exam YoPBh7znuG: clear cell RCC, 5.3 cm, right kidney. Non-contrast, venous and delayed phases (no registered arterial volume): heterogeneous enhancement in the venous phase and excreted contrast nearby in the delayed phase.', 'Three contrast phases of CT of a large renal mass marked by a red rectangle.'),
    ],
}

CPTAC = {
    'release': 'cptac-ccrcc-v14', 'folder': 'cptac',
    'attribution': ('Images: CPTAC-CCRCC collection, The Cancer Imaging Archive (National Cancer Institute CPTAC, 2018, '
                    'doi:10.7937/K9/TCIA.2018.OBLAMN27). Masks: BAMF AI-generated segmentations from the AIMI Annotations '
                    'initiative (Van Oss et al. 2024, doi:10.5281/zenodo.8345959; Murugesan et al. 2024). Rendered by the '
                    'Kidney-VLM project from its processed volumes: windowed, cropped and outlined.'),
    'reuseTerms': ('CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/) for both the TCIA images and the BAMF masks. This '
                   'preview is an adaptation; reuse requires attribution to both.'),
    'sources': ['cptac-ccrcc-tcia', 'bamf-aimi-zenodo', 'bamf-aimi-paper'],
    'alignment': 'BAMF DICOM-SEG masks placed on the processed CT volumes. Masks are AI output unless marked as corrected.',
    'items': [
        ('C3L-00766', 'CPTAC-CCRCC C3L-00766 (phase not recorded; GE; 0.82 × 0.82 × 2.5 mm; radiologist-corrected BAMF mask): a small tumour at the upper edge of the right kidney.', 'CT with a small tumour outlined in red at the upper edge of the right kidney.'),
        ('C3N-00313', 'CPTAC-CCRCC C3N-00313 (phase not recorded; GE; 0.62 × 0.62 × 5.0 mm; uncorrected BAMF mask): a round tumour in the left kidney. The AI mask also marks a second small tumour region in the right kidney and a tiny cyst region.', 'CT with a round tumour outlined in red in the left kidney.'),
        ('C3N-02063', 'CPTAC-CCRCC C3N-02063 (venous phase from the series description; Siemens; 0.77 × 0.77 × 1.5 mm; radiologist-corrected BAMF mask): an exophytic tumour on the lateral side of the right kidney.', 'CT with a tumour outlined in red bulging from the lateral side of the right kidney.'),
        ('C3N-02723', 'CPTAC-CCRCC C3N-02723 (venous phase from the series description; Toshiba; 0.98 × 0.98 × 5.0 mm; uncorrected BAMF mask): a large, heterogeneous right-kidney tumour.', 'CT with a large heterogeneous tumour outlined in red in the right kidney.'),
        ('C3N-02723_cyst', 'CPTAC-CCRCC C3N-02723, the same scan centred on a tiny cyst at the edge of the left kidney. The uncorrected AI mask also carries small tumour fragments.', 'CT centred on a tiny cyst outlined in yellow at the edge of the left kidney.'),
        ('C3L-01462_cyst', 'CPTAC-CCRCC C3L-01462 (arterial phase from the series description; GE; 0.87 × 0.87 × 5.0 mm; uncorrected BAMF mask): a cyst directly beside a small tumour in the right kidney.', 'CT with a yellow-outlined cyst directly beside a red-outlined small tumour in the right kidney.'),
        ('C3N-00435_cyst', 'CPTAC-CCRCC C3N-00435 (venous phase from the series description; Siemens; 0.67 × 0.67 × 1.2 mm; uncorrected BAMF mask): several cysts in the left kidney and tumour regions in the right kidney.', 'CT with several yellow-outlined cysts in the left kidney and red-outlined tumour regions in the right kidney.'),
    ],
}

def cptac_mask(name, caption):
    if 'radiologist-corrected BAMF' in caption:
        return 'Mask: BAMF (AI-generated, AIMI Annotations), corrected by a radiologist.'
    return 'Mask: BAMF (AI-generated, AIMI Annotations), uncorrected AI output.'


MASK_LINE = {
    'kits23': lambda n, c: "Mask: KiTS23's own reference labels, drawn by trained annotators with expert review of doubtful cases.",
    'ucsf-rmac-2025': lambda n, c: "Mask: UCSF RMaC's own annotation, drawn by a radiology resident and reviewed by an attending radiologist. In these examples it is a bounding box, not an outline.",
    'cptac-ccrcc-v14': cptac_mask,
}

samples, total_in, total_out = [], 0, 0
for spec in (KITS, RMAC, CPTAC):
    out_dir = os.path.join(REPO, 'public', 'previews', spec['release'])
    os.makedirs(out_dir, exist_ok=True)
    intro = RMAC_PANELS if spec is RMAC else FOUR_PANEL
    for name, caption, alt in spec['items']:
        src = os.path.join(FIG, spec['folder'], name + '.png')
        dst = os.path.join(out_dir, name + '.webp')
        im = Image.open(src).convert('RGB')
        im.save(dst, 'WEBP', quality=82, method=6)
        total_in += os.path.getsize(src); total_out += os.path.getsize(dst)
        mask = MASK_LINE[spec['release']](name, caption)
        caption = re.sub(r';? ?(radiologist-corrected |uncorrected )?BAMF mask', '', caption).replace(' ()', '').replace('; )', ')')
        samples.append({
            'id': f"{spec['release']}-{name.lower().replace('_', '-')}",
            'release': spec['release'],
            'kind': 'dataset_sample',
            'assets': [{'path': f"/previews/{spec['release']}/{name}.webp", 'role': 'image', 'sliceIndex': None,
                        'width': im.width, 'height': im.height}],
            'caption': f'{mask} {caption} {intro} {GUIDE}',
            'alt': alt,
            'attribution': spec['attribution'],
            'reuseTerms': spec['reuseTerms'],
            'permissionApprovedBy': None,
            'permissionApprovedOn': None,
            'alignment': spec['alignment'],
            'sources': spec['sources'],
        })

out = os.path.join(REPO, 'src', 'data', 'samples', 'processed-figures.json')
with open(out, 'w', encoding='utf8', newline='\n') as f:
    json.dump(samples, f, ensure_ascii=False, indent='\t')
    f.write('\n')
print(f'{len(samples)} samples; {total_in/1e6:.1f} MB of PNG -> {total_out/1e6:.2f} MB of WebP')
