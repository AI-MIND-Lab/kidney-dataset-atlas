"""Build src/data/variables/deeptumorvqa-2-0.json from the DeepTumorVQA 2.0 text files.

Every observed value (fill counts, codes, ranges) is recounted from all rows of the question files, the metadata
table, the subtype schema and the leaderboard at Hugging Face revision a8b9db5, and each file's sha256 is checked
against the pinned value. Meanings come from the dataset card (the QA record schema) and the paper (sections 3.1-3.3,
Appendix b); a field no source explains is described as such.

The files (about 290 MB) are downloaded once into .research-cache/dictionary/deeptumorvqa/; set DEEPTUMORVQA_DIR to a
local copy of the release's text files to skip the download. ABDOMENATLAS_CSV must point to AbdomenAtlas3.0MiniWithMeta.csv
(see build_abdomenatlas3.py), which is used to compare the report columns with AbdomenAtlas's.
"""
import collections
import csv
import hashlib
import json
import os
import re
import statistics
import sys

import _setup  # noqa: F401
from common import REPO, cache_dir, get, write_json

csv.field_size_limit(sys.maxsize)
RELEASE = 'deeptumorvqa-2-0'
REV = 'a8b9db5133fda02567476dcb49498ec51f6aed37'
BASE = f'https://huggingface.co/datasets/tumor-vqa/DeepTumorVQA_2.0/resolve/{REV}'
OUT = REPO / 'src' / 'data' / 'variables' / f'{RELEASE}.json'
ON = '2026-09-30'
SHA256 = {
    'train/train_qa.csv': '0fc2d339901c412f0d61e802ef7f9177c61263717ada0962813ca6253eb8c38f',
    'train/val_qa_pool.csv': 'bf1c23a07a4a64a7b2fe7dfaa3b123928dfde49e61526fbf09f6d5b40a140bbf',
    'benchmark/test_qa.json': '3fd22c8ec4cc7d4a9bbf8de32572b0947a25fe1bec6f6a1e4af5fc03d1060db2',
    'benchmark/test_qa.jsonl': '2f7ba54960089fc41d95c89fddb41f888687316e914c15a22038d256f35723dd',
    'metadata/reports_and_metadata.csv': '55cb96cd04fcf3ed4b516c64048beb6c177516f0c4aa13c47ceed155ecf8149e',
    'metadata/subtype_schema.csv': 'a231e9814bc4dee4025cbfe0df62343f094599e21674fb745c4c660bd9cadc1d',
    'metadata/leaderboard.csv': 'ab14a4f9ee4764193d7397255bf2468fa860b22239a31a8aa17fab0b532f3e44',
    'agent_sft/train.jsonl': '6d4c086cd459a57f06d29e3042d05b0bd43dd94f2c72015cfea59eabd541b64e',
    'agent_sft/holdout.jsonl': '44265b2e650ff7304695e48098333804af45fb0349c6c89d19155d3a3bc49c31',
    'tool_cache/benchmark_oracle_tool_cache.json': '91005b461b75e355c5afe0e4c8352fd8e66dcd3c16986472b74be5be891a2721',
    'tool_cache/benchmark_totalsegmentator_cache.json': '1ba359068a6da68f46f7e38abfe7e0cc30b8a15afd16bbe7ecc61be61988b149',
    'tool_cache/training_oracle_tool_cache.json': 'a8f809c4bb3bf857c890df94431fc007343a6ad26685275f04ded25bd6f8a517',
}


def path(name):
    local = os.environ.get('DEEPTUMORVQA_DIR')
    if local:
        p = os.path.join(local, name)
    else:
        p = cache_dir('dictionary', 'deeptumorvqa') / name.replace('/', '__')
        if not p.exists():
            body = get(f'{BASE}/{name}', binary=True)
            if body is None:
                raise SystemExit(f'Could not download {name} at revision {REV[:7]}')
            p.write_bytes(body)
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    if h != SHA256[name]:
        raise SystemExit(f'{name} does not match revision {REV[:7]}')
    return p


def rows(name):
    with open(path(name), newline='') as f:
        return list(csv.DictReader(f))


