"""Step 2: find open-access papers that name each dataset, in their Methods section and anywhere in the text.

Output: .research-cache/literature/epmc_methods/ and epmc_fulltext/, one JSON file per dataset.
"""
import time
import urllib.parse
from pathlib import Path

import _setup  # noqa: F401
from common import cache_dir, get_json, read_json, write_json

API = 'https://www.ebi.ac.uk/europepmc/webservices/rest/search?format=json&resultType=lite&pageSize=1000'


def search(query, max_pages):
    results, cursor = [], '*'
    for _ in range(max_pages):
        page = get_json(f'{API}&cursorMark={urllib.parse.quote(cursor)}&query={urllib.parse.quote(query)}')
        if not page:
            break
        results += page.get('resultList', {}).get('result', [])
        nxt = page.get('nextCursorMark')
        if not nxt or nxt == cursor or len(results) >= page.get('hitCount', 0):
            break
        cursor = nxt
        time.sleep(0.2)
    return results


for d in read_json(Path(__file__).with_name('anchors.json'))['datasets']:
    if d.get('mergeInto'):
        continue
    for folder, query, pages in (('epmc_methods', f"METHODS:({d['epmc']})", 6), ('epmc_fulltext', f"({d['epmc']})", 4)):
        out = cache_dir('literature', folder) / f"{d['id']}.json"
        if out.exists():
            continue
        hits = search(query, pages)
        write_json(out, {'query': query, 'results': hits})
        print(d['id'], folder, len(hits), flush=True)
print('done')
