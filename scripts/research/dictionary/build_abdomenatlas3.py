"""Build src/data/variables/abdomenatlas-3-0-mini.json from the AbdomenAtlas 3.0 metadata table and mask file list.

Observed values (fill counts, codes, ranges) are recounted from every row of AbdomenAtlas3.0MiniWithMeta.csv at
Hugging Face revision 122e04f (source abdomenatlas3-metadata-csv). Definitions come from the RadGPT metadata
script, which reads the numbers back out of the report text (source radgpt-metadata-script), and from the paper
(source radgpt-paper). A column no source explains is described as such.

The CSV (16 MB) is downloaded once into .research-cache/dictionary/; set ABDOMENATLAS_CSV to a local copy to skip
the download. Either way its sha256 must match the Hugging Face file. The mask file names below were listed from
the mask tarballs (source abdomenatlas3-mask-files); the builder cannot recount them without those tarballs.
"""
import collections
import csv
import hashlib
import os
import re

import _setup  # noqa: F401
from common import REPO, cache_dir, get, write_json

RELEASE = 'abdomenatlas-3-0-mini'
REV = '122e04fc188949ed60a74f3bc6b4fa74e06a6152'
SHA256 = '6d1803094b2e454ba11d5da905b99f3073ac84b75baa870bfa848ed0f637922b'
FILE = 'AbdomenAtlas3.0MiniWithMeta.csv'
URL = f'https://huggingface.co/datasets/AbdomenAtlas/AbdomenAtlas3.0Mini/resolve/{REV}/{FILE}'
OUT = REPO / 'src' / 'data' / 'variables' / f'{RELEASE}.json'
ON = '2026-09-30'


def load_csv():
    path = os.environ.get('ABDOMENATLAS_CSV')
    if path:
        data = open(path, 'rb').read()
    else:
        local = cache_dir('dictionary') / f'abdomenatlas3-{REV[:7]}.csv'
        if not local.exists():
            body = get(URL, binary=True)
            if body is None:
                raise SystemExit(f'Could not download {FILE} at revision {REV[:7]}')
            local.write_bytes(body)
        data = local.read_bytes()
    if hashlib.sha256(data).hexdigest() != SHA256:
        raise SystemExit(f'{FILE} does not match the pinned revision {REV[:7]}')
    return list(csv.DictReader(data.decode('utf8').splitlines(keepends=True)))


rows = load_csv()
N = len(rows)
COLUMNS = list(rows[0].keys())

TABLE = {'sources': ['abdomenatlas3-metadata-csv'], 'locator': f'{FILE}, all {N:,} rows', 'status': 'verified', 'verifiedOn': ON}
SCRIPT = {'sources': ['abdomenatlas3-metadata-csv', 'radgpt-metadata-script'],
          'locator': f'{FILE}, all {N:,} rows; ExtractComprehensiveMedatadaReports.py (parse_radiology_report, parse_lesions, fill_nan_in_specific_columns)',
          'status': 'verified', 'verifiedOn': ON}
ORIGIN = {'sources': ['abdomenatlas3-metadata-csv', 'radgpt-metadata-script'],
          'locator': f'{FILE}, all {N:,} rows; ExtractComprehensiveMedatadaReports.py (create_big_table)', 'status': 'verified', 'verifiedOn': ON}


def filled(col):
    return [r[col] for r in rows if r[col].strip() != '']


def n_blank(col):
    return N - len(filled(col))


def num(v):
    return float(v)


def fmt(x):
    return f'{x:g}'


def blank_note(col, meaning):
    b = n_blank(col)
    return [f'blank: {meaning} ({b:,} of {N:,} rows)'] if b else []


def codes(col, meanings=None):
    c = collections.Counter(filled(col))
    return [{'code': v, 'meaning': ((meanings or {}).get(v, '') + ' ' if (meanings or {}).get(v) else '') + f'({n:,} of {N:,} rows)'}
            for v, n in c.most_common()]


def value_range(col):
    vals = [num(v) for v in filled(col)]
    return min(vals), max(vals)


def spacing_first():
    out = 0
    for r in rows:
        s = [float(x) for x in r['spacing'].strip('[]').split()]
        out += s[0] > s[1] and s[0] > s[2]
    return out


