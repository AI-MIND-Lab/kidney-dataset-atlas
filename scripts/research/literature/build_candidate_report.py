"""Step 6: write docs/literature/paper-candidates.md and paper-candidates.csv from the classified candidates.

Rows verified or excluded by hand (verified_status.py) are marked in the CSV. The markdown page carries the
attribution that the Semantic Scholar API licence requires; keep that section when editing this script.
"""
import collections
import csv
import datetime
import urllib.parse
from pathlib import Path

import _setup  # noqa: F401
from common import CACHE, REPO, read_json
from verified_status import VERIFIED, EXCLUDED

OUT = REPO / 'docs' / 'literature'
OUT.mkdir(parents=True, exist_ok=True)
TODAY = datetime.date.today().isoformat()
LIT = CACHE / 'literature'

entries = read_json(Path(__file__).with_name('anchors.json'))['datasets']
anchors = {d['id']: d for d in entries if not d.get('mergeInto')}
extra = {d['id']: d for d in entries if d.get('mergeInto')}
cands = read_json(LIT / 'candidates.json')
oa = read_json(LIT / 'openalex_ids.json') if (LIT / 'openalex_ids.json').exists() else {}
DATA_DOIS = {d['id']: d['dataDois'] for d in entries if d.get('dataDois')}
ATTRIBUTION = """## Sources, attribution and terms

This sheet was compiled from the following services. Their terms apply to the data drawn from them, and they
also apply to the `evidence_sentence` column of the CSV.

- **Semantic Scholar.** Citation lists, citing sentences ("contexts"), citation intents and paper metadata come
  from the [Semantic Scholar Academic Graph API](https://www.semanticscholar.org/product/api), used under its
  [API License Agreement](https://www.semanticscholar.org/product/api/license). Data provided by Semantic
  Scholar is subject to the [S2 data licences](https://www.semanticscholar.org/product/api/license)
  (ODC-BY or CC BY-NC, as applicable). Please cite: Kinney, R., et al. *The Semantic Scholar Open Data Platform*.
  arXiv:2301.10140 (2023). <https://arxiv.org/abs/2301.10140>
- **OpenAlex.** Citing-work lists and abstracts come from [OpenAlex](https://openalex.org), whose data is
  released under [CC0](https://creativecommons.org/publicdomain/zero/1.0/). Please cite: Priem, J., Piwowar, H.,
  & Orr, R. *OpenAlex: A fully-open index of scholarly works, authors, venues, institutions, and concepts*.
  arXiv:2205.01833 (2022). <https://arxiv.org/abs/2205.01833>
- **Europe PMC.** Methods-section and full-text searches use the
  [Europe PMC RESTful API](https://europepmc.org/RestfulWebService).
- **DataCite and Crossref.** Works citing dataset DOIs come from the [DataCite REST API](https://support.datacite.org/docs/api)
  (metadata released under CC0), with bibliographic details from the [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/).

**Quoted text.** The `evidence_sentence` column quotes one sentence per row from the citing paper. It is either
a citing sentence supplied by Semantic Scholar or a sentence from the paper's abstract. The excerpts are there
only so a reviewer can judge whether the paper used the dataset. Copyright in each excerpt stays with the
paper's authors and publisher, and each row links to the source paper. The rest of this sheet is covered by
the repository's terms for research content (see [LICENSE](../../LICENSE)).
"""
# Where a host keeps its own list of work built on the data.
HOST = {
    'K01': [('KiTS19 leaderboard (Grand Challenge)', 'https://kits19.grand-challenge.org/evaluation/challenge/leaderboard/')],
    'K05': [('Kaggle "Code" tab (notebooks, not papers)', 'https://www.kaggle.com/datasets/nazmul0087/ct-kidney-dataset-normal-cyst-tumor-and-stone/code')],
    'K09': [('TCIA publication list', 'https://www.cancerimagingarchive.net/publications/')],
    'G02': [('TCIA publication list', 'https://www.cancerimagingarchive.net/publications/')],
    'M05': [('TCIA publication list', 'https://www.cancerimagingarchive.net/publications/')],
    'K10': [('Kaggle competition "Code" tab', 'https://www.kaggle.com/competitions/hubmap-kidney-segmentation/code')],
    'K11-K12': [('Kaggle competition "Code" tab', 'https://www.kaggle.com/competitions/hubmap-organ-segmentation/code')],
    'M13': [('Hugging Face dataset page', 'https://huggingface.co/datasets/blueyo0/SA-Med3D-140K')],
    'H10': [('Hugging Face dataset page', 'https://huggingface.co/datasets/stanfordmimi/Merlin')],
    'H11': [('Hugging Face dataset page', 'https://huggingface.co/datasets/raidium/RadImageNet-VQA')],
}
# Name used for a Google Scholar full-text search (Scholar indexes body text).
SCHOLAR_NAME = {
    'K01': '"KiTS19"', 'K02': '"KiTS21"', 'K03': '"KiTS23"', 'K04': '"kidney abnormality segmentation" Radboud',
    'K05': '"CT KIDNEY DATASET: Normal-Cyst-Tumor and Stone"', 'K06-K08': '"TCGA-KIRC" OR "TCGA-KIRP" OR "TCGA-KICH" whole-slide deep learning',
    'K09': '"TCGA-KIRC" TCIA CT segmentation', 'K10': '"Hacking the Kidney" HuBMAP', 'K11-K12': '"Hacking the Human Body" HuBMAP',
    'K13': '"TRUSTED" kidney ultrasound CT dataset', 'K14': '"Axial CT Imaging Dataset for AI-Powered Kidney Stone Detection"',
    'M01': '"TotalSegmentator dataset"', 'M02': '"TotalSegmentator MRI"', 'M03': '"AMOS22" OR "AMOS dataset"', 'M04': '"CHAOS challenge" kidney',
    'M05': '"CT-ORG"', 'M06': '"WORD dataset" abdominal', 'M07': '"AbdomenAtlas"', 'M08': '"FLARE21" OR "FLARE 2021"',
    'M09': '"FLARE22" OR "FLARE 2022"', 'M10': '"FLARE23" OR "FLARE 2023"', 'M11': '"AbdomenAtlas 3.0" OR "RadGPT"', 'M12': '"AMOS-MM"',
    'M13': '"SA-Med3D-140K"', 'M14': '"ULS23"', 'M15': '"3DLAND"', 'M16': '"DeepLesion" kidney', 'M17': '"M3D-Seg" OR "M3D-Cap" OR "M3D-VQA"',
    'G01': '"UCSF RMaC" OR "UCSF-RMaC"', 'G02': '"CPTAC-CCRCC"', 'G03': '"RCC-AID"', 'H01': '"Open Kidney Ultrasound"', 'H03': '"KiPA22" OR "KiPA"',
    'H04': '"KPIs 2024" glomerular', 'H05': '"AbdomenCT-1K"', 'H06': '"RAOS" abdominal organ segmentation', 'H07': '"BTCV" multi-organ',
    'H09': 'NEPTUNE "whole slide" deep learning kidney', 'H10': '"Merlin" abdominal CT dataset', 'H11': '"RadImageNet-VQA"',
}
DATASET_NOTES = {
    'M01': 'Most papers citing TotalSegmentator run the released **model** on their own scans. That is not use of the dataset. Rows marked `check_model_vs_dataset_use` look (by a text heuristic) like runs of the model; they are sorted last. The flag is a hint, not a verdict.',
    'M02': 'As with M01, citing papers usually run the model rather than train or test on the MRI dataset.',
    'K06-K08': 'The three TCGA renal slide projects share one candidate list. Record which project(s) each paper used when verifying.',
    'K09': 'Candidates cover TCIA radiology for TCGA-KIRC, -KIRP and -KICH. Radiogenomics studies use the images; genomics-only papers that cite the collection DOI do not.',
    'M16': 'DeepLesion is body-wide. Only papers that use or report the kidney lesions matter for this atlas.',
    'H07': 'BTCV has no indexed dataset paper. Candidates come from papers citing UNETR (WACV 2022) that name BTCV/Synapse, plus Europe PMC. TransUNet citations were not harvested.',
    'H03': 'Includes citations of the two papers the KiPA22 organizers ask users to cite (He et al., MedIA 2020 and 2021).',
    'K03': 'KiTS23 has no challenge report yet. Candidates come from sentences naming KiTS23 in papers citing the KiTS19/KiTS21 reports, plus Europe PMC.',
    'M09': 'The FLARE22 summary paper is in The Lancet Digital Health (2024; arXiv:2308.05862).',
    'M06': 'The WORD paper is not indexed by Semantic Scholar, so there are no citing sentences. Candidates come from OpenAlex abstracts and Europe PMC; use the OpenAlex and Google Scholar links for the full list.',
    'K04': 'The dataset paper is not indexed by Semantic Scholar and OpenAlex records no citations. Check Google Scholar.',
    'M14': 'Includes the 34 Semantic Scholar citations of the ULS23 challenge paper. Only papers using its kidney-lesion or KiTS21-derived component matter here.',
    'M13': 'The SAM-Med3D paper introduces both a model and the SA-Med3D-140K data. Only sentences naming the data are kept; many papers only compare against the SAM-Med3D model.',
    'M17': 'The M3D paper introduces both a model (M3D-LaMed) and the M3D-Data sets. Only sentences naming the data components are kept.',
    'H10': 'Merlin is both a model and a dataset. Only sentences naming the dataset are kept; most citing papers use the model.',
    'M11': 'RadGPT/AbdomenAtlas 3.0 is both a report-generation method and a dataset. Confirm that the data were used.',
    'M04': 'CHAOS kidney labels exist only in the MRI part. Papers using only CHAOS-CT (liver) are not kidney uses.',
    'G02': 'The anchor is the proteogenomic Cell paper, which is mostly cited for genomics. Only imaging/pathology users belong here; sentences without an imaging term were moved to tier C.',
    'H09': 'Citations of Jayapandian et al. Most use their own cohorts, not NEPTUNE data. Verify the data source.',
}
NAMES = {i: d['name'] for i, d in anchors.items()}
ORDER = list(anchors.keys())
TIER_TEXT = {
    'A': 'Strong: a citing sentence names the dataset and says the authors trained, tested, evaluated or used it',
    'B': 'Probable: named in the Methods (Europe PMC), cites the dataset DOI (DataCite), or a citing sentence describes the data',
    'C': 'Possible: cited in a methods context without naming the data, or named somewhere in the full text',
    'D': 'Citation only: kept for small datasets so no user is missed; usually background',
}


