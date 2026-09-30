import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import yaml from 'js-yaml';
import { dataset, paper, release } from '../src/lib/schemas.mjs';
import { datasetRecord, paperRecord, releaseRecord } from '../scripts/new-record.mjs';

const frontmatter = (text) => yaml.load(text.split('---\n')[1]);

test('a new dataset skeleton is a valid record', () => {
	const record = frontmatter(datasetRecord({ id: 'new-set', name: 'New "quoted" set', url: 'https://example.org/set' }));
	assert.equal(dataset.safeParse(record).success, true);
	assert.equal(record.name, 'New "quoted" set');
});

test('a new release skeleton is a valid draft with every eligibility check unknown', () => {
	const record = yaml.load(releaseRecord({ id: 'new-set-v1', dataset: 'new-set', label: 'Version 1', by: 'someone' }));
	const parsed = release.safeParse(record);
	assert.equal(parsed.success, true, JSON.stringify(parsed.error?.issues));
	assert.equal(record.catalogStatus, 'draft');
	assert.equal(record.approvedBy, null);
	assert.ok(Object.values(record.eligibility).every((check) => check.status === 'unknown'));
});

test('a new paper skeleton is a valid draft', () => {
	const record = frontmatter(paperRecord({ id: 'new-paper', title: 'A title: with a colon' }));
	assert.equal(paper.safeParse(record).success, true);
	assert.equal(record.catalogStatus, 'draft');
});