PHASE_LINES = ('CT Venous Phase', 'CT Arterial Phase', 'Non-contrast CT', 'CT Delay Phase')
PHASE_IN_REPORT = sum(1 for r in rows if r['structured report'].split('\n')[0].strip() in PHASE_LINES)

V = []


def add(col, definition, vtype, group, role, unit=None, coding=None, missing=None, level='examination',
        provenance=None, evidence=SCRIPT, derivation='derived', concept=None, file=FILE, key=None):
    V.append({
        'id': f'{RELEASE}-' + (key or re.sub(r'[^a-z0-9]+', '-', col.lower()).strip('-')),
        'release': RELEASE,
        'originalName': col,
        'file': file,
        'definition': definition,
        'type': vtype,
        'unit': unit,
        'coding': coding or [],
        'missingValues': missing or [],
        'observationLevel': level,
        'timePoint': None,
        'role': role,
        'group': group,
        'derivation': derivation,
        'normalizedConcept': concept,
        **({'provenance': provenance} if provenance else {}),
        'evidence': evidence,
    })


# --- identifier, geometry, demographics, acquisition
ids = [r['BDMAP ID'] for r in rows]
assert len(set(ids)) == N
add('BDMAP ID', f'Scan identifier: "BDMAP_" followed by eight digits, unique per row ({ids[0]} to {max(ids)}). It names the '
    'case folder in the image and mask tarballs and the rows of the train/test lists.', 'text', 'administrative', 'identifier',
    evidence=TABLE, derivation='raw', key='bdmap-id', provenance='Joins the table to ct.nii.gz, the mask files and TrainTestIDS/.')
add('spacing', 'Voxel size of the CT, three numbers written like a NumPy array (for example "[0.8222656 0.8222656 2.5]"), in the '
    f'file\'s own axis order. In {spacing_first():,} rows the largest value comes first, so the slice axis is not always the last axis. '
    'No source states the unit. In the 232 CT headers checked, 170 give millimetres and 62 give no unit.',
    'other', 'imaging', 'descriptor', evidence=ORIGIN,
    provenance='Copied by the metadata script from an input table that is not part of the release. Matched the NIfTI header in all 232 cases checked (BDMAP_00000001 to BDMAP_00000232).')
add('shape', 'Voxel grid size, three numbers, for example "(512, 512, 339)". It does not describe the released CT files. In '
    'all 232 cases checked, the released volume is smaller along at least one axis (see the quality findings).',
    'other', 'imaging', 'descriptor', evidence=ORIGIN,
    provenance='Copied by the metadata script from an input table that is not part of the release. Which processing step it describes is not documented.')
add('sex', 'Patient sex.', 'categorical', 'clinical', 'predictor', level='patient', coding=codes('sex', {'M': 'Male', 'F': 'Female'}),
    missing=blank_note('sex', 'not available'), evidence=ORIGIN, derivation='raw', concept='sex',
    provenance='Taken by the metadata script from two input tables that are not part of the release (a "dap atlas" table and a TotalSegmentator table).')
lo, hi = value_range('age')
add('age', f'Patient age. The unit is not stated. The metadata script removes a leading zero and a trailing "Y" from the '
    f'source value. Observed range {fmt(lo)} to {fmt(hi)}.', 'decimal', 'clinical', 'predictor', level='patient',
    missing=blank_note('age', 'not available'), evidence=ORIGIN, derivation='raw', concept='age',
    provenance='Taken by the metadata script from the same two input tables as sex.')
add('scanner', 'CT scanner manufacturer.', 'categorical', 'imaging', 'descriptor', coding=codes('scanner'),
    missing=blank_note('scanner', 'not available'), evidence=ORIGIN, derivation='raw', concept='scanner manufacturer',
    provenance='Taken by the metadata script only from a TotalSegmentator input table that is not part of the release.')
add('contrast', f'Contrast phase of the scan. The structured report\'s first line names a phase for more scans ({PHASE_IN_REPORT:,}) '
    'than this column does.', 'categorical', 'imaging', 'descriptor', coding=codes('contrast'),
    missing=blank_note('contrast', 'not recorded'), evidence=ORIGIN, derivation='raw', concept='contrast phase',
    provenance='Copied by the metadata script from an input table that is not part of the release. How the phase was determined is not documented.')

