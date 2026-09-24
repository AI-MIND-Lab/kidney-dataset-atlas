"""Step 5: turn the harvested citations into ranked dataset-paper candidates.

Reads the caches written by steps 1-4 and writes .research-cache/literature/candidates.json. Tiers only order the
review; they are not verification. See docs/literature/paper-candidates.md for what each tier means.
"""
import collections
import re
from pathlib import Path

import _setup  # noqa: F401
from common import CACHE, read_json, write_json

LIT = CACHE / 'literature'
entries = read_json(Path(__file__).with_name('anchors.json'))['datasets']
A = {d['id']: d for d in entries}
MERGE = {d['id']: d['mergeInto'] for d in entries if d.get('mergeInto')}

Y = r"\s?-?[’']?(?:20)?"
# A sentence naming a specific edition is assigned to that edition, whichever paper it cites.
EDITION = [('K03', r'KiTS' + Y + '23'), ('K02', r'KiTS' + Y + '21'), ('K01', r'KiTS' + Y + '19|C4KC'),
           ('M10', r'FLARE' + Y + '23'), ('M09', r'FLARE' + Y + '22'), ('M08', r'FLARE' + Y + '21'),
           ('M11', r'AbdomenAtlas\s?3|RadGPT'), ('M12', r'AMOS-MM')]
FAMILY = {'K01': 'KITS', 'K02': 'KITS', 'K03': 'KITS', 'M08': 'FLARE', 'M09': 'FLARE', 'M10': 'FLARE',
          'M07': 'ATLAS', 'M11': 'ATLAS', 'M03': 'AMOS', 'M12': 'AMOS'}
STRONG = re.compile(
    r"\b(we|our)\b[^.]{0,120}\b(train|trained|training|evaluat|test|tested|validat|experiment|use[ds]?|using|employ|adopt|fine-?tun|pre-?train|benchmark|select|collect|conduct)"
    r"|\b(experiments?|evaluat\w*|train\w*|test\w*|validat\w*|fine-?tun\w*|pre-?train\w*)\b[^.]{0,40}\b(on|using|with)\b[^.]{0,60}(dataset|data|challenge|benchmark|cases|scans|images)"
    r"|all (of )?(the )?(data|images|cases|experiments)[^.]{0,60}(from|on)"
    r"|(dataset|data)s? (used|employed|adopted) (in|for) (this|our)"
    r"|in this (study|work|paper)[^.]{0,80}(dataset|data)", re.I)
LIKELY = re.compile(
    r"\b(consist|compris|contain|composed of|includ)\w*\b[^.]{0,80}\b(\d[\d,]*)\s*(cases|scans|patients|volumes|images|subjects|CT|WSIs|slides)"
    r"|\b(train|trained|training|evaluat\w*|test\w*|validat\w*|experiment\w*|benchmark\w*|fine-?tun\w*|pre-?train\w*)\b"
    r"|\b(dataset|datasets)\b[^.]{0,30}\b(is|was|are|were)\b[^.]{0,20}(used|adopted|employed|utilized)"
    r"|(obtained|downloaded|collected|acquired|sourced|derived) from", re.I)
