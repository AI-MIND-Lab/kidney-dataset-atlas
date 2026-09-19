import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import {
	MAX_COMPARE,
	defaultState,
	emptyFilters,
	matches,
	paramsToState,
	sortEntries,
	stateToParams,
	toggleCompare,
} from '../src/lib/explorer.ts';

const entry = (overrides = {}) => ({
	id: 'r1',
	slug: 'd1',
	name: 'Alpha Collection',
	aliases: ['ALC'],
	summary: 'Renal tumour CT with masks.',
	release: 'v1',
	href: '/datasets/d1/',
	patients: 100,
	verified: Date.parse('2026-01-01'),
	facets: {
		disease: ['renal_tumor'],
		modality: ['ct'],
		task: ['segmentation'],
		annotations: ['segmentation_masks'],
		pairing: ['none'],
		access: ['open_download'],
		docs: ['partial'],
	},
	preview: null,
	...overrides,
});

const withFilters = (overrides) => ({ ...defaultState(), filters: { ...emptyFilters(), ...overrides } });

test('search matches names, abbreviations and descriptions', () => {
	const state = { ...defaultState(), q: 'alc' };
	assert.equal(matches(entry(), state), true);
	assert.equal(matches(entry(), { ...defaultState(), q: 'masks tumour' }), true);
	assert.equal(matches(entry(), { ...defaultState(), q: 'ultrasound' }), false);
});

test('values within one filter are alternatives, across filters they all apply', () => {
	assert.equal(matches(entry(), withFilters({ modality: ['ct', 'mri'] })), true);
	assert.equal(matches(entry(), withFilters({ modality: ['ct'], access: ['registration_required'] })), false);
	assert.equal(matches(entry(), withFilters({ modality: ['ct'], access: ['open_download'] })), true);
});

test('unknown patient counts sort last in both directions', () => {
	const entries = [
		entry({ id: 'unknown', name: 'B unknown', patients: null }),
		entry({ id: 'small', name: 'C small', patients: 10 }),
		entry({ id: 'big', name: 'A big', patients: 900 }),
	];

	assert.deepEqual(
		sortEntries(entries, 'patients-desc').map((e) => e.id),
		['big', 'small', 'unknown'],
	);
	assert.deepEqual(
		sortEntries(entries, 'patients-asc').map((e) => e.id),
		['small', 'big', 'unknown'],
	);
});

test('unknown verification dates also sort last', () => {
	const entries = [
		entry({ id: 'never', name: 'A', verified: null }),
		entry({ id: 'recent', name: 'B', verified: Date.parse('2026-09-01') }),
	];
	assert.deepEqual(
		sortEntries(entries, 'verified-desc').map((e) => e.id),
		['recent', 'never'],
	);
	assert.deepEqual(
		sortEntries(entries, 'verified-asc').map((e) => e.id),
		['recent', 'never'],
	);
});

test('state survives a round trip through the URL', () => {
	const state = {
		q: 'kidney ct',
		filters: { ...emptyFilters(), modality: ['ct', 'mri'], access: ['open_download'] },
		sort: 'patients-desc',
		view: 'table',
	};
	const restored = paramsToState(new URLSearchParams(stateToParams(state).toString()));
	assert.deepEqual(restored, state);
});

test('the default state leaves the address bar clean', () => {
	assert.equal(stateToParams(defaultState()).toString(), '');
});

test('an unknown sort in the URL falls back to the default', () => {
	const restored = paramsToState(new URLSearchParams('sort=by-vibes&view=grid'));
	assert.equal(restored.sort, 'name-asc');
	assert.equal(restored.view, 'cards');
});

test('the comparison tray holds at most four releases', () => {
	let selected = [];
	for (const id of ['a', 'b', 'c', 'd', 'e']) selected = toggleCompare(selected, id);
	assert.deepEqual(selected, ['a', 'b', 'c', 'd']);
	assert.equal(selected.length, MAX_COMPARE);

	selected = toggleCompare(selected, 'b');
	assert.deepEqual(selected, ['a', 'c', 'd']);
	selected = toggleCompare(selected, 'e');
	assert.deepEqual(selected, ['a', 'c', 'd', 'e']);
});
