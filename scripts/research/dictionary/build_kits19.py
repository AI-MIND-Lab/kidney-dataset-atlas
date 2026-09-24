"""Build src/data/variables/kits19.json from the released kits.json and the KiTS19 data paper, section 3.

Definitions paraphrase the paper (source kits19-data-paper, section 3 "Data Records") or the README.
Observed values, types and missing counts come from data/kits.json at commit 67e495d (source kits19-kits-json).
The hand-written ranges and notes below were checked against that file; rerunning on another file needs a review.
"""
import json, collections

from kits_files import REPO_ROOT, flat, load

OUT = REPO_ROOT / 'src' / 'data' / 'variables' / 'kits19.json'
rows = [flat(c) for c in load('kits19')]
N = len(rows)
PAPER = {'sources': ['kits19-data-paper', 'kits19-kits-json'], 'locator': 'Section 3, Data Records; data/kits.json',
         'status': 'verified', 'verifiedOn': '2026-09-23'}
FILEONLY = {'sources': ['kits19-kits-json'], 'locator': 'data/kits.json', 'status': 'verified', 'verifiedOn': '2026-09-23'}
README = {'sources': ['kits19-repo'], 'locator': 'README, "Usage" and "Voxel Spacing"', 'status': 'verified',
          'verifiedOn': '2026-09-23'}


def counts(key):
    return collections.Counter(json.dumps(r.get(key)) for r in rows)


def nulls(key):
    return sum(1 for r in rows if r.get(key) is None)


def observed_codes(key, meanings=None):
    c = counts(key)
    out = []
    for v, n in sorted(c.items(), key=lambda t: -t[1]):
        if v == 'null':
            continue
        val = json.loads(v)
        code = str(val).lower() if isinstance(val, bool) else str(val)
        m = (meanings or {}).get(code, '')
        out.append({'code': code, 'meaning': (m + ' ' if m else '') + f'({n} of {N} cases)'})
    return out


V = []


def add(key, definition, vtype, group, role, time_point, unit=None, coding=None, missing=None, level='patient',
        provenance=None, evidence=PAPER, derivation='raw', concept=None):
    V.append({
        'id': 'kits19-' + key.replace('.', '-').replace('_', '-'),
        'release': 'kits19',
        'originalName': key,
        'file': 'data/kits.json',
        'definition': definition,
        'type': vtype,
        'unit': unit,
        'coding': coding or [],
        'missingValues': missing or [],
        'observationLevel': level,
        'timePoint': time_point,
        'role': role,
        'group': group,
        'derivation': derivation,
        'normalizedConcept': concept,
        **({'provenance': provenance} if provenance else {}),
        'evidence': evidence,
    })


def null_note(key, meaning):
    n = nulls(key)
    return [f'null: {meaning} ({n} of {N} cases)'] if n else []


# --- identifiers and demographics
add('case_id', 'Unique case identifier: "case_" followed by five digits giving the case index, zero-padded. Cases 00000 to 00209 are the public portion.',
    'text', 'administrative', 'identifier', None, provenance='Joins the clinical record to the case folder holding imaging.nii.gz and segmentation.nii.gz.')
add('age_at_nephrectomy', f"Patient's age when they underwent nephrectomy for the renal tumor. Observed range 1 to 90.",
    'integer', 'clinical', 'predictor', 'At nephrectomy', unit='years', concept='age')
add('gender', "The patient's gender.", 'categorical', 'clinical', 'predictor', None, coding=observed_codes('gender'), concept='sex/gender')
add('body_mass_index', 'Body mass index at the time measured nearest to the most recent imaging in the dataset. Observed range 16.2 to 49.61.',
    'decimal', 'clinical', 'predictor', 'Nearest to the preoperative CT', unit='kg/m²', concept='body mass index')

# --- comorbidities (bitmap)
COMORB = ['myocardial_infarction', 'congestive_heart_failure', 'peripheral_vascular_disease', 'cerebrovascular_disease',
          'dementia', 'copd', 'connective_tissue_disease', 'peptic_ulcer_disease', 'uncomplicated_diabetes_mellitus',
          'diabetes_mellitus_with_end_organ_damage', 'chronic_kidney_disease', 'hemiplegia_from_stroke', 'leukemia',
          'malignant_lymphoma', 'localized_solid_tumor', 'metastatic_solid_tumor', 'mild_liver_disease',
          'moderate_to_severe_liver_disease', 'aids']
