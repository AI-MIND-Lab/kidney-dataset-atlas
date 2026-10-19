'use strict';
// Interactive parts of a data dictionary page built by build_page.py: tables, filters, field details, previews,
// search, glossary and downloads. The page's data is the JSON block with id "dictionary-data".
const D = JSON.parse(document.getElementById('dictionary-data').textContent);
const $ = (s) => document.querySelector(s), $$ = (s) => [...document.querySelectorAll(s)];
const esc = (x) => String(x ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
const fmt = (n) => (n == null ? '—' : Number(n).toLocaleString('en-US'));
const P = D.columns;
const badge = (c) => `<span class="badge ${esc(c)}" title="${esc(D.evidence_labels[c] || c)}" aria-label="${esc(c + ': ' + (D.evidence_labels[c] || c))}">${esc(c)}</span>`;
const refs = (ids) => (ids || []).map((id) => (D.sources[id] ? `<a class="source-ref" href="#src-${esc(id)}" title="${esc(D.sources[id].title)}">[${esc(D.sources[id].n)}]</a>` : '')).join('');
const byId = new Map([...D.fields, ...D.analysis].map((f) => [f.id, f]));
const short = (s, n = 120) => (s && s.length > n ? s.slice(0, n - 1) + '…' : s || '');
const table = (heads, rows, num = []) =>
	`<div class="tablewrap"><table class="static-sort"><thead><tr>${heads.map((h) => `<th class="sortable" tabindex="0" scope="col">${h}</th>`).join('')}</tr></thead><tbody>${rows
		.map((r) => '<tr>' + r.map((v, i) => `<td${num.includes(i) ? ' class="num"' : ''}>${v}</td>`).join('') + '</tr>')
		.join('')}</tbody></table></div>`;

function coverage(f, p) {
	const x = f.projects[p];
	if (!x) return { text: '<span class="muted">not in project</span>', v: -2 };
	const c = x.cov;
	if (!c) return { text: '—', v: -1 };
	if (c.cases_n != null) return { text: `${fmt(c.cases_n)} / ${fmt(c.cases_total)}`, v: c.cases_n / c.cases_total };
	return { text: `${fmt(c.n)} / ${fmt(c.total)}`, v: c.n / c.total };
}

/* ---------------- master field dictionary ---------------- */
const fs = { preset: 'all', sort: null, dir: 1 };
const FILTERS = ['#field-query', '#field-project', '#field-entity', '#field-type', '#field-evidence'];
function renderFields() {
	const q = $('#field-query').value.trim().toLowerCase(), proj = $('#field-project').value, ent = $('#field-entity').value, typ = $('#field-type').value, ev = $('#field-evidence').value;
	let rows = D.fields.filter(
		(f) => (fs.preset === 'all' || f.group === fs.preset) && (!proj || f.projects[proj]) && (!ent || f.entity === ent) && (!typ || f.type === typ) && (!ev || f.ev === ev) && (!q || (f.name + ' ' + f.def).toLowerCase().includes(q)),
	);
	if (fs.sort) {
		const key = fs.sort;
		const val = (f) => (P.includes(key) ? coverage(f, key).v : String(f[key] ?? '').toLowerCase());
		rows = [...rows].sort((a, b) => (val(a) > val(b) ? 1 : val(a) < val(b) ? -1 : 0) * fs.dir);
	}
	const heads = [['Field', 'name'], ['Type', 'type'], ...P.map((p) => [p, p]), ['Evidence', 'ev']];
	$('#field-table').innerHTML = `<div class="tablewrap"><table><thead><tr>${heads
		.map(([h, k]) => `<th class="sortable" tabindex="0" scope="col" data-fsort="${k}" aria-sort="${fs.sort === k ? (fs.dir === 1 ? 'ascending' : 'descending') : 'none'}">${h}</th>`)
		.join('')}</tr></thead><tbody>${rows
		.map(
			(f) =>
				`<tr><td><button class="fieldname" data-field="${esc(f.id)}">${esc(f.name)}</button><div class="fieldsub">${esc(f.entity)} · ${esc(f.group)}</div><div class="fieldsub">${esc(short(f.def)) || '—'}</div></td><td><code>${esc(f.type)}</code>${f.unit ? `<div class="fieldsub">${esc(f.unit)}</div>` : ''}</td>${P.map((p) => `<td class="num">${coverage(f, p).text}</td>`).join('')}<td>${badge(f.ev)}</td></tr>`,
		)
		.join('')}</tbody></table></div>`;
	$('#field-count').textContent = `${rows.length} of ${D.fields.length} fields`;
}
FILTERS.forEach((s) => ($(s).oninput = renderFields));
$('#field-reset').onclick = () => {
	FILTERS.forEach((s) => ($(s).value = ''));
	fs.sort = null;
	setPreset('all');
};
function setPreset(p) {
	fs.preset = p;
	$$('#field-presets .btn').forEach((b) => b.classList.toggle('selected', b.dataset.preset === p));
	renderFields();
}

/* ---------------- analysis-result tables ---------------- */
const as = { preset: 'all' };
function renderAnalysis() {
	const q = $('#analysis-query').value.trim().toLowerCase();
	const rows = D.analysis.filter((a) => (as.preset === 'all' || a.table === as.preset) && (!q || (a.name + ' ' + a.def).toLowerCase().includes(q)));
	$('#analysis-table').innerHTML = table(
		['Column', 'Table', 'Type', 'Evidence'],
		rows.map((a) => [`<button class="fieldname" data-field="${esc(a.id)}">${esc(a.name)}</button><div class="fieldsub">${esc(short(a.def, 150)) || '—'}</div>`, esc(a.table), `<code>${esc(a.type)}</code>${a.unit ? `<div class="fieldsub">${esc(a.unit)}</div>` : ''}`, badge(a.ev)]),
	);
	$('#analysis-count').textContent = `${rows.length} of ${D.analysis.length} columns`;
}
$('#analysis-query').oninput = renderAnalysis;

/* ---------------- field details ---------------- */
const kv = (pairs) => '<dl class="keyvalue">' + pairs.filter(([, v]) => v != null && v !== '').map(([k, v]) => `<dt>${esc(k)}</dt><dd>${v}</dd>`).join('') + '</dl>';
const missing = (m) => (m || []).map((x) => `<code>${esc(x.marker)}</code> ${fmt(x.n)}`).join(' · ');
function openField(id) {
	const f = byId.get(id);
	if (!f) return;
	const isGdc = !!f.projects;
	$('#dialog-layer').textContent = isGdc ? `${f.layer} · ${f.entity}` : `${f.table} · ${f.file || ''}`;
	$('#dialog-title').textContent = f.name;
	$('#dialog-subtitle').innerHTML = badge(f.ev) + ' ' + refs(f.sources);
	let out = f.def ? `<p class="lede">“${esc(f.def)}”</p>` : '<p class="lede">—</p>';
	out += `<div class="chips"><button class="btn" data-copy="${esc(f.name)}">Copy field name</button></div>`;
	if (isGdc) {
		out += kv([['Entity', `<code>${esc(f.entity)}</code>`], ['Property', `<code>${esc(f.property || '')}</code>`], ['Type', `<code>${esc(f.type)}</code>`], ['Unit', esc(f.unit || '')], ['Definition from', f.defloc ? esc(f.defloc) : '']]);
		out += '<h3>By project</h3>' + table(['Project', 'Values present', 'Missing-value markers'], P.map((p) => {
			const x = f.projects[p];
			if (!x) return [p, '<span class="muted">not in project</span>', ''];
			const c = x.cov;
			const pres = !c ? '—' : c.cases_n != null ? `${fmt(c.n)} / ${fmt(c.total)} ${esc(c.unit)}; ${fmt(c.cases_n)} / ${fmt(c.cases_total)} cases` : `${fmt(c.n)} / ${fmt(c.total)} ${esc(c.unit)}`;
			return [p, pres + (x.hidden ? `<div class="fieldsub">identifier values not shown: ${x.hidden}</div>` : ''), missing(x.missing)];
		}));
		const codes = new Map();
		let unit = '';
		for (const p of P) for (const c of (f.projects[p] || {}).codes || []) {
			if (!codes.has(c.code)) codes.set(c.code, { meaning: c.meaning, counts: {} });
			codes.get(c.code).counts[p] = c.n;
			unit = unit || c.unit || '';
		}
		if (codes.size) out += `<h3>Codes · ${codes.size}</h3>` + table(['Stored value', 'Meaning', ...P.map((p, i) => (i ? p : `${p} (${esc(unit || 'records')})`))], [...codes].map(([k, v]) => [`<code>${esc(k)}</code>`, v.meaning ? `“${esc(v.meaning)}”` : '—', ...P.map((p) => (v.counts[p] == null ? '' : fmt(v.counts[p])))]), [2, 3, 4]);
	} else {
		out += kv([['Table', esc(f.table)], ['File', `<code>${esc(f.file || '')}</code>`], ['Type', `<code>${esc(f.type)}</code>`], ['Unit', esc(f.unit || '')], ['Definition from', f.def ? esc(f.loc || '') + ' ' + refs(f.sources) : '']]);
		if (f.codes.length) out += `<h3>Values · ${f.codes.length}</h3>` + table(['Stored value', 'Count'], f.codes.map((c) => [`<code>${esc(c.code)}</code>`, c.n == null ? '' : fmt(c.n)]), [1]);
		if (f.missing.length) out += '<h3>Missing-value markers</h3><p>' + missing(f.missing) + '</p>';
	}
	$('#dialog-body').innerHTML = out;
	const el = $('#field-dialog');
	if (!el.open) el.showModal();
	el.scrollTop = 0;
	$('#dialog-close').focus();
}
$('#dialog-close').onclick = () => $('#field-dialog').close();

/* ---------------- preview images ---------------- */
function openImage(btn) {
	const img = btn.querySelector('img');
	const fig = btn.closest('figure');
	$('#image-big').src = img.dataset.large || img.src;
	$('#image-big').alt = img.alt;
	$('#image-title').textContent = fig.querySelector('figcaption strong')?.textContent || '';
	$('#image-cap').innerHTML = fig.querySelector('figcaption').innerHTML;
	const d = $('#image-dialog');
	if (!d.open) d.showModal();
	$('#image-close').focus();
}
$('#image-close').onclick = () => $('#image-dialog').close();
for (const d of ['#field-dialog', '#image-dialog'])
	$(d).addEventListener('click', (ev) => {
		if (ev.target === $(d)) {
			const r = ev.target.getBoundingClientRect();
			if (ev.clientX < r.left || ev.clientX > r.right || ev.clientY < r.top || ev.clientY > r.bottom) ev.target.close();
		}
	});

/* ---------------- copy and toast ---------------- */
let toastTimer;
function toast(t) {
	$('#toast').textContent = t;
	$('#toast').hidden = false;
	clearTimeout(toastTimer);
	toastTimer = setTimeout(() => ($('#toast').hidden = true), 2200);
}
async function copyText(t) {
	let ok = false;
	try {
		if (navigator.clipboard && window.isSecureContext) {
			await navigator.clipboard.writeText(t);
			ok = true;
		}
	} catch {}
	if (!ok) {
		const a = document.createElement('textarea');
		a.value = t;
		a.style.position = 'fixed';
		a.style.opacity = '0';
		($('#field-dialog').open ? $('#field-dialog') : document.body).append(a);
		a.select();
		try {
			ok = document.execCommand('copy');
		} catch {}
		a.remove();
	}
	toast(ok ? 'Copied: ' + t : 'Copy not available');
}

/* ---------------- navigation ---------------- */
function navigate(id) {
	$('#search-results').hidden = true;
	$('#global-search').setAttribute('aria-expanded', 'false');
	for (const d of ['#field-dialog', '#image-dialog']) if ($(d).open) $(d).close();
	const el = document.getElementById(id);
	if (!el) return;
	if (el.tagName === 'DETAILS') el.open = true;
	for (let par = el.parentElement; par; par = par.parentElement) if (par.tagName === 'DETAILS') par.open = true;
	el.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'start' });
	history.replaceState(null, '', '#' + encodeURIComponent(id));
	$('#sidebar').classList.remove('open');
	$('#nav-toggle').setAttribute('aria-expanded', 'false');
}
$('#nav-toggle').onclick = () => {
	const open = $('#sidebar').classList.toggle('open');
	$('#nav-toggle').setAttribute('aria-expanded', String(open));
};
$('#back-top').onclick = () => {
	window.scrollTo({ top: 0, behavior: 'instant' });
	history.replaceState(null, '', '#overview');
};
const observer = new IntersectionObserver(
	(entries) => {
		for (const x of entries) if (x.isIntersecting) $$('.sidebar a').forEach((a) => a.classList.toggle('active', a.getAttribute('href') === '#' + x.target.id));
	},
	{ rootMargin: '-80px 0px -65% 0px', threshold: 0 },
);
$$('.section').forEach((s) => observer.observe(s));

