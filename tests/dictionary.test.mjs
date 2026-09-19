import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import {
	DICTIONARY_HEADER,
	dictionaryRow,
	emptyFilters,
	indexEntry,
	matchesVariable,
	pageCount,
	pageSlice,
} from '../src/lib/dictionary.ts';

const variable = (overrides = {}) => ({
	id: 'v1',
	release: 'r1',
	originalName: 'egfr_baseline',
	file: 'clinical.csv',
	definition: 'Estimated glomerular filtration rate at baseline.',
	type: 'decimal',
	unit: 'mL/min/1.73m2',
	coding: [],
	missingValues: ['NA'],
	observationLevel: 'patient',
	timePoint: 'baseline',
	role: 'predictor',
	group: 'clinical',
	derivation: 'derived',
	normalizedConcept: null,
	provenance: 'Provider documentation.',
	evidence: { sources: ['docs'], status: 'verified', locator: 'Table 1', verifiedOn: null },
	...overrides,
});

test('search covers names, meanings and coded values', () => {
	const entry = indexEntry(
		variable({ coding: [{ code: 'L', meaning: 'Left kidney' }], definition: 'Side of the lesion.' }),
	);
	assert.equal(matchesVariable(entry, { ...emptyFilters(), q: 'egfr' }), true);
	assert.equal(matchesVariable(entry, { ...emptyFilters(), q: 'left kidney' }), true);
	assert.equal(matchesVariable(entry, { ...emptyFilters(), q: 'tumour grade' }), false);
});

test('filters combine with the search', () => {
	const entry = indexEntry(variable());
	assert.equal(matchesVariable(entry, { ...emptyFilters(), group: 'clinical' }), true);
	assert.equal(matchesVariable(entry, { ...emptyFilters(), group: 'imaging' }), false);
	assert.equal(matchesVariable(entry, { ...emptyFilters(), q: 'egfr', level: 'slide' }), false);
});

test('paging is 1-based and a stale page cannot empty the table', () => {
	const items = Array.from({ length: 120 }, (_, index) => index);
	assert.equal(pageCount(120, 50), 3);
	assert.deepEqual(pageSlice(items, 1, 50).slice(0, 2), [0, 1]);
	assert.equal(pageSlice(items, 3, 50).length, 20);
	assert.deepEqual(pageSlice(items, 99, 50), pageSlice(items, 3, 50));
	assert.deepEqual(pageSlice(items, 0, 50), pageSlice(items, 1, 50));
});

test('an empty dictionary still reports one page', () => {
	assert.equal(pageCount(0, 50), 1);
	assert.deepEqual(pageSlice([], 1, 50), []);
});

test('an exported row carries its release and completeness', () => {
	const meta = { releaseId: 'r1', completeness: 'partial', inspectedScope: 'clinical.csv' };
	const row = dictionaryRow(variable(), meta);
	assert.equal(row.length, DICTIONARY_HEADER.length);
	assert.equal(row[DICTIONARY_HEADER.indexOf('release_id')], 'r1');
	assert.equal(row[DICTIONARY_HEADER.indexOf('dictionary_completeness')], 'partial');
	assert.equal(row[DICTIONARY_HEADER.indexOf('original_name')], 'egfr_baseline');
	assert.equal(row[DICTIONARY_HEADER.indexOf('evidence_sources')], 'docs');
});

test('unknown fields export as empty cells, not invented values', () => {
	const meta = { releaseId: 'r1', completeness: 'partial', inspectedScope: 'clinical.csv' };
	const row = dictionaryRow(variable({ unit: null, timePoint: null, provenance: undefined }), meta);
	assert.equal(row[DICTIONARY_HEADER.indexOf('unit')], '');
	assert.equal(row[DICTIONARY_HEADER.indexOf('time_point')], '');
	assert.equal(row[DICTIONARY_HEADER.indexOf('provenance')], '');
});