def s2_anchor_ids(ds):
    out = []
    for f in [LIT / 's2' / f'{ds}.json'] + [LIT / 's2' / f'{e}.json' for e, d in extra.items() if d['mergeInto'] == ds]:
        if f.exists():
            for a in read_json(f)['anchors']:
                if not a.get('missing'):
                    out.append((a['title'], a['paperId'], a.get('citationCount'), a.get('query')))
    return out


def md_escape(s):
    return (s or '').replace('|', '\\|').replace('\n', ' ')


# ---------- CSV ----------
def status(r):
    ids = {x.lower() for x in (r['doi'], r['arxiv']) if x}
    if r['doi'].lower().startswith('10.48550/arxiv.'): ids.add(r['doi'][15:].lower())
    if ids & set(VERIFIED.get(r['dataset'], [])): return 'verified: in research inventory 6.4'
    for i, why in EXCLUDED.get(r['dataset'], []):
        if i in ids: return 'checked and excluded: ' + why
    return ''

rows = []
for ds in ORDER:
    for r in cands.get(ds, {}).values():
        rows.append(r)
rank = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
rows.sort(key=lambda r: (ORDER.index(r['dataset']), r['tool_only'], rank[r['tier']], not r['influential'], -(r['year'] or 0), -(r['cites'] or 0)))
with open(OUT / 'paper-candidates.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(['status_2026_09_23', 'review_decision', 'dataset_id', 'dataset', 'evidence_tier', 'title', 'year', 'venue', 'link', 'doi', 'arxiv',
                'times_cited', 's2_influential_citation', 'check_model_vs_dataset_use', 'evidence_sentence', 'evidence_sources', 'cited_work',
                'semantic_scholar', 'role_if_used', 'train_test_role', 'method_used', 'evidence_locator', 'reviewer_notes'])
    for r in rows:
        w.writerow([status(r), '', r['dataset'], NAMES[r['dataset']], r['tier'], r['title'], r['year'] or '', r['venue'], r['link'], r['doi'], r['arxiv'],
                    r['cites'], 'yes' if r['influential'] else '', 'yes' if r['tool_only'] else '', (r['evidence'] or '')[:600],
                    '; '.join(r['sources']), '; '.join(r['anchors']),
                    ('https://www.semanticscholar.org/paper/' + r['s2']) if r['s2'] else '', '', '', '', '', ''])

