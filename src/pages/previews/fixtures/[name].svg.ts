import type { APIRoute, GetStaticPaths } from 'astro';
import { SITE } from '../../../lib/site';

/**
 * Synthetic preview images for interface work.
 *
 * These are drawings, not medical images, and they are generated only in a
 * fixture build: a normal build produces no routes here at all. Real previews
 * live in public/previews/ and appear only where reuse permission has been
 * checked for that specific image.
 */
const SLICES = 9;

export const getStaticPaths = (async () => {
	if (!SITE.usingFixtures) return [];
	const paths = [];
	for (let slice = 1; slice <= SLICES; slice++) {
		paths.push({ params: { name: `ct-image-${slice}` }, props: { slice, kind: 'image' as const } });
		paths.push({ params: { name: `ct-mask-${slice}` }, props: { slice, kind: 'mask' as const } });
	}
	paths.push({ params: { name: 'figure' }, props: { slice: 5, kind: 'figure' as const } });
	// The enlarged copy of the figure, so the viewer's "open large" path is exercised.
	paths.push({ params: { name: 'figure-large' }, props: { slice: 5, kind: 'figure' as const } });
	return paths;
}) satisfies GetStaticPaths;

/** Lesion grows towards the middle slice, so the slider visibly does something. */
const lesionRadius = (slice: number) => 10 + 26 * Math.sin((Math.PI * slice) / (SLICES + 1));

export const GET: APIRoute = ({ props }) => {
	const { slice, kind } = props as { slice: number; kind: 'image' | 'mask' | 'figure' };
	const radius = lesionRadius(slice);
	const cx = 150;
	const cy = 128 + (slice - 5) * 2;

	const body =
		kind === 'mask'
			? `<ellipse cx="${cx}" cy="${cy}" rx="${radius}" ry="${radius * 0.85}" fill="#e06c5a" />`
			: `<rect width="256" height="256" fill="#12161a"/>
			   <ellipse cx="128" cy="128" rx="110" ry="86" fill="#3a434c"/>
			   <ellipse cx="86" cy="128" rx="34" ry="46" fill="#5c6771"/>
			   <ellipse cx="${cx}" cy="${cy}" rx="34" ry="46" fill="#5c6771"/>
			   <ellipse cx="${cx}" cy="${cy}" rx="${radius}" ry="${radius * 0.85}" fill="#8d9aa6"/>
			   <text x="128" y="243" fill="#9aa7b3" font-family="monospace" font-size="13" text-anchor="middle">SYNTHETIC — NOT A DATASET IMAGE</text>
			   <text x="10" y="20" fill="#9aa7b3" font-family="monospace" font-size="12">${
						kind === 'figure' ? 'figure' : `slice ${slice}/${SLICES}`
					}</text>`;

	const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img">${body}</svg>`;

	return new Response(svg, { headers: { 'Content-Type': 'image/svg+xml; charset=utf-8' } });
};
