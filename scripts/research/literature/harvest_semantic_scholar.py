"""Step 1: download every paper citing each dataset's anchor papers, with citing sentences and intents.

Semantic Scholar's shared rate limit is slow without an API key; expect hours for the full list. Datasets already
harvested are skipped, so the script can be stopped and restarted. Output: .research-cache/literature/s2/.
Data from Semantic Scholar is subject to its API License Agreement; see docs/literature/paper-candidates.md.
"""
import time
import urllib.parse
from pathlib import Path

import _setup  # noqa: F401
from common import cache_dir, get_json, read_json, write_json

S2 = 'https://api.semanticscholar.org/graph/v1'
FIELDS = 'title,year,venue,externalIds,citationCount,url,publicationTypes,journal'
MAX_CITES = 3000
out_dir = cache_dir('literature', 's2')

for d in read_json(Path(__file__).with_name('anchors.json'))['datasets']:
    out = out_dir / f"{d['id']}.json"
    if out.exists():
        continue
    rec = {'id': d['id'], 'anchors': [], 'search': []}
    for anchor in d['anchors']:
        paper = get_json(f'{S2}/paper/{anchor}?fields=paperId,title,year,citationCount,influentialCitationCount,url,externalIds', tries=12)
        time.sleep(1.2)
        if not paper:
            rec['anchors'].append({'query': anchor, 'missing': True})
            print(d['id'], anchor, 'NOT FOUND', flush=True)
            continue
        cites, offset = [], 0
        while offset < min(paper['citationCount'] or 0, MAX_CITES) + 1:
            page = get_json(f"{S2}/paper/{paper['paperId']}/citations?fields=contexts,intents,isInfluential,{FIELDS}"
                            f'&limit=500&offset={offset}', tries=12)
            time.sleep(1.2)
            if not page or not page.get('data'):
                break
            cites += page['data']
            if 'next' not in page:
                break
            offset = page['next']
        paper['citations'], paper['query'] = cites, anchor
        rec['anchors'].append(paper)
        print(d['id'], anchor, '|', paper['title'][:60], '| citations', paper['citationCount'], 'fetched', len(cites), flush=True)
    if d.get('s2search'):
        found = get_json(f"{S2}/paper/search?query={urllib.parse.quote(d['s2search'])}&limit=40&fields={FIELDS},abstract", tries=12)
        time.sleep(1.2)
        rec['search'] = (found or {}).get('data', [])
    write_json(out, rec)
print('done')
