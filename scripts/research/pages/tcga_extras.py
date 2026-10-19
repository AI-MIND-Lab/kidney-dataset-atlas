"""Counts and GDC wording for the TCGA kidney page (docs/contributions/i-sababishraq/tcga_page.yaml).

    python scripts/research/dictionary/build_tcga_gdc.py      # once: GDC case records and data dictionary
    python scripts/research/pages/tcga_extras.py

build_page.py takes everything a page needs from the atlas records and the saved source texts. A page that also shows
numbers counted from provider files, or wording from a provider's own dictionary, gets them from an "extras" file
written by a script like this one. This one reads:

- the GDC case records and data dictionary cached by build_tcga_gdc.py (field definitions, code meanings, cohort);
- the GDC API: release status, project summaries, and slide-file facets;
- the TCIA API series lists for TCGA-KIRC, TCGA-KIRP and TCGA-KICH;
- BAMF's qa-results.csv and RCC-AID's metadata.csv from Zenodo.

It writes .research-cache/pages/tcga_extras.json. Only counts and dictionary text go in it, never patient-level records.
Use it as a model for another dataset's extras script; the file format is described in docs/contributions/README.md.
"""
import collections
import csv
import io
import json
import statistics
import sys
import urllib.parse
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import CACHE, cache_dir, get, get_json, write_json  # noqa: E402

P = ['KIRC', 'KIRP', 'KICH']
GDC = 'https://api.gdc.cancer.gov'
TCIA = 'https://services.cancerimagingarchive.net/nbia-api/services/v1/getSeries?Collection='
BAMF = 'https://zenodo.org/records/13244892/files/kidney-ct.zip?download=1'
RCCAID = 'https://zenodo.org/records/20719257/files/metadata.csv?download=1'
GDC_CACHE = CACHE / 'dictionary' / 'gdc'
HERE = cache_dir('pages', 'tcga')
OUT = CACHE / 'pages' / 'tcga_extras.json'
ENTITIES = ['case', 'demographic', 'diagnosis', 'treatment', 'pathology_detail', 'follow_up', 'molecular_test', 'exposure', 'sample', 'slide', 'slide_image']
DICT_CITE = 'GDC data dictionary'


def cached(name, fetch):
    """Download once into .research-cache/pages/tcga/<name>."""
    path = HERE / name
    if not path.exists():
        data = fetch()
        if data is None:
            raise SystemExit(f'Download failed for {name}. Try again later, or save the file as {path}.')
        path.write_bytes(data if isinstance(data, bytes) else json.dumps(data).encode('utf8'))
    return path


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def ws(x):
    return ' '.join(str(x).split()) if x else ''


# ---------------------------------------------------------------- GDC dictionary wording
def gdc_dictionary():
    out = {}
    for path in GDC_CACHE.glob('dictionary-*.json'):
        out[path.stem[len('dictionary-'):]] = load(path)
    if not out:
        raise SystemExit(f'No GDC dictionary in {GDC_CACHE}. Run scripts/research/dictionary/build_tcga_gdc.py first.')
    return out


def entity_of(name):
    if name in ('data_format', 'experimental_strategy'):
        return 'slide_image'
    for prefix, ent in [('diagnoses.treatments.', 'treatment'), ('diagnoses.pathology_details.', 'pathology_detail'), ('diagnoses.', 'diagnosis'),
                        ('follow_ups.molecular_tests.', 'molecular_test'), ('follow_ups.', 'follow_up'), ('exposures.', 'exposure'),
                        ('demographic.', 'demographic'), ('cases.samples.portions.slides.', 'slide'), ('cases.samples.', 'sample')]:
        if name.startswith(prefix):
            return ent
    return 'case'


def gdc_property(D, name):
    """The GDC entity, property name and dictionary entry of an atlas field name."""
    ent, prop = entity_of(name), name.split('.')[-1]
    p = (D.get(ent, {}).get('properties') or {}).get(prop)
    if isinstance(p, dict):
        return ent, prop, p
    for e, d in D.items():
        q = (d.get('properties') or {}).get(prop)
        if isinstance(q, dict) and q.get('description'):
            return e, prop, q
    return ent, prop, None


