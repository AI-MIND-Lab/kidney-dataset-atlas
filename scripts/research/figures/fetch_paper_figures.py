"""Download architecture figures from openly licensed papers into public/figures/<paper id>/ as WebP.

Only papers whose licence permits reuse are listed (see REUSABLE_FIGURE_LICENSES in src/lib/schemas.mjs). For each
DOI, the Crossref licence is checked before anything is saved; an arXiv figure must name the licence shown on its
abstract page. The paper record then quotes the caption and carries the credit line; the validator refuses a
reproduced figure under any other licence.

Pass paper ids to fetch only those papers' figures (python fetch_paper_figures.py deeptumorvqa-2026); with no
arguments every figure is fetched.

Requires: pip install -r scripts/research/requirements.txt (pypdf only for figures taken from a PDF)
"""
import io
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import REPO, get, get_json  # noqa: E402

CC_BY = ('creativecommons.org/licenses/by/4.0', 'creativecommons.org/licenses/by/3.0')

# (paper id, figure file name, DOI or None, how to get the image)
FIGURES = [
    ('uhm-2021', 'figure-1', '10.1038/s41698-021-00195-y',
     ('url', 'https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41698-021-00195-y/MediaObjects/41698_2021_195_Fig1_HTML.png')),
    ('wessels-2022', 'figure-1', '10.1371/journal.pone.0272656',
     ('url', 'https://journals.plos.org/plosone/article/figure/image?size=large&id=10.1371/journal.pone.0272656.g001')),
    ('jasti-2025', 'figure-1', '10.1038/s41467-025-57717-6',
     ('url', 'https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41467-025-57717-6/MediaObjects/41467_2025_57717_Fig1_HTML.png')),
    ('tabibu-2019', 'figure-1', '10.1038/s41598-019-46718-3',
     ('url', 'https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41598-019-46718-3/MediaObjects/41598_2019_46718_Fig1_HTML.png')),
    # arXiv:2106.00908 is CC BY 4.0 on its abstract page; Figure 3 is the raster image on page 5 of the PDF.
    ('transmil-2021', 'figure-3', None, ('pdf', 'https://arxiv.org/pdf/2106.00908', 5, 'Im3.png')),
    # arXiv:2310.04110 is CC BY 4.0 on its abstract page; Fig. 2 is the raster image on page 4.
    ('kits23-auto3dseg', 'figure-2', None, ('pdf', 'https://arxiv.org/pdf/2310.04110', 4, 'Im2.png')),
    # arXiv:2605.09679 is CC BY 4.0 on its abstract page; Figure 1 is a vector drawing in the PDF, so the PNG from
    # arXiv's HTML version of the paper is used.
    ('deeptumorvqa-2026', 'figure-1', None, ('url', 'https://arxiv.org/html/2605.09679v1/task_demonstration.png')),
]


def licence_ok(doi):
    record = get_json(f'https://api.crossref.org/works/{doi}') or {}
    urls = [entry.get('URL', '') for entry in record.get('message', {}).get('license', [])]
    return any(any(cc in url for cc in CC_BY) for url in urls)


ONLY = set(sys.argv[1:])
for paper, name, doi, (kind, url, *rest) in FIGURES:
    if ONLY and paper not in ONLY:
        continue
    if doi and not licence_ok(doi):
        print(f'SKIP {paper}: Crossref does not list a CC BY licence for {doi}')
        continue
    data = get(url, binary=True, tries=3)
    if data is None:
        print(f'FAIL {paper}: could not download {url}')
        continue
    if kind == 'pdf':
        import pypdf
        page, image_name = rest
        image = next(im.image for im in pypdf.PdfReader(io.BytesIO(data)).pages[page - 1].images if im.name == image_name)
    else:
        image = Image.open(io.BytesIO(data))
    image = image.convert('RGB')
    out = REPO / 'public' / 'figures' / paper / f'{name}.webp'
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out, 'WEBP', quality=90, method=6)
    print(f'{paper}/{name}.webp  {image.width} x {image.height}  {out.stat().st_size / 1e3:.0f} kB')