for c in COMORB:
    key = 'comorbidities.' + c
    human = c.replace('_', ' ').replace('copd', 'COPD').replace('aids', 'AIDS')
    true_n = sum(1 for r in rows if r.get(key) is True)
    note = ' No case in the public portion is recorded as true.' if true_n == 0 else ''
    add(key, f'Whether the patient has {human}, one entry in the comorbidities bitmap.{note}', 'boolean', 'clinical',
        'predictor', 'Before nephrectomy', coding=observed_codes(key, {'true': 'Present', 'false': 'Not present'}),
        concept='comorbidity')

# --- lifestyle
add('smoking_history', "The patient's smoking history.", 'categorical', 'clinical', 'predictor', 'Before nephrectomy',
    coding=observed_codes('smoking_history'), concept='smoking status')
add('age_when_quit_smoking', 'Age at which the patient quit smoking. Stored in the file as text (for example "43"), although the paper specifies an integer.',
    'text', 'clinical', 'predictor', 'Before nephrectomy', unit='years',
    missing=[f'"not_applicable": not applicable ({counts("age_when_quit_smoking")[json.dumps("not_applicable")]} of {N} cases)'] + null_note('age_when_quit_smoking', 'not known'))
pack_int = sum(1 for r in rows if isinstance(r.get('pack_years'), int))
pack_str = sum(1 for r in rows if isinstance(r.get('pack_years'), str))
add('pack_years', f'Estimated cigarette pack-years smoked. Stored inconsistently: {pack_int} cases hold the number 0 and {pack_str} hold a number written as text (for example "30").',
    'integer', 'clinical', 'predictor', 'Before nephrectomy', unit='pack-years', missing=null_note('pack_years', 'unknown'))
add('chewing_tobacco_use', "The patient's chewing-tobacco use. The file's values differ from the paper's list (the paper gives \"never or not for more than 3mo\", \"quit in last 3mo\", \"currently chews\").",
    'categorical', 'clinical', 'predictor', 'Before nephrectomy', coding=observed_codes('chewing_tobacco_use'))
add('alcohol_use', "The patient's alcohol use.", 'categorical', 'clinical', 'predictor', 'Before nephrectomy',
    coding=observed_codes('alcohol_use'), concept='alcohol use')

# --- intraoperative complications (bitmap)
for c in ['blood_transfusion', 'injury_to_surrounding_organ', 'cardiac_event']:
    key = 'intraoperative_complications.' + c
    true_n = sum(1 for r in rows if r.get(key) is True)
    note = ' No case in the public portion is recorded as true.' if true_n == 0 else ''
    add(key, f'Whether a {c.replace("_", " ")} occurred during the operation, one entry in the intraoperative-complications bitmap.{note}',
        'boolean', 'outcome', 'outcome', 'During nephrectomy', coding=observed_codes(key, {'true': 'Occurred', 'false': 'Did not occur'}),
        concept='intraoperative complication')

# --- perioperative
add('hospitalization', 'Number of days the patient spent in hospital after the nephrectomy. Observed range 0 to 28.', 'integer', 'outcome',
    'outcome', 'After nephrectomy', unit='days',
    missing=[f'"died_before_discharge": the patient died before discharge ({counts("hospitalization")[json.dumps("died_before_discharge")]} of {N} cases)'],
    concept='length of stay')
add('ischemia_time', 'Minutes the kidney was deprived of blood during the nephrectomy. Observed range 0 to 54.', 'integer', 'clinical',
    'descriptor', 'During nephrectomy', unit='minutes',
    missing=[f'"not_applicable": radical nephrectomy ({counts("ischemia_time")[json.dumps("not_applicable")]} of {N} cases)'] + null_note('ischemia_time', 'partial nephrectomy with no value available'),
    concept='ischemia time')
add('radiographic_size', 'Tumor size reported in the radiology report. The unit is not stated by the source. Observed range 1.2 to 16.2.',
    'decimal', 'imaging', 'predictor', 'Preoperative', concept='tumor size')
add('pathologic_size', 'Tumor size reported in the surgical pathology report. The unit is not stated by the source. Observed range 0.8 to 22.5.',
    'decimal', 'pathology', 'outcome', 'Postoperative pathology', concept='tumor size')

# --- pathology
add('malignant', 'Whether the postoperative surgical pathology report indicates the tumor was malignant.', 'boolean', 'pathology',
    'outcome', 'Postoperative pathology', coding=observed_codes('malignant', {'true': 'Malignant', 'false': 'Not malignant'}), concept='malignancy')
add('pathology_t_stage', 'T stage reported in the postoperative surgical pathology report. The paper also allows "X", "1c" and "2b"; not every allowed value occurs in the public portion.',
    'categorical', 'pathology', 'outcome', 'Postoperative pathology', coding=observed_codes('pathology_t_stage'), concept='pathologic T stage')