# Anchors whose sentences must mention imaging to count (their anchor papers are mostly cited for genomics or methods).
IMAGING_REQ = {'G02', 'K06-K08', 'K09', 'H09'}
IMAGING_WORDS = re.compile(r'whole[- ]slide|\bWSIs?\b|\bslides?\b|histolog|histopatholog|patholog|\bH&E\b|\bCT\b|computed tomograph|radiolog|radiomic|\bMRI?\b|imag', re.I)
# Anchors that are method or model papers: citing them is not evidence of using the data.
METHOD_ANCHORS = {'H07b', 'K06-K08', 'H09', 'G02', 'K09', 'M13', 'M17', 'H10', 'M11'}
# Datasets with few citations, where even weak candidates are kept so no user is missed.
SMALL = {'K04', 'K13', 'G01', 'G03', 'H01', 'H04', 'H06', 'M15', 'H11', 'M14', 'M13', 'M17', 'M11', 'H03', 'K10', 'K11-K12'}
# Common-word names, for which full-text matches are unreliable.
AMBIGUOUS = {'K13', 'M06', 'H06', 'H10'}
OWN_DESCRIPTORS = {'10.1038/s41597-025-04467-1'}  # TRUSTED's data paper
TIER_RANK = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
# Title/abstract patterns for OpenAlex citing works, and extra words some datasets require.
ABS = {
    'K01': r'KiTS\s?-?(20)?19|C4KC', 'K02': r'KiTS\s?-?(20)?21', 'K03': r'KiTS\s?-?(20)?23', 'K05': r'CT KIDNEY DATASET|Normal-Cyst-Tumou?r|12,?446',
    'K06-K08': r'(TCGA[^.]{0,40}(KIRC|KIRP|KICH|renal|kidney))[^.]*|(KIRC|KIRP|KICH)[^.]*TCGA', 'K09': r'TCGA-KIRC|TCIA[^.]{0,80}(renal|kidney)',
    'K10': r'Hacking the Kidney|HuBMAP', 'K11-K12': r'Hacking the Human Body|HuBMAP|Human Protein Atlas', 'K13': r'\bTRUSTED\b',
    'M01': r'TotalSegmentator (dataset|data\b|training)', 'M02': r'TotalSegmentator MRI (dataset|data\b)', 'M03': r'\bAMOS', 'M04': r'\bCHAOS\b',
    'M05': r'CT-?ORG', 'M06': r'\bWORD\b', 'M07': r'AbdomenAtlas', 'M08': r'FLARE\s?-?(20)?21|FLARE challenge', 'M09': r'FLARE\s?-?(20)?22',
    'M13': r'SA-Med3D|SAM-Med3D', 'M14': r'ULS23', 'M16': r'DeepLesion', 'M17': r'M3D-(Cap|VQA|Seg|RefSeg|Data)', 'G02': r'CPTAC',
    'H03b': r'KiPA', 'H05': r'AbdomenCT-?1K', 'H07': r'BTCV|Beyond the Cranial Vault', 'H07b': r'BTCV|Beyond the Cranial Vault|Synapse multi-organ',
    'H09': r'NEPTUNE', 'H10': r'Merlin',
}
EXTRA_REQ = {'K06-K08': r'slide|histolog|histopatholog|patholog', 'G02': r'image|slide|histolog|radiom|CT\b|patholog', 'M16': r'kidney|renal',
             'H09': r'slide|histolog|segment'}


def key(p):
    e = p.get('externalIds') or {}
    if e.get('DOI'):
        return 'doi:' + e['DOI'].lower()
    if e.get('ArXiv'):
        return 'arxiv:' + e['ArXiv']
    return 'title:' + re.sub(r'\W+', ' ', (p.get('title') or '').lower()).strip()


def link(p):
    e = p.get('externalIds') or {}
    if e.get('DOI'):
        return 'https://doi.org/' + e['DOI']
    if e.get('ArXiv'):
        return 'https://arxiv.org/abs/' + e['ArXiv']
    return p.get('url') or ('https://www.semanticscholar.org/paper/' + p['paperId'] if p.get('paperId') else '')


cands = collections.defaultdict(dict)


def add(ds, p, tier, evidence, source, anchor):
    k = key(p)
    r = cands[ds].get(k)
    if r is None:
        r = cands[ds][k] = {
            'dataset': ds, 'title': ' '.join((p.get('title') or '').split()), 'year': p.get('year'),
            'venue': p.get('venue') or (p.get('journal') or {}).get('name') or '', 'link': link(p),
            'doi': (p.get('externalIds') or {}).get('DOI', ''), 'arxiv': (p.get('externalIds') or {}).get('ArXiv', ''),
            's2': p.get('paperId') or '', 'cites': p.get('citationCount') or 0, 'tier': tier, 'evidence': evidence,
            'sources': {source}, 'anchors': {anchor}, 'influential': False, 'tool_only': False}
    else:
        r['sources'].add(source)
        r['anchors'].add(anchor)
        if r['link'].startswith('https://europepmc') and not link(p).startswith('https://europepmc'):
            r['link'] = link(p)
        if not r['s2'] and p.get('paperId'):
            r['s2'] = p['paperId']
        r['cites'] = max(r['cites'], p.get('citationCount') or 0)
        if TIER_RANK[tier] < TIER_RANK[r['tier']]:
            r['tier'], r['evidence'] = tier, evidence or r['evidence']
        elif not r['evidence'] and evidence:
            r['evidence'] = evidence
    return r


