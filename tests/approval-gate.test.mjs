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
});

test('a reference to a missing record fails validation', () => {
	const result = runValidator('tests/bad-records/content', 'tests/bad-records/data');
	assert.match(result.stderr, /points at missing datasets record "no-such-dataset"/);
});

test('the fixture catalog passes validation', () => {
	const result = runValidator('tests/fixtures/content', 'tests/fixtures/data');
	assert.equal(result.status, 0, result.stderr);
	assert.match(result.stdout, /All records valid/);
});
