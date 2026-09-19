/**
 * Queries over the catalog records.
 *
 * Every page reads from here, so counts and relationships have exactly one
 * source. Drafts are filtered out at this boundary: nothing downstream needs
 * to remember to exclude them.
 */
import { getCollection, type CollectionEntry } from 'astro:content';
import type { z } from 'astro/zod';
import { overlap, qualityFinding, sample, source, studyUse, variable } from './schemas.mjs';
import { FACET_KEYS, type ExplorerEntry, type FacetKey } from './explorer';
import { datasetPath, SITE } from './site';

export type Dataset = CollectionEntry<'datasets'>;
export type Release = CollectionEntry<'releases'>;
export type Paper = CollectionEntry<'papers'>;

export type Variable = z.infer<typeof variable>;
export type StudyUse = z.infer<typeof studyUse>;
export type Sample = z.infer<typeof sample>;
export type QualityFinding = z.infer<typeof qualityFinding>;
export type Source = z.infer<typeof source>;
export type Overlap = z.infer<typeof overlap>;

/** A dataset with its published releases, newest first. */
export interface DatasetWithReleases {
	dataset: Dataset;
	releases: Release[];
	current: Release;
}

const isPublished = (entry: { data: { catalogStatus: string } }) => entry.data.catalogStatus === 'published';

type JsonModules = Record<string, unknown>;

const realData: Record<string, JsonModules> = {
	variables: import.meta.glob('../data/variables/*.json', { eager: true, import: 'default' }),
	'study-uses': import.meta.glob('../data/study-uses/*.json', { eager: true, import: 'default' }),
	samples: import.meta.glob('../data/samples/*.json', { eager: true, import: 'default' }),
	quality: import.meta.glob('../data/quality/*.json', { eager: true, import: 'default' }),
	sources: import.meta.glob('../data/sources/*.json', { eager: true, import: 'default' }),
	overlap: import.meta.glob('../data/overlap/*.json', { eager: true, import: 'default' }),
};

const fixtureData: Record<string, JsonModules> = {
	variables: import.meta.glob('../../tests/fixtures/data/variables/*.json', { eager: true, import: 'default' }),
	'study-uses': import.meta.glob('../../tests/fixtures/data/study-uses/*.json', { eager: true, import: 'default' }),
	samples: import.meta.glob('../../tests/fixtures/data/samples/*.json', { eager: true, import: 'default' }),
	quality: import.meta.glob('../../tests/fixtures/data/quality/*.json', { eager: true, import: 'default' }),
	sources: import.meta.glob('../../tests/fixtures/data/sources/*.json', { eager: true, import: 'default' }),
	overlap: import.meta.glob('../../tests/fixtures/data/overlap/*.json', { eager: true, import: 'default' }),
};

function loadData<T>(dir: string, schema: { parse: (input: unknown) => T }): T[] {
	const modules = SITE.usingFixtures ? fixtureData[dir] : realData[dir];
	const records: T[] = [];
	for (const contents of Object.values(modules ?? {})) {
		for (const record of contents as unknown[]) {
			records.push(schema.parse(record));
		}
	}
	return records;
}

let cache: {
	variables?: Variable[];
	studyUses?: StudyUse[];
	samples?: Sample[];
	quality?: QualityFinding[];
	sources?: Source[];
	overlaps?: Overlap[];
} = {};

export const allVariables = () => (cache.variables ??= loadData('variables', variable));
export const allStudyUses = () => (cache.studyUses ??= loadData('study-uses', studyUse));
export const allSamples = () => (cache.samples ??= loadData('samples', sample));
export const allQuality = () => (cache.quality ??= loadData('quality', qualityFinding));
export const allSources = () => (cache.sources ??= loadData('sources', source));
export const allOverlaps = () => (cache.overlaps ??= loadData('overlap', overlap));

/** Published releases only, newest first within each dataset. */
export async function publishedReleases(): Promise<Release[]> {
	const releases = await getCollection('releases', isPublished);
	return releases.sort(byReleaseRecency);
}

function byReleaseRecency(a: Release, b: Release): number {
	const aDate = a.data.releaseDate?.getTime() ?? 0;
	const bDate = b.data.releaseDate?.getTime() ?? 0;
	if (aDate !== bDate) return bDate - aDate;
	return b.data.versionLabel.localeCompare(a.data.versionLabel);
}

