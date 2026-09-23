// @ts-check
import { defineConfig } from 'astro/config';

// Deployment target is configurable so the same build works when run locally
// and under a GitHub Pages project base path.
// SITE_URL=https://i-sababishraq.github.io BASE_PATH=/kidney-dataset-atlas
const site = process.env.SITE_URL ?? 'http://localhost:4321';
const base = process.env.BASE_PATH ?? '/';

// https://astro.build/config
export default defineConfig({
	site,
	base,
	output: 'static',
	trailingSlash: 'always',
	build: { format: 'directory' },
});
