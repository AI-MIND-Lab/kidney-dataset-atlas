#!/usr/bin/env node
/**
 * Checks the built site before it is published or shared.
 *
 * - no fixture record reached the public build
 * - no two indexed pages describe the same release (duplicate search results)
 * - the output still fits the host it is headed for
 */
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(fileURLToPath(new URL('../', import.meta.url)));
const dist = join(root, 'dist');
const usingFixtures = process.env.ATLAS_FIXTURES === '1';
const showingDrafts = process.env.ATLAS_DRAFTS === '1';

/** GitHub Pages publishes at most 1 GB; warn before the site gets close. */
const LIMIT_BYTES = 1024 ** 3;
const WARN_BYTES = 0.8 * LIMIT_BYTES;

const errors = [];
const files = [];

function walk(dir) {
	for (const entry of readdirSync(dir, { withFileTypes: true })) {
		const path = join(dir, entry.name);
		if (entry.isDirectory()) walk(path);
		else files.push(path);
	}
}

try {
	walk(dist);
} catch {
	console.error('No dist/ directory. Run the build first.');
	process.exit(1);
}

const totalBytes = files.reduce((sum, file) => sum + statSync(file).size, 0);
const mib = (bytes) => `${(bytes / 1024 ** 2).toFixed(1)} MiB`;

// Synthetic preview drawings are generated only for fixture builds.
if (!usingFixtures) {
	for (const file of files) {
		const name = relative(dist, file).replace(/\\/g, '/');
		if (name.startsWith('previews/fixtures/')) {
			errors.push(`${name}: fixture preview asset in a public build`);
		}
	}
}

const canonicals = new Map();
for (const file of files.filter((path) => path.endsWith('.html'))) {
	const html = readFileSync(file, 'utf8');
	const name = relative(dist, file).replace(/\\/g, '/');

	if (!usingFixtures && (/data-atlas-fixture/.test(html) || html.includes('/previews/fixtures/'))) {
		errors.push(`${name}: contains fixture data, which must never reach a public build`);
	}

	if (!showingDrafts && /data-atlas-draft/.test(html)) {
		errors.push(`${name}: contains an unapproved draft record, which must never reach a public build`);
	}

	if (!html.includes('data-pagefind-body')) continue;
	const canonical = html.match(/<link rel="canonical" href="([^"]+)"/)?.[1];
	if (!canonical) {
		errors.push(`${name}: indexed for search but has no canonical URL`);
		continue;
	}
	if (canonicals.has(canonical)) {
		errors.push(`${name}: same canonical URL as ${canonicals.get(canonical)}, so search would return it twice`);
	}
	canonicals.set(canonical, name);
}

console.log(`Built site: ${files.length} files, ${mib(totalBytes)}, ${canonicals.size} indexed pages`);

if (totalBytes > LIMIT_BYTES) {
	errors.push(`output is ${mib(totalBytes)}, above the 1 GB GitHub Pages limit`);
} else if (totalBytes > WARN_BYTES) {
	console.warn(`warning: output is ${mib(totalBytes)}, approaching the 1 GB GitHub Pages limit`);
}

if (errors.length > 0) {
	console.error(`\n${errors.length} problem${errors.length === 1 ? '' : 's'} found:`);
	for (const message of errors) console.error(`  ${message}`);
	process.exit(1);
}

console.log('Output checks passed.');