def totalsegmentator_tool_use(best):
    """True when a TotalSegmentator sentence looks like running the model rather than using the dataset."""
    data_use = re.search(r'TotalSegmentator\W+(MRI\W+|CT\W+)?(dataset|data\b|data set|training data|cases|volumes|scans|subset|images|annotations)'
                         r'|\(\d[\d,]* (cases|scans|volumes|images)\)|\d+ from TotalSegmentator|from the TotalSegmentator(?!\W+(toolkit|tool|model|software))'
                         r'|TotalSegmentator\W*\[\d+\][^.]{0,40}\b\d{2,4} (cases|scans|volumes|CT)', best, re.I)
    tool_use = re.search(r'(using|with|by|via|of|from|run|ran|applied) (the )?(pretrained |pre-trained |publicly available )?TotalSegmentator'
                         r'|TotalSegmentator\W*(\[\d+\]\W*)?(tool|model|software|toolkit|network|framework|was used to|to segment|to generate|to obtain|segment|predict|generat)',
                         best, re.I)
    if data_use and not re.search(r'TotalSegmentator\W+(toolkit|tool|model|software)', best, re.I):
        return False
    if tool_use or not STRONG.search(best):
        return True
    return None  # inconclusive: keep whatever an earlier sentence decided


kwre = {i: re.compile('|'.join(re.escape(k) for k in d['kw']), re.I) for i, d in A.items()}

# Semantic Scholar citations with citing sentences.
for f in sorted((LIT / 's2').glob('*.json')):
    rec = read_json(f)
    ds0 = MERGE.get(rec['id'], rec['id'])
    kw0 = kwre[rec['id']]
    for anchor in rec['anchors']:
        if anchor.get('missing'):
            continue
        for c in anchor['citations']:
            p = c['citingPaper']
            if not p or not p.get('title'):
                continue
            ctxs, intents = c.get('contexts') or [], c.get('intents') or []
            targets = collections.defaultdict(list)
            for s in ctxs:
                hit = next((ds for ds, rx in EDITION if re.search(rx, s, re.I) and FAMILY.get(ds) == FAMILY.get(ds0, 'x')), None)
                targets[hit or ds0].append(s)
            if not ctxs:
                targets[ds0] = []
            for ds, sentences in targets.items():
                best, tier = None, 'D'
                for s in sentences:
                    named = bool(kw0.search(s)) or ds != ds0
                    t = 'A' if STRONG.search(s) and named else 'B' if LIKELY.search(s) and named else 'C'
                    if rec['id'] in IMAGING_REQ and t in ('A', 'B') and not IMAGING_WORDS.search(s):
                        t = 'C'
                    if best is None or TIER_RANK[t] < TIER_RANK[tier]:
                        tier, best = t, s
                if not sentences:
                    tier = 'C' if 'methodology' in intents else 'D'
                if rec['id'] in METHOD_ANCHORS and tier in ('C', 'D'):
                    continue
                if tier == 'D' and not c.get('isInfluential') and ds0 not in SMALL:
                    continue
                if tier == 'C' and not ('methodology' in intents or c.get('isInfluential')) and ds0 not in SMALL:
                    continue
                r = add(ds, p, tier, best or '', 'S2 citation sentence' if sentences else 'S2 citation (no sentence available)',
                        anchor['title'][:70])
                r['influential'] |= bool(c.get('isInfluential'))
                if ds in ('M01', 'M02') and best and 'totalsegmentator' in best.lower():
                    verdict = totalsegmentator_tool_use(best)
                    if verdict is not None:
                        r['tool_only'] = verdict
    for p in rec.get('search', []):
        if kw0.search((p.get('title') or '') + ' ' + (p.get('abstract') or '')):
            add(ds0, p, 'B', ('Title/abstract: ' + (p.get('abstract') or p.get('title') or ''))[:400],
                'S2 search: title/abstract names dataset', 'search')