add('pathology_n_stage', 'N stage reported in the postoperative surgical pathology report.', 'categorical', 'pathology', 'outcome',
    'Postoperative pathology', coding=observed_codes('pathology_n_stage', {'X': 'Not assessed'}), concept='pathologic N stage')
add('pathology_m_stage', 'M stage reported in the postoperative surgical pathology report.', 'categorical', 'pathology', 'outcome',
    'Postoperative pathology', coding=observed_codes('pathology_m_stage', {'X': 'Not assessed'}), concept='pathologic M stage')
add('tumor_histologic_subtype', 'Histologic subtype proved by surgical pathology.', 'categorical', 'pathology', 'outcome',
    'Postoperative pathology', coding=observed_codes('tumor_histologic_subtype'), concept='histologic subtype')
add('tumor_necrosis', 'Whether the surgical pathology report indicates necrotic tissue within the tumor.', 'boolean', 'pathology',
    'outcome', 'Postoperative pathology', coding=observed_codes('tumor_necrosis', {'true': 'Necrosis present', 'false': 'Necrosis absent'}),
    missing=null_note('tumor_necrosis', 'the report does not mention necrosis'), concept='tumor necrosis')
add('tumor_isup_grade', 'WHO/ISUP grade of the tumor in the postoperative surgical pathology report.', 'integer', 'pathology', 'outcome',
    'Postoperative pathology', coding=observed_codes('tumor_isup_grade'),
    missing=null_note('tumor_isup_grade', 'ISUP grade does not apply, e.g. benign tumors or chromophobe RCC'), concept='ISUP grade')

# --- postoperative outcomes
add('clavien_surgical_complications', 'Grade of surgical complications on the Clavien-Dindo scale.', 'categorical', 'outcome',
    'outcome', 'After nephrectomy', coding=observed_codes('clavien_surgical_complications'),
    missing=null_note('clavien_surgical_complications', 'could not be determined'), concept='Clavien-Dindo grade')
add('er_visit', 'Whether the patient visited the emergency room less than 24 hours after discharge without being admitted.', 'boolean',
    'outcome', 'outcome', 'After discharge', coding=observed_codes('er_visit', {'true': 'Visited', 'false': 'Did not visit'}),
    missing=null_note('er_visit', 'could not be determined'))
add('readmission', 'Whether the patient was readmitted to hospital within 90 days of surgery.', 'boolean', 'outcome', 'outcome',
    'Within 90 days of surgery', coding=observed_codes('readmission', {'true': 'Readmitted', 'false': 'Not readmitted'}),
    missing=null_note('readmission', 'could not be determined, e.g. censor or death date within 90 days'), concept='90-day readmission')
add('estimated_blood_loss', "Surgeon's estimate of blood lost during the nephrectomy. Observed range 0 to 2000.", 'integer', 'clinical',
    'descriptor', 'During nephrectomy', unit='ml', missing=null_note('estimated_blood_loss', 'not available'), concept='estimated blood loss')
add('surgery_type', 'Surgical technique used.', 'categorical', 'clinical', 'descriptor', 'At nephrectomy', coding=observed_codes('surgery_type'))
add('surgical_procedure', 'Whether the nephrectomy was partial or radical.', 'categorical', 'clinical', 'descriptor', 'At nephrectomy',
    coding=observed_codes('surgical_procedure'), concept='nephrectomy type')
add('surgical_approach', 'Surgical approach. Values are capitalized in the file, unlike the lowercase values in the paper.', 'categorical',
    'clinical', 'descriptor', 'At nephrectomy', coding=observed_codes('surgical_approach'))
add('operative_time', 'Duration of the nephrectomy procedure. Observed range 44 to 613.', 'integer', 'clinical', 'descriptor',
    'During nephrectomy', unit='minutes', missing=null_note('operative_time', 'could not be retrieved'), concept='operative time')
add('cytoreductive', 'Whether the nephrectomy was performed for debulking (cytoreduction).', 'boolean', 'clinical', 'descriptor',
    'At nephrectomy', coding=observed_codes('cytoreductive', {'true': 'Cytoreductive', 'false': 'Not cytoreductive'}))
add('positive_resection_margins', 'Whether the surgical pathology report indicates malignant tissue remaining at the margins of the excised tissue.',
    'boolean', 'pathology', 'outcome', 'Postoperative pathology', coding=observed_codes('positive_resection_margins', {'true': 'Positive margins', 'false': 'Clear margins'}),
    concept='surgical margin status')

