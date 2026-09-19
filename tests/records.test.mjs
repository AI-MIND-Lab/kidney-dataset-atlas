import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import { collectSourceIds } from '../src/lib/records.ts';

test('sources are collected from nested evidence, without duplicates', () => {
	const release = {
		sources: ['docs-page'],
		counts: {
			patients: { value: 10, status: 'present', evidence: { sources: ['docs-page', 'paper'] } },
		},
		pairing: [{ status: 'not_documented', evidence: { sources: ['readme'] } }],
	};

	assert.deepEqual(collectSourceIds(release), ['docs-page', 'paper', 'readme']);
});

test('records with no sources yield nothing', () => {
	assert.deepEqual(collectSourceIds({ counts: {}, pairing: [] }), []);
	assert.deepEqual(collectSourceIds(null), []);
});

test('non-string entries in a sources array are ignored', () => {
	assert.deepEqual(collectSourceIds({ sources: ['ok', 42, null] }), ['ok']);
});
