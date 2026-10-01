"""Compress the Kidney-VLM quality-check figures into public/previews/ and write src/data/samples/processed-figures.json.

Input: the full-size PNG renderings in figures/<folder>/, committed so anyone can rebuild the previews. Only
renderings that a preview uses belong there. They were rendered by the Kidney-VLM project, whose rendering code is
not in this repository; a new preview needs a four-view (or one-panel-per-phase) PNG made the same way, added here
with an entry below. Captions were written from the Kidney-VLM figure guide, checked against each image, and are kept below;
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
ATLAS_PANELS = ('Four views of one scan: the whole axial slice where the centred label is largest, a zoomed axial crop, '
                'and coronal and sagittal cuts through the same point. Kidney is outlined in green and the kidney lesion '
                'in orange; the release does not say whether a lesion is a tumour or a cyst. Window 50/500 HU; '
                'radiological orientation (patient left on viewer right).')
DTV_PANELS = ('Five axial slices spread across the kidneys, side by side, exactly as DeepTumorVQA releases the image for its '
              'questions; per the paper they use a window of -150 to 250 HU. No outline is drawn.')

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

TCGA = {
    'release': 'tcga-kirc-tcia', 'folder': 'tcga',
    'attribution': ('Images: TCGA-KIRC collection, The Cancer Imaging Archive (Akin et al. 2016, '
                    'doi:10.7937/K9/TCIA.2016.V6PBVTDR). Masks: BAMF AI-generated segmentations from the AIMI Annotations '
                    'initiative (Van Oss et al. 2024, doi:10.5281/zenodo.8345959; Murugesan et al. 2024) or RCC-AID '
                    '(de Boer et al. 2026, doi:10.5281/zenodo.20719257), as the caption states. Rendered by the Kidney-VLM '
                    'project from its own conversion of the TCIA series: windowed, cropped and outlined.'),
    'reuseTerms': ('Images CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/); BAMF and RCC-AID masks CC BY 4.0 '
                   '(https://creativecommons.org/licenses/by/4.0/). This preview is an adaptation; reuse requires attribution '
                   'to the TCIA collection and to the mask source.'),
    'sources': ['tcia-tcga-kirc', 'bamf-aimi-zenodo', 'bamf-aimi-paper', 'rcc-aid-zenodo', 'rcc-aid-paper'],
    'alignment': ('BAMF DICOM-SEG and RCC-AID NIfTI masks placed on the Kidney-VLM conversion of the same TCIA series; the '
                  'outlines were checked visually against the anatomy in every view.'),
    'items': [
        ('TCGA-BP-5200', "TCGA-KIRC TCGA-BP-5200 (venous phase from a reader's label; GE; 0.86 × 0.86 × 5.0 mm; uncorrected BAMF mask): a tumour replaces much of the right kidney, and the left kidney is outlined normally. The largest tumour section is slice 5 of 35, so the tumour sits at the bottom of this volume, as the coronal view shows.", 'CT with a tumour outlined in red replacing much of the right kidney and a normal left kidney outlined in green.'),
        ('TCGA-CJ-6033', "TCGA-KIRC TCGA-CJ-6033 (arterial phase from a reader's label; GE; 0.70 × 0.70 × 1.5 mm; uncorrected BAMF mask): a very large, heterogeneous right-kidney tumour with a dark, probably necrotic centre and a thick enhancing rim; only a small rim of kidney remains.", 'CT with a very large heterogeneous tumour outlined in red in the right kidney, with a thin rim of kidney outlined in green.'),
        ('TCGA-CZ-5984', "TCGA-KIRC TCGA-CZ-5984 (delayed phase from a reader's label; Siemens; 0.82 × 0.82 × 5.0 mm; RCC-AID mask): a rounded tumour in the left kidney, clearly separated from the kidney outline and consistent across all three planes.", 'CT with a rounded tumour outlined in red in the left kidney.'),
        ('TCGA-DV-5574', "TCGA-KIRC TCGA-DV-5574 (arterial phase from a reader's label; Philips; 0.68 × 0.68 × 1.0 mm; RCC-AID mask): a small tumour at the upper medial edge of the right kidney; both kidneys enhance strongly. Thin 1 mm slices make the coronal and sagittal views smooth.", 'Thin-slice CT with a small tumour outlined in red at the upper edge of the right kidney.'),
        ('TCGA-B8-5158_cyst', "TCGA-KIRC TCGA-B8-5158, centred on a cyst (delayed phase from a reader's label; Siemens; 0.81 × 0.81 × 5.0 mm; RCC-AID mask): two large, dark, fluid-density cysts on the right kidney and a large tumour in the left kidney. The cysts are much darker than the tumour, which is why they carry their own label.", 'CT with two large yellow-outlined cysts on the right kidney and a red-outlined tumour in the left kidney.'),
        ('TCGA-CJ-4918_cyst', "TCGA-KIRC TCGA-CJ-4918, centred on a small right-kidney cyst (arterial phase from a reader's label; GE; 0.74 × 0.74 × 2.5 mm; uncorrected BAMF mask); the left kidney carries a large tumour. This series is mainly a chest scan: the coronal view shows the lungs, the cyst lies on slice 5 of 133, the kidneys are cut off at the lower edge, and the image is grainy, as from a sharp lung reconstruction. Such series do not fully cover the kidneys.", 'Mainly chest CT whose lower edge shows the kidneys, with a small yellow-outlined cyst and a red-outlined tumour.'),
        ('TCGA-CJ-5677_cyst', "TCGA-KIRC TCGA-CJ-5677, centred on a small cyst in the left kidney (arterial phase from a reader's label; GE; 0.70 × 0.70 × 1.5 mm; uncorrected BAMF mask); a large tumour occupies the right kidney. Small cysts like this one would not appear in a tumour-centred view.", 'CT centred on a small yellow-outlined cyst in the left kidney, with a large red-outlined tumour in the right kidney.'),
    ],
}

RCCAID = {
    'release': 'rcc-aid-v2', 'folder': 'rccaid',
    'attribution': ("Images and labels: RCC-AID version 2.0.0 (de Boer, Häntze et al. 2026, doi:10.5281/zenodo.20719257; "
                    "doi:10.59275/j.melba.2026-2dg2), whose images come from The Cancer Imaging Archive's TCGA-KIRC, "
                    "TCGA-KIRP and TCGA-KICH collections (Akin et al. 2016; Linehan et al. 2016). Rendered by the Kidney-VLM "
                    "project: reoriented for display, windowed, cropped and outlined."),
    'reuseTerms': ('Masks CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/); images CC BY 3.0 '
                   '(https://creativecommons.org/licenses/by/3.0/), from TCIA. This preview is an adaptation; reuse requires '
                   'attribution to RCC-AID and to the TCIA collections.'),
    'sources': ['rcc-aid-zenodo', 'rcc-aid-paper', 'tcia-tcga-kirc', 'tcia-tcga-kirp', 'tcia-tcga-kich'],
    'alignment': "RCC-AID's released image and label files, which share one grid; nothing was re-registered.",
    'items': [
        ('KIRC_TCGA-BP-4777_239334', 'Clear cell RCC, TCGA-BP-4777 (delayed phase; GE; 0.78 × 0.78 × 2.5 mm): a small tumour on the front of the right kidney. The series spans only 51 slices of 2.5 mm, so the coronal view is a thin strip.', 'CT with a small tumour outlined in red on the front of the right kidney.'),
        ('KIRC_TCGA-BP-4777_239334_cyst', 'Clear cell RCC, TCGA-BP-4777, the same scan centred on a small cyst near the collecting system of the left kidney: tumour and cyst in opposite kidneys.', 'CT centred on a small yellow-outlined cyst in the left kidney, with a red-outlined tumour in the right kidney.'),
        ('KIRC_TCGA-BP-4797_717080', 'Clear cell RCC, TCGA-BP-4797 (venous phase; GE; 0.71 × 0.71 × 5.0 mm): a tumour set within the right kidney.', 'CT with a tumour outlined in red within the right kidney.'),
        ('KIRP_TCGA-B9-4114_196173', 'Papillary RCC, TCGA-B9-4114 (venous phase; Siemens; 0.68 × 0.68 × 5.0 mm): a very large, weakly enhancing tumour replacing and displacing the left kidney.', 'CT with a very large tumour outlined in red replacing the left kidney.'),
        ('KIRP_TCGA-B9-4114_658236', "Papillary RCC, TCGA-B9-4114, the same patient's delayed-phase scan (Siemens; 0.64 × 0.64 × 0.6 mm): two scans of one patient with consistent labels, here with very thin slices. Both scans are in the release, so splits must be made by patient.", 'Thin-slice CT of the same very large left-kidney tumour outlined in red.'),
        ('KICH_TCGA-KN-8430_337648', 'Chromophobe RCC, TCGA-KN-8430 (delayed phase; Siemens; 0.74 × 0.74 × 5.0 mm): a round tumour at the lower pole of the left kidney.', 'CT with a round tumour outlined in red at the lower pole of the left kidney.'),
        ('KICH_TCGA-KN-8419_166781', 'Chromophobe RCC, TCGA-KN-8419 (delayed phase; Siemens; 0.60 × 0.60 × 3.0 mm): a very large left-sided tumour with a darker central area. The tumour mask has small unlabelled holes near its centre and a ragged upper edge, left over from correction.', 'CT with a very large left-sided tumour outlined in red, with a darker centre.'),
        ('KICH_TCGA-KN-8419_166781_cyst', 'Chromophobe RCC, TCGA-KN-8419, the same scan centred on two small cysts in the left kidney, which the tumour has pushed down to pelvic level.', 'CT centred on two small yellow-outlined cysts in a displaced left kidney.'),
        ('KICH_TCGA-KM-8440_736060_cyst', 'Chromophobe RCC, TCGA-KM-8440 (venous phase; Siemens; 0.78 × 0.78 × 1.0 mm): a tumour at the hilum of the left kidney with a cyst beside it.', 'CT with a red-outlined tumour at the hilum of the left kidney and a yellow-outlined cyst beside it.'),
    ],
}

AMOS_PANELS = ('Four views of one scan: the whole axial slice where the right kidney is largest, a zoomed axial crop, '
               'and coronal and sagittal cuts through the centre of the right kidney. Both kidneys are outlined in green; '
               'there is no stone or cyst mask. Window 50/500 HU; radiological orientation (patient left on viewer right).')
# Rendered by the Kidney-VLM project with RadGPT/tools/render_preview.py (kept outside this repository), which follows
# the four-panel conventions in docs/previews.md; the lesion has its own colour because the release does not type it.
ATLAS = {
    'release': 'abdomenatlas-3-0-mini', 'folder': 'abdomenatlas',
    'attribution': ('Images and masks: AbdomenAtlas 3.0 (Bassi et al., ICCV 2025, doi:10.1109/ICCV51701.2025.02202), '
                    'Hugging Face AbdomenAtlas/AbdomenAtlas3.0Mini, revision 122e04f. The release does not record which of '
                    'its 17 source datasets this scan came from. Rendered by the Kidney-VLM project: reoriented for '
                    'display, windowed, cropped and outlined.'),
    'reuseTerms': ('CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/), the licence on the dataset card. '
                   'This preview is an adaptation and is shared under the same licence. The RadGPT repository\'s LICENSE '
                   'states CC BY-NC-ND 4.0, which does not allow adaptations; a curator has to settle which applies before '
                   'approving this preview.'),
    'sources': ['abdomenatlas3-metadata-csv', 'abdomenatlas3-image-files', 'abdomenatlas3-hf-card', 'radgpt-paper',
                'radgpt-repo-license'],
    'alignment': ("The release's own CT and mask files; in this case they share one voxel grid and header (checked). "
                  'Nothing was re-registered.'),
    'items': [
        ('BDMAP_00000061', "AbdomenAtlas 3.0 BDMAP_00000061 (venous phase, Siemens scanner and voxel spacing 1.5 × 1.5 × 1.5 from the release's metadata table; no unit is stated in the table or this file's header): the release's report lists a 9.5 × 8.6 cm hypoattenuating lesion in the right kidney and five in the left kidney, the largest 7.8 × 5.4 cm. The kidney masks overlap the lesion mask, so the green kidney outline also runs around most of the lesion.", 'CT with a large round lesion outlined in orange in the right kidney and a lesion in the left kidney, shown in axial, zoomed, coronal and sagittal views.'),
    ],
}

# Not a Kidney-VLM rendering: DeepTumorVQA's own organ PNG, downloaded from the release and only compressed here.
DTV = {
    'release': 'deeptumorvqa-2-0', 'folder': 'deeptumorvqa',
    'attribution': ('Image: DeepTumorVQA 2.0 (Chen et al. 2026, arXiv:2605.09679), Hugging Face tumor-vqa/DeepTumorVQA_2.0, '
                    'revision a8b9db5, benchmark/images_2d/organ/BDMAP_00000162_kidney.png, rendered by DeepTumorVQA from the '
                    'AbdomenAtlas 3.0 scan BDMAP_00000162, which DeepTumorVQA\'s ID mapping gives as KiTS21_img0205 (KiTS, Heller et al.). '
                    'Compressed to WebP for the atlas; nothing else was changed.'),
    'reuseTerms': ('Governed by the source CT licence, according to the DeepTumorVQA card, which points to AbdomenAtlas3.0Mini. '
                   'That dataset\'s card states CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/) and its '
                   'repository CC BY-NC-ND 4.0. By DeepTumorVQA\'s ID mapping the scan is a KiTS case, and KiTS23 is CC BY-NC-SA 4.0. '
                   'A curator has to settle which applies before approving this preview.'),
    'sources': ['deeptumorvqa-image-files', 'deeptumorvqa-hf-card', 'deeptumorvqa-paper', 'deeptumorvqa-question-files',
                'deeptumorvqa-metadata-files', 'deeptumorvqa-id-mapping'],
    'alignment': 'No mask is drawn; the image is shown as released.',
    'items': [
        ('BDMAP_00000162_kidney', "DeepTumorVQA benchmark scan BDMAP_00000162 (KiTS21_img0205 by DeepTumorVQA's ID mapping). Its benchmark questions ask whether the kidney has tumours (answer: Yes) and where the largest one is (answer: left). The metadata lists three kidney tumours with a total volume of 15.3 cm³; its recorded largest-tumour diameter, 16.1 cm, is one of the values affected by the diameter defect described in the quality findings.", 'Five axial CT slices of the abdomen side by side, at levels through the kidneys, without outlines.'),
    ],
}


# Rendered by the Kidney-VLM project with AMOS-MM/tools/render_preview.py (kept outside this repository), adapted from the
# AbdomenAtlas renderer. AMOS-MM releases no masks; this CT is an AMOS22 file, so AMOS22's label map fits it.
AMOS = {
    'release': 'amos-mm-2024', 'folder': 'amos-mm',
    'attribution': ('CT: AMOS-MM (MICCAI 2024 AMOS-MM challenge; Ji, Ge, Li and Luo), imagesTr/amos_0088.nii.gz from the public '
                    'Google Drive release, which matches amos_0088 of AMOS22 in size and CRC32 (Ji et al., NeurIPS 2022; '
                    'doi:10.5281/zenodo.7262581). Kidney mask: AMOS22 labelsTr/amos_0088.nii.gz. Rendered by the Kidney-VLM '
                    'project: reoriented for display, windowed, cropped and outlined.'),
    'reuseTerms': ('Unresolved. The CT matches an AMOS22 file in size and CRC32, and AMOS22\'s own statements differ: its Zenodo '
                   'record says CC BY 4.0, its dataset.json "CC-BY-SA 4.0" and the AMOS paper CC BY-NC-SA. AMOS-MM\'s JSON '
                   'files state CC BY-ND 4.0, which does not allow adaptations, and its design document CC BY-SA. A curator '
                   'has to settle which applies before approving this preview.'),
    'sources': ['amos-mm-image-files', 'amos-mm-report-json', 'amos-mm-vqa-json', 'amos-mm-zip-listings', 'amos22-zenodo',
                'amos-paper', 'amos-mm-design-doc', 'deeptumorvqa-id-mapping', 'abdomenatlas3-metadata-csv'],
    'alignment': 'The AMOS22 mask and the AMOS-MM CT share one voxel grid and affine (checked). Nothing was re-registered.',
    'items': [
        ('amos_0088', "AMOS-MM amos_0088, a training case from site A (Aquilion ONE scanner in the release's metadata; voxel size 0.75 × 0.75 × 5.0 mm from the file header). Its report finds \"a small dot-like high-density focus\" and \"an unenhanced low-density focus\" of about 6 mm in the right kidney, and the impression reads \"Small kidney stone in the right kidney and a small cyst.\" Six of its questions are about the right kidney. AMOS22 outlines organs only, so neither finding is outlined here; the same scan is AbdomenAtlas 3.0 BDMAP_00001989, whose metadata lists one 0.6 cm hypoattenuating lesion in the right kidney.", 'CT with both kidneys outlined in green, shown in axial, zoomed, coronal and sagittal views.'),
    ],
}


def cptac_mask(name, caption):
    if 'radiologist-corrected BAMF' in caption:
        return 'Mask: BAMF (AI-generated, AIMI Annotations), corrected by a radiologist.'
    return 'Mask: BAMF (AI-generated, AIMI Annotations), uncorrected AI output.'


def tcga_mask(name, caption):
    if 'RCC-AID mask' in caption:
        return ('Mask: RCC-AID, started by a model and corrected by trained students, with a radiologist deciding '
                'uncertain cases.')
    return cptac_mask(name, caption)


MASK_LINE = {
    'kits23': lambda n, c: "Mask: KiTS23's own reference labels, drawn by trained annotators with expert review of doubtful cases.",
    'ucsf-rmac-2025': lambda n, c: "Mask: UCSF RMaC's own annotation, drawn by a radiology resident and reviewed by an attending radiologist. In these examples it is a bounding box, not an outline.",
    'cptac-ccrcc-v14': cptac_mask,
    'tcga-kirc-tcia': tcga_mask,
    'rcc-aid-v2': lambda n, c: ("Mask: RCC-AID's own label, started by a model and corrected by trained students, with a "
                                "radiologist deciding uncertain cases. Phase is RCC-AID's radiologist label."),
    'abdomenatlas-3-0-mini': lambda n, c: ("Mask: AbdomenAtlas 3.0's own masks. The kidney masks come from AbdomenAtlas 1.1 "
                                           "(AI with radiologists in the loop); the kidney lesion mask was drawn by AI and "
                                           "corrected by radiologists."),
    'deeptumorvqa-2-0': lambda n, c: "No mask: DeepTumorVQA's own image, as released for its questions.",
    'amos-mm-2024': lambda n, c: ("Mask: AMOS22's organ mask, not part of AMOS-MM. AMOS22's masks were pre-labelled by models "
                                  "and checked by junior and then senior radiologists; a few scans were drawn by hand."),
}

samples, total_in, total_out = [], 0, 0
for spec in (KITS, RMAC, CPTAC, TCGA, RCCAID, ATLAS, DTV, AMOS):
    out_dir = os.path.join(REPO, 'public', 'previews', spec['release'])
    os.makedirs(out_dir, exist_ok=True)
    intro = {id(RMAC): RMAC_PANELS, id(ATLAS): ATLAS_PANELS, id(DTV): DTV_PANELS, id(AMOS): AMOS_PANELS}.get(id(spec), FOUR_PANEL)
    for name, caption, alt in spec['items']:
        src = os.path.join(FIG, spec['folder'], name + '.png')
        dst = os.path.join(out_dir, name + '.webp')
        im = Image.open(src).convert('RGB')
        im.save(dst, 'WEBP', quality=82, method=6)
        total_in += os.path.getsize(src); total_out += os.path.getsize(dst)
        mask = MASK_LINE[spec['release']](name, caption)
        caption = re.sub(r';? ?((radiologist-corrected |uncorrected )?BAMF|RCC-AID) mask', '', caption).replace(' ()', '').replace('; )', ')')
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
