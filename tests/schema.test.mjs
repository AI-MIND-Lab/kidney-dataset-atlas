import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import { count, recordId, studyUse } from '../src/lib/schemas.mjs';

test('record ids and route slugs reject markup and path syntax', () => {
	for (const value of ['../escape', 'Bad Uppercase', '</script>', 'two--hyphens']) {
		assert.equal(recordId.safeParse(value).success, false, value);
	}
	assert.equal(recordId.safeParse('safe-record-2').success, true);
});

test('count state and value must agree in both directions', () => {
	assert.equal(count.safeParse({ value: null, status: 'present' }).success, false);
	assert.equal(count.safeParse({ value: 12, status: 'not_documented' }).success, false);
	assert.equal(count.safeParse({ value: 12, status: 'present' }).success, true);
	assert.equal(count.safeParse({ value: null, status: 'not_verified' }).success, true);
});

test('a study use requires exactly one catalogued or external target', () => {
	const base = {
		id: 'one-use',
		paper: 'one-paper',
		role: 'downstream',
		actualUseEvidence: { sources: [], status: 'not_verified' },
		trainTestRole: 'not_documented',
		results: [],
	};
	assert.equal(studyUse.safeParse(base).success, false);
	assert.equal(studyUse.safeParse({ ...base, release: 'one-release' }).success, true);
	assert.equal(
		studyUse.safeParse({
			...base,
			externalCohort: {
				name: 'Private cohort',
				accessMode: 'private_institutional',
				evidence: { sources: [], status: 'not_verified' },
			},
		}).success,
		true,
	);
});
