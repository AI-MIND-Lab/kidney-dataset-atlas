"""Build src/data/variables/amos-mm-2024.json from the two AMOS-MM JSON files.

Every observed value (fill counts, codes, ranges) is recounted from all records of report_generation_train_val.json
and vqa_train_val.json, and each file's sha256 is checked against the pinned value (the files on the public Google
Drive folder on 2026-09-30). Meanings come from the Codabench "Dataset" page (record structure, site names) and the
challenge design document (how the reports and questions were made); a field no source explains is described as such.

The two files (about 21 MB) are downloaded once into .research-cache/dictionary/amos-mm/; set AMOSMM_DIR to a folder
that holds local copies to skip the download.
"""
import collections
import hashlib
import json
import os
import re
import statistics

import _setup  # noqa: F401
from common import REPO, cache_dir, get, write_json

RELEASE = 'amos-mm-2024'
OUT = REPO / 'src' / 'data' / 'variables' / f'{RELEASE}.json'
ON = '2026-09-30'
DRIVE = 'https://drive.usercontent.google.com/download?id={}&confirm=t'
FILES = {
    'report_generation_train_val.json': ('14ZIhEM1IDvrj6JkIjjCju-YAjLaJ22As',
                                         '13f029d38d00dc05f99bad487c77a6a255d2cb56837122212bac537c2c18a837'),
    'vqa_train_val.json': ('1VPvuMvbXo2puVj-rcN-vZy4oksKJhA_W',
                           'ddc7c0824a26bb9c7f0f94850ed92696bf7b2ae35c11af79a2988587ff9e13ae'),
}


def load(name):
    drive_id, sha = FILES[name]
    local = os.environ.get('AMOSMM_DIR')
    if local:
        data = open(os.path.join(local, name), 'rb').read()
    else:
        p = cache_dir('dictionary', 'amos-mm') / name
        if not p.exists():
            body = get(DRIVE.format(drive_id), binary=True)
            if body is None:
                raise SystemExit(f'Could not download {name} from Google Drive')
            p.write_bytes(body)
        data = p.read_bytes()
    if hashlib.sha256(data).hexdigest() != sha:
        raise SystemExit(f'{name} does not match the pinned file (sha256)')
    return json.loads(data)


REP = load('report_generation_train_val.json')
VQA = load('vqa_train_val.json')
SPLITS = ('training', 'validation')
CASES = [x for s in SPLITS for x in REP[s]]
N = len(CASES)
QS = [q for s in SPLITS for x in VQA[s] for q in x['labels'].get('qa', [])]
NQ = len(QS)
PER_CASE = [len(x['labels'].get('qa', [])) for s in SPLITS for x in VQA[s]]
WITH_Q = sum(1 for p in PER_CASE if p)
assert {x['image']: x['meta'] for s in SPLITS for x in VQA[s]} == {x['image']: x['meta'] for x in CASES}

RF, VF = 'report_generation_train_val.json', 'vqa_train_val.json'
SAMPLE = {'sources': ['amos-mm-report-json', 'amos-mm-vqa-json', 'amos-mm-image-files'],
          'locator': f'Both JSON files, all {N:,} case records; NIfTI headers of the 16 sample files', 'status': 'verified', 'verifiedOn': ON}
BOTH = f'{RF}, {VF}'
ALL = {'sources': ['amos-mm-report-json', 'amos-mm-vqa-json'], 'locator': f'Both JSON files, all {N:,} case records',
       'status': 'verified', 'verifiedOn': ON}
CODA = {'sources': ['amos-mm-report-json', 'amos-mm-vqa-json', 'amos-mm-codabench'],
        'locator': f'Both JSON files, all {N:,} case records; Codabench "Dataset" page', 'status': 'verified', 'verifiedOn': ON}
REPORT = {'sources': ['amos-mm-report-json', 'amos-mm-codabench', 'amos-mm-design-doc'],
          'locator': f'{RF}, all {N:,} case records; Codabench "Dataset" page ("MRG Annotations"); design document p. 13',
          'status': 'verified', 'verifiedOn': ON}
QUEST = {'sources': ['amos-mm-vqa-json', 'amos-mm-codabench', 'amos-mm-design-doc'],
         'locator': f'{VF}, all {NQ:,} questions; Codabench "Dataset" page ("VQA Annotations"); design document p. 26',
         'status': 'verified', 'verifiedOn': ON}
