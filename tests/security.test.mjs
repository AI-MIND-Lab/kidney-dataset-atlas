import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import { safeJson } from '../src/lib/safe-json.ts';
import { emptyFilters, paramsToState, sanitizeState, DEFAULT_SORT, DEFAULT_VIEW } from '../src/lib/explorer.ts';
import { compareCsv } from '../src/lib/compare.ts';
import { escapeField } from '../src/lib/csv.ts';

test('embedded JSON escapes script terminators and HTML-significant characters', () => {
	const payload = {
		name: '</script><script>globalThis.pwned=true</script>',
		query: '<img src=x onerror=alert(1)> &    ',
	};
	const serialized = safeJson(payload);
	assert.equal(serialized.includes('</script>'), false);
	assert.equal(serialized.includes('<'), false);
	assert.equal(serialized.includes('>'), false);
	assert.deepEqual(JSON.parse(serialized), payload);
});

test('a record name carrying markup survives serialisation without becoming markup', () => {
	// Records are reviewed, but a page must not depend on that review to be safe.
	const entry = { name: '<b onmouseover="steal()">KiTS23</b>', summary: 'Ends with </SCRIPT >' };
	const serialized = safeJson([entry]);
	assert.equal(/<\/?[a-z]/i.test(serialized), false);
	assert.deepEqual(JSON.parse(serialized), [entry]);
});

test('filter values that are not in the catalog are dropped before rendering', () => {
	const allowed = {
		species: new Set(['human']),
		disease: new Set(['renal_tumor']),
		modality: new Set(['ct']),
		task: new Set(['segmentation']),
		annotations: new Set(['segmentation_masks']),
		pairing: new Set(['none']),
		access: new Set(['direct_open_download']),
		docs: new Set(['partial']),
	};
	const hostile = new URLSearchParams(
		'modality=ct&modality=<img src=x onerror=alert(1)>&species=" onload="alert(1)&disease=renal_tumor&disease=__proto__',
	);

	const state = sanitizeState(paramsToState(hostile), allowed);

	assert.deepEqual(state.filters.modality, ['ct']);
	assert.deepEqual(state.filters.species, []);
	assert.deepEqual(state.filters.disease, ['renal_tumor']);
});

test('an unknown sort or view in the URL falls back to the default instead of being echoed', () => {
	const state = paramsToState(new URLSearchParams('sort=<script>&view=javascript:alert(1)'));
	assert.equal(state.sort, DEFAULT_SORT);
	assert.equal(state.view, DEFAULT_VIEW);
});

test('a query string is carried as data, never interpreted', () => {
	const state = paramsToState(new URLSearchParams('q=%3Cscript%3Ealert(1)%3C%2Fscript%3E'));
	// The value is preserved verbatim for searching; escaping belongs to the renderer,
	// which uses textContent, and to safeJson for embedded blocks.
	assert.equal(state.q, '<script>alert(1)</script>');
	assert.equal(safeJson({ q: state.q }).includes('<'), false);
	assert.deepEqual(state.filters, emptyFilters());
});

test('a comparison export neutralises cells a spreadsheet would execute', () => {
	const entries = [
		{
			id: 'a',
			name: '=HYPERLINK("http://evil","click")',
			release: 'v1',
			href: '/datasets/a/',
			cells: { release: { text: '@SUM(1)', unknown: false } },
		},
		{
			id: 'b',
			name: 'Plain',
			release: 'v1',
			href: '/datasets/b/',
			cells: { release: { text: '-5', unknown: false } },
		},
	];

	const csv = compareCsv(entries, [{ key: 'release', label: 'Release' }]);
	assert.match(csv, /"'=HYPERLINK/);
	assert.match(csv, /'@SUM\(1\)/);
	// A negative number is a number, not a formula.
	assert.equal(escapeField(-5), '-5');
	assert.match(csv, /,-5$/);
});
