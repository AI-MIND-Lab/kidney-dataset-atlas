import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import { count, paperFigure, recordId, studyUse } from '../src/lib/schemas.mjs';

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

test('a reproduced paper figure needs a reusable licence and a figures/ path', () => {
	const base = {
		id: 'fig-1',
		label: 'Figure 1',
		title: 'Overview',
		path: '/figures/some-paper/figure-1.webp',
		width: 800,
		height: 400,
		alt: 'A diagram',
		caption: 'Quoted caption.',
		credit: 'Author A. Title. Journal (2024), Figure 1.',
		license: { name: 'CC BY 4.0', url: 'https://creativecommons.org/licenses/by/4.0/' },
		changes: 'None.',
		source: 'https://doi.org/10.0000/example',
	};
	assert.equal(paperFigure.safeParse(base).success, true);
	const closed = { ...base, license: { name: 'All rights reserved', url: 'https://www.springernature.com/gp/researchers/text-and-data-mining' } };
	assert.equal(paperFigure.safeParse(closed).success, false);
	assert.equal(paperFigure.safeParse({ ...base, path: '/previews/some-paper/figure-1.webp' }).success, false);
});
