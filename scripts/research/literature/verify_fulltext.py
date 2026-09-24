"""Step 7: fetch each paper in fulltext_checklist.py and show where its body names the dataset.

Full text comes from the arXiv PDF, Europe PMC, or an open-access copy found through Unpaywall (which needs
RESEARCH_CONTACT_EMAIL). The script only locates mentions; a person reads them and decides whether the paper
really trained, tested or benchmarked on the dataset. Output: .research-cache/literature/fulltext/ (one text file
per paper) and verify_results.json with up to four surrounding passages per paper.

Requires: pip install -r scripts/research/requirements.txt
"""
import io
import json
import re
import urllib.parse

import pypdf

import _setup  # noqa: F401
from common import CONTACT, cache_dir, get, write_json
from fulltext_checklist import V

TEXT_DIR = cache_dir('literature', 'fulltext')


def pdf_text(data):
    try:
        return '\n'.join((page.extract_text() or '') for page in pypdf.PdfReader(io.BytesIO(data)).pages)
    except Exception:
        return None


def fulltext(ident):
    name = re.sub(r'\W', '_', ident)
    text_file, source_file = TEXT_DIR / f'{name}.txt', TEXT_DIR / f'{name}.src'
    if text_file.exists():
        return text_file.read_text(encoding='utf8'), source_file.read_text(encoding='utf8')
    text, source = None, 'none'
    if ident.startswith('arxiv:'):
        data = get(f'https://arxiv.org/pdf/{ident[6:]}', binary=True, tries=4)
        if data and data[:4] == b'%PDF':
            text, source = pdf_text(data), f'arXiv PDF {ident[6:]}'
    else:
        doi = ident[4:]
        found = get(f'https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={urllib.parse.quote(f"DOI:{chr(34)}{doi}{chr(34)}")}'
                    '&format=json&resultType=lite', tries=4)
        results = json.loads(found)['resultList']['result'] if found else []
        pmcid = results[0].get('pmcid') if results else None
        if pmcid:
            xml = get(f'https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML', tries=4)
            if xml:
                text, source = re.sub(r'<[^>]+>', ' ', xml), f'Europe PMC {pmcid}'
        if not text and CONTACT:
            oa = get(f'https://api.unpaywall.org/v2/{urllib.parse.quote(doi)}?email={CONTACT}', tries=4)
            oa = json.loads(oa) if oa else {}
            locations = ([oa['best_oa_location']] if oa.get('best_oa_location') else []) + (oa.get('oa_locations') or [])
            for loc in locations:
                for field in ('url_for_pdf', 'url'):
                    link = loc.get(field)
                    data = get(link, binary=True, tries=2) if link else None
                    if not data:
                        continue
                    if data[:4] == b'%PDF':
                        text, source = pdf_text(data), f'open-access PDF {link}'
                    else:
                        page = data.decode('utf8', 'ignore')
                        if len(page) > 20000 and re.search(r'method|experiment', page, re.I):
                            text, source = re.sub(r'<[^>]+>', ' ', page), f'open-access HTML {link}'
                    if text:
                        break
                if text:
                    break
    text = ' '.join((text or '').split())
    text_file.write_text(text, encoding='utf8')
    source_file.write_text(source, encoding='utf8')
    return text, source


results = []
for ds, ident, pattern in V:
    text, source = fulltext(ident)
    refs = max(text.rfind('References'), text.rfind('REFERENCES'), text.rfind('Bibliography'))
    body = text[:refs] if refs > len(text) * 0.4 else text  # ignore mentions in the reference list
    hits = list(re.finditer(pattern, body, re.I))
    passages = []
    for m in hits:
        if not any(abs(m.start() - p) < 300 for p, _ in passages):
            passages.append((m.start(), body[max(0, m.start() - 220): m.end() + 220]))
        if len(passages) >= 4:
            break
    results.append({'ds': ds, 'id': ident, 'src': source, 'chars': len(text), 'body_hits': len(hits), 'ctx': [p for _, p in passages]})
    print(f'{ds:8} {ident:45} {source[:40]:40} chars={len(text):>7} hits={len(hits)}', flush=True)
write_json(cache_dir('literature') / 'verify_results.json', results)
