"""Build src/data/variables/tcga-{kirc,kirp,kich}-gdc-open.json from the GDC API.

Every clinical property the GDC returns with a real value for at least one case in the project is documented,
together with the metadata of the open slide-image files. Definitions come from the GDC data dictionary
(api.gdc.cancer.gov/v0/submission/_dictionary/<entity>); observed values, counts and missing-value markers come
from the project's case and file records. A property whose only values are GDC's "Not Reported"-style markers is
left out and counted in the summary printed at the end.

Downloads are cached in .research-cache/dictionary/gdc/; delete that folder to rebuild from a newer GDC release.
"""
import collections
import json
import sys
import urllib.parse

import _setup  # noqa: F401
from common import REPO as REPO_ROOT, cache_dir, get, get_json

VERIFIED_ON = '2026-09-26'
PROJECTS = ['KIRC', 'KIRP', 'KICH']
GDC = 'https://api.gdc.cancer.gov'
CACHE = cache_dir('dictionary', 'gdc')

# API path of each clinical entity, as it appears in an expanded case record.
EXPAND = {'demographic': 'demographic', 'diagnoses': 'diagnosis', 'treatments': 'treatment',
          'pathology_details': 'pathology_detail', 'exposures': 'exposure', 'follow_ups': 'follow_up',
          'molecular_tests': 'molecular_test', 'family_histories': 'family_history'}
PATH = {'case': '', 'demographic': 'demographic.', 'diagnosis': 'diagnoses.', 'treatment': 'diagnoses.treatments.',
        'pathology_detail': 'diagnoses.pathology_details.', 'exposure': 'exposures.', 'follow_up': 'follow_ups.',
        'molecular_test': 'follow_ups.molecular_tests.', 'family_history': 'family_histories.'}
SKIP = {'created_datetime', 'updated_datetime', 'state', 'id'} | {e + '_id' for e in EXPAND.values()}
MARKERS = {'Not Reported', 'not reported', 'Unknown', 'unknown', 'Not Applicable', 'not applicable', '--'}
SLIDE_FIELDS = ['section_location', 'percent_tumor_cells', 'percent_tumor_nuclei', 'percent_normal_cells',
                'percent_stromal_cells', 'percent_necrosis', 'percent_lymphocyte_infiltration',
                'percent_monocyte_infiltration', 'percent_neutrophil_infiltration', 'number_proliferating_cells']

LEVEL = {'case': 'patient', 'demographic': 'patient', 'exposure': 'patient', 'slide': 'slide', 'file': 'slide'}
TIME = {'diagnosis': 'Diagnosis', 'pathology_detail': 'Diagnosis', 'treatment': 'Treatment', 'follow_up': 'Follow-up',
        'molecular_test': 'Initial diagnosis', 'slide': 'Tissue collection', 'file': 'Tissue collection'}
OUTCOME = {'vital_status', 'days_to_death', 'days_to_last_follow_up', 'lost_to_followup', 'days_to_follow_up',
           'days_to_progression', 'days_to_recurrence', 'disease_response', 'progression_or_recurrence',
           'progression_or_recurrence_type', 'treatment_outcome'}
PATHOLOGY = {'tumor_grade', 'morphology', 'primary_diagnosis', 'ajcc_pathologic_stage', 'ajcc_pathologic_t',
             'ajcc_pathologic_n', 'ajcc_pathologic_m', 'classification_of_tumor', 'tissue_or_organ_of_origin'}
CONCEPT = {'case_id': 'case identifier', 'submitter_id': 'case identifier', 'age_at_index': 'age',
           'age_at_diagnosis': 'age at diagnosis', 'sex_at_birth': 'sex/gender', 'race': 'race',
           'ethnicity': 'ethnicity', 'vital_status': 'vital status', 'days_to_death': 'overall survival time',
           'days_to_last_follow_up': 'follow-up time', 'ajcc_pathologic_stage': 'pathologic stage',
           'ajcc_pathologic_t': 'pathologic T stage', 'ajcc_pathologic_n': 'pathologic N stage',
           'ajcc_pathologic_m': 'pathologic M stage', 'ajcc_clinical_stage': 'clinical stage',
           'tumor_grade': 'histologic grade', 'primary_diagnosis': 'histologic subtype', 'morphology': 'histologic subtype',
           'laterality': 'laterality', 'pack_years_smoked': 'pack-years', 'tobacco_smoking_status': 'smoking status',
           'therapeutic_agents': 'systemic therapy', 'prcc_type': 'papillary RCC type', 'sample_type': 'sample type',
           'percent_tumor_cells': 'tumour cell percentage', 'percent_necrosis': 'necrosis percentage'}