/* ---------------- global search ---------------- */
const index = [
	...D.fields.map((f) => ({ kind: 'Field', title: f.name, sub: f.entity + ' · ' + short(f.def, 90), text: (f.name + ' ' + f.def).toLowerCase(), field: f.id })),
	...D.analysis.map((a) => ({ kind: 'Analysis column', title: a.name, sub: a.table + (a.def ? ' · ' + short(a.def, 90) : ''), text: (a.name + ' ' + a.def + ' ' + a.table).toLowerCase(), field: a.id })),
	...D.fields.flatMap((f) => {
		const seen = new Set();
		return P.flatMap((p) => ((f.projects[p] || {}).codes || []).filter((c) => !seen.has(c.code) && seen.add(c.code)).map((c) => ({ kind: 'Code', title: c.code, sub: f.name, text: (c.code + ' ' + (c.meaning || '')).toLowerCase(), field: f.id })));
	}),
	...$$('.section').map((s) => ({ kind: 'Section', title: s.dataset.title, sub: '', text: s.dataset.title.toLowerCase(), goto: s.id })),
	...D.glossary.map((g) => ({ kind: 'Glossary', title: g.term, sub: short(g.definition, 90), text: (g.term + ' ' + g.definition).toLowerCase(), goto: 'glossary' })),
	...$$('#previews figure').map((fig) => ({ kind: 'Preview', title: fig.querySelector('figcaption strong').textContent, sub: short(fig.querySelector('figcaption').textContent, 90), text: fig.querySelector('figcaption').textContent.toLowerCase(), goto: 'previews' })),
];
function search() {
	const q = $('#global-search').value.trim().toLowerCase();
	const box = $('#search-results');
	if (q.length < 2) {
		box.hidden = true;
		$('#global-search').setAttribute('aria-expanded', 'false');
		return;
	}
	const words = q.split(/\s+/);
	const hits = index.filter((x) => words.every((w) => x.text.includes(w) || x.title.toLowerCase().includes(w))).slice(0, 14);
	box.innerHTML = hits.length
		? hits.map((h) => `<button class="result" ${h.field ? `data-field="${esc(h.field)}"` : `data-goto="${esc(h.goto)}"`}><b>${esc(h.title)}</b> <span class="tag">${esc(h.kind)}</span><small>${esc(h.sub)}</small></button>`).join('')
		: '<div class="result">No match.</div>';
	box.hidden = false;
	$('#global-search').setAttribute('aria-expanded', 'true');
}
$('#global-search').addEventListener('input', search);
$('#global-search').addEventListener('focus', () => {
	if ($('#global-search').value.length >= 2) search();
});

