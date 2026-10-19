"""Verbatim quotes from saved copies of source texts.

A page quotes its sources word for word. The text of each source is saved by fetch_texts.py in
.research-cache/pages/texts/<key>.txt, and every quote is cut from that text: if a phrase is not found, the build
stops, so a quote can never drift from its source.

Texts are normalised once, on loading: runs of white space become one space, and the line-break hyphens of PDF
text are joined ("in- cludes" becomes "includes", while "board- certified" keeps its hyphen). Write phrases in that
clean form.
"""
import re
from pathlib import Path

# First parts of words that are hyphenated compounds, so a line break after their hyphen keeps the hyphen.
COMPOUND = {'board', 'multi', 'well', 'inter', 'intra', 'non', 'pre', 'post', 'self', 'semi', 'co', 'cross', 'high', 'low',
            'state', 'whole', 'slide', 'patch', 'patient', 'case', 'one', 'two', 'three', 'four', 'deep', 'open', 'end', 'long', 'short'}


class Texts:
    def __init__(self, folder):
        self.folder = Path(folder)
        self._cache = {}

    def get(self, key):
        if key not in self._cache:
            path = self.folder / f'{key}.txt'
            if not path.exists():
                raise SystemExit(f'No saved text for "{key}" ({path}). Run fetch_texts.py with the same config first.')
            self._cache[key] = normalise(path.read_text(encoding='utf8', errors='replace'))
        return self._cache[key]

    def sentence(self, key, phrase):
        """The sentence that contains `phrase`."""
        t = self.get(key)
        i = t.find(phrase)
        if i < 0:
            raise SystemExit(f'Phrase not found in "{key}": {phrase!r}')
        start = max(t.rfind(sep, 0, i) for sep in ('. ', '? ', '! ', ': '))
        start = 0 if start < 0 else start + 2
        end = t.find('. ', i + len(phrase))
        end = len(t) if end < 0 else end + 1
        return t[start:end].strip().lstrip('• ').strip()

    def span(self, key, first, last):
        """The text from `first` to the end of `last`."""
        t = self.get(key)
        i = t.find(first)
        j = t.find(last, i + len(first)) if i >= 0 else -1
        if i < 0 or j < 0:
            raise SystemExit(f'Span not found in "{key}": {first!r} … {last!r}')
        return t[i:j + len(last)].strip()

    def has(self, key, value):
        if value not in self.get(key):
            raise SystemExit(f'Value not found in "{key}": {value!r}')
        return value

    def quote(self, spec):
        """A quote from a spec: {text, phrase} for a sentence, or {text, first, last} for a span."""
        if spec.get('phrase'):
            return self.sentence(spec['text'], spec['phrase'])
        return self.span(spec['text'], spec['first'], spec['last'])


def normalise(t):
    t = re.sub(r'\s+', ' ', t)
    words = set(re.findall(r'\b[A-Za-z]*[a-z]-[a-z]+\b', t))

    def join(m):
        a, b = m.group(1), m.group(2)
        return f'{a}-{b}' if a.lower() in COMPOUND or f'{a}-{b}' in words else a + b

    t = re.sub(r'\b([A-Za-z]*[a-z])- ([a-z]+)\b', join, t)
    t = re.sub(r'(?<=[A-Z0-9])- (?=[A-Z0-9])', '-', t)
    t = t.replace('https: //', 'https://')
    return re.sub(r' ([.,;:)])', r'\1', re.sub(r'\( ', '(', t))