# Facts the dictionary does not carry, each checked against the cited source.
NOTES = {
    'case_id': "The GDC's unique identifier (UUID) for the case.",
    'submitter_id': ("The TCGA patient barcode, such as TCGA-B0-5098. The Cancer Imaging Archive uses the same barcode "
                     "as PatientID for this project's radiology."),
    'age_at_diagnosis': 'The GDC schema caps this value at 32,872 days (90 years); age_is_obfuscated marks cases whose age was altered for compliance.',
    'age_at_index': 'The index date for these cases is the diagnosis (see index_date).',
    'days_to_birth': 'Negative: counted backwards from the index date.',
    'tumor_of_origin': 'Links a diagnosis record to the primary diagnosis it arose from.',
    'diagnosis_is_primary_disease': 'Cases can carry several diagnosis records; this flag separates the primary renal diagnosis from others such as prior malignancies.',
}
DIAG_NOTE = ('A case can have several diagnosis records (see diagnosis_is_primary_disease), so a patient-level '
             'analysis must choose which record to use.')
STRATEGY = {'Diagnostic Slide': ('Formalin-fixed paraffin-embedded slide submitted by the tissue source site to confirm '
                                 'the diagnosis; its relationship to the material sent for genomic analysis is unknown'),
            'Tissue Slide': ('Top- or bottom-section slide cut from the tissue submitted to TCGA, reviewed to check '
                             'tumour and necrosis content before genomic analysis')}


def case_records(project):
    path = CACHE / f'cases-{project}.json'
    if not path.exists():
        filters = {'op': 'in', 'content': {'field': 'project.project_id', 'value': [f'TCGA-{project}']}}
        expand = 'demographic,diagnoses,diagnoses.treatments,diagnoses.pathology_details,exposures,follow_ups,follow_ups.molecular_tests,family_histories'
        text = get(f'{GDC}/cases?' + urllib.parse.urlencode({'filters': json.dumps(filters), 'expand': expand, 'size': 5000}))
        path.write_text(text, encoding='utf8')
    return json.loads(path.read_text(encoding='utf8'))['data']['hits']


def slide_files(project):
    path = CACHE / f'slides-{project}.json'
    if not path.exists():
        filters = {'op': 'and', 'content': [
            {'op': 'in', 'content': {'field': 'cases.project.project_id', 'value': [f'TCGA-{project}']}},
            {'op': 'in', 'content': {'field': 'data_type', 'value': ['Slide Image']}}]}
        fields = ['file_id', 'data_format', 'experimental_strategy', 'access', 'cases.submitter_id', 'cases.samples.sample_type']
        fields += [f'cases.samples.portions.slides.{f}' for f in SLIDE_FIELDS]
        text = get(f'{GDC}/files?' + urllib.parse.urlencode({'filters': json.dumps(filters), 'fields': ','.join(fields), 'size': 10000}))
        path.write_text(text, encoding='utf8')
    return json.loads(path.read_text(encoding='utf8'))['data']['hits']


def dictionary(entity):
    path = CACHE / f'dictionary-{entity}.json'
    if not path.exists():
        path.write_text(json.dumps(get_json(f'{GDC}/v0/submission/_dictionary/{entity}')), encoding='utf8')
    return json.loads(path.read_text(encoding='utf8'))['properties']


def gdc_type(prop):
    if 'enum' in prop:
        return 'categorical'
    kinds = prop.get('type') or [o.get('type') for o in prop.get('oneOf', [])]
    kinds = kinds if isinstance(kinds, list) else [kinds]
    for gdc, ours in (('boolean', 'boolean'), ('integer', 'integer'), ('number', 'decimal')):
        if gdc in kinds:
            return ours
    return 'text'


def unit(field):
    if field.startswith('days_to') or field == 'age_at_diagnosis':
        return 'days'
    if field == 'age_at_index':
        return 'years'
    if field.startswith('year_') or field.endswith('_year'):
        return 'calendar year'
    if field.startswith('percent_'):
        return '%'
    return {'pack_years_smoked': 'pack-years', 'lymph_nodes_positive': 'lymph nodes',
            'lymph_nodes_tested': 'lymph nodes', 'prescribed_dose': 'given in prescribed_dose_units',
            'treatment_dose': 'given in treatment_dose_units'}.get(field)