# --- organ volumes, read from the report text
ORGAN_VOL = {
    'liver volume (cm^3)': ('the liver', 'the "(volume: ... cc)" text in the Liver section of the structured report'),
    'pancreas volume (cm^3)': ('the pancreas', 'the "(volume: ... cc)" text in the Pancreas section of the structured report'),
    'spleen volume (cm^3)': ('the spleen', 'the "(volume: ... cc)" text in the Spleen section of the structured report'),
    'left kidney volume (cm^3)': ('the left kidney', 'the "left kidney volume:" text in the Kidney section of the structured report'),
    'right kidney volume (cm^3)': ('the right kidney', 'the "right kidney volume:" text in the Kidney section of the structured report'),
    'kidney volume (cm^3)': ('both kidneys together', 'the "total kidney volume:" text in the Kidney section of the structured report'),
}
for col, (organ, where) in ORGAN_VOL.items():
    zeros = sum(1 for v in filled(col) if num(v) == 0)
    lo, hi = value_range(col)
    add(col, f'Volume of {organ}, read from {where}. The report computes it from the mask. Observed range {fmt(lo)} to {fmt(hi)}'
        + (f', with {zeros} rows at 0.' if zeros else '.'), 'decimal', 'imaging', 'descriptor', unit='cm³',
        missing=blank_note(col, 'no value in the report'), concept='organ volume',
        provenance='The metadata script parsed the report while its volumes still read "cm^3". The script\'s main() then rewrote them as "cc" in the released report text.',
        evidence={**SCRIPT, 'sources': SCRIPT['sources'] + ['radgpt-paper'], 'locator': SCRIPT['locator'] + ' and main() (cm^3 rewritten as cc); paper section 3.1.2'})

# --- lesion columns, read from the numbered lesions in the report text
ORGANS = {'liver': 'Liver', 'pancreatic': 'Pancreas', 'kidney': 'Kidney', 'colon': 'Colon'}
LOC = {'liver': ('largest liver lesion location (1-8)', 'liver segment numbers 1 to 8, joined by commas when the lesion spans several'),
       'pancreatic': ('largest pancreatic lesion location (head, body, tail)',
                      'the pancreas part (head, body or tail), with several parts joined by commas'),
       'kidney': ('largest kidney lesion location (left, right)', 'the side, left or right')}
NO_LESION = 'no lesion in the report, or no report at all (BDMAP_00005266)'
ZERO = '0: no numbered lesion in the report\'s {s} section, or no report at all. The script writes 0 when a lesion count, size or volume is missing.'
for organ, section in ORGANS.items():
    c_vol = f'total {organ} lesion volume (cm^3)'
    c_n = f'number of {organ} lesion instances'
    c_d = f'largest {organ} lesion diameter (cm)'
    c_att = f'largest {organ} lesion attenuation (hyperattenuating, isoattenuating, hypoattenuating)'
    pos_n = sum(1 for v in filled(c_n) if num(v) > 0)
    lo, hi = value_range(c_n)
    add(c_n, f'Number of numbered lesion entries ("{section} lesion N:" or "{section} tumor N:") in the report\'s {section} '
        f'section. Above 0 in {pos_n:,} rows, with a maximum of {fmt(hi)}.', 'integer', 'imaging', 'descriptor',
        missing=[ZERO.format(s=section)], level='examination', concept='lesion count')
    pos_v = sum(1 for v in filled(c_vol) if num(v) > 0)
    lo, hi = value_range(c_vol)
    add(c_vol, f'Sum of the "Volume:" values of all numbered lesions in the report\'s {section} section. Above 0 in {pos_v:,} '
        f'rows, with a maximum of {fmt(hi)}.', 'decimal', 'imaging', 'descriptor', unit='cm³', missing=[ZERO.format(s=section)],
        concept='lesion volume')
    lo, hi = value_range(c_d)
    add(c_d, f'Longest diameter of lesion 1, the first lesion the report lists. The column name calls this lesion the largest. '
        f'The value is the first number of its first "A x B cm" measurement. Maximum {fmt(hi)}.', 'decimal', 'imaging', 'descriptor',
        unit='cm', missing=[ZERO.format(s=section)], level='lesion', concept='lesion diameter')
    if organ in LOC:
        c_loc, what = LOC[organ]
        nan_text = sum(1 for v in filled(c_loc) if v == 'nan')
        add(c_loc, f'Where lesion 1 lies, taken from its "Location:" line in the report. It is given as {what}.',
            'categorical', 'imaging', 'descriptor', coding=[c for c in codes(c_loc) if c['code'] != 'nan'],
            missing=blank_note(c_loc, NO_LESION) + ([f'"nan" (text): lesion 1 has no readable location ({nan_text:,} of {N:,} rows)'] if nan_text else []),
            level='lesion', concept='lesion location')
    add(c_att, 'Attenuation of lesion 1 relative to its organ: the first of "hyperattenuating", "hypoattenuating" or '
        '"isoattenuating" found in its report text.', 'categorical', 'imaging', 'descriptor', coding=codes(c_att),
        missing=blank_note(c_att, NO_LESION), level='lesion', concept='lesion attenuation')

