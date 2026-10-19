"""Build a standalone data dictionary page in the format of docs/contributions/ghazal/rmac_data_dictionary.html.

    python scripts/research/pages/build_page.py docs/contributions/<name>/<page>.yaml

The page is assembled from the atlas records (releases, variables, sources, previews, overlaps, study uses, papers)
and from quotes cut from saved source texts (fetch_texts.py). A config file says which releases to cover and which
sentences to quote; docs/contributions/README.md describes it. The page is written next to the config.
"""
import argparse
import base64
import collections
import datetime
import glob
import html
import json
import os
import re
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
from common import CACHE, REPO  # noqa: E402
from quotes import Texts  # noqa: E402

SOURCES_HERE = '<!--sources-->'
EVIDENCE = {
    'DOCUMENTED': 'Stated in a dataset-author source or an authoritative reference.',
    'OBSERVED': 'Present in the released records or files; the source is identified.',
    'CALCULATED': 'A count, summary, or measurement calculated from those records or files.',
    'UNVERIFIED': 'A relevant detail is not established by the available evidence.',
    'CONFLICTING': 'The cited sources or file records disagree on this point.',
}


# ---------------------------------------------------------------- records
def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def load_front(path):
    return yaml.safe_load(Path(path).read_text(encoding='utf8').split('---', 2)[1])


class Records:
    def __init__(self):
        self.sources = {s['id']: s for f in glob.glob(str(REPO / 'src/data/sources/*.json')) for s in load_json(f)}
        self.datasets = {d['id']: d for d in (load_front(f) for f in glob.glob(str(REPO / 'src/content/datasets/*.md')))}
        self.papers = {d['id']: d for d in (load_front(f) for f in glob.glob(str(REPO / 'src/content/papers/*.md')))}
        self.samples = load_json(REPO / 'src/data/samples/processed-figures.json')
        self.overlaps = [o for f in glob.glob(str(REPO / 'src/data/overlap/*.json')) for o in load_json(f)]
        self.uses = [u for f in sorted(glob.glob(str(REPO / 'src/data/study-uses/*.json'))) for u in load_json(f)]
        self._releases = {}

    def release(self, rid):
        if rid not in self._releases:
            self._releases[rid] = yaml.safe_load((REPO / f'src/content/releases/{rid}.yaml').read_text(encoding='utf8'))
        return self._releases[rid]

    def variables(self, rid):
        path = REPO / f'src/data/variables/{rid}.json'
        return load_json(path) if path.exists() else []

    def release_name(self, rid, names=None):
        if names and rid in names:
            return names[rid]
        r = self.release(rid)
        ds = self.datasets.get(r['dataset'], {}).get('name', r['dataset']).split(' — ')[0]
        return f'{ds} ({r["versionLabel"]})'


# ---------------------------------------------------------------- helpers
def esc(x):
    return html.escape('' if x is None else str(x), quote=True)


def ws(x):
    return ' '.join(str(x).split()) if x else ''


def short(x, n=120):
    return x if not x or len(x) <= n else x[:n - 1] + '…'


def parse_cov(defn):
    m = re.search(r'Has a value in ([\d,]+) of ([\d,]+) ([\w -]+?)(?: records| files)?(?:, covering ([\d,]+) of ([\d,]+) cases)?\.', defn or '')
    if not m:
        return None
    toint = lambda x: int(x.replace(',', '')) if x else None
    unit = m.group(3).strip()
    unit = unit if unit.endswith(('files', 'records')) else unit + (' files' if 'slide' in unit else ' records')
    return {'n': toint(m.group(1)), 'total': toint(m.group(2)), 'unit': unit, 'cases_n': toint(m.group(4)), 'cases_total': toint(m.group(5))}


def parse_code(c):
    """Count and unit from an atlas coding meaning such as "… (360 demographic records)" or "… (5 of 103)"."""
    meaning = c.get('meaning') or ''
    m = re.search(r'\(([\d,]+) of ([\d,]+)\)\s*$', meaning)
    if m:
        return meaning[:m.start()].strip(), int(m.group(1).replace(',', '')), None
    m = re.search(r'\(([\d,]+) ([^()]+?)\)\s*$', meaning)
    if m:
        return meaning[:m.start()].strip(), int(m.group(1).replace(',', '')), m.group(2)
    return meaning.strip(), None, None


