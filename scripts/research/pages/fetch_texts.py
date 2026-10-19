"""Save the text of every source a page quotes, so build_page.py can cut its quotes from it.

    python scripts/research/pages/fetch_texts.py docs/contributions/<name>/<page>.yaml [--refresh]

For each entry under `texts:` in the page config, this downloads the page or PDF and writes its plain text to
.research-cache/pages/texts/<key>.txt (git ignores the cache: these are third-party texts). The URL is the entry's
`url`, or else the URL of its atlas source record. A PDF is read with pypdf.

When a source cannot be downloaded (a login, a refused request), save it yourself as
.research-cache/pages/files/<key>.pdf, .html or .txt and run this again: a file there is used instead of the URL.
Existing texts are kept unless you pass --refresh.
"""
import argparse
import glob
import html
import io
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import CACHE, REPO, get  # noqa: E402

TEXTS = CACHE / 'pages' / 'texts'
FILES = CACHE / 'pages' / 'files'


def html_to_text(raw):
    raw = re.sub(r'(?is)<(script|style|noscript|svg)\b.*?</\1>', ' ', raw)
    raw = re.sub(r'(?s)<!--.*?-->', ' ', raw)
    raw = re.sub(r'(?s)<[^>]+>', ' ', raw)
    return re.sub(r'\s+', ' ', html.unescape(raw)).strip()


def pdf_to_text(data):
    from pypdf import PdfReader
    return '\n'.join(page.extract_text() or '' for page in PdfReader(io.BytesIO(data)).pages)


def text_of(data, kind):
    if kind == 'pdf' or data[:5] == b'%PDF-':
        return pdf_to_text(data)
    raw = data.decode('utf8', 'ignore')
    return raw if kind == 'txt' else html_to_text(raw)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('config')
    ap.add_argument('--refresh', action='store_true', help='download again even if a text is saved')
    args = ap.parse_args()
    cfg = yaml.safe_load(Path(args.config).read_text(encoding='utf8'))
    sources = {s['id']: s for f in glob.glob(str(REPO / 'src/data/sources/*.json')) for s in json.loads(Path(f).read_text(encoding='utf-8-sig'))}
    TEXTS.mkdir(parents=True, exist_ok=True)
    failed = []
    for key, entry in (cfg.get('texts') or {}).items():
        out = TEXTS / f'{key}.txt'
        if out.exists() and not args.refresh:
            print(f'kept      {key}')
            continue
        manual = next((p for p in (FILES / f'{key}.{ext}' for ext in ('pdf', 'html', 'txt')) if p.exists()), None)
        if manual:
            data, kind, where = manual.read_bytes(), manual.suffix[1:], str(manual)
        else:
            url = entry.get('url') or (sources.get(entry.get('source')) or {}).get('url')
            if not url:
                failed.append((key, 'no url and no atlas source record'))
                continue
            data = get(url, binary=True)
            kind, where = ('pdf' if entry.get('pdf') else None), url
            if not data:
                failed.append((key, f'download refused or missing: {url}'))
                continue
        text = text_of(data, kind)
        if len(text) < 200:
            failed.append((key, f'almost no text extracted from {where}'))
            continue
        out.write_text(text, encoding='utf8')
        print(f'saved     {key}  ({len(text):,} characters from {where})')
    for key, why in failed:
        print(f'MISSING   {key}: {why}. Save it as {FILES / key}.pdf, .html or .txt and run again.')
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
