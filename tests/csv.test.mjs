import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import { escapeField, guardFormula, toCsv } from '../src/lib/csv.ts';

test('a cell a spreadsheet would execute is neutralised', () => {
	assert.equal(guardFormula('=SUM(A1:A9)'), "'=SUM(A1:A9)");
	assert.equal(guardFormula('+1-800-CALL'), "'+1-800-CALL");
	assert.equal(guardFormula('@import'), "'@import");
	assert.equal(guardFormula('-lookup'), "'-lookup");
});

test('numbers, including negative ones, stay numbers', () => {
	assert.equal(guardFormula('-5'), '-5');
	assert.equal(guardFormula('-2.75'), '-2.75');
	assert.equal(escapeField(-5), '-5');
});

test('commas, quotes and line breaks survive quoting', () => {
	assert.equal(escapeField('Left, right'), '"Left, right"');
	assert.equal(escapeField('She said "no"'), '"She said ""no"""');
	assert.equal(escapeField('line one\nline two'), '"line one\nline two"');
	assert.equal(escapeField(' padded '), '" padded "');
});

test('empty values render as empty cells, not as "null"', () => {
	assert.equal(escapeField(null), '');
	assert.equal(escapeField(undefined), '');
	assert.equal(escapeField(''), '');
});

test('a guarded cell that also needs quoting gets both', () => {
	assert.equal(escapeField('=1,2'), `"'=1,2"`);
});

test('rows are joined with CRLF, as spreadsheets expect', () => {
	const csv = toCsv(['a', 'b'], [[1, 'two']]);
	assert.equal(csv, 'a,b\r\n1,two');
});