# ---------- Markdown ----------
L = []
L.append('# Paper candidates for each dataset: review sheet\n')
L.append(f'**Generated:** {TODAY}. **Status: candidates.** Rows marked `verified` in the `status_2026_09_23` column were checked in full text and appear in section 6.4 of the research inventory; rows marked `checked and excluded` were rejected with a reason. Every other row is unverified. '
         'None of it may be imported into `src/data/study-uses/` until a reviewer has opened the paper and confirmed, in its methods, '
         'that the dataset was used, and recorded where.\n')
L.append('The full list is [`paper-candidates.csv`](paper-candidates.csv), one row per dataset–paper pair. It opens in Excel with filters. '
         'Fill in `review_decision` (`keep`, `reject` or `unsure`), and for kept rows `role_if_used`, `train_test_role`, `method_used` '
         'and `evidence_locator` (section, table or page). This page lists the citation pages for each dataset and its strongest candidates.\n')
L.append(ATTRIBUTION)
L.append('## How candidates were found\n')
L.append('1. **Semantic Scholar citations with citing sentences.** Every paper citing each dataset\'s descriptor or challenge paper was downloaded, '
         'including the sentence where the citation occurs and Semantic Scholar\'s citation-intent label. '
         'A sentence naming a specific edition (e.g. "KiTS23") is assigned to that edition, whichever paper it cites.')