def field_overrides(D, repo):
    out, entries = {}, 0
    for p in P:
        for v in load(repo / f'src/data/variables/tcga-{p.lower()}-gdc-open.json'):
            name, entries = v['originalName'], entries + 1
            ent, prop, pdef = gdc_property(D, name)
            enum = (pdef or {}).get('enumDef') or {}
            f = out.setdefault(name, {'entity': ent.replace('_', ' '), 'property': prop, 'definition': ws((pdef or {}).get('description')),
                                      'source': 'gdc-data-dictionary', 'locator': f'{ent}.{prop}', 'codes': {}})
            f['codes'].update({c['code']: ws((enum.get(c['code']) or {}).get('description')) for c in v.get('coding', [])})
    return out, entries


def snapshot_overrides(D, repo):
    """GDC definitions for the clinical columns of the Crowds-Cure-2017 snapshot. gender and tumor_stage are left out:
    their stored values do not follow the current GDC definitions."""
    out = {}
    for v in load(repo / 'src/data/variables/crowds-cure-2017-v1.json'):
        if v.get('file', '').startswith('CrowdsCure') or v['originalName'] in ('gender', 'tumor_stage'):
            continue
        ent, prop, pdef = gdc_property(D, v['originalName'])
        if pdef and pdef.get('description'):
            out[v['originalName']] = {'definition': ws(pdef['description']), 'source': 'gdc-data-dictionary', 'locator': f'{ent}.{prop}'}
    return out


# ---------------------------------------------------------------- provider downloads
def gdc_live():
    def q(path, **params):
        return get_json(f'{GDC}/{path}?' + urllib.parse.urlencode(params) if params else f'{GDC}/{path}')
    out = {'status': q('status')}
    for p in P:
        proj = q(f'projects/TCGA-{p}', expand='summary')['data']
        flt = {'op': 'and', 'content': [{'op': 'in', 'content': {'field': 'cases.project.project_id', 'value': [f'TCGA-{p}']}},
                                        {'op': 'in', 'content': {'field': 'data_type', 'value': ['Slide Image']}}]}
        agg = q('files', filters=json.dumps(flt), facets='experimental_strategy,access,data_format', size=0)['data']['aggregations']
        out[p] = {'cases': proj['summary']['case_count'], 'slides': {k: {b['key']: b['doc_count'] for b in v['buckets']} for k, v in agg.items()}}
    return out


