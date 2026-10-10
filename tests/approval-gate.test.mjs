import { strict as assert } from 'node:assert';
import { spawnSync } from 'node:child_process';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { resolve } from 'node:path';

const root = resolve(fileURLToPath(new URL('../', import.meta.url)));

const runValidator = (contentRoot, dataRoot) =>
	spawnSync(process.execPath, ['scripts/validate.mjs'], {
		cwd: root,
		encoding: 'utf8',
		env: { ...process.env, ATLAS_CONTENT_ROOT: contentRoot, ATLAS_DATA_ROOT: dataRoot, ATLAS_FIXTURES: '' },
	});

test('a release cannot be published without a curator approval', () => {
	const result = runValidator('tests/bad-records/content', 'tests/bad-records/data');
	assert.equal(result.status, 1, 'validation should fail');
	assert.match(result.stderr, /is published but has no approvedBy/);
	assert.match(result.stderr, /eligibility check publicAccess is "unknown"/);
	assert.match(result.stderr, /passes deidentification without verified source evidence/);
});

test('publication graph rejects draft leaks, missing paper approval, and unverified cohort evidence', () => {
	const result = runValidator('tests/bad-records/content', 'tests/bad-records/data');
	assert.match(result.stderr, /paper "bad-public-paper" is published but has no approvedBy/);
	assert.match(result.stderr, /published release "bad-public-current-a" cites draft paper "bad-draft-paper"/);
	assert.match(result.stderr, /published paper "bad-public-paper" cites draft release "bad-draft-release"/);
	assert.match(result.stderr, /lacks verified external-cohort evidence/);
});

test('route, count, current-release, and study target invariants are enforced', () => {
	const result = runValidator('tests/bad-records/content', 'tests/bad-records/data');
	assert.match(result.stderr, /duplicate datasets slug "duplicate-route"/);
	assert.match(result.stderr, /count must use null/);
	assert.match(result.stderr, /present count requires a numeric value/);
	assert.match(result.stderr, /has 2 current published releases; expected exactly one/);
	assert.match(result.stderr, /Name exactly one target: a catalogued release or an external cohort/);
	assert.match(result.stderr, /release "bad-part-current" is a part of its dataset and cannot also be current/);
});

test('a preview quotes the provider only from a source it lists, and its image must exist', () => {
	const result = runValidator('tests/bad-records/content', 'tests/bad-records/data');
	assert.match(result.stderr, /sample "bad-sample-unlisted-quote" quotes diagnosis from source "bad-source", which its sources do not list/);
	assert.match(result.stderr, /sample "bad-sample-unlisted-quote" points at missing file public\/previews\/no-such-release\/no-such-image\.webp/);
});

test('a reference to a missing record fails validation', () => {
	const result = runValidator('tests/bad-records/content', 'tests/bad-records/data');
	assert.match(result.stderr, /points at missing datasets record "no-such-dataset"/);
});

test('a relationship must name exactly one collection on the other side', () => {
	const result = runValidator('tests/bad-records/content', 'tests/bad-records/data');
	assert.match(result.stderr, /relation "relation-pointing-nowhere" names nothing on the other side/);
	assert.match(
		result.stderr,
		/relation "relation-pointing-both-ways" names both a catalogued release and an external one/,
	);
});

test('a reproduced paper figure needs a reusable licence and an existing file', () => {
	const result = runValidator('tests/bad-records/content', 'tests/bad-records/data');
	assert.match(result.stderr, /bad-figure-licence\.md: figures\.0\.license\.url: A reproduced figure needs a reusable licence/);
	assert.match(result.stderr, /figure "bad-figure-absent" points at missing file public\/figures\/bad-figure-missing\/figure-1\.webp/);
});

test('the fixture catalog passes validation', () => {
	const result = runValidator('tests/fixtures/content', 'tests/fixtures/data');
	assert.equal(result.status, 0, result.stderr);
	assert.match(result.stdout, /All records valid/);
});