# --- report texts
REPORTS = {
    'structured report': 'Report built by RadGPT\'s rules from the masks, filling a radiologist-designed template (paper, section 3.1). The first line names the contrast phase when known.',
    'narrative report': 'The structured report rewritten by Llama 3.1 70B (AWQ) in the style of a US hospital\'s reports, told not to change findings (paper, section 3.2).',
    'radiologist note': 'The human note merged into this scan\'s enhanced reports. The paper describes clinical notes for TotalSegmentator scans and notes from the authors\' radiologists (section 3.3).',
    'fusion structured report': 'Enhanced report: the structured report with the human note merged in by the language model (paper, section 3.3).',
    'fusion narrative report': 'Enhanced report: the narrative report with the human note merged in by the language model (paper, section 3.3).',
}
for col, definition in REPORTS.items():
    add(col, definition, 'text', 'imaging', 'annotation', missing=blank_note(col, 'no text'),
        evidence={**SCRIPT, 'sources': ['abdomenatlas3-metadata-csv', 'radgpt-paper']}, concept='radiology report')

assert sorted(v['originalName'] for v in V) == sorted(COLUMNS), set(COLUMNS) ^ {v['originalName'] for v in V}

# --- files outside the table
MASK_EVIDENCE = {'sources': ['abdomenatlas3-mask-files', 'abdomenatlas3-image-files', 'radgpt-paper', 'radgpt-staging-script'],
                 'locator': 'mask_only tarballs (file names); paper Figure 2 caption, sections 3.1.1 and 3.1.3, footnote 1 and Appendix C (how each group was made); staging.py type2name (vessel names)',
                 'status': 'verified', 'verifiedOn': ON,
                 'note': ('The Kidney-VLM project checked the file names and stored values for every case on 2026-09-23, and '
                          're-checked them on the first 232 cases on 2026-09-30. Each case has 43 files, or 44 where '
                          'colon_lesion is present. The log of the first check was not kept.')}
BINARY = ('Each file is one binary mask, and masks of different files can overlap. In the 232 cases checked, every mask '
          'has the same array shape as its CT. But in 56 of them, some mask headers differ from the CT header (see the '
          'quality findings).')
STORE = ('Masks are stored as 0/1, 0/255, or signed bytes -128/127 with a NIfTI scale that maps them to 0/1. Read them with a '
         'loader that applies the scale, then threshold at 0.5.')