/* ---------------- static tables ---------------- */
function sortStatic(th) {
	const tableEl = th.closest('table');
	const i = [...th.parentElement.children].indexOf(th);
	const dir = th.getAttribute('aria-sort') === 'ascending' ? -1 : 1;
	[...th.parentElement.children].forEach((h) => h.setAttribute('aria-sort', 'none'));
	th.setAttribute('aria-sort', dir === 1 ? 'ascending' : 'descending');
	const key = (tr) => {
		const t = tr.children[i]?.textContent.trim() ?? '';
		const n = parseFloat(t.replace(/[,%]/g, ''));
		return Number.isFinite(n) && /^[\d,.\s%/]+/.test(t) ? n : t.toLowerCase();
	};
	const body = tableEl.tBodies[0];
	[...body.rows].sort((a, b) => (key(a) > key(b) ? 1 : key(a) < key(b) ? -1 : 0) * dir).forEach((r) => body.append(r));
}

/* ---------------- glossary ---------------- */
function filterGlossary() {
	const q = $('#glossary-query').value.trim().toLowerCase(), c = $('#glossary-category').value;
	$$('.glossterm').forEach((el) => (el.hidden = !!((c && el.dataset.category !== c) || (q && !el.textContent.toLowerCase().includes(q)))));
}
$('#glossary-query').oninput = filterGlossary;
$('#glossary-category').onchange = filterGlossary;

