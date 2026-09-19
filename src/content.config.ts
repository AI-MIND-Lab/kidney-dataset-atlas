import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { dataset, paper, release } from './lib/schemas.mjs';

// Development can run against synthetic fixtures instead of the real catalog.
// The fixtures live outside src/ and are never mixed with real records: this
// swaps the source directory wholesale, and scripts/check-output.mjs fails the
// build if a fixture marker ever reaches dist/.
const useFixtures = process.env.ATLAS_FIXTURES === '1';
const contentBase = useFixtures ? './tests/fixtures/content' : './src/content';

const datasets = defineCollection({
	loader: glob({ pattern: '**/*.md', base: `${contentBase}/datasets` }),
	schema: dataset,
});

const releases = defineCollection({
	loader: glob({ pattern: '**/*.{yaml,yml}', base: `${contentBase}/releases` }),
	schema: release,
});

const papers = defineCollection({
	loader: glob({ pattern: '**/*.md', base: `${contentBase}/papers` }),
	schema: paper,
});

export const collections = { datasets, releases, papers };
