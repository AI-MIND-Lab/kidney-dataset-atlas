"""The KiTS clinical files, pinned to the commits the dictionaries were built from, and helpers to read them."""
import json

import _setup  # noqa: F401
from common import REPO as REPO_ROOT, cache_dir, get  # noqa: F401  (REPO_ROOT is re-exported for the builders)

KITS_FILES = {
    'kits19': ('neheller/kits19', '67e495dd48dc40830df57719ef6f7f1d389c7a89', 'data/kits.json'),
    'kits21': ('neheller/kits21', '77b7d07fa9f94f5d4d963fc6e3a20d23d1bcb0c9', 'kits21/data/kits.json'),
    'kits23': ('neheller/kits23', '5f2b8cd369df7936d3253201560ba831b343ce9f', 'dataset/kits23.json'),
}


def load(release):
    """The release's case records, downloaded once into .research-cache/dictionary/."""
    repo, commit, path = KITS_FILES[release]
    local = cache_dir('dictionary') / f'{release}-{commit[:7]}.json'
    if not local.exists():
        text = get(f'https://raw.githubusercontent.com/{repo}/{commit}/{path}')
        if text is None:
            raise SystemExit(f'Could not download {path} from {repo} at {commit[:7]}')
        local.write_text(text, encoding='utf8')
    return json.loads(local.read_text(encoding='utf8'))


def flat(record, prefix=''):
    """Flatten nested objects into dotted keys: {'a': {'b': 1}} becomes {'a.b': 1}."""
    out = {}
    for k, v in record.items():
        if isinstance(v, dict):
            out.update(flat(v, prefix + k + '.'))
        else:
            out[prefix + k] = v
    return out