V = []


def add(name, definition, vtype, group, role, file, *, unit=None, coding=None, missing=None, level='examination',
        provenance=None, evidence=ALL, derivation='raw', key=None):
    V.append({
        'id': f'{RELEASE}-' + (key or re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')),
        'release': RELEASE, 'originalName': name, 'file': file, 'definition': definition, 'type': vtype, 'unit': unit,
        'coding': coding or [], 'missingValues': missing or [], 'observationLevel': level, 'timePoint': None,
        'role': role, 'group': group, 'derivation': derivation, 'normalizedConcept': None,
        **({'provenance': provenance} if provenance else {}), 'evidence': evidence,
    })


def counts(values, meanings=None, total=None):
    c = collections.Counter(values)
    total = total or len(values)
    return [{'code': v, 'meaning': ((meanings or {}).get(v, '') + ' ').lstrip() + f'({n:,} of {total:,})'} for v, n in c.most_common()]


# ---- header
h = REP
add('header', ('File-level fields at the top of both JSON files: name ("AMOS-MM"), description, author, reference ("HKU"), '
               f'licence ("{h["licence"]}"), release ("{h["release"]}"), contact (an e-mail address), tensorImageSize '
               f'("{h["tensorImageSize"]}"), modality ({{"0": "CT"}}) and the number of cases per split (numTraining '
               f'{h["numTraining"]:,}, numValidation {h["numValidation"]:,}, numTest {h["numTest"]:,}). The "testing" list is '
               'empty, so the test cases announced here are not in the release. The values are the same in both files.'),
    'other', 'administrative', 'descriptor', BOTH, level='record',
    evidence={**ALL, 'locator': 'Header fields of both JSON files'})

# ---- case fields
names = [x['image'] for x in CASES]
assert len(set(names)) == N
add('image', (f'Relative path of the case\'s CT in the image archives (./imagesTr/amos_xxxx.nii.gz for the '
              f'{len(REP["training"]):,} training cases, ./imagesVa/... for the {len(REP["validation"]):,} validation cases). '
              'It is the case key; the file name, without folder, matches the name inside the zip. Three validation files '
              '(amos_7008, amos_7312, amos_7333) are also in imagesTr.zip.'),
    'text', 'administrative', 'identifier', BOTH,
    evidence={**ALL, 'sources': ALL['sources'] + ['amos-mm-zip-listings'], 'locator': ALL['locator'] + '; member names of both zips'})
SITES = {'A': 'Longgang District Central Hospital, Shenzhen', 'B': "Longgang District People's Hospital, Shenzhen"}
add('meta.site', 'Hospital the scan comes from, as a one-letter code. The site names are from the Codabench "Dataset" page.',
    'categorical', 'administrative', 'descriptor', BOTH, coding=counts([x['meta']['site'] for x in CASES], SITES), evidence=CODA)
sc = [x['meta']['scanner'] for x in CASES]
add('meta.scanner', ('CT scanner model. Seven values; two of them, Prisma and SIGNA HDe, are MRI scanner models although '
                     'these 4 cases are listed as CT and the 2 checked hold CT values (see the quality findings).'),
    'categorical', 'imaging', 'descriptor', BOTH, coding=counts(sc))
inplane = collections.Counter('x'.join(map(str, x['meta']['shape'][:2])) for x in CASES)
sl = [x['meta']['shape'][2] for x in CASES]
add('meta.shape', ('Size of the CT voxel grid, three integers in the file\'s axis order. In-plane: '
                   + ', '.join(f'{k.replace("x", " × ")} in {v:,}' for k, v in inplane.most_common())
                   + f'. Third value {min(sl)} to {max(sl)} (median {statistics.median(sl):g}); it is the number of axial slices '
                   'except in amos_5553 and amos_5693, which are stored as sagittal and coronal slices. In the 16 files checked, '
                   'it equals the NIfTI header.'),
    'other', 'imaging', 'descriptor', BOTH, evidence=SAMPLE)
ip = [x['meta']['spacing'][0] for x in CASES]
z = collections.Counter(round(x['meta']['spacing'][2], 3) for x in CASES)
main = [5.0, 2.0, 1.25, 2.5]
assert all(x['meta']['spacing'][0] == x['meta']['spacing'][1] for x in CASES)
add('meta.spacing', ('Voxel size, three numbers in the file\'s axis order; the first two are equal in every case. In-plane '
                     f'{min(ip):.3f} to {max(ip):.3f} (median {statistics.median(ip):.3f}); third value '
                     + ', '.join(f'{k:g} in {z[k]:,}' for k in main)
                     + f', other values in {N - sum(z[k] for k in main)}. The JSON states no unit; the 16 NIfTI headers checked '
                     'give millimetres and the same values.'),
    'decimal', 'imaging', 'descriptor', BOTH, evidence=SAMPLE)

# ---- report fields
for part in ('findings', 'impression'):
    for region in ('chest', 'abdomen', 'pelvis'):
        vals = [x['labels']['report'][part].get(region) for x in CASES]
        absent = sum(1 for v in vals if v is None)
        empty = sum(1 for v in vals if v is not None and not (v.strip() if isinstance(v, str) else v))
        full = N - absent - empty
        if part == 'findings':
            d = (f'Findings for the {region}: one English text describing what the radiologist saw. Filled in {full:,} of '
                 f'{N:,} cases; empty when the region was not reported.')
            vt = 'text'
        else:
            d = (f'Impression for the {region}: a list of English sentences with the radiologist\'s conclusions. Non-empty in '
                 f'{full:,} of {N:,} cases.')
            vt = 'other'
        miss = ([f'{"[]" if part == "impression" else chr(34) * 2}: region not reported ({empty:,} of {N:,})'] if empty else []) + \
               ([f'key absent ({absent:,} of {N:,})'] if absent else [])
        add(f'labels.report.{part}.{region}', d, vt, 'clinical', 'annotation', RF, missing=miss, evidence=REPORT,
            provenance=('The hospitals\' Chinese reports, translated into English by three junior radiologists and corrected '
                        'by two senior radiologists (design document p. 13). In vqa_train_val.json, "labels.report" is an empty object in '
                        'every case, so this field is absent there.'),
            key=f'{part}-{region}')

# ---- question fields
types = collections.Counter(q['type'] for q in QS)
med = statistics.median([p for p in PER_CASE if p])
add('labels.qa', (f'List of multiple-choice questions about the case: {NQ:,} questions on {WITH_Q:,} of {N:,} cases, '
                  f'{min(p for p in PER_CASE if p)} to {max(PER_CASE)} per case (median {med:g}); {N - WITH_Q} cases have none. '
                  'Each question has the five fields below.'),
    'other', 'clinical', 'annotation', VF, level='record', evidence=QUEST, derivation='derived',
    provenance='Generated by GPT-4 from the reports and reviewed by a senior radiologist and a clinical physician (design document p. 26).')
add('question', f'Question text in English. {len({q["question"] for q in QS}):,} distinct texts among {NQ:,} questions.',
    'text', 'clinical', 'annotation', VF, level='record', evidence=QUEST, derivation='derived', key='qa-question')
assert all(sorted(q['options']) == ['A', 'B', 'C', 'D'] for q in QS)
add('options', 'The four answer choices, keyed A to D (four in every question).',
    'other', 'clinical', 'annotation', VF, level='record', evidence=QUEST, derivation='derived', key='qa-options')
add('answer', 'Letter of the correct option.', 'categorical', 'outcome', 'outcome', VF, level='record',
    coding=counts([q['answer'] for q in QS]), evidence=QUEST, derivation='derived', key='qa-answer')
rl = [len(q['reasoning']) for q in QS]
add('reasoning', (f'Short English justification of the answer, written with the question (median {statistics.median(rl):g} '
                  'characters; none empty). The design document calls it the rationale.'),
    'text', 'clinical', 'annotation', VF, level='record', evidence=QUEST, derivation='derived', key='qa-reasoning')
add('type', ('Question category; 6 values, matching the 6 skills on the Codabench page. One is spelled '
             '"anaotomical_identification" in the file. The design document describes 8 skills.'),
    'categorical', 'clinical', 'descriptor', VF, level='record', coding=counts(list(q['type'] for q in QS)),
    evidence=QUEST, derivation='derived', key='qa-type')

write_json(OUT, V, tabs=True)
print(len(V), 'variables ->', OUT.relative_to(REPO))
