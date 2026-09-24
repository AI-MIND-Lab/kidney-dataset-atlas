"""Shared paths and polite HTTP helpers for the research scripts.

Downloaded data (API responses, full texts, provider files) goes in .research-cache/ at the repository root,
which git ignores: it can always be fetched again, and much of it belongs to third parties.
Set RESEARCH_CONTACT_EMAIL so that APIs which ask for a contact address (OpenAlex, Crossref, Unpaywall) can
reach you; it is sent only to those services.
"""
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
CACHE = REPO / '.research-cache'
CONTACT = os.environ.get('RESEARCH_CONTACT_EMAIL', '')
USER_AGENT = 'kidney-dataset-atlas-research' + (f' (mailto:{CONTACT})' if CONTACT else '')


def cache_dir(*parts):
    """A subdirectory of the cache, created on demand."""
    path = CACHE.joinpath(*parts)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get(url, binary=False, tries=6, retry_on=(429, 500, 502, 503, 504), accept=None):
    """GET with backoff. Returns bytes or text, or None when the resource is missing or refused."""
    headers = {'User-Agent': USER_AGENT}
    if accept:
        headers['Accept'] = accept
    for attempt in range(tries):
        try:
            body = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120).read()
            return body if binary else body.decode('utf8', 'ignore')
        except urllib.error.HTTPError as err:
            if err.code in retry_on:
                time.sleep(min(60, 3 * (attempt + 1)))
                continue
            return None
        except Exception:
            time.sleep(4 * (attempt + 1))
    return None


def get_json(url, **kw):
    text = get(url, **kw)
    return json.loads(text) if text else None


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf8'))


def write_json(path, data, tabs=False):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent='\t' if tabs else None)
    Path(path).write_text(text + '\n', encoding='utf8', newline='\n')
