#!/usr/bin/env node
/**
 * Validates every catalog record before a build.
 *
 * Three jobs: the records match their schemas, every reference resolves, and
 * nothing reaches the public catalog without a curator's approval. Run with
 * `npm run validate`; the build runs it first.
 */
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import yaml from 'js-yaml';
import { schemas } from '../src/lib/schemas.mjs';
import { ELIGIBILITY_LABELS } from '../src/lib/eligibility.mjs';

const root = resolve(fileURLToPath(new URL('../', import.meta.url)));
const useFixtures = process.env.ATLAS_FIXTURES === '1';
// ATLAS_CONTENT_ROOT / ATLAS_DATA_ROOT let the tests point the validator at a
// throwaway set of records; normal runs use the real catalog or the fixtures.
const contentRoot = process.env.ATLAS_CONTENT_ROOT
	? resolve(root, process.env.ATLAS_CONTENT_ROOT)
	: join(root, useFixtures ? 'tests/fixtures/content' : 'src/content');
const dataRoot = process.env.ATLAS_DATA_ROOT
	? resolve(root, process.env.ATLAS_DATA_ROOT)
	: join(root, useFixtures ? 'tests/fixtures/data' : 'src/data');

const errors = [];
const fail = (file, message) => errors.push({ file, message });
const rel = (file) => relative(root, file).replace(/\\/g, '/');

/** Every file in a directory tree, or nothing if the directory is absent. */
function filesIn(dir, extensions) {
	if (!existsSync(dir)) return [];
	return readdirSync(dir, { withFileTypes: true, recursive: true })
		.filter((entry) => entry.isFile() && extensions.some((ext) => entry.name.endsWith(ext)))
		.map((entry) => join(entry.parentPath ?? dir, entry.name));
}

function parseFrontmatter(file) {
	const raw = readFileSync(file, 'utf8');
	const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---/);
	if (!match) {
		fail(rel(file), 'missing frontmatter block');
		return null;
	}
	return yaml.load(match[1]);
}

/** Load and schema-check one collection. Returns the records that parsed. */
function load(name, files, parser) {
	const schema = schemas[name];
	const records = [];
	for (const file of files) {
		let raw;
		try {
			raw = parser(file);
		} catch (error) {
			fail(rel(file), `could not be read: ${error.message}`);
			continue;
		}
		if (raw === null || raw === undefined) continue;
		const list = Array.isArray(raw) ? raw : [raw];
		for (const item of list) {
			const result = schema.safeParse(item);
			if (!result.success) {
				for (const issue of result.error.issues) {
					fail(rel(file), `${issue.path.join('.') || '(root)'}: ${issue.message}`);
				}
				continue;
			}
			records.push({ file: rel(file), data: result.data });
		}
	}
	return records;
}

const readJson = (file) => JSON.parse(readFileSync(file, 'utf8'));
const readYaml = (file) => yaml.load(readFileSync(file, 'utf8'));

const datasets = load('datasets', filesIn(join(contentRoot, 'datasets'), ['.md']), parseFrontmatter);
const releases = load('releases', filesIn(join(contentRoot, 'releases'), ['.yaml', '.yml']), readYaml);
const papers = load('papers', filesIn(join(contentRoot, 'papers'), ['.md']), parseFrontmatter);
const variables = load('variables', filesIn(join(dataRoot, 'variables'), ['.json']), readJson);
const studyUses = load('study-uses', filesIn(join(dataRoot, 'study-uses'), ['.json']), readJson);
const samples = load('samples', filesIn(join(dataRoot, 'samples'), ['.json']), readJson);
const quality = load('quality', filesIn(join(dataRoot, 'quality'), ['.json']), readJson);
const sources = load('sources', filesIn(join(dataRoot, 'sources'), ['.json']), readJson);
const overlaps = load('overlap', filesIn(join(dataRoot, 'overlap'), ['.json']), readJson);
const relations = load('relations', filesIn(join(dataRoot, 'relations'), ['.json']), readJson);

const curatorsFile = join(root, 'src/data/curators.yaml');
const curators = existsSync(curatorsFile) ? (yaml.load(readFileSync(curatorsFile, 'utf8'))?.curators ?? []) : [];
if (curators.length === 0) fail('src/data/curators.yaml', 'no curators are listed, so nothing can be published');

/* Unique IDs ------------------------------------------------------------- */

const ids = {};
for (const [name, records] of Object.entries({
	datasets,
	releases,
	papers,
	variables,
	'study-uses': studyUses,
	samples,
	quality,
	sources,
	overlap: overlaps,
	relations,
})) {
	const seen = new Map();
	for (const record of records) {
		if (seen.has(record.data.id)) {
			fail(record.file, `duplicate id "${record.data.id}" (also in ${seen.get(record.data.id)})`);
		}
		seen.set(record.data.id, record.file);
	}
	ids[name] = seen;
}

