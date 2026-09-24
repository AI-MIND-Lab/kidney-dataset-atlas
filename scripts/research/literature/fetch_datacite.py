"""Step 4: list works that cite each dataset DOI (TCIA, Zenodo, Mendeley, Figshare) through DataCite.

The dataset DOIs are the dataDois field of each entry in anchors.json. DataCite metadata is CC0; titles come from
Crossref, or from DataCite when Crossref has none. Output: .research-cache/literature/datacite_citing.json.
"""
import time
from pathlib import Path

import _setup  # noqa: F401
from common import cache_dir, get_json, read_json, write_json

out = {}
for d in read_json(Path(__file__).with_name('anchors.json'))['datasets']:
    for doi in d.get('dataDois', []):
        record = get_json(f'https://api.datacite.org/dois/{doi}')
        citing = [x['id'] for x in (record or {}).get('data', {}).get('relationships', {}).get('citations', {}).get('data', [])]
        rows = []
        for cited_by in citing:
            meta = get_json(f'https://api.crossref.org/works/{cited_by}')
            if meta:
                m = meta['message']
                rows.append({'doi': cited_by, 'title': (m.get('title') or [''])[0],
                             'year': (m.get('published') or m.get('issued'))['date-parts'][0][0],
                             'venue': (m.get('container-title') or [''])[0], 'cites': m.get('is-referenced-by-count', 0)})
            else:
                dc = get_json(f'https://api.datacite.org/dois/{cited_by}')
                a = (dc or {}).get('data', {}).get('attributes', {})
                rows.append({'doi': cited_by, 'title': (a.get('titles') or [{}])[0].get('title', ''), 'year': a.get('publicationYear'),
                             'venue': a.get('publisher') if isinstance(a.get('publisher'), str) else '', 'cites': 0})
            time.sleep(0.1)
        out.setdefault(d['id'], []).append({'dataset_doi': doi, 'citing': rows})
        print(d['id'], doi, len(rows), flush=True)
write_json(cache_dir('literature') / 'datacite_citing.json', out)
print('done')
