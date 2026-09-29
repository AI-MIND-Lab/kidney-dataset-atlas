import type { APIRoute, GetStaticPaths } from 'astro';
import { SITE } from '../../../lib/site';

/**
 * A synthetic "architecture figure" for the fixture paper, so tests exercise the figure block on paper pages.
 *
 * It is a drawing of labelled boxes, not a figure from any real paper, and it is generated only in a fixture
 * build: a normal build produces no routes here, and scripts/check-output.mjs fails if one appears.
 */
export const getStaticPaths = (async () => (SITE.usingFixtures ? [{ params: { name: 'figure-1' } }] : [])) satisfies GetStaticPaths;

const box = (x: number, label: string) =>
	`<rect x="${x}" y="40" width="110" height="60" rx="6" fill="#e4f1ef" stroke="#0d6e66"/>` +
	`<text x="${x + 55}" y="75" font-family="sans-serif" font-size="13" text-anchor="middle" fill="#0f2a44">${label}</text>`;
const arrow = (x: number) => `<path d="M${x} 70 h22" stroke="#0d6e66" stroke-width="2" marker-end="url(#a)"/>`;

export const GET: APIRoute = () => {
	const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 140" width="440" height="140" role="img">
<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#0d6e66"/></marker></defs>
<rect width="440" height="140" fill="#fff"/>
${box(10, 'Synthetic CT')}${arrow(122)}${box(160, 'FixtureNet')}${arrow(272)}${box(310, 'Invented mask')}
<text x="220" y="128" font-family="monospace" font-size="11" text-anchor="middle" fill="#4a5b6b">SYNTHETIC FIGURE — NOT FROM A REAL PAPER</text>
</svg>`;
	return new Response(svg, { headers: { 'Content-Type': 'image/svg+xml; charset=utf-8' } });
};