MASKS = [
    ('lesion masks', 'lesion', [
        ('kidney_lesion', 'Kidney lesions; the file does not say whether a lesion is a tumour or a cyst'), ('liver_lesion', 'Liver lesions'),
        ('pancreatic_lesion', 'Pancreatic lesions'), ('colon_lesion', 'Colon lesions; present only in the cases that have one')],
     'Drawn by AI (DiffTumor and nnU-Net), then checked and corrected by radiologists one by one, using source-dataset ground truth where it existed. The paper does not say how colon lesions were annotated.'),
    ('organ masks', 'organ', [(n, n.replace('_', ' ')) for n in (
        'liver', 'kidney_left', 'kidney_right', 'pancreas', 'spleen', 'stomach', 'gall_bladder', 'adrenal_gland_left',
        'adrenal_gland_right', 'bladder', 'colon', 'duodenum', 'esophagus', 'femur_left', 'femur_right', 'intestine',
        'lung_left', 'lung_right', 'prostate', 'rectum', 'common_bile_duct')],
     'From AbdomenAtlas 1.1, made by AI with radiologists in the loop (paper, Appendix C).'),
    ('sub-region masks', 'subregion', [(f'liver_segment_{i}', f'Liver segment {i}') for i in range(1, 9)] +
     [('pancreas_head', 'Pancreas head'), ('pancreas_body', 'Pancreas body'), ('pancreas_tail', 'Pancreas tail')],
     'Liver segments came from an nnU-Net fine-tuned on 131 LiTS scans. Pancreas parts were split by a fixed rule from a superior mesenteric artery segmentation, and radiologists judged them only qualitatively. The paper describes both in sections 3.1.1 and 4.2.'),
    ('vessel masks', 'vessel', [
        ('aorta', 'Aorta'), ('postcava', 'Inferior vena cava (IVC in the RadGPT code)'),
        ('superior_mesenteric_artery', 'Superior mesenteric artery'),
        ('celiac_aa', 'Celiac artery and common hepatic artery ("CA and CHA" in the RadGPT code)'),
        ('veins', 'Portal vein and superior mesenteric vein ("portal vein and SMV" in the RadGPT code)'),
        ('celiac_trunk', 'Celiac trunk'), ('portal_vein_and_splenic_vein', 'Portal vein and splenic vein'),
        ('hepatic_vessel', 'Hepatic vessels')],
     'The vessels used for pancreatic tumour staging came from an nnU-Net trained on private data and were revised by radiologists (paper, footnote 1). Where the other vessel files came from is not stated.'),
]
for group, key, files, how in MASKS:
    add(f'segmentations/<structure>.nii.gz ({group})', f'One mask file per structure in each case folder. {BINARY} {STORE}',
        'image', 'imaging', 'annotation', file='mask_only tarballs, BDMAP_xxxxxxxx/segmentations/',
        coding=[{'code': f'{n}.nii.gz', 'meaning': m} for n, m in files], level='examination', provenance=how,
        evidence=MASK_EVIDENCE, derivation='derived', concept='segmentation mask', key=f'mask-{key}')
add('ct.nii.gz', 'The CT volume of the case, one NIfTI file per BDMAP ID, stored as 16-bit integers in the 232 cases checked.',
    'image', 'imaging', 'predictor', file='image_only tarballs, BDMAP_xxxxxxxx/ct.nii.gz', derivation='raw', key='ct',
    evidence={'sources': ['abdomenatlas3-hf-files', 'abdomenatlas3-image-files', 'radgpt-generate-readme'], 'locator': 'image_only listing; the 232 ct.nii.gz headers in the first image tarball; generate_reports README, "Dataset Format"',
              'status': 'verified', 'verifiedOn': ON, 'note': 'Headers opened for the first 232 cases only.'}, concept='CT image')
add('TrainTestIDS split membership', 'Which part of each split a scan belongs to, from four ID lists. IID is a random 90/10 split '
    'and the one the paper used. OOD keeps hospitals apart and was not used in the paper. Each split covers all 9,262 scans with no overlap.',
    'categorical', 'administrative', 'other', file='TrainTestIDS/IID_train.csv, IID_test.csv, OOD_train.csv, OOD_test.csv',
    coding=[{'code': 'IID_train', 'meaning': '(8,336 scans)'}, {'code': 'IID_test', 'meaning': '(926 scans)'},
            {'code': 'OOD_train', 'meaning': '(4,696 scans)'}, {'code': 'OOD_test', 'meaning': '(4,566 scans)'}],
    derivation='raw', key='split',
    evidence={'sources': ['abdomenatlas3-split-files', 'radgpt-repo-readme'], 'locator': 'All four lists; README "Train/Test Splits"',
              'status': 'verified', 'verifiedOn': ON}, concept='data split')

write_json(OUT, V, tabs=True)
print(f'{len(V)} variables ({len(COLUMNS)} table columns) -> {OUT.relative_to(REPO)}')
