/**
 * Filtering, sorting and URL state for the dataset explorer.
 *
 * Pure functions with no DOM: the page renders every entry at build time, the
 * browser script decides which ones to show, and the tests check the rules
 * that matter (unknown values never sort as zero, state survives the URL).
 */

export type FacetKey =
	| 'species'
	| 'disease'
	| 'modality'
	| 'task'
	| 'annotations'
	| 'pairing'
	| 'access'
	| 'docs';

export const FACET_KEYS: FacetKey[] = [
	'species',
	'disease',
	'modality',
	'task',
	'annotations',
	'pairing',
	'access',
	'docs',
];

export const FACET_LABELS: Record<FacetKey, string> = {
	species: 'Species',
	disease: 'Disease',
	modality: 'Modality',
	task: 'Research task',
	annotations: 'Annotations',
	pairing: 'Pairing',
	access: 'Access',
	docs: 'Documentation',
};

export interface ExplorerEntry {
	/** Release id: what the comparison tray and /compare/ work with. */
	id: string;
	slug: string;
	name: string;
	aliases: string[];
	summary: string;
	release: string;
	href: string;
	/** null when the patient count is unknown; never 0 as a stand-in. */
	patients: number | null;
	/** Epoch milliseconds, or null when the record has no verification date. */
	verified: number | null;
	facets: Record<FacetKey, string[]>;
	/** A permitted preview image, where one exists for this release. */
	preview: { src: string; alt: string } | null;
}

export type SortKey =
	| 'name-asc'
	| 'name-desc'
	| 'verified-desc'
	| 'verified-asc'
	| 'patients-desc'
	| 'patients-asc';

export const SORTS: { key: SortKey; label: string }[] = [
	{ key: 'name-asc', label: 'Name (A–Z)' },
	{ key: 'name-desc', label: 'Name (Z–A)' },
	{ key: 'verified-desc', label: 'Last verified (newest)' },
	{ key: 'verified-asc', label: 'Last verified (oldest)' },
	{ key: 'patients-desc', label: 'Patients (most first)' },
	{ key: 'patients-asc', label: 'Patients (fewest first)' },
];

export type View = 'cards' | 'table';

export interface ExplorerState {
	q: string;
	filters: Record<FacetKey, string[]>;
	sort: SortKey;
	view: View;
}

export const DEFAULT_SORT: SortKey = 'name-asc';
export const DEFAULT_VIEW: View = 'cards';

export function emptyFilters(): Record<FacetKey, string[]> {
	const filters = {} as Record<FacetKey, string[]>;
	for (const key of FACET_KEYS) filters[key] = [];
	return filters;
}

export const defaultState = (): ExplorerState => ({
	q: '',
	filters: emptyFilters(),
	sort: DEFAULT_SORT,
	view: DEFAULT_VIEW,
});

const searchText = (entry: ExplorerEntry) =>
	[entry.name, ...entry.aliases, entry.summary, entry.release].join(' ').toLowerCase();

/** Every word typed must appear somewhere in the entry. */
export function matchesQuery(entry: ExplorerEntry, query: string): boolean {
	const words = query.toLowerCase().split(/\s+/).filter(Boolean);
	if (words.length === 0) return true;
	const haystack = searchText(entry);
	return words.every((word) => haystack.includes(word));
}

/** Within a facet the selected values are alternatives; across facets they all apply. */
export function matchesFilters(entry: ExplorerEntry, filters: Record<FacetKey, string[]>): boolean {
	return FACET_KEYS.every((key) => {
		const selected = filters[key];
		if (!selected || selected.length === 0) return true;
		return selected.some((value) => entry.facets[key].includes(value));
	});
}

export const matches = (entry: ExplorerEntry, state: ExplorerState): boolean =>
	matchesQuery(entry, state.q) && matchesFilters(entry, state.filters);

/**
 * Unknown values sort last whichever direction is chosen: a dataset whose
 * patient count is undocumented is not the smallest, it is unknown.
 */
function compareUnknownLast(a: number | null, b: number | null, direction: 1 | -1): number {
	if (a === null && b === null) return 0;
	if (a === null) return 1;
	if (b === null) return -1;
	return (a - b) * direction;
}

export function sortEntries(entries: ExplorerEntry[], sort: SortKey): ExplorerEntry[] {
	const byName = (a: ExplorerEntry, b: ExplorerEntry) => a.name.localeCompare(b.name);
	const sorted = [...entries];
	switch (sort) {
		case 'name-desc':
			return sorted.sort((a, b) => byName(b, a));
		case 'verified-desc':
			return sorted.sort((a, b) => compareUnknownLast(a.verified, b.verified, -1) || byName(a, b));
		case 'verified-asc':
			return sorted.sort((a, b) => compareUnknownLast(a.verified, b.verified, 1) || byName(a, b));
		case 'patients-desc':
			return sorted.sort((a, b) => compareUnknownLast(a.patients, b.patients, -1) || byName(a, b));
		case 'patients-asc':
			return sorted.sort((a, b) => compareUnknownLast(a.patients, b.patients, 1) || byName(a, b));
		default:
			return sorted.sort(byName);
	}
}

/** Only what differs from the default is written to the address bar. */
export function stateToParams(state: ExplorerState): URLSearchParams {
	const params = new URLSearchParams();
	if (state.q.trim()) params.set('q', state.q.trim());
	for (const key of FACET_KEYS) {
		for (const value of state.filters[key]) params.append(key, value);
	}
	if (state.sort !== DEFAULT_SORT) params.set('sort', state.sort);
	if (state.view !== DEFAULT_VIEW) params.set('view', state.view);
	return params;
}

export function paramsToState(params: URLSearchParams): ExplorerState {
	const filters = emptyFilters();
	for (const key of FACET_KEYS) filters[key] = params.getAll(key);
	const sort = params.get('sort') as SortKey | null;
	const view = params.get('view') as View | null;
	return {
		q: params.get('q') ?? '',
		filters,
		sort: SORTS.some((option) => option.key === sort) ? sort! : DEFAULT_SORT,
		view: view === 'table' || view === 'cards' ? view : DEFAULT_VIEW,
	};
}

/**
 * Drop facet values that are not present in the visible catalog. URL state is
 * untrusted input; unknown values must never reach the rendered filter chips.
 */
export function sanitizeState(
	state: ExplorerState,
	allowedValues: Record<FacetKey, ReadonlySet<string>>,
): ExplorerState {
	return {
		...state,
		filters: Object.fromEntries(
			FACET_KEYS.map((key) => [
				key,
				state.filters[key].filter((value) => allowedValues[key].has(value)),
			]),
		) as Record<FacetKey, string[]>,
	};
}

export const activeFilterCount = (state: ExplorerState): number =>
	FACET_KEYS.reduce((total, key) => total + state.filters[key].length, 0);

/** The comparison tray holds at most four releases. */
export const MAX_COMPARE = 4;

export function toggleCompare(selected: string[], id: string): string[] {
	if (selected.includes(id)) return selected.filter((entry) => entry !== id);
	if (selected.length >= MAX_COMPARE) return selected;
	return [...selected, id];
}
