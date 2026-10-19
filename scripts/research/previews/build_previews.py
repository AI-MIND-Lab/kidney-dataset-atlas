"""Compress the preview renderings into public/previews/ and write src/data/samples/processed-figures.json.

Input: the full-size PNG renderings in figures/<folder>/, committed so anyone can rebuild the previews. Only
renderings that a preview uses belong there. KiTS23, UCSF RMaC and TCGA-KIRC are drawn by render_previews.py in this
folder (at 2x, 220 DPI); the others came from the Kidney-VLM project as they are. docs/previews.md explains how the
previews were made and who drew each mask.

Under each image the site shows only facts and the provider's own words: the case identifier, who drew the mask, and
text the provider published about that case, copied exactly (QUOTE below), marked when a program generated it. Nothing
written by the atlas describes the image. How to read a kind of preview (VIEW guides) and the credit are shown once per
group, not per image.

The page loads a copy at most PAGE_WIDTH pixels wide; a wider rendering also ships whole, as the copy the reader opens
when enlarging the image. Every sample stays unapproved: permissionApprovedBy is a curator's decision.

Requires: pip install -r scripts/research/requirements.txt
"""
import json, os
from pathlib import Path
from PIL import Image

REPO = str(Path(__file__).resolve().parents[3])
FIG = os.path.join(REPO, 'figures')
PAGE_WIDTH = 1700  # wider renderings (the 2x ones) are halved for the page and also shipped whole


def quote(field, value, source, locator, generated_by=None):
    """Text the provider published about the case, copied exactly; generated_by names the program, if one wrote it."""
    return {'field': field, 'value': value, 'source': source, 'locator': locator, 'generatedBy': generated_by}


# Who drew the outlines, in a few words; shown under each image as "Mask: ...".
BAMF_CORRECTED = 'BAMF, AI-generated, corrected by a radiologist'
BAMF_UNCORRECTED = 'BAMF, AI-generated, not corrected'
RCCAID_MASK = 'RCC-AID, drawn by a model and corrected by trained students'
# BAMF's radiologist rated these AI masks in its review file (qa-results.csv): 5 = use as is, 4 = acceptable.
BAMF_REVIEWED = 'BAMF, AI-generated, reviewed by a radiologist and rated acceptable'


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
    'sources': ['kits23-challenge-page', 'kits23-readme', 'kits23-repo-dataset'],
    'alignment': 'Outlines come from the reference segmentation on the same voxel grid as the image.',
    'mask': 'KiTS23 reference labels, drawn by trained annotators, with experts consulted on doubtful cases',
    'view': 'four-panel',
    # (file name, case, quotes): the case's histologic subtype in the release's clinical file.
    'items': [
        (name, case, None, [quote('tumor_histologic_subtype', subtype, 'kits23-repo-dataset', f'dataset/kits23.json, {case}')])
        for name, case, subtype in [
            ('case_00062', 'case_00062', 'chromophobe_rcc'),
            ('case_00236', 'case_00236', 'clear_cell_rcc'),
            ('case_00242', 'case_00242', 'clear_cell_rcc'),
            ('case_00242_cyst', 'case_00242', 'clear_cell_rcc'),
            ('case_00203_cyst', 'case_00203', 'clear_cell_rcc'),
            ('case_00433_cyst', 'case_00433', 'clear_cell_rcc'),
        ]
    ],
}