# Europe PMC: named in the Methods section (tier B) or anywhere in the full text (tier C).
for folder, source, tier in (('epmc_methods', 'Europe PMC: named in Methods', 'B'), ('epmc_fulltext', 'Europe PMC: named in full text', 'C')):
    for f in sorted((LIT / folder).glob('*.json')):
        ds = MERGE.get(f.stem, f.stem)
        for x in read_json(f)['results']:
            if ds == 'G01' and 'RMaC' not in (x.get('title') or '') and folder == 'epmc_fulltext':
                continue
            p = {'title': x.get('title'), 'year': int(x['pubYear']) if x.get('pubYear') else None, 'venue': x.get('journalTitle') or '',
                 'externalIds': {'DOI': x['doi']} if x.get('doi') else {}, 'citationCount': x.get('citedByCount') or 0,
                 'url': 'https://europepmc.org/article/' + x.get('source', 'MED') + '/' + str(x.get('id'))}
            add(ds, p, 'C' if ds in AMBIGUOUS else tier, '', source + (' (ambiguous name)' if ds in AMBIGUOUS else ''), 'Europe PMC search')

# DataCite: works that cite the dataset DOI itself.
datacite = LIT / 'datacite_citing.json'
for ds, groups in (read_json(datacite).items() if datacite.exists() else []):
    for g in groups:
        for x in g['citing']:
            # A dataset's own descriptor citing its own data DOI is not a use.
            if not x.get('title') or x['doi'].lower() in OWN_DESCRIPTORS:
                continue
            p = {'title': x['title'], 'year': x.get('year'), 'venue': x.get('venue') or '', 'externalIds': {'DOI': x['doi']},
                 'citationCount': x.get('cites') or 0}
            add(ds, p, 'B', f"Cites the dataset DOI {g['dataset_doi']} (DataCite)", 'DataCite: cites dataset DOI', g['dataset_doi'])

# OpenAlex: citing works whose title or abstract names the dataset.
for f in sorted((LIT / 'openalex').glob('*.json')):
    src_id = f.stem
    ds = MERGE.get(src_id, src_id)
    rx = ABS.get(src_id)
    for x in read_json(f):
        text = (x.get('title') or '') + '. ' + (x.get('abstract') or '')
        p = {'title': x.get('title'), 'year': x.get('year'), 'venue': x.get('venue') or '',
             'externalIds': {'DOI': x['doi']} if x.get('doi') else {}, 'citationCount': x.get('cites') or 0, 'url': x['id']}
        m = re.search(rx, text, re.I) if rx else None
        if m and (src_id not in EXTRA_REQ or re.search(EXTRA_REQ[src_id], text, re.I)):
            sentence = next((s for s in re.split(r'(?<=[.!?])\s+', text) if re.search(rx, s, re.I)), m.group(0))
            target = next((eds for eds, erx in EDITION if re.search(erx, sentence, re.I) and FAMILY.get(eds) == FAMILY.get(ds, 'x')), ds)
            add(target, p, 'B', 'Abstract/title: ' + sentence[:400], 'OpenAlex: citing work names dataset in title/abstract', x['anchor'])
        elif ds in SMALL and src_id not in METHOD_ANCHORS:
            add(ds, p, 'D', '', 'OpenAlex: citing work (no dataset mention in abstract)', x['anchor'])

write_json(LIT / 'candidates.json', {ds: {k: {**v, 'sources': sorted(v['sources']), 'anchors': sorted(v['anchors'])} for k, v in m.items()}
                                     for ds, m in cands.items()})
for ds in sorted(cands):
    print(ds, dict(sorted(collections.Counter(v['tier'] for v in cands[ds].values()).items())))