L.append('2. **Europe PMC Methods-section search.** Open-access papers whose *Methods* name the dataset, plus a whole-text search as weaker evidence.')
L.append('3. **DataCite.** Papers that cite the dataset DOI itself (TCIA, Zenodo, Mendeley, Figshare).')
L.append('4. **Semantic Scholar keyword search** for datasets without a paper.\n')
L.append('### Evidence tiers\n')
L.append('| Tier | Meaning |\n|---|---|')
for t, s in TIER_TEXT.items():
    L.append(f'| **{t}** | {s} |')
L.append('\nTiers only set the order of review; they are not verification. Automatic text matching makes mistakes both ways: '
         'a survey can describe a dataset in words that look like use, and a real user may cite only a website. '
         'Coverage is also limited: papers not indexed by these services, and paywalled Methods sections, can be missed. '
         'Use the citation pages below for an exhaustive check.\n')
L.append('### How to verify a candidate\n')
L.append('- Open the paper and find the dataset in the **Methods / Experiments / Datasets** section. A reference-list entry or a mention in the introduction is not use.')
L.append('- Check it is **this release/edition** (KiTS19 vs KiTS21 vs KiTS23; FLARE21 vs 22 vs 23; TotalSegmentator dataset vs the TotalSegmentator model).')
L.append('- Record the role: training, validation, test, external validation, or challenge entry. Also record the method or model, and the locator (section, table or figure).')
L.append('- The dataset\'s own descriptor or challenge paper is already in the research inventory. It is a benchmark relationship, not downstream use.\n')

L.append('## Summary\n')
L.append('| ID | Dataset | Strong (A) | Probable (B) | Possible (C) | Citation only (D) | Total |\n|---|---|---:|---:|---:|---:|---:|')
for ds in ORDER:
    c = collections.Counter(r['tier'] for r in cands.get(ds, {}).values())
    L.append(f"| {ds} | {NAMES[ds]} | {c['A']} | {c['B']} | {c['C']} | {c['D']} | {sum(c.values())} |")
L.append('\n*H08 (3D U-Net Xenopus microscopy) is not included: the method paper has over 10,000 citations and no dataset release was found.*\n')

L.append('## Per-dataset citation pages and top candidates\n')
for ds in ORDER:
    L.append(f'### {ds} — {NAMES[ds]}\n')
    if ds in DATASET_NOTES: L.append(f'> {DATASET_NOTES[ds]}\n')
    L.append('**Where to find every paper that cites or uses it:**\n')
    s2 = s2_anchor_ids(ds)
    for title, pid, n, q in s2:
        L.append(f'- Semantic Scholar citations of *{md_escape(title)}* ({n} citing works; filter by "Methods" intent): '
                 f'<https://www.semanticscholar.org/paper/{pid}>')
    for a in anchors[ds]['anchors'] + [x for e, d in extra.items() if d['mergeInto'] == ds for x in d['anchors']]:
        w = oa.get(a)
        if w and w.get('id'):
            wid = w['id'].rsplit('/', 1)[-1]
            L.append(f"- OpenAlex works citing *{md_escape(w['display_name'])}* ({w['cited_by_count']}): <https://openalex.org/works?filter=cites:{wid}>")
    for d in DATA_DOIS.get(ds, []):
        L.append(f'- DataCite Commons, works citing the dataset DOI `{d}`: <https://commons.datacite.org/doi.org/{d}>')
    q = SCHOLAR_NAME.get(ds)
    if q:
        L.append(f'- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q={urllib.parse.quote(q)}>')
    ep = anchors[ds]['epmc']
    L.append(f'- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query={urllib.parse.quote("METHODS:(" + ep + ")")}>')
    for label, url in HOST.get(ds, []):
        L.append(f'- {label}: <{url}>')
    top = [r for r in rows if r['dataset'] == ds and r['tier'] in ('A', 'B')][:12]
    L.append('')
    if not top:
        L.append('_No strong or probable candidates were found automatically. Use the citation pages above._\n')
        continue
    L.append('| Tier | Paper | Year | Evidence |\n|---|---|---|---|')
    for r in top:
        ev = r['evidence'] or '; '.join(r['sources'])
        ev = md_escape(ev)[:260] + ('…' if len(ev) > 260 else '')
        flag = ' (model use?)' if r['tool_only'] else ''
        L.append(f"| {r['tier']}{flag} | [{md_escape(r['title'])}]({r['link']}) | {r['year'] or ''} | {ev} |")
    more = sum(1 for r in rows if r['dataset'] == ds) - len(top)
    if more > 0: L.append(f'\n{more} more candidate(s) in the CSV.\n')
    else: L.append('')

(OUT / 'paper-candidates.md').write_text('\n'.join(L) + '\n', encoding='utf-8', newline='\n')
print('rows', len(rows))
