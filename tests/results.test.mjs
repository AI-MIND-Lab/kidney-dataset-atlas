import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import { groupResults } from '../src/lib/results.ts';

const result = (model, metric, value, extra = {}) => ({
	model,
	metric,
	value,
	units: null,
	confidenceInterval: null,
	subset: 'All three projects together',
	split: '4-fold cross-validation',
	evaluation: 'internal',
	...extra,
});

test('a result recorded against several releases becomes one row listing each release', () => {
	const joint = result('net', 'AUC', 0.98);
	const uses = [
		{ release: 'kirc', results: [joint] },
		{ release: 'kirp', results: [{ ...joint }] },
		{ release: 'kich', results: [{ ...joint }] },
	];
	const rows = groupResults(uses);
	assert.equal(rows.length, 1);
	assert.deepEqual(
		rows[0].uses.map((use) => use.release),
		['kirc', 'kirp', 'kich'],
	);
});

test('results that differ in anything a reader sees stay separate', () => {
	const uses = [
		{ release: 'a', results: [result('net', 'AUC', 0.98), result('net', 'Accuracy', 0.95)] },
		{ release: 'b', results: [result('net', 'AUC', 0.98, { evaluation: 'external' })] },
		{ release: 'c', results: [result('net', 'AUC', 0.98, { confidenceInterval: '95% CI 0.97-0.99' })] },
	];
	assert.equal(groupResults(uses).length, 4);
});

test('rows follow the given model order, keeping recorded order within a model', () => {
	const uses = [
		{
			release: 'a',
			results: [result('baseline', 'Dice', 0.8), result('proposed', 'Dice', 0.9), result('proposed', 'HD95', 3)],
		},
	];
	const rows = groupResults(uses, ['proposed', 'baseline']);
	assert.deepEqual(
		rows.map((row) => `${row.result.model} ${row.result.metric}`),
		['proposed Dice', 'proposed HD95', 'baseline Dice'],
	);
});