RMAC = {
    'release': 'ucsf-rmac-2025', 'folder': 'rmac',
    'attribution': ('Images and annotations: UCSF RMaC, the UCSF 3D Multi-Phase Renal Mass CT dataset (Larson 2025, '
                    'doi:10.58078/C2WC74; Sahin et al. 2026). Pathology from each exam file\'s attributes. Rendered by the '
                    'Kidney-VLM project: cropped, windowed and outlined.'),
    'reuseTerms': ('CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/). This preview is an adaptation of UCSF RMaC data; '
                   'reuse requires attribution to the dataset.'),
    'sources': ['ucsf-rmac-repo', 'ucsf-rmac-aws', 'ucsf-rmac-preprint', 'ucsf-rmac-exam-attributes'],
    'alignment': 'Phases shown are those the release registers to the non-contrast scan, so they share the annotation grid.',
    'mask': "UCSF RMaC's own bounding box, drawn by a radiology resident and reviewed by an attending radiologist",
    'view': 'phases',
    # The exam file's pathology attribute. Its numeric pathology_grade and tumor_type codes are not shown: the
    # provider does not document what they mean.
    'items': [
        (exam, exam, None, [quote('pathology', pathology, 'ucsf-rmac-exam-attributes', f'{exam}.hdf5, attribute pathology')])
        for exam, pathology in [
            ('3LYUFVSwiY', 'clear cell'),
            ('Mnx1XxZZPN', 'clear cell'),
            ('WC3J7Q0yat', 'chromophobe'),
            ('YoPBh7znuG', 'clear cell'),
        ]
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
    'sources': ['cptac-ccrcc-tcia', 'bamf-aimi-zenodo', 'bamf-aimi-paper', 'gdc-cptac-ccrcc-preview-cases'],
    'alignment': 'BAMF DICOM-SEG masks placed on the processed CT volumes. Masks are AI output unless marked as corrected.',
    'view': 'four-panel',
    # (file name, case, mask, quotes): the primary diagnosis in the case's GDC record (project CPTAC-3).
    'items': [
        (name, case, mask, [quote('primary_diagnosis', 'Renal cell carcinoma, NOS', 'gdc-cptac-ccrcc-preview-cases',
                                  f'case {case}, primary diagnosis record')])
        for name, case, mask in [
            ('C3L-00766', 'C3L-00766', BAMF_CORRECTED),
            ('C3N-00313', 'C3N-00313', BAMF_UNCORRECTED),
            ('C3N-02063', 'C3N-02063', BAMF_CORRECTED),
            ('C3N-02723', 'C3N-02723', BAMF_UNCORRECTED),
            ('C3N-02723_cyst', 'C3N-02723', BAMF_UNCORRECTED),
            ('C3L-01462_cyst', 'C3L-01462', BAMF_UNCORRECTED),
            ('C3N-00435_cyst', 'C3N-00435', BAMF_UNCORRECTED),
        ]
    ],
}

TCGA = {
    'release': 'tcga-kirc-tcia', 'folder': 'tcga',
    'attribution': ('Images: TCGA-KIRC collection, The Cancer Imaging Archive (Akin et al. 2016, '
                    'doi:10.7937/K9/TCIA.2016.V6PBVTDR). Masks: BAMF AI-generated segmentations from the AIMI Annotations '
                    'initiative (Van Oss et al. 2024, doi:10.5281/zenodo.8345959; Murugesan et al. 2024) or RCC-AID '
                    '(de Boer et al. 2026, doi:10.5281/zenodo.20719257), as the line under each image states. Rendered by the Kidney-VLM '
                    'project from its own conversion of the TCIA series: windowed, cropped and outlined.'),
    'reuseTerms': ('Images CC BY 3.0 (https://creativecommons.org/licenses/by/3.0/); BAMF and RCC-AID masks CC BY 4.0 '
                   '(https://creativecommons.org/licenses/by/4.0/). This preview is an adaptation; reuse requires attribution '
                   'to the TCIA collection and to the mask source.'),
    'sources': ['tcia-tcga-kirc', 'bamf-aimi-zenodo', 'bamf-aimi-paper', 'rcc-aid-zenodo', 'rcc-aid-paper', 'gdc-kirc-case-records'],
    'alignment': ('BAMF DICOM-SEG and RCC-AID NIfTI masks placed on the Kidney-VLM conversion of the same TCIA series; the '
                  'outlines were checked visually against the anatomy in every view.'),
    'view': 'four-panel',
    # (file name, case, mask, quotes): the primary diagnosis in the case's GDC record.
    'items': [
        (name, case, mask, [quote('primary_diagnosis', 'Clear cell adenocarcinoma, NOS', 'gdc-kirc-case-records',
                                  f'case {case}, primary diagnosis record')])
        for name, case, mask in [
            ('TCGA-BP-5200', 'TCGA-BP-5200', BAMF_REVIEWED),
            ('TCGA-CJ-6033', 'TCGA-CJ-6033', BAMF_REVIEWED),
            ('TCGA-CZ-5984', 'TCGA-CZ-5984', RCCAID_MASK),
            ('TCGA-DV-5574', 'TCGA-DV-5574', RCCAID_MASK),
            ('TCGA-B8-5158_cyst', 'TCGA-B8-5158', RCCAID_MASK),
            ('TCGA-CJ-4918_cyst', 'TCGA-CJ-4918', BAMF_UNCORRECTED),
            ('TCGA-CJ-5677_cyst', 'TCGA-CJ-5677', BAMF_UNCORRECTED),
        ]
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
    'mask': "RCC-AID's own labels, drawn by a model and corrected by trained students",
    'view': 'four-panel',
    # (file name, case, quotes): the collection and the radiologist's phase label of the scan's row in metadata.csv.
    'items': [
        (name, case, None, [
            quote('Collection', collection, 'rcc-aid-zenodo', f'metadata.csv, SeriesInstanceUID {uid}'),
            quote('phase_name', phase, 'rcc-aid-zenodo', f'metadata.csv, SeriesInstanceUID {uid}'),
        ])
        for name, case, collection, phase, uid in [
            ('KIRC_TCGA-BP-4777_239334', 'TCGA-BP-4777', 'TCGA-KIRC', 'delayed', '1.3.6.1.4.1.14519.5.2.1.9203.4004.235936898371580050182795239334'),
            ('KIRC_TCGA-BP-4777_239334_cyst', 'TCGA-BP-4777', 'TCGA-KIRC', 'delayed', '1.3.6.1.4.1.14519.5.2.1.9203.4004.235936898371580050182795239334'),
            ('KIRC_TCGA-BP-4797_717080', 'TCGA-BP-4797', 'TCGA-KIRC', 'venous', '1.3.6.1.4.1.14519.5.2.1.9203.4004.327825894677305020949379717080'),
            ('KIRP_TCGA-B9-4114_196173', 'TCGA-B9-4114', 'TCGA-KIRP', 'venous', '1.3.6.1.4.1.14519.5.2.1.8421.4010.338032800865844595006312196173'),
            ('KIRP_TCGA-B9-4114_658236', 'TCGA-B9-4114', 'TCGA-KIRP', 'delayed', '1.3.6.1.4.1.14519.5.2.1.8421.4010.147114767224735098774858658236'),
            ('KICH_TCGA-KN-8430_337648', 'TCGA-KN-8430', 'TCGA-KICH', 'delayed', '1.3.6.1.4.1.14519.5.2.1.3671.4011.201561248326219335494793337648'),
            ('KICH_TCGA-KN-8419_166781', 'TCGA-KN-8419', 'TCGA-KICH', 'delayed', '1.3.6.1.4.1.14519.5.2.1.3671.4011.214911382968244656730175166781'),
            ('KICH_TCGA-KN-8419_166781_cyst', 'TCGA-KN-8419', 'TCGA-KICH', 'delayed', '1.3.6.1.4.1.14519.5.2.1.3671.4011.214911382968244656730175166781'),
            ('KICH_TCGA-KM-8440_736060_cyst', 'TCGA-KM-8440', 'TCGA-KICH', 'venous', '1.3.6.1.4.1.14519.5.2.1.1357.4011.315847359121056583828629736060'),
        ]
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
                   'states CC BY-NC-ND 4.0, which does not allow adaptations. A curator has to decide which applies before '
                   'approving this preview.'),
    'sources': ['abdomenatlas3-metadata-csv', 'abdomenatlas3-image-files', 'abdomenatlas3-hf-card', 'radgpt-paper',
                'radgpt-repo-license'],
    'alignment': ("The release's own CT and mask files. In this case they share one voxel grid and header (checked). "
                  'Nothing was re-registered.'),
    'mask': "AbdomenAtlas 3.0's own masks, drawn by AI and corrected by radiologists",
    'view': 'atlas',
    'items': [
        ('BDMAP_00000061', 'BDMAP_00000061', None, [
            quote('narrative report, IMPRESSION',
                  'Enlarged kidneys with multiple hypoattenuating kidney masses, with the largest one measuring 9.5 x 8.6 cm.',
                  'abdomenatlas3-metadata-csv', 'AbdomenAtlas3.0MiniWithMeta.csv, row BDMAP_00000061, column "narrative report"',
                  generated_by='the RadGPT report pipeline (rules and a language model)'),
        ]),
    ],
}

# Not a Kidney-VLM rendering: DeepTumorVQA's own organ PNG, downloaded from the release and only compressed here.
DTV = {
    'release': 'deeptumorvqa-2-0', 'folder': 'deeptumorvqa',
    'attribution': ('Image: DeepTumorVQA 2.0 (Chen et al. 2026, arXiv:2605.09679), Hugging Face tumor-vqa/DeepTumorVQA_2.0, '
                    'revision a8b9db5, benchmark/images_2d/organ/BDMAP_00000162_kidney.png. Rendered by DeepTumorVQA from the '
                    'AbdomenAtlas 3.0 scan BDMAP_00000162, which DeepTumorVQA\'s ID mapping gives as KiTS21_img0205 (KiTS, Heller et al.). '
                    'Compressed to WebP for the atlas, with nothing else changed.'),
    'reuseTerms': ('Governed by the source CT licence, according to the DeepTumorVQA card, which points to AbdomenAtlas3.0Mini. '
                   'That dataset\'s card states CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/) and its '
                   'repository CC BY-NC-ND 4.0. By DeepTumorVQA\'s ID mapping the scan is a KiTS case, and KiTS23 is CC BY-NC-SA 4.0. '
                   'A curator has to settle which applies before approving this preview.'),
    'sources': ['deeptumorvqa-image-files', 'deeptumorvqa-hf-card', 'deeptumorvqa-paper', 'deeptumorvqa-question-files',
                'deeptumorvqa-metadata-files', 'deeptumorvqa-id-mapping'],
    'alignment': 'No mask is drawn. The image is shown as released.',
    'mask': None,
    'view': 'dtv',
    # Two of the benchmark questions asked about this kidney image, with their answers.
    'items': [
        ('BDMAP_00000162_kidney', 'BDMAP_00000162', None, [
            quote('question', 'Are there any tumors present in the kidney?', 'deeptumorvqa-question-files',
                  'benchmark/test_qa.jsonl, qid bench_00699', generated_by="DeepTumorVQA's question generator"),
            quote('answer', 'Yes', 'deeptumorvqa-question-files', 'benchmark/test_qa.jsonl, qid bench_00699',
                  generated_by="DeepTumorVQA's question generator"),
            quote('question', 'Indicate the position of the largest kidney tumor:', 'deeptumorvqa-question-files',
                  'benchmark/test_qa.jsonl, qid bench_00214', generated_by="DeepTumorVQA's question generator"),
            quote('answer', 'left', 'deeptumorvqa-question-files', 'benchmark/test_qa.jsonl, qid bench_00214',
                  generated_by="DeepTumorVQA's question generator"),
        ]),
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
    'reuseTerms': ('Unresolved. The CT matches an AMOS22 file in size and CRC32, and AMOS22\'s own statements differ. The AMOS22 '
                   'Zenodo record says CC BY 4.0, its dataset.json "CC-BY-SA 4.0" and the AMOS paper CC BY-NC-SA. AMOS-MM\'s '
                   'JSON files state CC BY-ND 4.0, which does not allow adaptations, while its design document says CC BY-SA. '
                   'A curator has to settle which applies before approving this preview.'),
    'sources': ['amos-mm-image-files', 'amos-mm-report-json', 'amos-mm-vqa-json', 'amos-mm-zip-listings', 'amos22-zenodo',
                'amos-paper', 'amos-mm-design-doc', 'deeptumorvqa-id-mapping', 'abdomenatlas3-metadata-csv'],
    'alignment': ('The AMOS22 mask and the AMOS-MM CT have the same voxel grid, and the same position, orientation and spacing '
                  'in their headers (checked). Nothing was re-registered.'),
    'mask': "AMOS22 organ masks (not part of AMOS-MM), pre-labelled by models and checked by radiologists",
    'view': 'amos',
    'items': [
        ('amos_0088', 'amos_0088', None, [
            quote('impression (abdomen)', 'Small kidney stone in the right kidney and a small cyst.', 'amos-mm-report-json',
                  'report_generation_train_val.json, imagesTr/amos_0088, labels.report.impression.abdomen'),
        ]),
    ],
}


# How to read each kind of preview; shown once above a group of previews, never as a caption.
VIEW = {'four-panel': FOUR_PANEL, 'phases': RMAC_PANELS, 'atlas': ATLAS_PANELS, 'dtv': DTV_PANELS, 'amos': AMOS_PANELS}
# Alt text says what kind of image it is, not what the atlas thinks it shows.
ALT = {
    'four-panel': 'Four views of CT {case}: axial, zoomed axial, coronal and sagittal, with the mask drawn as outlines.',
    'phases': "Contrast phases of CT exam {case} at one slice, with the dataset's bounding box.",
    'atlas': 'Four views of CT {case}: axial, zoomed axial, coronal and sagittal, with kidney and kidney lesion outlines.',
    'dtv': 'Five axial CT slices of {case} side by side, as released by DeepTumorVQA.',
    'amos': 'Four views of CT {case}: axial, zoomed axial, coronal and sagittal, with kidney outlines.',
}


def webp(image, path):
    image.save(path, 'WEBP', quality=82, method=6)
    return os.path.getsize(path)


samples, total_in, total_out = [], 0, 0
for spec in (KITS, RMAC, CPTAC, TCGA, RCCAID, ATLAS, DTV, AMOS):
    out_dir = os.path.join(REPO, 'public', 'previews', spec['release'])
    os.makedirs(out_dir, exist_ok=True)
    for name, case, mask, quotes in spec['items']:
        src = os.path.join(FIG, spec['folder'], name + '.png')
        full = Image.open(src).convert('RGB')
        total_in += os.path.getsize(src)
        page = full
        large = None
        if full.width > PAGE_WIDTH:  # a 2x rendering: the page gets half, the enlarged view the whole
            page = full.resize((full.width // 2, full.height // 2), Image.LANCZOS)
            total_out += webp(full, os.path.join(out_dir, name + '-large.webp'))
            large = {'path': f"/previews/{spec['release']}/{name}-large.webp", 'width': full.width, 'height': full.height}
        else:
            stale = os.path.join(out_dir, name + '-large.webp')
            if os.path.exists(stale):
                os.remove(stale)
        total_out += webp(page, os.path.join(out_dir, name + '.webp'))
        samples.append({
            'id': f"{spec['release']}-{name.lower().replace('_', '-')}",
            'release': spec['release'],
            'kind': 'dataset_sample',
            'assets': [{'path': f"/previews/{spec['release']}/{name}.webp", 'role': 'image', 'sliceIndex': None,
                        'width': page.width, 'height': page.height, 'large': large}],
            'caseId': case,
            'mask': mask if mask is not None else spec['mask'],
            'providerText': quotes,
            'viewGuide': VIEW[spec['view']],
            'alt': ALT[spec['view']].format(case=case),
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
