"""Step 3: resolve each anchor paper in OpenAlex and download its citing works with their abstracts.

OpenAlex data is CC0. Output: .research-cache/literature/openalex_ids.json and openalex/<dataset>.json.
"""
import time
import urllib.parse
from pathlib import Path

import _setup  # noqa: F401
from common import cache_dir, get_json, read_json, write_json

API = 'https://api.openalex.org/works'
datasets = read_json(Path(__file__).with_name('anchors.json'))['datasets']
ids_file = cache_dir('literature') / 'openalex_ids.json'
ids = read_json(ids_file) if ids_file.exists() else {}


def resolve(anchor):
    if anchor in ids:
        return ids[anchor]
    work = None
    if anchor.startswith('DOI:'):
        work = get_json(f'{API}/doi:{anchor[4:]}?select=id,display_name,cited_by_count,publication_year')
    elif anchor.startswith('ARXIV:'):
        for flt in (f'locations.landing_page_url:https://arxiv.org/abs/{anchor[6:]}', f'doi:10.48550/arxiv.{anchor[6:]}'):
            found = get_json(f'{API}?filter={flt}&select=id,display_name,cited_by_count,publication_year')
            if found and found.get('results'):
                work = found['results'][0]
                break
    ids[anchor] = work
    return work


def abstract(inverted):
    if not inverted:
        return ''
    pos = {i: word for word, idx in inverted.items() for i in idx}
    return ' '.join(pos[i] for i in sorted(pos))


for d in datasets:
    out = cache_dir('literature', 'openalex') / f"{d['id']}.json"
    if out.exists():
        continue
    works = []
    for anchor in d['anchors']:
        work = resolve(anchor)
        if not work:
            continue
        wid, cursor = work['id'].rsplit('/', 1)[-1], '*'
        while cursor and len(works) < 4000:
            page = get_json(f'{API}?filter=cites:{wid}&per-page=200&cursor={urllib.parse.quote(cursor)}'
                            '&select=id,doi,display_name,publication_year,cited_by_count,primary_location,abstract_inverted_index,type')
            if not page:
                break
            for w in page['results']:
                source = (w.get('primary_location') or {}).get('source') or {}
                works.append({'id': w['id'], 'doi': (w.get('doi') or '').replace('https://doi.org/', ''), 'title': w.get('display_name'),
                              'year': w.get('publication_year'), 'cites': w.get('cited_by_count'), 'venue': source.get('display_name') or '',
                              'type': w.get('type'), 'abstract': abstract(w.get('abstract_inverted_index')), 'anchor': anchor})
            cursor = page['meta'].get('next_cursor')
            time.sleep(0.12)
    write_json(out, works)
    print(d['id'], len(works), flush=True)
write_json(ids_file, ids)
print('done')