def fmt(v):
    return f'{v:,}' if isinstance(v, int) and not isinstance(v, bool) else str(v)


def describe(project, entity, field, values, n_records, n_cases, n_total, prop, observed_on):
    """One variable record. values holds every value of the field, None included, one per entity record."""
    present = [v for v in values if v is not None]
    real = [v for v in present if not (isinstance(v, str) and v in MARKERS)]
    counts = collections.Counter(real)
    vtype = gdc_type(prop) if prop else ('decimal' if all(isinstance(v, (int, float)) for v in real) else 'text')
    parts = [(prop or {}).get('description', '').strip() or 'Not described in the GDC data dictionary.']
    if field in NOTES and not (entity == 'diagnosis' and field == 'submitter_id'):
        parts.append(NOTES[field])
    if entity == 'file' and field == 'experimental_strategy':
        parts.append('Meanings from Cooper et al. 2018.')
    per = {'case': 'cases', 'file': 'slide-image files', 'slide': 'slide-image files'}.get(entity, f'{entity.replace("_", " ")} records')
    one_per_case = entity in ('case', 'file', 'slide') or n_records == n_total
    parts.append(f'Has a value in {len(real):,} of {n_records:,} {per}' + ('' if one_per_case else f', covering {n_cases:,} of {n_total:,} cases') + '.')
    numeric = vtype in ('integer', 'decimal') and real and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in real)
    coding = []
    if numeric:
        parts.append(f'Observed range {fmt(min(real))} to {fmt(max(real))}.')
    elif vtype in ('categorical', 'boolean') or len(counts) <= 30:
        enum_def = (prop or {}).get('enumDef') or {}
        shown = counts.most_common(25)
        if len(counts) > 25:
            parts.append(f'{len(counts)} distinct values; the 25 most frequent are listed.')
        for v, n in shown:
            code = str(v).lower() if isinstance(v, bool) else str(v)
            meaning = STRATEGY.get(code, '') if field == 'experimental_strategy' else (enum_def.get(code) or {}).get('description', '')
            meaning = (meaning[:157] + '...') if len(meaning) > 160 else meaning
            coding.append({'code': code, 'meaning': (meaning + ' ' if meaning else '') + f'({n:,} {per})'})
    else:
        parts.append(f'{len(counts):,} distinct values.')
    missing = [f'"{m}": {n:,} {per}' for m, n in collections.Counter(v for v in present if isinstance(v, str) and v in MARKERS).most_common()]
    if len(present) < n_records:
        missing.append(f'null: no value ({n_records - len(present):,} {per})')
    if entity == 'diagnosis' and field not in NOTES:
        parts.append(DIAG_NOTE)

    group = ('administrative' if entity == 'case' and field not in OUTCOME else
             'outcome' if field in OUTCOME else
             'pathology' if entity in ('pathology_detail', 'slide', 'file') or field in PATHOLOGY else 'clinical')
    role = ('identifier' if field in ('case_id', 'submitter_id') else
            'outcome' if field in OUTCOME else 'descriptor')
    path = 'cases.samples.portions.slides.' if entity == 'slide' else 'cases.samples.' if field == 'sample_type' else PATH.get(entity, '')
    source = 'gdc-slide-files' if entity in ('file', 'slide') else 'gdc-case-records'
    return {
        'id': f'{project.lower()}-{entity.replace("_", "-")}-{field.replace("_", "-")}',
        'release': f'tcga-{project.lower()}-gdc-open',
        'originalName': path + field,
        'file': 'GDC API file record (Slide Image)' if source == 'gdc-slide-files' else f'GDC API case record ({entity.replace("_", " ")})',
        'definition': ' '.join(parts),
        'type': 'integer' if numeric and vtype == 'decimal' and all(isinstance(v, int) for v in real) and field.startswith('days') else vtype,
        'unit': unit(field),
        'coding': coding,
        'missingValues': missing,
        'observationLevel': LEVEL.get(entity, 'record'),
        'timePoint': TIME.get(entity),
        'role': role,
        'group': group,
        'derivation': 'raw',
        'normalizedConcept': CONCEPT.get(field),
        'provenance': (f'GDC data model entity "{"slide" if entity == "file" else entity}". Values observed in the {project} '
                       f'{"slide-image file" if source == "gdc-slide-files" else "case"} records returned by the GDC API ({observed_on}).'),
        'evidence': {'sources': ['gdc-data-dictionary', f'gdc-{project.lower()}-{"slide-files" if source == "gdc-slide-files" else "case-records"}']
                     + (['cooper-2018-tcga-pathology'] if field == 'experimental_strategy' else []),
                     'locator': f'Dictionary entity "{"slide_image" if entity == "file" else entity}", property "{field}"',
                     'status': 'verified', 'verifiedOn': VERIFIED_ON},
    }


