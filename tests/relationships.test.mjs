import { strict as assert } from 'node:assert';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import { studyUseTarget } from '../src/lib/study-use-target.ts';

test('the KiTS21 challenge paper targets the KiTS21 release', () => {
	const uses = JSON.parse(readFileSync(new URL('../src/data/study-uses/seed.json', import.meta.url), 'utf8'));
	const relationship = uses.find((entry) => entry.id === 'use-kits21-challenge');
	assert.ok(relationship);
	assert.equal(relationship.release, 'kits21');
});

test('release links use dataset slugs rather than dataset ids', () => {
	const target = studyUseTarget(
		{ release: 'release-id', externalCohort: null },
		{
			datasetSlug: 'actual-route-slug',
			datasetName: 'Example dataset',
			releaseId: 'release-id',
			versionLabel: 'v2',
		},
	);
	assert.equal(target.path, '/datasets/actual-route-slug/releases/release-id/');
});

test('private external cohorts receive labels but no dataset routes', () => {
	const target = studyUseTarget({
		release: null,
		externalCohort: { name: 'Private hospital cohort' },
	});
	assert.deepEqual(target, { label: 'Private hospital cohort', path: null });
});
