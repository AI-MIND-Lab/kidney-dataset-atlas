import { strict as assert } from 'node:assert';
import { test } from 'node:test';
import { dateLabel, facetValueLabel } from '../src/lib/display.ts';

test('a calendar date renders as the day it was written, in any time zone', () => {
	// Parsed as UTC midnight; formatting in a local zone west of Greenwich used
	// to render the day before, which quietly misdated every verification.
	assert.equal(dateLabel(new Date('2026-09-19')), '19 September 2026');
	assert.equal(dateLabel(new Date('2026-01-01')), '1 January 2026');
});

test('a missing date says so rather than showing a default', () => {
	assert.equal(dateLabel(null), 'Not documented');
	assert.equal(dateLabel(undefined), 'Not documented');
});

test('modality labels keep their usual capitalisation', () => {
	assert.equal(facetValueLabel('modality', 'ct'), 'CT');
	assert.equal(facetValueLabel('modality', 'mri'), 'MRI');
	assert.equal(facetValueLabel('modality', 'pathology'), 'Pathology');
	assert.equal(facetValueLabel('modality', 'clinical_table'), 'Clinical table');
});