def build(project, observed_on):
    cases = case_records(project)
    n_total = len(cases)
    fields = collections.defaultdict(list)       # (entity, field) -> values, one per entity record
    covered = collections.defaultdict(set)       # (entity, field) -> case ids with a real value
    records = collections.Counter()

    def walk(obj, entity, cid):
        if entity != 'case':
            records[entity] += 1
        for k, v in obj.items():
            if k in EXPAND:
                for item in (v if isinstance(v, list) else [v]):
                    walk(item, EXPAND[k], cid)
            elif isinstance(v, (dict, list)) or k in SKIP or (entity != 'case' and k == 'submitter_id'):
                continue
            else:
                fields[(entity, k)].append(v)
                if v is not None and not (isinstance(v, str) and v in MARKERS):
                    covered[(entity, k)].add(cid)

    for c in cases:
        walk(c, 'case', c['case_id'])
    records['case'] = n_total
    # Properties absent from a record count as null for that record.
    for (entity, k), vals in fields.items():
        vals.extend([None] * (records[entity] - len(vals)))

    files = slide_files(project)
    for f in files:
        fields[('file', 'experimental_strategy')].append(f.get('experimental_strategy'))
        fields[('file', 'data_format')].append(f.get('data_format'))
        samples = [s for c in f.get('cases', []) for s in c.get('samples', [])]
        fields[('file', 'sample_type')].append(samples[0].get('sample_type') if samples else None)
        slides = [sl for s in samples for p in s.get('portions', []) for sl in p.get('slides', [])]
        for name in SLIDE_FIELDS:
            fields[('slide', name)].append(slides[0].get(name) if slides else None)
    records['file'] = records['slide'] = len(files)

    dicts = {e: dictionary(e) for e in set(EXPAND.values()) | {'case', 'slide', 'sample'}}
    dicts['file'] = {**dictionary('slide_image'), 'sample_type': dicts['sample']['sample_type']}
    out, dropped = [], []
    order = ['case', 'demographic', 'diagnosis', 'pathology_detail', 'treatment', 'exposure', 'follow_up', 'molecular_test',
             'family_history', 'file', 'slide']
    for (entity, k) in sorted(fields, key=lambda t: (order.index(t[0]), t[1])):
        vals = fields[(entity, k)]
        if not any(v is not None and not (isinstance(v, str) and v in MARKERS) for v in vals):
            dropped.append(f'{entity}.{k}')
            continue
        out.append(describe(project, entity, k, vals, records[entity], len(covered[(entity, k)]), n_total,
                            dicts[entity].get(k), observed_on))
    ids = [v['id'] for v in out]
    assert len(ids) == len(set(ids)), 'duplicate ids'
    target = REPO_ROOT / 'src' / 'data' / 'variables' / f'tcga-{project.lower()}-gdc-open.json'
    with open(target, 'w', encoding='utf8', newline='\n') as fh:
        json.dump(out, fh, ensure_ascii=False, indent='\t')
        fh.write('\n')
    print(f'TCGA-{project}: {n_total} cases, {len(files)} slide files, {len(out)} variables; '
          f'{len(dropped)} properties with no real value left out: {", ".join(dropped)}')


if __name__ == '__main__':
    status_file = CACHE / 'status.json'  # the GDC release the cached records came from
    if not status_file.exists():
        status_file.write_text(json.dumps(get_json(f'{GDC}/status') or {}), encoding='utf8')
    release = json.loads(status_file.read_text(encoding='utf8')).get('data_release', 'GDC data release not recorded')
    for p in sys.argv[1:] or PROJECTS:
        build(p, release)