train, val = rows('train/train_qa.csv'), rows('train/val_qa_pool.csv')
bench = json.load(open(path('benchmark/test_qa.json')))['questions']
benchl = [json.loads(line) for line in open(path('benchmark/test_qa.jsonl'))]
meta = rows('metadata/reports_and_metadata.csv')
AA_CSV = os.environ.get('ABDOMENATLAS_CSV')
if not AA_CSV:
    raise SystemExit('Set ABDOMENATLAS_CSV to AbdomenAtlas3.0MiniWithMeta.csv (see build_abdomenatlas3.py) to compare the report columns')
with open(AA_CSV, newline='') as f:
    AA = {r['BDMAP ID']: r for r in csv.DictReader(f)}
schema = rows('metadata/subtype_schema.csv')
board = rows('metadata/leaderboard.csv')
QA = train + val
NQ, NM = len(QA), len(meta)
PHASES = ('CT Venous Phase', 'CT Arterial Phase', 'Non-contrast CT', 'CT Delay Phase')
PHASE_IN_REPORT = sum(1 for r in meta if r['structured report'].split('\n')[0].strip() in PHASES)

CARD = {'sources': ['deeptumorvqa-hf-card', 'deeptumorvqa-question-files'],
        'locator': f'Card, "QA record schema (benchmark/test_qa.json)"; train_qa.csv and val_qa_pool.csv, all {NQ:,} rows',
        'status': 'verified', 'verifiedOn': ON}
PAPER_Q = {'sources': ['deeptumorvqa-paper', 'deeptumorvqa-question-files'],
           'locator': f'Paper section 3.1 (question types, templates, distractors); train_qa.csv and val_qa_pool.csv, all {NQ:,} rows',
           'status': 'verified', 'verifiedOn': ON}
FILEONLY = {'sources': ['deeptumorvqa-question-files'], 'locator': f'train_qa.csv and val_qa_pool.csv, all {NQ:,} rows',
            'status': 'verified', 'verifiedOn': ON}
BENCH = {'sources': ['deeptumorvqa-question-files', 'deeptumorvqa-hf-files'],
         'locator': 'test_qa.jsonl, all 10,000 records; paths looked up in the file list', 'status': 'verified', 'verifiedOn': ON}
META = {'sources': ['deeptumorvqa-metadata-files', 'deeptumorvqa-paper'],
        'locator': f'reports_and_metadata.csv, all {NM:,} rows; paper Appendix b', 'status': 'verified', 'verifiedOn': ON}
SCHEMA = {'sources': ['deeptumorvqa-metadata-files', 'deeptumorvqa-question-files'],
          'locator': 'subtype_schema.csv, all 42 rows, compared with the per-subtype question counts', 'status': 'verified', 'verifiedOn': ON}
BOARD = {'sources': ['deeptumorvqa-metadata-files', 'deeptumorvqa-paper'],
         'locator': 'leaderboard.csv, all 38 rows, compared with paper Tables 3 and 4', 'status': 'verified', 'verifiedOn': ON}
AGENT = {'sources': ['deeptumorvqa-agent-files', 'deeptumorvqa-paper'],
         'locator': 'All 40,000 trajectories and the three tool caches; paper sections 3.3 and Appendix e.4', 'status': 'verified', 'verifiedOn': ON}

V = []