const has = (collection, id) => ids[collection].has(id);

/** Route slugs are independent from ids, but must still be unique per route family. */
for (const [name, records] of [
	['datasets', datasets],
	['papers', papers],
]) {
	const seen = new Map();
	for (const record of records) {
		const existing = seen.get(record.data.slug);
		if (existing) fail(record.file, `duplicate ${name} slug "${record.data.slug}" (also in ${existing})`);
		seen.set(record.data.slug, record.file);
	}
}

/* References ------------------------------------------------------------- */

const reference = (record, collection, id, field) => {
	if (id && !has(collection, id)) fail(record.file, `${field} points at missing ${collection} record "${id}"`);
};

for (const record of releases) reference(record, 'datasets', record.data.dataset, 'dataset');
for (const record of variables) reference(record, 'releases', record.data.release, 'release');
for (const record of samples) reference(record, 'releases', record.data.release, 'release');
for (const record of quality) reference(record, 'releases', record.data.release, 'release');
for (const record of overlaps) {
	for (const id of record.data.releases) reference(record, 'releases', id, 'releases');
}

for (const record of relations) {
	reference(record, 'releases', record.data.from, 'from');
	// A relation names either a catalogued release or an external collection,
	// never both and never neither: otherwise it says nothing checkable.
	if (record.data.to && record.data.toExternal) {
		fail(record.file, `relation "${record.data.id}" names both a catalogued release and an external one`);
	}
	if (!record.data.to && !record.data.toExternal) {
		fail(record.file, `relation "${record.data.id}" names nothing on the other side`);
	}
	if (record.data.to) reference(record, 'releases', record.data.to, 'to');
}

const paperModels = new Map(papers.map((paper) => [paper.data.id, new Set(paper.data.models.map((m) => m.id))]));

for (const record of studyUses) {
	reference(record, 'papers', record.data.paper, 'paper');
	if (record.data.release) reference(record, 'releases', record.data.release, 'release');
	const models = paperModels.get(record.data.paper);
	for (const result of record.data.results) {
		if (models && !models.has(result.model)) {
			fail(record.file, `result names model "${result.model}", which paper "${record.data.paper}" does not define`);
		}
	}
}

/** Source ids can appear on a record or inside any evidence object. */
function checkSources(record, value, path = '') {
	if (!value || typeof value !== 'object') return;
	if (Array.isArray(value)) {
		value.forEach((item, index) => checkSources(record, item, `${path}[${index}]`));
		return;
	}
	for (const [key, item] of Object.entries(value)) {
		const next = path ? `${path}.${key}` : key;
		if (key === 'sources' && Array.isArray(item)) {
			for (const id of item) {
				if (!has('sources', id)) fail(record.file, `${next} points at missing source "${id}"`);
			}
			continue;
		}
		checkSources(record, item, next);
	}
}

for (const record of [
	...datasets,
	...releases,
	...papers,
	...variables,
	...studyUses,
	...samples,
	...quality,
	...overlaps,
	...relations,
]) {
	checkSources(record, record.data);
}

/* Publication gate ------------------------------------------------------- */

const publishedReleases = releases.filter((record) => record.data.catalogStatus === 'published');
const draftReleases = releases.filter((record) => record.data.catalogStatus !== 'published');
const publishedPapers = papers.filter((record) => record.data.catalogStatus === 'published');
const publishedReleaseIds = new Set(publishedReleases.map((record) => record.data.id));
const publishedPaperIds = new Set(publishedPapers.map((record) => record.data.id));
const evidenceIsVerified = (value) =>
	value?.status === 'verified' && Array.isArray(value.sources) && value.sources.length > 0;
const evidenceRequiredEligibility = ['publicAccess', 'deidentification', 'termsPermitUse'];
const publiclyEligibleAccessModes = new Set([
	'direct_open_download',
	'public_account_or_terms',
	'registration_gated',
]);

for (const record of publishedReleases) {
	const { approvedBy, approvedOn, eligibility, verifiedOn, id } = record.data;
	if (!approvedBy) {
		fail(record.file, `release "${id}" is published but has no approvedBy`);
	} else if (!curators.includes(approvedBy)) {
		fail(record.file, `release "${id}" was approved by "${approvedBy}", who is not listed in curators.yaml`);
	}
	if (!approvedOn) fail(record.file, `release "${id}" is published but has no approvedOn`);
	if (!verifiedOn) fail(record.file, `release "${id}" is published but has no verifiedOn`);
	for (const [key, check] of Object.entries(eligibility)) {
		if (check.status !== 'pass') {
			fail(record.file, `release "${id}" is published but eligibility check ${key} is "${check.status}"`);
		}
		if (check.status === 'pass' && evidenceRequiredEligibility.includes(key) && !evidenceIsVerified(check.evidence)) {
			fail(record.file, `release "${id}" passes ${key} without verified source evidence`);
		}
	}
	if (!publiclyEligibleAccessModes.has(record.data.access.mode)) {
		fail(record.file, `release "${id}" uses ineligible public access mode "${record.data.access.mode}"`);
	}
	for (const sample of samples.filter((entry) => entry.data.release === id)) {
		if (!sample.data.permissionApprovedBy) {
			fail(sample.file, `sample "${sample.data.id}" is shown on a published release without permission approval`);
		} else if (!curators.includes(sample.data.permissionApprovedBy)) {
			fail(
				sample.file,
				`sample "${sample.data.id}" permission was approved by "${sample.data.permissionApprovedBy}", who is not a curator`,
			);
		}
	}
}