# --- eGFR
EGFR_MISSING = ['">=90": the value was 90 or greater', '"age<16": patient younger than 16, for whom GFR cannot be reliably estimated']
for obj, label, tp, field_role, grp in [
        ('last_preop_egfr', 'the most recent eGFR measured before the nephrectomy', 'Before nephrectomy', 'predictor', 'clinical'),
        ('first_postop_egfr', 'the first eGFR measured after the nephrectomy', 'After nephrectomy', 'outcome', 'outcome'),
        ('last_postop_egfr', 'the most recent eGFR measured after the nephrectomy', 'After nephrectomy', 'outcome', 'outcome')]:
    vkey = obj + '.value'
    n_null = nulls(vkey)
    extra = {'last_postop_egfr': ' Null when one or fewer postoperative values were available.'}.get(obj, '')
    obs = counts(vkey)
    miss = [m + f' ({obs[json.dumps(m.split(":")[0].strip(chr(34)))]} of {N} cases)' for m in EGFR_MISSING if obs[json.dumps(m.split(":")[0].strip(chr(34)))]]
    miss += [f'null: no value available ({n_null} of {N} cases)'] if n_null else []
    add(vkey, f'Value of {label}.{extra}', 'decimal', grp, field_role, tp, unit='ml/min (as stated by the source)', missing=miss,
        concept='eGFR')
    dkey = [k for k in rows[0] if k.startswith(obj + '.days')] or [k for r in rows for k in r if k.startswith(obj + '.days')]
    dkey = dkey[0]
    dvals = [r[dkey] for r in rows if isinstance(r.get(dkey), int)]
    drange = f'Observed range {min(dvals):,} to {max(dvals):,}.'
    if obj == 'last_preop_egfr':
        ddef = f'Number of days before the nephrectomy that the preoperative eGFR was measured. {drange}'
    else:
        ddef = ('Days between the nephrectomy and this eGFR measurement. The paper defines this subfield as '
                '"days after nephrectomy", but the released file names it days_before_nephrectomy. '
                f'{drange}')
    add(dkey, ddef, 'integer', grp, 'descriptor', tp, unit='days', missing=[f'null: no value available ({nulls(dkey)} of {N} cases)'] if nulls(dkey) else [])

# --- survival
add('vital_status', "The patient's current vital status. Values are lowercase in the file, unlike the capitalized values in the paper.",
    'categorical', 'outcome', 'outcome', 'Last follow-up', coding=observed_codes('vital_status', {'censored': 'Alive at censor date', 'dead': 'Died'}),
    concept='vital status')
add('vital_days_after_surgery', 'Days from nephrectomy to the censor date or the date of death. Observed range 0 to 3,070.', 'integer',
    'outcome', 'outcome', 'Last follow-up', unit='days', concept='overall survival time')

# --- imaging geometry (file only; documented in README)
for ax, what in [('x', 'pixel width'), ('y', 'pixel height'), ('z', 'slice thickness')]:
    key = f'voxel_spacing.{ax}_spacing'
    add(key, f'Voxel spacing along the {ax}-axis of the CT volume ({what}), matching the affine of imaging.nii.gz. Not listed in the data paper; the README describes it. The unit is not stated.',
        'decimal', 'imaging', 'descriptor', 'Preoperative CT', level='examination', evidence={**README, 'sources': ['kits19-repo', 'kits19-kits-json']},
        provenance='Added to kits.json on 12 July 2021 ("finally added voxel spacing").')

# --- segmentation labels (imaging files, not kits.json)
V.append({
    'id': 'kits19-segmentation-label', 'release': 'kits19', 'originalName': 'segmentation label', 'file': 'segmentation.nii.gz',
    'definition': 'Voxel label in each case\'s segmentation volume.', 'type': 'categorical', 'unit': None,
    'coding': [{'code': '0', 'meaning': 'Background'}, {'code': '1', 'meaning': 'Kidney'}, {'code': '2', 'meaning': 'Tumor'}],
    'missingValues': [], 'observationLevel': 'slice', 'timePoint': 'Preoperative CT', 'role': 'annotation', 'group': 'imaging',
    'derivation': 'raw', 'normalizedConcept': 'segmentation class',
    'provenance': 'Manual annotation by students under clinician supervision, as described in the data paper; label values from the README.',
    'evidence': {'sources': ['kits19-repo'], 'locator': 'README, "Usage"', 'status': 'verified', 'verifiedOn': '2026-09-23'}})

ids = [v['id'] for v in V]
assert len(ids) == len(set(ids)), 'duplicate ids'
with open(OUT, 'w', encoding='utf8', newline='\n') as f:
    json.dump(V, f, ensure_ascii=False, indent='\t')
print(len(V), 'variables written')