def main():
    repo = Path(__file__).resolve().parents[3]
    D = gdc_dictionary()
    live = load(cached('gdc_live.json', gdc_live))
    series = {p: load(cached(f'tcia_TCGA-{p}.json', lambda p=p: get_json(TCIA + f'TCGA-{p}'))) for p in P}
    with zipfile.ZipFile(cached('bamf_kidney.zip', lambda: get(BAMF, binary=True))) as z:
        bamf = list(csv.DictReader(io.TextIOWrapper(z.open('qa-results.csv'), encoding='utf8')))
    rcc = list(csv.DictReader(io.StringIO(cached('rccaid_metadata.csv', lambda: get(RCCAID, binary=True)).read_text(encoding='utf-8-sig'))))
    cases = {p: load(GDC_CACHE / f'cases-{p}.json')['data']['hits'] for p in P}
    release = live['status']['data_release']
    summary_src = [f'gdc-{p.lower()}-summary' for p in P]
    slide_src = ['gdc-kirc-slides']  # the atlas has a slide-facet source record for TCGA-KIRC only
    series_src = [f'tcia-tcga-{p.lower()}-series' for p in P]
    record_src = [f'gdc-{p.lower()}-case-records' for p in P]

    # radiology
    tsum = {}
    for p in P:
        rows, pat_mod = series[p], collections.defaultdict(set)
        for r in rows:
            pat_mod[r['PatientID']].add(r.get('Modality'))
        tsum[p] = {'patients': len(pat_mod), 'studies': len({r['StudyInstanceUID'] for r in rows}), 'series': len(rows),
                   'images': sum(int(r.get('ImageCount') or 0) for r in rows),
                   'mod_series': collections.Counter(r.get('Modality') for r in rows).most_common(),
                   'mod_patients': collections.Counter(m for mods in pat_mod.values() for m in mods).most_common(),
                   'manufacturers': collections.Counter((r.get('Manufacturer') or '').strip() or '(not recorded)' for r in rows).most_common(6)}

    # cohort
    cohort = {}
    for p in P:
        demo = [c.get('demographic') or {} for c in cases[p]]
        ages = [d['age_at_index'] for d in demo if isinstance(d.get('age_at_index'), int)]
        count = lambda k: collections.Counter(d.get(k) or '(no value)' for d in demo).most_common()
        cohort[p] = {'cases': len(cases[p]), 'sex': count('sex_at_birth'), 'race': count('race'), 'ethnicity': count('ethnicity'), 'vital': count('vital_status'),
                     'age': (statistics.median(ages), statistics.quantiles(ages, n=4), min(ages), max(ages), len(ages)) if len(ages) > 3 else None}

    def age(a):
        return f'{a[0]:g} ({a[1][0]:g}–{a[1][2]:g}); {a[2]}–{a[3]}; n = {a[4]}' if a else '—'

    n_slides = {p: sum(live[p]['slides']['experimental_strategy'].values()) for p in P}
    fo, entries = field_overrides(D, repo)
    extras = {
        'values': {'data_release': {'value': release, 'cite': 'GDC API status', 'sources': ['gdc-kirc-summary']}},
        'cards': [
            {'value': f'{sum(live[p]["cases"] for p in P):,}', 'label': 'Cases (GDC)', 'detail': ' · '.join(f'{p} {live[p]["cases"]:,}' for p in P)},
            {'value': f'{sum(tsum[p]["patients"] for p in P):,}', 'label': 'Patients with radiology (TCIA)', 'detail': ' · '.join(f'{p} {tsum[p]["patients"]:,}' for p in P)},
            {'value': f'{sum(n_slides.values()):,}', 'label': 'Slide image files (GDC)', 'detail': ' · '.join(f'{p} {n_slides[p]:,}' for p in P)},
            {'value': f'{len(fo)}', 'label': 'GDC fields', 'detail': f'{entries} entries in {len(P)} projects'}],
        'overview_caption': {'text': f'Counts: GDC {release} and TCIA series lists', 'sources': summary_src + series_src},
        'field_overrides': fo,
        'analysis_overrides': {'Crowds-Cure clinical snapshot': snapshot_overrides(D, repo)},
        'tables': {
            'gdc_entities': {'evidence': 'DOCUMENTED', 'sources': ['gdc-data-dictionary'], 'columns': ['Entity', 'GDC title', 'GDC description'], 'format': {'0': 'code', '2': 'quote'},
                             'rows': [[e, ws(D[e].get('title')), ws(D[e].get('description'))] for e in ENTITIES if e in D]},
            'slides': {'evidence': 'CALCULATED', 'sources': slide_src, 'columns': ['Project', 'Tissue Slide', 'Diagnostic Slide', 'data_format', 'access'], 'numcols': [1, 2],
                       'rows': [[f'TCGA-{p}', f'{live[p]["slides"]["experimental_strategy"].get("Tissue Slide", 0):,}', f'{live[p]["slides"]["experimental_strategy"].get("Diagnostic Slide", 0):,}',
                                 ', '.join(f'{k} {v:,}' for k, v in live[p]['slides']['data_format'].items()), ', '.join(f'{k} {v:,}' for k, v in live[p]['slides']['access'].items())] for p in P]},
            'radiology': {'evidence': 'CALCULATED', 'sources': series_src, 'columns': ['Collection', 'Patients', 'Studies', 'Series', 'Images', 'Patients by Modality'], 'numcols': [1, 2, 3, 4],
                          'rows': [[f'TCGA-{p}', *(f'{tsum[p][k]:,}' for k in ('patients', 'studies', 'series', 'images')), ', '.join(f'{m} {n:,}' for m, n in tsum[p]['mod_patients'])] for p in P]},
            'bamf': {'evidence': 'CALCULATED', 'sources': ['bamf-aimi-zenodo'], 'caption': 'qa-results.csv', 'columns': ['Collection', 'Scans (series)', 'Patients', 'Reviewer rad*', 'CorrectedSegmentation'],
                     'numcols': [1, 2, 3, 4], 'rows': []},
            'rccaid': {'evidence': 'CALCULATED', 'sources': ['rcc-aid-zenodo'], 'caption': 'metadata.csv', 'columns': ['Collection', 'Scans', 'Patients'], 'numcols': [1, 2],
                       'rows': [[f'TCGA-{p}', f'{sum(1 for r in rcc if r["Collection"] == f"TCGA-{p}"):,}', f'{len({r["PatientID"] for r in rcc if r["Collection"] == f"TCGA-{p}"}):,}'] for p in P]},
            'cohort': {'evidence': 'CALCULATED', 'sources': record_src, 'columns': ['Project', 'Cases', 'sex_at_birth', 'vital_status', 'age_at_index: median (IQR); range; n'], 'numcols': [1],
                       'rows': [[f'TCGA-{p}', f'{cohort[p]["cases"]:,}', ', '.join(f'{k} {v}' for k, v in cohort[p]['sex']), ', '.join(f'{k} {v}' for k, v in cohort[p]['vital']), age(cohort[p]['age'])] for p in P]},
        },
        'bars': {
            'radiology': [[{'title': f'TCGA-{p}: Modality (series)', 'rows': tsum[p]['mod_series'], 'total': tsum[p]['series']},
                           {'title': 'Manufacturer (series)', 'rows': tsum[p]['manufacturers'], 'total': tsum[p]['series']}] for p in P],
            'cohort': [[{'title': f'TCGA-{p}: race', 'rows': cohort[p]['race'], 'total': cohort[p]['cases']},
                        {'title': 'ethnicity', 'rows': cohort[p]['ethnicity'], 'total': cohort[p]['cases']}] for p in P],
        },
        'glossary': {'gdc': [{'term': D[e]['title'], 'definition': ws(D[e]['description']), 'cite': DICT_CITE, 'source': 'gdc-data-dictionary', 'category': 'Technical'}
                             for e in ('case', 'demographic', 'diagnosis', 'follow_up', 'treatment', 'exposure', 'sample', 'slide') if e in D]
                     + [{'term': 'ajcc_pathologic_stage', 'definition': fo['diagnoses.ajcc_pathologic_stage']['definition'], 'cite': DICT_CITE,
                         'source': 'gdc-data-dictionary', 'category': 'Medical'}]},
    }
    for p in P:
        r = [x for x in bamf if x['Collection'] == f'tcga_{p.lower()}']
        n = (len({x['SeriesInstanceUID'] for x in r}), len({x['PatientID'] for x in r}),
             len({x['SeriesInstanceUID'] for x in r if x['Reviewer'].startswith('rad')}), len({x['SeriesInstanceUID'] for x in r if x['CorrectedSegmentation']}))
        extras['tables']['bamf']['rows'].append([f'TCGA-{p}', *(f'{x:,}' for x in n)])
    write_json(OUT, extras)
    print(f'wrote {OUT.relative_to(repo)}: {release}, {len(fo)} GDC fields, {sum(len(series[p]) for p in P):,} TCIA series, {len(bamf):,} BAMF rows, {len(rcc):,} RCC-AID rows')


if __name__ == '__main__':
    main()