for (const record of releases) {
	if (record.data.approvedBy && !curators.includes(record.data.approvedBy)) {
		fail(record.file, `approvedBy "${record.data.approvedBy}" is not listed in curators.yaml`);
	}
}

for (const record of publishedPapers) {
	const { approvedBy, approvedOn, id } = record.data;
	if (!approvedBy) {
		fail(record.file, `paper "${id}" is published but has no approvedBy`);
	} else if (!curators.includes(approvedBy)) {
		fail(record.file, `paper "${id}" was approved by "${approvedBy}", who is not listed in curators.yaml`);
	}
	if (!approvedOn) fail(record.file, `paper "${id}" is published but has no approvedOn`);
}

for (const record of papers) {
	if (record.data.approvedBy && !curators.includes(record.data.approvedBy)) {
		fail(record.file, `approvedBy "${record.data.approvedBy}" is not listed in curators.yaml`);
	}
}

// Every public dataset has one explicit canonical release; dates and labels
// are display metadata and are never used to guess which release is current.
for (const dataset of datasets) {
	const ownPublished = publishedReleases.filter((record) => record.data.dataset === dataset.data.id);
	if (ownPublished.length === 0) continue;
	const current = ownPublished.filter((record) => record.data.current);
	if (current.length !== 1) {
		fail(dataset.file, `dataset "${dataset.data.id}" has ${current.length} current published releases; expected exactly one`);
	}
}

// A public page may only expose relationships whose catalogued endpoints are
// public. External/private cohorts can appear on approved paper pages, but
// only with verified relationship and cohort evidence and never with a route.
for (const record of studyUses) {
	const paperIsPublic = publishedPaperIds.has(record.data.paper);
	const releaseIsPublic = record.data.release ? publishedReleaseIds.has(record.data.release) : false;
	if (releaseIsPublic && !paperIsPublic) {
		fail(record.file, `published release "${record.data.release}" cites draft paper "${record.data.paper}"`);
	}
	if (paperIsPublic && record.data.release && !releaseIsPublic) {
		fail(record.file, `published paper "${record.data.paper}" cites draft release "${record.data.release}"`);
	}
	if (!paperIsPublic && !releaseIsPublic) continue;
	if (!evidenceIsVerified(record.data.actualUseEvidence)) {
		fail(record.file, `public study use "${record.data.id}" lacks verified relationship evidence`);
	}
	if (record.data.externalCohort && !evidenceIsVerified(record.data.externalCohort.evidence)) {
		fail(record.file, `public study use "${record.data.id}" lacks verified external-cohort evidence`);
	}
}

/* Report ----------------------------------------------------------------- */

const counts = `${datasets.length} datasets, ${releases.length} releases (${publishedReleases.length} published), ${papers.length} papers (${publishedPapers.length} published), ${variables.length} variables, ${samples.length} samples`;
console.log(`Kidney Dataset Atlas — record validation${useFixtures ? ' (fixtures)' : ''}`);
console.log(counts);

if (draftReleases.length > 0) {
	console.log('\nAwaiting curator approval:');
	for (const record of draftReleases) {
		console.log(`\n  ${record.data.id} — ${record.file}`);
		console.log(`    researched by: ${record.data.researchedBy}`);
		for (const [key, label] of Object.entries(ELIGIBILITY_LABELS)) {
			const check = record.data.eligibility[key];
			const sourceIds = check.evidence?.sources ?? [];
			const links = sourceIds
				.map((id) => sources.find((entry) => entry.data.id === id)?.data.url ?? `missing source ${id}`)
				.join(', ');
			console.log(`    [${check.status === 'pass' ? 'x' : ' '}] ${label}${links ? ` — ${links}` : ''}`);
		}
	}
}

if (errors.length > 0) {
	console.error(`\n${errors.length} problem${errors.length === 1 ? '' : 's'} found:`);
	for (const { file, message } of errors) console.error(`  ${file}: ${message}`);
	process.exit(1);
}

console.log('\nAll records valid.');
