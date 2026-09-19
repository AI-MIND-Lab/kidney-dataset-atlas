import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import { MAX_COMPARE, compareCsv, differingRows, parseSelection, visibleRows } from '../src/lib/compare.ts';

const known = (text) => ({ text, unknown: false });
const unknown = (text) => ({ text, unknown: true });

const entry = (id, cells) => ({
	id,
	name: `Dataset ${id}`,
	release: 'v1',
	href: `/datasets/${id}/`,
	cells: { release: known('v1'), access: known('Open download'), ...cells },
});

test('two unknowns are not agreement', () => {
	const entries = [
		entry('a', { wsi: unknown('Not documented') }),
		entry('b', { wsi: unknown('Not documented') }),
	];
	assert.equal(differingRows(entries).has('wsi'), true);
});

test('a known value never counts as equal to an unknown one', () => {
	const entries = [entry('a', { wsi: known('Yes') }), entry('b', { wsi: unknown('Not documented') })];
	assert.equal(differingRows(entries).has('wsi'), true);
});

test('matching known values agree, and differences-only hides them', () => {
	const entries = [entry('a', { wsi: known('No') }), entry('b', { wsi: known('No') })];
	const differing = differingRows(entries);
	assert.equal(differing.has('wsi'), false);
	assert.equal(differing.has('access'), false);

	const rows = visibleRows(entries, true).map((row) => row.key);
	assert.equal(rows.includes('wsi'), false);
	assert.equal(rows.includes('access'), false);
});

test('a single selection has nothing to differ from', () => {
	assert.equal(differingRows([entry('a', {})]).size, 0);
	assert.equal(differingRows([]).size, 0);
});

test('a retired or mistyped id is reported, not silently dropped', () => {
	const { selected, missing } = parseSelection('alive,retired-release', ['alive']);
	assert.deepEqual(selected, ['alive']);
	assert.deepEqual(missing, ['retired-release']);
});

test('the selection is capped at four and de-duplicated', () => {
	const ids = ['a', 'b', 'c', 'd', 'e'];
	const { selected } = parseSelection('a,a,b,c,d,e', ids);
	assert.deepEqual(selected, ['a', 'b', 'c', 'd']);
	assert.equal(selected.length, MAX_COMPARE);
});

test('an empty or missing parameter selects nothing', () => {
	assert.deepEqual(parseSelection(null, ['a']), { selected: [], missing: [] });
	assert.deepEqual(parseSelection('', ['a']), { selected: [], missing: [] });
	assert.deepEqual(parseSelection(' , ', ['a']), { selected: [], missing: [] });
});

test('the CSV export names each release and keeps unknown text', () => {
	const entries = [entry('a', { wsi: known('Yes') }), entry('b', { wsi: unknown('Not documented') })];
	const csv = compareCsv(entries, [{ key: 'wsi', label: 'Whole-slide images' }]);
	assert.equal(csv, 'field,Dataset a (a),Dataset b (b)\r\nWhole-slide images,Yes,Not documented');
});