/**
 * Datasets that have at least one published release. A dataset with only draft
 * releases has nothing to show, so it stays out of the catalog entirely.
 */
export async function catalog(): Promise<DatasetWithReleases[]> {
	const [datasets, releases] = await Promise.all([getCollection('datasets'), publishedReleases()]);
	const entries: DatasetWithReleases[] = [];
	for (const dataset of datasets) {
		const own = releases.filter((release) => release.data.dataset === dataset.data.id);
		if (own.length === 0) continue;
		entries.push({ dataset, releases: own, current: own[0]! });
	}
	return entries.sort((a, b) => a.dataset.data.name.localeCompare(b.dataset.data.name));
}

/** The newest published release of a dataset, or undefined if it has none. */
export async function currentRelease(datasetId: string): Promise<Release | undefined> {
	const releases = await publishedReleases();
	return releases.find((release) => release.data.dataset === datasetId);
}

export async function publishedPapers(): Promise<Paper[]> {
	const papers = await getCollection('papers', isPublished);
	return papers.sort((a, b) => (b.data.year ?? 0) - (a.data.year ?? 0));
}

export const variablesForRelease = (releaseId: string) =>
	allVariables().filter((entry) => entry.release === releaseId);

export const samplesForRelease = (releaseId: string) => allSamples().filter((entry) => entry.release === releaseId);

export const qualityForRelease = (releaseId: string) => allQuality().filter((entry) => entry.release === releaseId);

export const studyUsesForRelease = (releaseId: string) =>
	allStudyUses().filter((entry) => entry.release === releaseId);

export const studyUsesForPaper = (paperId: string) => allStudyUses().filter((entry) => entry.paper === paperId);

export const sourceById = (id: string) => allSources().find((entry) => entry.id === id);

export async function paperById(id: string): Promise<Paper | undefined> {
	const papers = await publishedPapers();
	return papers.find((paper) => paper.data.id === id);
}

/** Patient count when it is known; null keeps unknown out of sorting and sums. */
export function patientCount(release: Release): number | null {
	const patients = release.data.counts?.patients;
	return patients?.status === 'present' ? (patients.value ?? null) : null;
}

/** What the explorer can filter on, derived from the records themselves. */
function facetsFor(dataset: Dataset, release: Release): Record<FacetKey, string[]> {
	const pairing = release.data.pairing;
	const pairingValue = pairing.some((entry) => entry.status === 'present')
		? 'verified'
		: pairing.some((entry) => entry.status === 'not_documented')
			? 'not_documented'
			: 'none';

	return {
		disease: dataset.data.diseaseTags,
		modality: release.data.modalities,
		task: release.data.tasks,
		annotations: release.data.annotations.length > 0 ? release.data.annotations : ['not_documented'],
		pairing: [pairingValue],
		access: [release.data.access.mode],
		docs: [release.data.dictionary.completeness],
	};
}

/** One row per dataset, describing its current release. */
export async function explorerEntries(): Promise<ExplorerEntry[]> {
	const entries = await catalog();
	return entries.map(({ dataset, current }) => {
		const preview = samplesForRelease(current.data.id)[0];
		return {
		id: current.data.id,
		slug: dataset.data.slug,
		name: dataset.data.name,
		aliases: dataset.data.aliases,
		summary: dataset.data.summary,
		release: current.data.versionLabel,
		href: datasetPath(dataset.data.slug),
			patients: patientCount(current),
			verified: current.data.verifiedOn?.getTime() ?? null,
			facets: facetsFor(dataset, current),
			preview: preview ? { src: preview.assets[0]!.path, alt: preview.alt } : null,
		};
	});
}

/** The values that actually occur, so no filter offers an empty result. */
export function facetOptions(entries: ExplorerEntry[]): Record<FacetKey, string[]> {
	const options = Object.fromEntries(FACET_KEYS.map((key) => [key, new Set<string>()])) as Record<
		FacetKey,
		Set<string>
	>;
	for (const entry of entries) {
		for (const key of FACET_KEYS) {
			for (const value of entry.facets[key]) options[key].add(value);
		}
	}
	return Object.fromEntries(
		FACET_KEYS.map((key) => [key, [...options[key]].sort()]),
	) as Record<FacetKey, string[]>;
}
