/** Site-wide constants and URL helpers. */

export const SITE = {
	title: 'Kidney Dataset Atlas',
	description:
		'Curated catalogue of open kidney research datasets.',
	/** Only the deliberate Pages deployment sets this; other builds stay out of search engines. */
	isPublic: import.meta.env.SITE_PUBLIC === 'true',
	usingFixtures: import.meta.env.ATLAS_FIXTURES === '1',
	/**
	 * Local review mode: includes records a curator has not approved yet, so
	 * they can be read as pages before being published. Every page is marked,
	 * and the output check refuses a build carrying that mark without this flag.
	 */
	showingDrafts: import.meta.env.ATLAS_DRAFTS === '1',
	repoUrl: 'https://github.com/AI-MIND-Lab/kidney-dataset-atlas',
};

export const NAV = [
	{ href: '/', label: 'Datasets' },
	{ href: '/papers/', label: 'Papers' },
	{ href: '/compare/', label: 'Compare' },
	{ href: '/about/', label: 'About' },
	{ href: '/contribute/', label: 'Contribute' },
];

/**
 * Prefix an internal path with the configured base path. Every internal link,
 * asset, download and search URL must go through this so the site works under
 * a repository sub-path.
 */
export function withBase(path: string): string {
	const base = import.meta.env.BASE_URL;
	const trimmedBase = base.endsWith('/') ? base.slice(0, -1) : base;
	const suffix = path.startsWith('/') ? path : `/${path}`;
	return `${trimmedBase}${suffix}` || '/';
}

/** Absolute URL for canonical links, built from the configured site URL. */
export function absoluteUrl(path: string): string {
	return new URL(withBase(path), import.meta.env.SITE ?? 'http://localhost:4321').href;
}

export function datasetPath(slug: string): string {
	return `/datasets/${slug}/`;
}

export function releasePath(slug: string, releaseId: string): string {
	return `/datasets/${slug}/releases/${releaseId}/`;
}

export function paperPath(slug: string): string {
	return `/papers/${slug}/`;
}
