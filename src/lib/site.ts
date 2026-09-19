/** Site-wide constants and URL helpers. */

export const SITE = {
	title: 'Kidney Dataset Atlas',
	description:
		'Explore open kidney research datasets, understand their variables, and discover the studies built with them.',
	/** The private phase is not published; keep the site out of search engines until it is. */
	isPublic: import.meta.env.SITE_PUBLIC === 'true',
	usingFixtures: import.meta.env.ATLAS_FIXTURES === '1',
	repoUrl: 'https://github.com/i-sababishraq/kidney-dataset-atlas',
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
