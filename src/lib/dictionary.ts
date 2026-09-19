/**
 * Dictionary filtering, pagination and export rows.
 *
 * Kept free of the content layer so the browser and the tests can both use it.
 */
import type { z } from 'astro/zod';
import type { variable } from './schemas.mjs';
import type { CsvRow } from './csv';

export type Variable = z.infer<typeof variable>;

/** What the browser needs to filter a row it is already showing. */
export interface DictionaryIndexEntry {
	id: string;
	text: string;
	group: string;
	type: string;
	level: string;
}

export interface DictionaryFilters {
	q: string;
	group: string;
	type: string;
	level: string;
}

export const emptyFilters = (): DictionaryFilters => ({ q: '', group: '', type: '', level: '' });

export const PAGE_SIZE = 50;

export function indexEntry(entry: Variable): DictionaryIndexEntry {
	const coding = entry.coding.map((code) => `${code.code} ${code.meaning}`).join(' ');
	return {
		id: entry.id,
		text: [entry.originalName, entry.definition, entry.normalizedConcept ?? '', coding].join(' ').toLowerCase(),
		group: entry.group,
		type: entry.type,
		level: entry.observationLevel,
	};
}

export function matchesVariable(entry: DictionaryIndexEntry, filters: DictionaryFilters): boolean {
	const words = filters.q.toLowerCase().split(/\s+/).filter(Boolean);
	if (!words.every((word) => entry.text.includes(word))) return false;
	if (filters.group && entry.group !== filters.group) return false;
	if (filters.type && entry.type !== filters.type) return false;
	if (filters.level && entry.level !== filters.level) return false;
	return true;
}

export const pageCount = (total: number, pageSize = PAGE_SIZE) => Math.max(1, Math.ceil(total / pageSize));

/** Pages are 1-based and clamped, so a stale page number cannot empty the table. */
export function pageSlice<T>(items: T[], page: number, pageSize = PAGE_SIZE): T[] {
	const clamped = Math.min(Math.max(1, page), pageCount(items.length, pageSize));
	const start = (clamped - 1) * pageSize;
	return items.slice(start, start + pageSize);
}

/**
 * Exports carry their release and how complete the dictionary is, so a
 * downloaded file cannot be mistaken for the whole variable list.
 */
export interface ExportMeta {
	releaseId: string;
	completeness: string;
	inspectedScope: string;
}

export const DICTIONARY_HEADER = [
	'release_id',
	'dictionary_completeness',
	'inspected_scope',
	'variable_id',
	'original_name',
	'file',
	'definition',
	'type',
	'unit',
	'coding',
	'missing_values',
	'observation_level',
	'time_point',
	'role',
	'group',
	'derivation',
	'normalized_concept',
	'provenance',
	'evidence_status',
	'evidence_sources',
	'evidence_locator',
];

export function dictionaryRow(entry: Variable, meta: ExportMeta): CsvRow {
	return [
		meta.releaseId,
		meta.completeness,
		meta.inspectedScope,
		entry.id,
		entry.originalName,
		entry.file ?? '',
		entry.definition,
		entry.type,
		entry.unit ?? '',
		entry.coding.map((code) => `${code.code}=${code.meaning}`).join('; '),
		entry.missingValues.join('; '),
		entry.observationLevel,
		entry.timePoint ?? '',
		entry.role,
		entry.group,
		entry.derivation,
		entry.normalizedConcept ?? '',
		entry.provenance ?? '',
		entry.evidence?.status ?? 'not_verified',
		(entry.evidence?.sources ?? []).join('; '),
		entry.evidence?.locator ?? '',
	];
}
