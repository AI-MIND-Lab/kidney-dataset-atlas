/**
 * Comparison rules.
 *
 * The hard rule here: unknown is never turned into "no". Two releases that
 * both fail to document something are not thereby the same, so a row where
 * every value is unknown is not treated as agreement.
 */
// Explicit extension: Node runs these modules directly in the tests, and its
// type stripping does not guess extensions the way a bundler does.
import { toCsv, type CsvRow } from './csv.ts';

export interface CompareCell {
	text: string;
	/** True when the value is any flavour of unknown rather than a fact. */
	unknown: boolean;
}

export interface CompareEntry {
	id: string;
	name: string;
	release: string;
	href: string;
	cells: Record<string, CompareCell>;
}

export const COMPARE_ROWS: { key: string; label: string }[] = [
	{ key: 'release', label: 'Release' },
	{ key: 'releaseDate', label: 'Release date' },
	{ key: 'species', label: 'Species' },
	{ key: 'patients', label: 'Patients' },
	{ key: 'examinations', label: 'Examinations' },
	{ key: 'lesions', label: 'Lesions' },
	{ key: 'slices', label: 'Slices' },
	{ key: 'slides', label: 'Slides' },
	{ key: 'images', label: 'Images' },
	{ key: 'patches', label: 'Patches' },
	{ key: 'records', label: 'Records' },
	{ key: 'disease', label: 'Disease' },
	{ key: 'modalities', label: 'Modalities' },
	{ key: 'annotations', label: 'Annotations' },
	{ key: 'annotationProvenance', label: 'Annotations made by' },
	{ key: 'ctPhases', label: 'CT phases' },
	{ key: 'wsi', label: 'Whole-slide images' },
	{ key: 'clinicalData', label: 'Clinical information' },
	{ key: 'followUp', label: 'Follow-up' },
	{ key: 'pairing', label: 'Verified pairing' },
	{ key: 'dictionary', label: 'Dictionary coverage' },
	{ key: 'access', label: 'Access' },
	{ key: 'license', label: 'Licence' },
	{ key: 'verified', label: 'Last verified' },
	{ key: 'limitations', label: 'Limitations' },
	{ key: 'overlap', label: 'Known overlap' },
	{ key: 'relations', label: 'Related collections' },
];

export const MAX_COMPARE = 4;

/**
 * Selection from a URL, split into what exists and what does not, so a
 * retired or mistyped id is reported rather than silently dropped.
 */
export function parseSelection(param: string | null, validIds: string[]): { selected: string[]; missing: string[] } {
	const wanted = (param ?? '')
		.split(',')
		.map((id) => id.trim())
		.filter(Boolean);
	const seen = new Set<string>();
	const selected: string[] = [];
	const missing: string[] = [];
	for (const id of wanted) {
		if (seen.has(id)) continue;
		seen.add(id);
		if (validIds.includes(id)) {
			if (selected.length < MAX_COMPARE) selected.push(id);
		} else {
			missing.push(id);
		}
	}
	return { selected, missing };
}

/**
 * Rows where the entries actually disagree. A row of unknowns is not
 * agreement, and a known value never counts as equal to an unknown one.
 */
export function differingRows(entries: CompareEntry[]): Set<string> {
	const differing = new Set<string>();
	if (entries.length < 2) return differing;

	for (const { key } of COMPARE_ROWS) {
		const cells = entries.map((entry) => entry.cells[key]);
		const anyUnknown = cells.some((cell) => cell?.unknown);
		const values = new Set(cells.map((cell) => cell?.text ?? ''));
		if (anyUnknown || values.size > 1) differing.add(key);
	}
	return differing;
}

export function visibleRows(entries: CompareEntry[], differencesOnly: boolean) {
	if (!differencesOnly) return COMPARE_ROWS;
	const differing = differingRows(entries);
	return COMPARE_ROWS.filter((row) => differing.has(row.key));
}

export function compareCsv(entries: CompareEntry[], rows = COMPARE_ROWS): string {
	const header = ['field', ...entries.map((entry) => `${entry.name} (${entry.id})`)];
	const body: CsvRow[] = rows.map((row) => [row.label, ...entries.map((entry) => entry.cells[row.key]?.text ?? '')]);
	return toCsv(header, body);
}