/* ---------------- downloads ---------------- */
function download(text, name, type) {
	const url = URL.createObjectURL(new Blob([text], { type })), a = document.createElement('a');
	a.href = url;
	a.download = name;
	document.body.append(a);
	a.click();
	a.remove();
	setTimeout(() => URL.revokeObjectURL(url), 5000);
	toast('Download prepared: ' + name);
}
const csvCell = (x) => '"' + (typeof x === 'object' && x !== null ? JSON.stringify(x) : String(x ?? '')).replace(/"/g, '""') + '"';
$('#download-json').onclick = () =>
	download(JSON.stringify({ title: D.title, generated: D.generated, fields: D.fields, analysis: D.analysis, sources: D.sources }, null, 1), D.slug + '.json', 'application/json');
$('#download-csv').onclick = () => {
	const keys = ['field', 'column_or_table', 'entity', 'type', 'unit', 'values_present', 'of', 'counted', 'cases_present', 'cases_total', 'definition', 'codes', 'missing_markers', 'sources'];
	const rows = [];
	for (const f of D.fields)
		for (const p of P) {
			const x = f.projects[p];
			if (!x) continue;
			const c = x.cov || {};
			rows.push([f.name, p, f.entity, f.type, f.unit, c.n, c.total, c.unit, c.cases_n, c.cases_total, f.def, x.codes.map((k) => ({ code: k.code, n: k.n })), x.missing, f.sources.map((s) => D.sources[s]?.n || s).join(' ')]);
		}
	for (const a of D.analysis) rows.push([a.name, a.table, '', a.type, a.unit, '', '', '', '', '', a.def, a.codes.map((k) => ({ code: k.code, n: k.n })), a.missing, a.sources.map((s) => D.sources[s]?.n || s).join(' ')]);
	download([keys.map(csvCell).join(','), ...rows.map((r) => r.map(csvCell).join(','))].join('\r\n') + '\r\n', D.slug + '_fields.csv', 'text/csv');
};

/* ---------------- events ---------------- */
document.addEventListener('click', (ev) => {
	const t = ev.target.closest('button,a,th');
	if (!t) return;
	if (t.dataset.field) openField(t.dataset.field);
	if (t.dataset.goto) navigate(t.dataset.goto);
	if (t.dataset.img !== undefined) openImage(t);
	if (t.dataset.preset) setPreset(t.dataset.preset);
	if (t.dataset.apreset) {
		as.preset = t.dataset.apreset;
		$$('#analysis-presets .btn').forEach((b) => b.classList.toggle('selected', b.dataset.apreset === as.preset));
		renderAnalysis();
	}
	if (t.dataset.copy) copyText(t.dataset.copy);
	if (t.dataset.fsort) {
		fs.dir = fs.sort === t.dataset.fsort ? -fs.dir : 1;
		fs.sort = t.dataset.fsort;
		renderFields();
	} else if (t.tagName === 'TH' && t.closest('table.static-sort')) sortStatic(t);
	const href = t.getAttribute && t.getAttribute('href');
	if (href && href.startsWith('#') && href.length > 1) {
		ev.preventDefault();
		navigate(decodeURIComponent(href.slice(1)));
	}
});
document.addEventListener('keydown', (ev) => {
	if (ev.key === 'Escape') {
		$('#search-results').hidden = true;
		$('#global-search').setAttribute('aria-expanded', 'false');
		$('#sidebar').classList.remove('open');
	}
	if (ev.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName) && !$('#field-dialog').open && !$('#image-dialog').open) {
		ev.preventDefault();
		$('#global-search').focus();
	}
	const th = ev.target.closest && ev.target.closest('th.sortable');
	if (th && ['Enter', ' '].includes(ev.key)) {
		ev.preventDefault();
		th.click();
	}
});
document.addEventListener('click', (ev) => {
	if (!ev.target.closest('#search-results') && !ev.target.closest('.searchwrap')) $('#search-results').hidden = true;
});

renderFields();
renderAnalysis();
if (location.hash.length > 1) setTimeout(() => navigate(decodeURIComponent(location.hash.slice(1))), 50);
