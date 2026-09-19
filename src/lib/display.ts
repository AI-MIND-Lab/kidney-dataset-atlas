/**
 * Turning record values into text a reader can trust.
 *
 * "No", "not documented", "not verified" and "not applicable" stay distinct,
 * and an unknown number never renders as a number.
 */
import type { z } from 'astro/zod';
import type { count, state } from './schemas.mjs';

type State = z.infer<typeof state>;
type Count = z.infer<typeof count>;

const STATE_LABELS: Record<State, string> = {
	present: 'Yes',
	absent: 'No',
	not_documented: 'Not documented',
	not_verified: 'Not verified',
	not_applicable: 'Not applicable',
};

export const stateLabel = (value: State): string => STATE_LABELS[value];

/** Unknown counts say why they are unknown instead of showing a number. */
export function countLabel(value: Count | undefined): string {
	if (!value) return 'Not documented';
	if (value.status === 'present' && value.value !== null) return value.value.toLocaleString('en-US');
	return STATE_LABELS[value.status];
}

const ACCESS_LABELS: Record<string, string> = {
	open_download: 'Open download',
	registration_required: 'Registration required',
	restricted: 'Restricted',
};

export const accessLabel = (mode: string): string => ACCESS_LABELS[mode] ?? mode;

const COMPLETENESS_LABELS: Record<string, string> = {
	complete_for_inspected_release: 'Complete for the inspected release',
	partial: 'Partial',
	documentation_only: 'From documentation only',
};

export const completenessLabel = (value: string): string => COMPLETENESS_LABELS[value] ?? value;

const TRAIN_TEST_LABELS: Record<string, string> = {
	train: 'Training',
	test: 'Test',
	train_and_test: 'Training and test',
	validation: 'Validation',
	not_documented: 'Not documented',
};

export const trainTestLabel = (value: string): string => TRAIN_TEST_LABELS[value] ?? value;

/** Enum-ish values that read fine as plain words. */
export const humanize = (value: string): string => value.replace(/_/g, ' ').replace(/^\w/, (c) => c.toUpperCase());

export function dateLabel(value: Date | null | undefined): string {
	if (!value) return 'Not documented';
	return value.toLocaleDateString('en-GB', { year: 'numeric', month: 'long', day: 'numeric' });
}