def add(name, definition, vtype, group, role, file, *, unit=None, coding=None, missing=None, level='record',
        provenance=None, evidence=FILEONLY, derivation='derived', concept=None, key=None):
    V.append({
        'id': f'{RELEASE}-' + (key or re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')),
        'release': RELEASE, 'originalName': name, 'file': file, 'definition': definition, 'type': vtype, 'unit': unit,
        'coding': coding or [], 'missingValues': missing or [], 'observationLevel': level, 'timePoint': None,
        'role': role, 'group': group, 'derivation': derivation, 'normalizedConcept': concept,
        **({'provenance': provenance} if provenance else {}), 'evidence': evidence,
    })


def filled(rs, col):
    return [r[col] for r in rs if str(r[col]).strip() not in ('', 'nan', 'None')]


def codes(rs, col, top=None, meanings=None):
    c = collections.Counter(filled(rs, col))
    items = c.most_common(top)
    out = [{'code': v, 'meaning': ((meanings or {}).get(v, '') + ' ' if (meanings or {}).get(v) else '') + f'({n:,} of {len(rs):,} rows)'}
           for v, n in items]
    return out


def blank(rs, col, meaning):
    b = len(rs) - len(filled(rs, col))
    return [f'blank: {meaning} ({b:,} of {len(rs):,} rows)'] if b else []


QFILE = 'train/train_qa.csv, train/val_qa_pool.csv'
JSONNAME = {'Question ID': 'qid', 'Image ID': 'image_id', 'multiple-choice question': 'mc_question',
            'correct option': 'correct_option', 'question type': 'question_type', 'question subtype': 'question_subtype'}


def jn(col):
    return f' Called "{JSONNAME[col]}" in the benchmark files.' if col in JSONNAME else ''


# --- question files
qids = sorted(int(r['Question ID']) for r in QA)
add('Question ID', f'Question identifier: an integer, unique across the training file and validation pool ({qids[0]} to '
    f'{qids[-1]:,}, no gaps). Benchmark questions use "bench_00000" to "bench_09999" instead.' + jn('Question ID'),
    'integer', 'administrative', 'identifier', QFILE, evidence=CARD, derivation='raw', concept='question identifier')
per = collections.Counter(r['Image ID'] for r in train)
add('Image ID', f'BDMAP ID of the CT scan the question is about. AbdomenAtlas 3.0 uses the same IDs. The training file covers '
    f'{len(per):,} scans ({min(per.values())} to {max(per.values())} questions each, median {statistics.median(per.values()):g}).' + jn('Image ID'),
    'text', 'administrative', 'identifier', QFILE, evidence=CARD, derivation='raw', concept='scan identifier')
for col, what in [('spacing', 'Voxel size of the scan, three numbers written like a NumPy array, repeated from the metadata table'),
                  ('shape', 'Voxel grid of the scan, repeated from the metadata table. It matches the AbdomenAtlas 3.0 shape column, not the released AbdomenAtlas3.0Mini files (see the quality findings)')]:
    add(col, what + '.', 'other', 'imaging', 'descriptor', QFILE, evidence=CARD, derivation='raw')
add('sex', 'Patient sex, repeated in each question about the scan.', 'categorical', 'clinical', 'predictor', QFILE,
    coding=codes(QA, 'sex', meanings={'M': 'Male', 'F': 'Female'}), missing=blank(QA, 'sex', 'not available'), level='patient',
    evidence=CARD, derivation='raw', concept='sex')
ages = [float(v) for v in filled(QA, 'age')]
add('age', f'Patient age, repeated in each question about the scan. No unit is stated. Observed range {min(ages):g} to {max(ages):g}.',
    'decimal', 'clinical', 'predictor', QFILE, missing=blank(QA, 'age', 'not available'), level='patient', evidence=CARD,
    derivation='raw', concept='age')
add('scanner', 'CT scanner manufacturer, repeated in each question about the scan.', 'categorical', 'imaging', 'descriptor',
    QFILE, coding=codes(QA, 'scanner'), missing=blank(QA, 'scanner', 'not available'), evidence=FILEONLY, derivation='raw',
    concept='scanner manufacturer')
add('contrast', f'Contrast phase. Empty in every row. The phase is given only in the report text. In the metadata table, the '
    f'first line of the structured report names it for {PHASE_IN_REPORT:,} scans. The paper says it was read from DICOM headers.',
    'categorical', 'imaging', 'descriptor', QFILE, missing=[f'blank in all {NQ:,} rows (NaN in the benchmark files)'],
    evidence={**PAPER_Q, 'locator': PAPER_Q['locator'] + '; paper Appendix b'}, derivation='raw', concept='contrast phase')
add('question', f'The question text, without options. There are {len(set(r["question"] for r in QA)):,} distinct texts. '
    'Each subtype has 10 templates filled from the metadata (paper).', 'text', 'other', 'other', QFILE, evidence=PAPER_Q)
add('answer', f'The correct answer as text: a number or a label, computed by the subtype\'s program from the metadata table '
    f'(paper). There are {len(set(r["answer"] for r in QA)):,} distinct values.', 'text', 'outcome', 'outcome', QFILE,
    evidence=PAPER_Q)
nopt = collections.Counter(len(re.findall(r'(?:^|\s)[A-D]:\s', r['multiple-choice question'])) for r in train)
opts = [f'{k} in {v:,}' for k, v in sorted(nopt.items(), reverse=True)]
opts[0] += ' questions'
add('multiple-choice question', 'The question followed by its options, written as "A: ... B: ...". The paper says wrong options '
    'for volume and HU questions are drawn between 0.7 and 1.3 times the true value. In the files, this holds for organ volume '
    'and organ aggregation questions, and for all but 58 of the 106,476 wrong options of organ HU questions. It does not hold '
    'for lesion volume, diameter, count, HU ratio or HU difference questions. Options per question in the training file: '
    + ', '.join(opts[:-1]) + ' and ' + opts[-1] + '.' + jn('multiple-choice question'),
    'text', 'other', 'other', QFILE, evidence=PAPER_Q)
multi = sum(1 for r in QA if ',' in r['correct option'])
add('correct option', f'Letter of the correct option. In {multi:,} rows, the field gives several letters separated by commas.'
    + jn('correct option'), 'categorical', 'outcome', 'outcome', QFILE, coding=codes(QA, 'correct option', top=6), evidence=CARD)
add('organ', 'Organ, or pair of organs joined by a comma, that the question is about. The pancreas is written both as "pancreas" '
    'and as "pancreatic".', 'categorical', 'imaging', 'descriptor', QFILE, coding=codes(QA, 'organ', top=12), evidence=CARD)
add('lesion', 'Kind of lesion the question is about. The value is the text "False" when the question asks about no lesion.',
    'categorical', 'imaging', 'descriptor', QFILE, coding=codes(QA, 'lesion'), evidence=CARD)
add('question type', 'The stage the question tests (paper, section 3.1).' + jn('question type'), 'categorical', 'other', 'other',
    QFILE, coding=codes(QA, 'question type'), evidence=PAPER_Q)
add('question subtype', f'One of {len(set(r["question subtype"] for r in QA))} clinical subtypes. The 12 most frequent are listed with '
    'counts, and all 42 are in subtype_schema.csv.' + jn('question subtype'), 'categorical', 'other', 'other', QFILE,
    coding=codes(QA, 'question subtype', top=12), evidence=PAPER_Q)
add('split', 'Name of the file\'s split: "train" in train_qa.csv, "val" in val_qa_pool.csv. The benchmark files have no split field.',
    'categorical', 'administrative', 'other', QFILE, coding=codes(QA, 'split'), evidence=FILEONLY, derivation='raw', concept='data split')

# --- fields only in the benchmark JSONL
tools = collections.Counter(', '.join(q['requires_tools']) for q in benchl)
add('requires_tools', 'Tools an agent needs to answer the question.', 'other', 'other', 'other', 'benchmark/test_qa.jsonl, test_qa.json',
    coding=[{'code': k, 'meaning': f'({v:,} of 10,000 records)'} for k, v in tools.most_common()], evidence={**CARD, 'locator': 'Card, "QA record schema"; test_qa.jsonl, all 10,000 records'},
    key='requires-tools')
PATHS = {'slice_path': ('organ PNG', 'benchmark/images_2d/organ/'), 'whole_slice_path': ('whole-scan PNG', 'benchmark/images_2d/whole/'),
         'video_path': ('organ-level video', None), 'whole_video_path': ('whole-scan video', 'benchmark/videos/whole/')}
for col, (what, where) in PATHS.items():
    found = (f'The folder written here is not in the release, but the files exist under {where} with the same file name'
             if where else 'These videos are not in the release. The folder benchmark/videos/ exists, but it holds only the '
             'whole-scan videos, in its whole/ subfolder')
    add(col, f'Path of the {what} for the question. {found} (see the quality findings).',
        'text', 'imaging', 'other', 'benchmark/test_qa.jsonl, test_qa.json', evidence=BENCH, key=col.replace('_', '-'))

# --- metadata table
ORG = {'liver': 'liver', 'pancreatic': 'pancreas', 'kidney': 'kidneys', 'colon': 'colon', 'esophagus': 'oesophagus', 'uterus': 'uterus'}
LESION = {'lesion': ('lesion', 'lesions'), 'tumor': ('tumour', 'tumours'), 'cyst': ('cyst', 'cysts'),
          'PDAC': ('PDAC', 'PDAC lesions'), 'PNET': ('PNET', 'PNET lesions')}
TYPED = {'tumor', 'cyst', 'PDAC', 'PNET'}
MFILE = 'metadata/reports_and_metadata.csv'


def num(v):
    return float(v) if str(v).strip() else 0.0


def not_given(col, count_col):
    b = [r for r in meta if not str(r[col]).strip()]
    if not b:
        return []
    with_lesion = sum(1 for r in b if count_col in r and num(r[count_col]) > 0)
    return [f'blank: not given ({len(b):,} of {NM:,} rows' + (f', including {with_lesion:,} with such a lesion)' if with_lesion else ')')]


def zero_all(col):
    return all(num(r[col]) == 0 for r in meta)


AXIS_FIRST = sum(1 for r in meta if (lambda s: abs(s[1] - s[2]) < 1e-6 and s[0] - s[1] > 1e-6)(
    [float(x) for x in r['spacing'].strip('[]').split()]))
for col in meta[0].keys():
    m = re.match(r'(total|number of|largest) (\w+) (lesion|tumor|cyst|PDAC|PNET) (volume|instances|diameter|location|attenuation)', col)
    if col == 'BDMAP ID':
        add(col, f'Scan identifier. The table has {NM:,} rows, one per scan. Five scans that have questions (BDMAP_00001253, '
            '00002505, 00003582, 00003757, 00004545) have no row.', 'text', 'administrative', 'identifier', MFILE,
            level='examination', evidence=META, derivation='raw', key='meta-bdmap-id')
    elif col in ('spacing', 'shape', 'sex', 'age', 'scanner'):
        add(col, f'Same values as the AbdomenAtlas 3.0 metadata column of the same name in all {NM:,} rows.', 'other' if col in ('spacing', 'shape') else ('decimal' if col == 'age' else 'categorical'),
            'imaging' if col in ('spacing', 'shape', 'scanner') else 'clinical', 'descriptor', MFILE, level='examination',
            missing=blank(meta, col, 'not available'), evidence={**META, 'sources': META['sources'] + ['abdomenatlas3-metadata-csv']},
            derivation='raw', key=f'meta-{col}')
    elif col == 'contrast':
        add(col, f'Contrast phase. Empty in every row. The first line of the structured report names the phase for {PHASE_IN_REPORT:,} scans.', 'categorical', 'imaging', 'descriptor', MFILE, level='examination',
            missing=[f'blank in all {NM:,} rows'], evidence=META, derivation='raw', key='meta-contrast')
    elif col.endswith('volume (cm^3)') and not m:
        vals = [num(v) for v in filled(meta, col)]
        add(col, f'Organ volume. Observed range {min(vals):g} to {max(vals):g}, with a value of 0 in '
            f'{sum(1 for v in vals if v == 0):,} rows.',
            'decimal', 'imaging', 'descriptor', MFILE, unit='cm³', level='examination', missing=blank(meta, col, 'no value'),
            evidence=META, key='meta-' + re.sub(r'[^a-z0-9]+', '-', col.lower()).strip('-'))
    elif m:
        kind, organ, lesion, what = m.groups()
        word, words = LESION[lesion]
        typed = lesion in TYPED
        zero = zero_all(col) if what in ('volume', 'instances', 'diameter') else not filled(meta, col)
        base = {'volume': f'Sum of the volumes of all {words} in the {ORG.get(organ, organ)}',
                'instances': f'Number of {words} in the {ORG.get(organ, organ)} (connected components of the mask, per the paper)',
                'diameter': f'Largest axial diameter of the largest {word} in the {ORG.get(organ, organ)}',
                'location': f'Where the largest {word} in the {ORG.get(organ, organ)} lies',
                'attenuation': f'Attenuation of the largest {word} relative to its organ'}[what]
        if zero:
            note = ' Empty or 0 in every row.'
        elif what in ('volume', 'instances', 'diameter'):
            pos = sum(1 for r in meta if num(r[col]) > 0)
            note = f' Above 0 in {pos:,} rows, with a maximum of {max(num(r[col]) for r in meta):g}.'
        else:
            note = f' Filled in {len(filled(meta, col)):,} rows.'
        if typed and what == 'diameter' and not zero:
            note += (f' Values are far too large on the {AXIS_FIRST} scans whose spacing lists the thick slice axis first '
                     '(see the quality findings).')
        typed_note = ' The lesion type is a radiologist\'s label (paper, Appendix b).' if typed else ''
        add(col, base + '.' + note + typed_note, {'volume': 'decimal', 'instances': 'integer', 'diameter': 'decimal',
                                                   'location': 'categorical', 'attenuation': 'categorical'}[what],
            'imaging', 'descriptor', MFILE, unit={'volume': 'cm³', 'diameter': 'cm'}.get(what),
            coding=codes(meta, col, top=8) if what in ('location', 'attenuation') and not zero else [],
            missing=(['0: none'] if what in ('volume', 'instances', 'diameter') else not_given(col, f'number of {organ} {lesion} instances')),
            level='lesion' if what in ('diameter', 'location', 'attenuation') else 'examination', evidence=META,
            key='meta-' + re.sub(r'[^a-z0-9]+', '-', col.lower()).strip('-'))
    elif col == 'pancreatic tumor staging (T1-T4)':
        add(col, 'T stage of the pancreatic tumour, derived by a program from its diameter and contact with nearby vessels (paper, '
            'Appendix b).', 'categorical', 'imaging', 'descriptor', MFILE, coding=codes(meta, col), level='lesion',
            missing=[f'blank: not given ({sum(1 for r in meta if not r[col].strip()):,} of {NM:,} rows, including '
                     f'{sum(1 for r in meta if not r[col].strip() and num(r["number of pancreatic PDAC instances"]) + num(r["number of pancreatic PNET instances"]) > 0):,} '
                     'with a PDAC or PNET lesion)'], evidence=META, key='meta-pancreatic-staging')
    elif col in ('radiologist note', 'structured report', 'narrative report', 'fusion structured report', 'fusion narrative report'):
        add(col, f'Report text. The AbdomenAtlas 3.0 metadata table has a column of the same name, and the two differ in '
            f'{sum(1 for r in meta if r[col] != AA[r["BDMAP ID"]][col]):,} of {NM:,} rows.', 'text', 'imaging', 'annotation', MFILE, level='examination',
            missing=blank(meta, col, 'no text'), evidence={**META, 'sources': META['sources'] + ['abdomenatlas3-metadata-csv']},
            key='meta-' + re.sub(r'[^a-z0-9]+', '-', col.lower()).strip('-'))
    else:
        raise SystemExit(f'unhandled metadata column: {col}')

# --- subtype schema
bc = collections.Counter(q['question_subtype'] for q in bench)
vc = collections.Counter(r['question subtype'] for r in val)
assert all(int(r['n_benchmark']) == bc[r['subtype_name']] and int(r['n_full_dataset']) == vc[r['subtype_name']] for r in schema)
SFILE = 'metadata/subtype_schema.csv'
for col in schema[0].keys():
    if col == 'subtype_name':
        d = 'Name of the question subtype, as in the question files.'
    elif col == 'task_group':
        d = 'Question type the subtype belongs to.'
    elif col == 'gt_trace_steps':
        d = 'An integer from 1 to 5. The release does not document it beyond its name.'
    elif col == 'required_primitives':
        d = 'The subtype\'s ground-truth tool sequence, written with arrows.'
    elif col == 'n_benchmark':
        d = 'Number of benchmark questions of the subtype. It equals the benchmark count for all 42 subtypes (10,000 in total).'
    elif col == 'n_full_dataset':
        d = ('Number of validation-pool questions of the subtype, despite the name. It equals the validation-pool count for all 42 '
             'subtypes (47,933 in total), not the count in the full dataset.')
    else:
        d = 'True/False flag. The release does not document it beyond its name.'
    kind = 'integer' if col.startswith('n_') or col == 'gt_trace_steps' else ('boolean' if col.startswith('requires_') else 'categorical' if col == 'task_group' else 'text')
    add(col, d, kind, 'other', 'other', SFILE, coding=codes(schema, col) if kind in ('categorical', 'boolean') or col == 'gt_trace_steps' else [],
        evidence=SCHEMA, key='schema-' + col.replace('_', '-'))

# --- leaderboard
LFILE = 'metadata/leaderboard.csv'
LB = {'model': 'Name of the evaluated configuration (model plus input or agent mode), or one of two radiologists.',
      'params': 'Model size as written by the provider.', 'input': 'Input given to the model.',
      'mode': 'Evaluation mode: direct inference, or an agent with oracle, predicted or vision tools.',
      'overall': 'Overall accuracy on the 10,000-question benchmark (multiple choice).', 'recog': 'Accuracy on recognition questions.',
      'meas': 'Accuracy on measurement questions.', 'visr': 'Accuracy on visual reasoning questions.',
      'medr': 'Accuracy on medical reasoning questions.',
      'source': ('Where the provider says the row comes from. It cites "paper Table 1" and "Table 2". In arXiv v1, these results '
                 'are Tables 3 and 4.')}
for col in board[0].keys():
    score = col in ('overall', 'recog', 'meas', 'visr', 'medr')
    add(col, LB[col] + (' All 38 rows match paper Tables 3 and 4. The two radiologist rows are on a 200-question subset, and the '
                        'senior radiologist answered free-form.' if score else ''), 'decimal' if score else 'text', 'other',
        'outcome' if score else 'descriptor', LFILE, unit='%' if score else None,
        coding=codes(board, col) if col in ('input', 'mode', 'source') else [], evidence=BOARD, key='leaderboard-' + col)

# --- agent files
ids, roles = set(), collections.Counter()
for name in ('agent_sft/train.jsonl', 'agent_sft/holdout.jsonl'):
    for line in open(path(name)):
        conv = json.loads(line)['conversations']
        roles.update(c['from'] for c in conv)
        ids.update(re.findall(r'BDMAP_\d{8}', json.dumps(conv)))
empty_images = all(not json.loads(line)['images'] for n in ('agent_sft/train.jsonl', 'agent_sft/holdout.jsonl') for line in open(path(n)))
add('agent_sft conversations', f'20,000 training and 20,000 held-out conversations of a tool-using agent, on {len(ids)} training scans named '
    'in the text. Each is a list of turns, with the system prompt and tool definitions. A turn has a "from" field ('
    + ', '.join(sorted(roles)[:-1]) + ' or ' + sorted(roles)[-1] + ') and a "value" field that holds the text. The conversations '
    'were built by running each subtype\'s ground-truth tool trace against the tool cache (paper, '
    'Appendix e.4).' + (' The "images" field is empty in every conversation, although the paper describes a 2D image in the first turn.' if empty_images else ''),
    'text', 'other', 'other', 'agent_sft/train.jsonl, agent_sft/holdout.jsonl', evidence=AGENT, key='agent-sft')
caches = {n: json.load(open(path(f'tool_cache/{n}.json'))) for n in ('benchmark_oracle_tool_cache', 'benchmark_totalsegmentator_cache', 'training_oracle_tool_cache')}
add('tool_cache entries', 'Pre-computed tool outputs per scan. Each BDMAP ID has "segment" values (mask found, voxel count and '
    'bounding box for each structure) and "measure" values. The file benchmark_oracle_tool_cache.json covers '
    f'{len(caches["benchmark_oracle_tool_cache"]["cache"])} benchmark scans, with values from the ground-truth masks. The file '
    f'benchmark_totalsegmentator_cache.json covers the same {len(caches["benchmark_totalsegmentator_cache"]["cache"])} scans, '
    'with values from TotalSegmentator. The file training_oracle_tool_cache.json covers '
    f'{len(caches["training_oracle_tool_cache"]["cache"])} training scans. The last two files also hold a "knowledge" section '
    f'with {len(caches["benchmark_totalsegmentator_cache"]["knowledge"])} entries.',
    'other', 'imaging', 'other', 'tool_cache/*.json', evidence=AGENT, key='tool-cache')

write_json(OUT, V, tabs=True)
print(f'{len(V)} variables -> {OUT.relative_to(REPO)}')