def parse_missing(items):
    out = []
    for s in items or []:
        m = re.match(r'^"?([^":]+)"?:\s*(?:no value\s*)?\(?([\d,]+)', s)
        if m:
            out.append({'marker': m.group(1).strip(), 'n': int(m.group(2).replace(',', ''))})
    return out


# ---------------------------------------------------------------- page builder
class Page:
    def __init__(self, cfg, base, records, texts, extras):
        self.cfg, self.base, self.R, self.T, self.X = cfg, base, records, texts, extras
        self.snum, self.sections = {}, []
        self.hide = re.compile(cfg['hide_codes_matching']) if cfg.get('hide_codes_matching') else None
        self.columns = [c['label'] for c in cfg.get('columns', [])]
        self.label = {'column': 'Release', 'all_columns': 'All releases', 'absent': 'not in this release', 'entity': 'Entity', 'entity_prefix': '',
                      'meaning': 'Meaning', **(cfg.get('labels') or {})}
        self.fields = self.build_fields()
        self.analysis = self.build_analysis()
        self.image_index = 0

    # -- citations
    def sref(self, sid):
        if sid not in self.R.sources:
            raise SystemExit(f'Unknown source id "{sid}": add it to src/data/sources first.')
        if sid not in self.snum:
            self.snum[sid] = f'S{len(self.snum) + 1:02d}'
        return f'<a class="source-ref" href="#src-{esc(sid)}" title="{esc(self.R.sources[sid]["title"])}">[{self.snum[sid]}]</a>'

    def refs(self, ids):
        return ''.join(self.sref(i) for i in dict.fromkeys(ids or []))

    def text_source(self, key):
        entry = (self.cfg.get('texts') or {}).get(key)
        if not entry:
            raise SystemExit(f'Text "{key}" is not listed under texts: in the config.')
        return entry['source'], entry.get('cite') or self.R.sources[entry['source']]['title']

    def quote_text(self, spec):
        return self.T.quote(spec)

    def quote(self, spec):
        sid, cite = self.text_source(spec['text'])
        loc = f', {esc(spec["loc"])}' if spec.get('loc') else ''
        return f'<blockquote class="pq"><p>“{esc(self.quote_text(spec))}”</p><footer>{esc(cite)}{loc} {self.sref(sid)}</footer></blockquote>'

    def inline_quote(self, spec):
        sid, cite = self.text_source(spec['text'])
        value = self.T.has(spec['text'], spec['value']) if 'value' in spec else self.quote_text(spec)
        loc = f', {esc(spec["loc"])}' if spec.get('loc') else ''
        return f'“{esc(value)}” <span class="fieldsub">{esc(cite)}{loc} {self.sref(sid)}</span>'

    def extras_value(self, key):
        x = self.X['values'][key]
        return f'“{esc(x["value"])}” <span class="fieldsub">{esc(x.get("cite", ""))} {self.refs(x.get("sources"))}</span>'

    def fill(self, text):
        """Replace {key} with a value from the extras file."""
        return re.sub(r'\{(\w+)\}', lambda m: str(self.X.get('values', {}).get(m.group(1), {}).get('value', m.group(0))), text)

    # -- small parts
    def badge(self, cls):
        return f'<span class="badge {cls}" title="{esc(EVIDENCE[cls])}" aria-label="{esc(cls + ": " + EVIDENCE[cls])}">{cls}</span>'

    def evline(self, cls, ids=()):
        return f'<div class="evidence-line">{self.badge(cls)} {self.refs(ids)}</div>'

    @staticmethod
    def table(heads, rows, numcols=()):
        th = ''.join(f'<th tabindex="0" class="sortable" scope="col">{h}</th>' for h in heads)
        body = ''.join('<tr>' + ''.join(f'<td class="num">{c}</td>' if i in numcols else f'<td>{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
        return f'<div class="tablewrap"><table class="static-sort"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>'

    @staticmethod
    def bars(rows, total=None):
        top = max((n for _, n in rows), default=1) or 1
        return ''.join(f'<div class="barrow"><div class="barlabel">{esc(l)}</div><div class="track"><div class="fill" style="width:{100 * n / top:.1f}%"></div></div>'
                       f'<div class="barval">{n:,}{f" · {100 * n / total:.1f}%" if total else ""}</div></div>' for l, n in rows)

    # -- field data
    def definition(self, name, var, overrides):
        o = overrides.get(name)
        if o:
            return ws(o.get('definition')), [o['source']] if o.get('source') else [], o.get('locator', ''), 'DOCUMENTED' if o.get('definition') else 'UNVERIFIED'
        if self.cfg.get('definitions', 'atlas') == 'atlas':
            ev = var.get('evidence') or {}
            return var.get('definition', ''), ev.get('sources', []), ev.get('locator', ''), 'DOCUMENTED' if ev.get('status') == 'verified' else 'UNVERIFIED'
        return '', [], '', 'UNVERIFIED'

    def codes(self, var, meanings):
        kept, hidden = [], 0
        for c in var.get('coding', []):
            if self.hide and self.hide.search(c['code']):
                hidden += 1
                continue
            meaning, n, unit = parse_code(c)
            if meanings is not None:
                meaning = meanings.get(c['code'], '')
            elif self.cfg.get('definitions', 'atlas') != 'atlas':
                meaning = ''
            kept.append({'code': c['code'], 'meaning': ws(meaning), 'n': n, 'unit': unit})
        return kept, hidden

    def build_fields(self):
        overrides = self.X.get('field_overrides', {})
        fields = {}
        for col in self.cfg.get('columns', []):
            for v in self.R.variables(col['release']):
                name = v['originalName']
                o = overrides.get(name, {})
                d, src, loc, ev = self.definition(name, v, overrides)
                f = fields.setdefault(name, {'id': 'f:' + name, 'name': name, 'layer': self.cfg.get('field_layer', 'Field'),
                                             'entity': o.get('entity') or (name.split('.')[0] if '.' in name else v.get('observationLevel', 'record')),
                                             'property': o.get('property') or name.split('.')[-1], 'group': v.get('group', ''), 'type': v.get('type', ''),
                                             'unit': v.get('unit'), 'def': d, 'defloc': loc, 'ev': ev, 'sources': list(src), 'projects': {}})
                atlas_src = (v.get('evidence') or {}).get('sources', []) if self.cfg.get('definitions', 'atlas') == 'atlas' else []
                for s in atlas_src + col.get('sources', []):
                    if s not in f['sources']:
                        f['sources'].append(s)
                codes, hidden = self.codes(v, o.get('codes') if o else None)
                f['projects'][col['label']] = {'cov': parse_cov(v.get('definition')), 'codes': codes, 'hidden': hidden, 'missing': parse_missing(v.get('missingValues'))}
        order = {g: i for i, g in enumerate(self.cfg.get('group_order', ['administrative', 'clinical', 'pathology', 'outcome']))}
        return sorted(fields.values(), key=lambda f: (order.get(f['group'], 99), f['entity'], f['name']))

    def build_analysis(self):
        out = []
        aov = self.X.get('analysis_overrides', {})
        for t in self.cfg.get('analysis_tables', []):
            defs = t.get('definitions') or {}
            files = re.compile(t['files_matching']) if t.get('files_matching') else None
            for v in self.R.variables(t['release']):
                if files and not files.search(v.get('file') or ''):
                    continue
                name = v['originalName']
                if name in defs:
                    spec = defs[name]
                    d, src, loc, ev = self.quote_text(spec), [self.text_source(spec['text'])[0]], spec.get('loc', ''), 'DOCUMENTED'
                elif name in aov.get(t['label'], {}):
                    o = aov[t['label']][name]
                    d, src, loc, ev = ws(o['definition']), [o['source']], o.get('locator', ''), 'DOCUMENTED'
                elif self.cfg.get('definitions', 'atlas') == 'atlas':
                    e = v.get('evidence') or {}
                    d, src, loc, ev = v.get('definition', ''), e.get('sources', []), e.get('locator', ''), 'DOCUMENTED' if e.get('status') == 'verified' else 'UNVERIFIED'
                else:
                    d, src, loc, ev = '', [], '', 'UNVERIFIED'
                codes, _ = self.codes(v, {} if self.cfg.get('definitions', 'atlas') != 'atlas' else None)
                out.append({'id': f'{t["label"]}:{name}', 'name': name, 'table': t['label'], 'file': v.get('file'), 'def': d, 'loc': loc,
                            'type': v.get('type', ''), 'unit': v.get('unit'), 'codes': codes, 'missing': parse_missing(v.get('missingValues')),
                            'sources': src, 'ev': ev})
        return out

    def cov_text(self, f, p):
        x = f['projects'].get(p)
        if not x:
            return f'<span class="muted">{esc(self.label["absent"])}</span>'
        c = x['cov']
        if not c:
            return '—'
        return f'{c["cases_n"]:,} / {c["cases_total"]:,}' if c['cases_n'] is not None else f'{c["n"]:,} / {c["total"]:,}'

    # -- blocks
    def block(self, b):
        k = next(iter(b))
        v = b[k]
        if k == 'h3':
            return f'<h3>{esc(v)}</h3>'
        if k == 'caption':
            return f'<p class="caption">{esc(v)} {self.refs(b.get("sources"))}</p>'
        if k == 'evidence':
            return self.evline(v, b.get('sources', []))
        if k == 'quote':
            return self.quote(v)
        if k == 'quotes':
            return ''.join(self.quote(q) for q in v)
        if k == 'quote_table':
            rows = [(esc(r['label']), self.extras_value(r['extras']) if 'extras' in r else self.inline_quote(r)) for r in v['rows']]
            return self.table([esc(h) for h in v.get('columns', ['Item', 'From the provider'])], rows)
        if k == 'extras_table':
            t = self.X['tables'][v]
            fmt = {int(i): f for i, f in (t.get('format') or {}).items()}
            cell = lambda i, c: f'<code>{esc(c)}</code>' if fmt.get(i) == 'code' else f'“{esc(c)}”' if fmt.get(i) == 'quote' and c else esc(c)
            return ((self.evline(t['evidence'], t.get('sources', [])) if t.get('evidence') else '')
                    + self.table([esc(h) for h in t['columns']], [[cell(i, c) for i, c in enumerate(r)] for r in t['rows']], tuple(t.get('numcols', [])))
                    + (f'<p class="caption"><code>{esc(t["caption"])}</code> {self.refs(t.get("sources"))}</p>' if t.get('caption') else ''))
        if k == 'extras_bars':
            cards = self.X['bars'][v]
            return '<div class="grid three">' + ''.join(
                f'<div class="card">' + ''.join(f'<h4>{esc(g["title"])}</h4>{self.bars([tuple(r) for r in g["rows"]], g.get("total"))}' for g in c) + '</div>'
                for c in cards) + '</div>'
        if k == 'field_dictionary':
            return self.field_dictionary()
        if k == 'analysis_columns':
            return self.analysis_columns()
        if k == 'codebooks':
            return '<div class="codebookgrid">' + ''.join(self.codebook(n, i < 2) for i, n in enumerate(x for x in v if x in {f['name'] for f in self.fields})) + '</div>'
        if k == 'code_bars':
            return ''.join(self.code_bars(n) for n in v)
        if k == 'previews':
            return self.previews(v)
        if k == 'overlaps':
            return self.overlaps()
        if k == 'missing':
            return self.missing()
        if k == 'papers':
            return self.papers(v or {})
        if k == 'terms':
            return self.terms(v)
        if k == 'glossary':
            return self.glossary(v)
        if k == 'notes':
            return self.table(['Input', 'What was read', 'Sources'], [(esc(r['input']), esc(self.fill(r['what'])), self.refs(r.get('sources'))) for r in v])
        if k == 'sources':
            return SOURCES_HERE  # filled in last, once every source is numbered
        raise SystemExit(f'Unknown block type "{k}"')

    def field_dictionary(self):
        P = self.columns
        rows = [(f'<button class="fieldname" data-field="{esc(f["id"])}">{esc(f["name"])}</button><div class="fieldsub">{esc(self.label["entity_prefix"] + f["entity"])} · {esc(f["group"])}</div>'
                 f'<div class="fieldsub">{esc(short(f["def"])) or "—"}</div>', f'<code>{esc(f["type"])}</code>' + (f'<div class="fieldsub">{esc(f["unit"])}</div>' if f['unit'] else ''),
                 *[self.cov_text(f, p) for p in P], self.badge(f['ev'])) for f in self.fields]
        groups = [g for g in self.cfg.get('group_order', ['administrative', 'clinical', 'pathology', 'outcome']) if any(f['group'] == g for f in self.fields)]
        return (f'<div class="chips" id="field-presets"><button class="btn selected" data-preset="all">All {len(self.fields)} fields</button>'
                + ''.join(f'<button class="btn" data-preset="{g}">{esc(g.capitalize())} ({sum(1 for f in self.fields if f["group"] == g)})</button>' for g in groups)
                + '</div><div class="toolbar"><label class="wide">Field or definition<input id="field-query" type="search" placeholder="Search fields"></label>'
                + f'<label>{esc(self.label["column"])}<select id="field-project"><option value="">{esc(self.label["all_columns"])}</option>' + ''.join(f'<option>{esc(p)}</option>' for p in P) + '</select></label>'
                + f'<label>{esc(self.label["entity"])}<select id="field-entity"><option value="">All entities</option>' + ''.join(f'<option>{esc(e)}</option>' for e in sorted({f["entity"] for f in self.fields})) + '</select></label>'
                + '<label>Type<select id="field-type"><option value="">All types</option>' + ''.join(f'<option>{esc(t)}</option>' for t in sorted({f["type"] for f in self.fields})) + '</select></label>'
                + '<label>Evidence<select id="field-evidence"><option value="">All evidence</option>' + ''.join(f'<option>{e}</option>' for e in sorted({f["ev"] for f in self.fields})) + '</select></label>'
                + f'<button class="btn" id="field-reset">Reset</button></div><div id="field-table">{self.table(["Field", "Type", *map(esc, P), "Evidence"], rows, tuple(range(2, 2 + len(P))))}</div>'
                + '<p class="caption" id="field-count" aria-live="polite"></p>'
                + '<div class="chips"><button class="btn" id="download-json">Download dictionary JSON</button><button class="btn" id="download-csv">Download field CSV</button></div>')

    def analysis_columns(self):
        rows = [(f'<button class="fieldname" data-field="{esc(a["id"])}">{esc(a["name"])}</button><div class="fieldsub">{esc(short(a["def"], 150)) or "—"}</div>',
                 esc(a['table']), f'<code>{esc(a["type"])}</code>' + (f'<div class="fieldsub">{esc(a["unit"])}</div>' if a['unit'] else ''), self.badge(a['ev'])) for a in self.analysis]
        for a in self.analysis:
            self.refs(a['sources'])
        counts = collections.Counter(a['table'] for a in self.analysis)
        return ('<div class="chips" id="analysis-presets">' + f'<button class="btn selected" data-apreset="all">All {len(self.analysis)} columns</button>'
                + ''.join(f'<button class="btn" data-apreset="{esc(t)}">{esc(t)} ({n})</button>' for t, n in counts.items())
                + '</div><div class="toolbar"><label class="wide">Column or definition<input id="analysis-query" type="search" placeholder="Search columns"></label></div>'
                + f'<div id="analysis-table">{self.table(["Column", "Table", "Type", "Evidence"], rows)}</div><p class="caption" id="analysis-count" aria-live="polite"></p>')

    def codebook(self, name, open_):
        f = next(x for x in self.fields if x['name'] == name)
        P = self.columns
        codes, unit = collections.OrderedDict(), None
        for p in P:
            for c in (f['projects'].get(p) or {}).get('codes', []):
                row = codes.setdefault(c['code'], {'meaning': c['meaning'], **{q: '' for q in P}})
                row[p] = f'{c["n"]:,}' if c['n'] is not None else ''
                unit = unit or c['unit']
        rows = [(f'<code>{esc(k)}</code>', f'“{esc(v["meaning"])}”' if v['meaning'] else '—', *[v[p] for p in P]) for k, v in codes.items()]
        heads = ['Stored value', esc(self.label['meaning']), *[f'{esc(p)} ({esc(unit or "records")})' if i == 0 else esc(p) for i, p in enumerate(P)]]
        cid = 'codebook-' + re.sub(r'[^a-z0-9]+', '-', name.lower())
        return (f'<details id="{cid}"{" open" if open_ else ""}><summary><span>{esc(name)}</span></summary><div class="detailsbody">'
                + self.evline(f['ev'], f['sources']) + self.table(heads, rows, tuple(range(2, 2 + len(P))))
                + f'<button class="btn" data-field="{esc(f["id"])}">Open field details</button></div></details>')

    def code_bars(self, name, top=8):
        f = next((x for x in self.fields if x['name'] == name), None)
        if not f:
            return ''
        cards = []
        for col in self.cfg.get('columns', []):
            p = col['label']
            cs = [c for c in (f['projects'].get(p) or {}).get('codes', []) if c['n'] is not None]
            cards.append(f'<div class="card"><h4>{esc(col.get("title", p))}</h4>{self.bars([(c["code"], c["n"]) for c in cs[:top]], sum(c["n"] for c in cs) or None) or "—"}</div>')
        return f'<h3><button class="fieldname" data-field="{esc(f["id"])}">{esc(name)}</button></h3><div class="grid three">{"".join(cards)}</div>'

    def image(self, path):
        if self.cfg.get('embed_images', True):
            return f'data:image/{path.rsplit(".", 1)[-1]};base64,' + base64.b64encode((REPO / 'public' / path.lstrip('/')).read_bytes()).decode()
        return os.path.relpath(REPO / 'public' / path.lstrip('/'), self.base).replace(os.sep, '/')

    def previews(self, groups):
        out = []
        for g in groups:
            group = [s for s in self.R.samples if s['release'] == g['release']]
            if not group:
                continue
            out.append(f'<h3>{esc(g.get("title") or self.R.release_name(g["release"], self.cfg.get("names")))} · {len(group)}</h3>'
                       f'<details><summary>Credit and licence</summary><div class="detailsbody"><p>{esc(group[0].get("attribution"))}</p><p>{esc(group[0].get("reuseTerms"))}</p></div></details>')
            for s in group:
                a = s['assets'][0]
                big = f' data-large="{self.image(a["large"]["path"])}"' if a.get('large') else ''
                pt = ''.join(f'<p><code>{esc(t["field"])}</code> “{esc(t["value"])}”</p>' for t in s.get('providerText', []))
                pairs = list(dict.fromkeys((t['source'], t['locator']) for t in s.get('providerText', [])))
                src = '; '.join(f'<a href="{esc(self.R.sources[sid]["url"])}" target="_blank" rel="noopener">{esc(self.R.sources[sid]["title"])}</a>; {esc(loc)} {self.sref(sid)}' for sid, loc in pairs)
                mask = f' · Mask: {esc(s["mask"])}' if s.get('mask') else ''
                out.append(f'<figure class="card sample"><button class="sample-open" data-img="{self.image_index}" aria-label="Open larger: {esc(s.get("caseId"))}">'
                           f'<img src="{self.image(a["path"])}" alt="{esc(s.get("alt", ""))}" width="{a.get("width", "")}" height="{a.get("height", "")}"{big}></button>'
                           f'<figcaption><p><strong>{esc(s.get("caseId"))}</strong>{mask}</p>'
                           + (f'<p><strong>From the provider:</strong></p>{pt}<p class="caption">Source: {src}</p>' if pt else '') + '</figcaption></figure>')
                self.image_index += 1
        return ''.join(out)

    def family(self):
        return set(self.cfg.get('family') or [c['release'] for c in self.cfg.get('columns', [])])

    def overlaps(self):
        fam = self.family()
        rows = [(' ↔ '.join(esc(self.R.release_name(r, self.cfg.get('names'))) for r in o['releases']), f'{o["count"]["value"]:,}' if (o.get('count') or {}).get('value') is not None else '—',
                 self.refs((o.get('count') or {}).get('evidence', {}).get('sources', []))) for o in self.R.overlaps if set(o['releases']) & fam]
        return self.evline('CALCULATED') + self.table(['Releases', 'Patients in both', 'Sources'], rows, (1,))

    def missing(self):
        P = self.columns
        rows = []
        for f in self.fields:
            cells = []
            for p in P:
                x = f['projects'].get(p)
                c = (x or {}).get('cov')
                cells.append(f'<span class="muted">{esc(self.label["absent"])}</span>' if not x else '—' if not c else
                             f'{c["cases_n"]:,} / {c["cases_total"]:,} cases' if c['cases_n'] is not None else f'{c["n"]:,} / {c["total"]:,} {esc(c["unit"])}')
            rows.append((f'<button class="fieldname" data-field="{esc(f["id"])}">{esc(f["name"])}</button>', esc(f['entity']), *cells))
        return self.table(['Field', esc(self.label['entity']), *map(esc, P)], rows)

    def papers(self, cfg):
        fam, qmap = self.family(), cfg.get('quotes', {})
        rows = []
        for u in self.R.uses:
            if u.get('release') not in fam:
                continue
            p = self.R.papers.get(u['paper'], {})
            said = ''.join(f'<p>“{esc(self.quote_text(q))}”</p>' for q in qmap.get(u['id'], [])) or '—'
            src = [u['paper']] if u['paper'] in self.R.sources else u['actualUseEvidence']['sources']
            rows.append((f'{esc(p.get("title", u["paper"]))}<div class="fieldsub">{esc(p.get("venue") or "")} {p.get("year") or ""}</div>', esc(self.R.release_name(u['release'], self.cfg.get('names'))), said, self.refs(src)))
        return self.table(['Paper', 'Release', 'What the authors write', 'Sources'], rows)

    def terms(self, rows):
        out = []
        for r in rows:
            terms = self.R.release(r['release']).get('annotationTerms') or []
            out.append((esc(r['label']), '; '.join(f'“{esc(t["value"])}” {self.sref(t["source"])}' for t in terms) or '—'))
        return self.table(['Set', 'Terms'], out)

    def glossary(self, items):
        entries = []
        for it in items:
            if 'extras' in it:
                for g in self.X.get('glossary', {}).get(it['extras'], []):
                    entries.append((g['term'], g['definition'], g['cite'], g['source'], g.get('category', 'Technical')))
            else:
                sid, cite = self.text_source(it['quote']['text'])
                entries.append((it['term'], self.quote_text(it['quote']), cite, sid, it.get('category', 'Technical')))
        self.glossary_data = [{'term': t, 'definition': d} for t, d, _, _, _ in entries]
        return ('<div class="toolbar"><label class="wide">Find a term<input id="glossary-query" type="search" placeholder="Search terms"></label>'
                '<label>Domain<select id="glossary-category"><option value="">Medical &amp; technical</option><option>Medical</option><option>Technical</option></select></label></div>'
                '<div class="glossgrid">' + ''.join(f'<div class="glossterm" data-category="{esc(c)}"><h4>{esc(t)}</h4><p>“{esc(d)}”</p><p class="small muted">{esc(cite)} {self.sref(sid)}</p></div>'
                                                    for t, d, cite, sid, c in entries) + '</div>')

    # -- page
    def section(self, s):
        body = ''.join(self.block(b) for b in s.get('blocks', []))
        self.sections.append((s.get('group', ''), s['id'], s['title']))
        n = f'{len(self.sections):02d}'
        lab = f'<span class="layerlabel {esc(s["layer"][1])}">{esc(s["layer"][0])}</span>' if s.get('layer') else ''
        hd = f'<div class="sectionhead"><h2>{esc(s["title"])}</h2><span class="sectionnum">{n}</span></div>' if s.get('heading', True) else ''
        return f'<section id="{esc(s["id"])}" class="section" data-title="{esc(s["title"])}">{lab}{hd}{body}</section>'

    def overview(self):
        cfg = self.cfg
        cards = cfg.get('cards') or self.X.get('cards') or []
        head = '<br>'.join(esc(x) for x in cfg['title'].split('|'))
        caption = cfg.get('overview_caption') or self.X.get('overview_caption')
        body = (f'<h1>{head}</h1>' + (self.quote(cfg['lede']) if cfg.get('lede') else '')
                + ('<div class="grid four">' + ''.join(f'<div class="card"><div class="stat">{esc(c["value"])}</div><div class="statlabel">{esc(c["label"])}</div>'
                                                       f'<div class="statdetail">{esc(c.get("detail", ""))}</div></div>' for c in cards) + '</div>' if cards else '')
                + (f'<p class="caption">{esc(caption["text"])} {self.refs(caption.get("sources"))}</p>' if caption else '')
                + '<div class="chips">' + ''.join(f'<a class="btn{" primary" if i == 0 else ""}" href="#{esc(l["to"])}">{esc(l["label"])}</a>' for i, l in enumerate(cfg.get('links', []))) + '</div>')
        self.sections.append((cfg.get('overview_group', 'Dataset'), 'overview', 'Overview'))
        return f'<section id="overview" class="section" data-title="Overview">{body}</section>'

    def render(self):
        cfg = self.cfg
        self.glossary_data = []
        body = [self.overview()] + [self.section(s) for s in cfg.get('sections', [])]
        cards = ''.join(f'<details class="sourcecard" id="src-{esc(sid)}"><summary><span class="sourceid">{n}</span><span>{esc(self.R.sources[sid]["title"])}</span></summary>'
                        f'<div class="detailsbody"><p><a href="{esc(self.R.sources[sid]["url"])}" target="_blank" rel="noopener">{esc(self.R.sources[sid]["url"])}</a></p>'
                        f'<p class="caption">Read on {esc(self.R.sources[sid].get("accessedOn"))}</p></div></details>' for sid, n in self.snum.items())
        body = [b.replace(SOURCES_HERE, cards) for b in body]
        data = {'title': ws(cfg['title'].replace('|', ' ')), 'slug': cfg.get('slug', 'data_dictionary'), 'generated': datetime.date.today().isoformat(),
                'columns': self.columns, 'evidence_labels': EVIDENCE, 'fields': self.fields, 'analysis': self.analysis,
                'sources': {sid: {'n': n, 'title': self.R.sources[sid]['title'], 'url': self.R.sources[sid]['url']} for sid, n in self.snum.items()},
                'glossary': self.glossary_data}
        nav, last = [], None
        for group, sid, title in self.sections:
            if group != last:
                nav.append(f'<div class="navgroup">{esc(group)}</div>')
                last = group
            nav.append(f'<a href="#{esc(sid)}">{esc(title)}</a>')
        style_page = (REPO / cfg.get('style', 'docs/contributions/ghazal/rmac_data_dictionary.html')).read_text(encoding='utf8')
        css = re.search(r'(?s)<style>(.*?)</style>', style_page).group(1) + (HERE / 'page.css').read_text(encoding='utf8')
        js = (HERE / 'page.js').read_text(encoding='utf8')
        data_json = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
        title = esc(ws(cfg['title'].replace('|', ' ')))
        return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
                f'<meta name="description" content="{esc(cfg.get("description", title))}"><title>{title}</title><style>{css}</style></head><body>'
                '<a class="sr-only" href="#overview">Skip to content</a>'
                '<header class="topbar"><button class="menu" id="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">☰</button>'
                f'<a class="brand" href="#overview">{esc(cfg.get("brand", title))} <span class="long">/ <span>Dictionary</span></span></a>'
                '<div class="searchwrap"><span class="searchicon" aria-hidden="true">⌕</span><label class="sr-only" for="global-search">Global search</label>'
                '<input id="global-search" type="search" placeholder="Search fields, codes, concepts…" autocomplete="off" aria-controls="search-results" aria-expanded="false"></div></header>'
                f'<aside id="sidebar" class="sidebar" aria-label="Contents">{"".join(nav)}<div class="navfoot">Keyboard: / search · Esc close</div></aside>'
                '<div id="search-results" class="searchresults" hidden aria-live="polite"></div>'
                f'<main>{"".join(body)}<footer class="footer">{title} · {data["generated"]}</footer></main>'
                '<button class="topbutton" id="back-top" aria-label="Back to top">↑ Top</button>'
                '<dialog id="field-dialog" aria-labelledby="dialog-title"><div class="dialoghead"><div><div class="eyebrow" id="dialog-layer"></div><h2 id="dialog-title"></h2>'
                '<div id="dialog-subtitle"></div></div><button class="closebtn" id="dialog-close" aria-label="Close field details">×</button></div><div class="dialogbody" id="dialog-body"></div></dialog>'
                '<dialog id="image-dialog" aria-label="Preview image"><div class="dialoghead"><div><h2 id="image-title"></h2></div><button class="closebtn" id="image-close" aria-label="Close image">×</button></div>'
                '<img id="image-big" alt=""><div class="imgcap" id="image-cap"></div></dialog><div class="toast" id="toast" role="status" hidden></div>'
                f'<script type="application/json" id="dictionary-data">{data_json}</script><script>{js}</script></body></html>')


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    ap.add_argument('config')
    args = ap.parse_args()
    path = Path(args.config).resolve()
    cfg = yaml.safe_load(path.read_text(encoding='utf8'))
    extras = load_json(REPO / cfg['extras']) if cfg.get('extras') else {}
    page = Page(cfg, path.parent, Records(), Texts(CACHE / 'pages' / 'texts'), extras)
    out = path.parent / cfg['output']
    text = page.render()
    out.write_text(text, encoding='utf8', newline='\n')
    print(f'wrote {out.relative_to(REPO)}: {len(text) // 1024} KB, {len(page.sections)} sections, {len(page.fields)} fields, '
          f'{len(page.analysis)} analysis columns, {page.image_index} previews, {len(page.snum)} sources')


if __name__ == '__main__':
    main()
