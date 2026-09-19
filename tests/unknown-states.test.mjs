import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import { countLabel, stateLabel } from '../src/lib/display.ts';

test('an unknown count never renders as a number', () => {
	assert.equal(countLabel({ value: null, status: 'not_documented' }), 'Not documented');
	assert.equal(countLabel({ value: null, status: 'not_verified' }), 'Not verified');
	assert.equal(countLabel({ value: null, status: 'not_applicable' }), 'Not applicable');
	assert.equal(countLabel(undefined), 'Not documented');
});

test('a known count renders as a number', () => {
	assert.equal(countLabel({ value: 0, status: 'present' }), '0');
	assert.equal(countLabel({ value: 1489, status: 'present' }), '1,489');
});

test('"no" stays distinct from the three kinds of unknown', () => {
	const labels = ['absent', 'not_documented', 'not_verified', 'not_applicable'].map((value) =>
		stateLabel(value),
	);
	assert.deepEqual(labels, ['No', 'Not documented', 'Not verified', 'Not applicable']);
	assert.equal(new Set(labels).size, labels.length);
});
