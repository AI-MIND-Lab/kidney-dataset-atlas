#!/usr/bin/env node
/**
 * Creates a skeleton record with every required field, each set to "not documented" or "unknown", so it
 * validates as a draft straight away and `npm run checklist` lists what is still missing.
 *
 *   npm run new -- dataset <id> --name "Full name" --url https://official.page
 *   npm run new -- release <id> --dataset <dataset-id> [--label "Version 2"]
 *   npm run new -- paper <id> --title "Paper title" [--url https://doi.org/...]
 *
 * Add --by <github-username> to set researchedBy on a release (default: git config github.user, else user.name).
 * Existing files are never overwritten. See docs/authoring.md for what each field means.
 */
import { execSync } from 'node:child_process';
import { existsSync, mkdirSync, writeFileSync } from 'node:fs';
import { dirname, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(fileURLToPath(new URL('../', import.meta.url)));
const ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const q = (text) => JSON.stringify(text); // a YAML-safe quoted string

export function datasetRecord({ id, name, url }) {
	return `---
id: ${id}
slug: ${id}
name: ${q(name)}
aliases: []
summary: Not written yet.
diseaseTags: []
species: not_documented
officialUrl: ${url}
doi: null
sources: []
---

<!--
Two or three paragraphs: what the collection is, who publishes it, what one record or case is, and anything a
reader could misread (derived data, overlapping cohorts, public and restricted parts). Every claim needs a
source in src/data/sources/. See docs/authoring.md, "A dataset".
-->
`;
}

export function releaseRecord({ id, dataset, label, by }) {
	const unknown = (key) => `  ${key}:\n    status: unknown\n    note: Not checked yet.`;
	const notDocumented = (key) => `  ${key}:\n    value: null\n    status: not_documented`;
	return `# Skeleton from \`npm run new\`. Every value below is "not documented" or "unknown" until you check it
# against a source; see docs/authoring.md, "A release". Never fill in approvedBy, approvedOn or catalogStatus:
# a curator does that in their own commit.
id: ${id}
dataset: ${dataset}
versionLabel: ${q(label)}
current: false
releaseDate: null
counts:
${['patients', 'examinations', 'lesions', 'slides', 'records'].map(notDocumented).join('\n')}
modalities: []
tasks: []
annotations: []
annotationProvenance:
  kind: not_documented
doi: null
access:
  mode: access_unclear
  registrationVisible: false
  instructions: Not documented yet.
license:
  name: Not documented
deidentification:
  statement: Not documented yet.
  status: not_documented
pairing: []
dictionary:
  completeness: documentation_only
  inspectedScope: Nothing inspected yet.
features:
  wsi:
    status: not_documented
  ctPhases:
    status: not_documented
  clinicalData:
    status: not_documented
  followUp:
    status: not_documented
limitations: []
eligibility:
${['publicAccess', 'deidentification', 'noPhiHosted', 'termsPermitUse', 'samplePermission'].map(unknown).join('\n')}
catalogStatus: draft
verifiedOn: null
researchedBy: ${q(by)}
approvedBy: null
approvedOn: null
sources: []
`;
}

export function paperRecord({ id, title, url }) {
	return `---
id: ${id}
slug: ${id}
title: ${q(title)}
authors: []
year: null
venue: null
publicationStatus: not_documented
doi: null
url: ${url ?? 'null'}
figures: []
linkedFigures: []
models: []
catalogStatus: draft
approvedBy: null
approvedOn: null
sources: []
---

<!--
What the paper does with the data, in your own words from the full text. Add a methodSummary, every model the
paper reports results for (with pipeline and evidence), and a study use in src/data/study-uses/ for each release
it used. See docs/authoring.md, "Papers and their architectures".
-->
`;
}

function gitUser() {
	for (const key of ['github.user', 'user.name']) {
		try {
			const value = execSync(`git config ${key}`, { cwd: root, encoding: 'utf8' }).trim();
			if (value) return value;
		} catch {}
	}
	return 'unknown';
}

function main(argv) {
	const [kind, id, ...rest] = argv;
	const flags = {};
	for (let i = 0; i < rest.length; i += 2) flags[rest[i].replace(/^--/, '')] = rest[i + 1];
	const usage = () => {
		console.error(
			'usage:\n  npm run new -- dataset <id> --name "Full name" --url https://official.page\n' +
				'  npm run new -- release <id> --dataset <dataset-id> [--label "Version 2"] [--by <github-username>]\n' +
				'  npm run new -- paper <id> --title "Paper title" [--url https://doi.org/...]',
		);
		process.exit(1);
	};
	if (!kind || !id) usage();
	if (!ID.test(id)) {
		console.error(`"${id}" is not a valid id: use lowercase letters, numbers and single hyphens.`);
		process.exit(1);
	}

	let path;
	let text;
	if (kind === 'dataset') {
		if (!flags.name || !flags.url) usage();
		path = join(root, 'src/content/datasets', `${id}.md`);
		text = datasetRecord({ id, name: flags.name, url: flags.url });
	} else if (kind === 'release') {
		if (!flags.dataset) usage();
		if (!existsSync(join(root, 'src/content/datasets', `${flags.dataset}.md`))) {
			console.error(`No dataset "${flags.dataset}" in src/content/datasets/. Create it first with: npm run new -- dataset ...`);
			process.exit(1);
		}
		path = join(root, 'src/content/releases', `${id}.yaml`);
		text = releaseRecord({ id, dataset: flags.dataset, label: flags.label ?? id, by: flags.by ?? gitUser() });
	} else if (kind === 'paper') {
		if (!flags.title) usage();
		path = join(root, 'src/content/papers', `${id}.md`);
		text = paperRecord({ id, title: flags.title, url: flags.url });
	} else {
		usage();
	}

	if (existsSync(path)) {
		console.error(`${relative(root, path).replace(/\\/g, '/')} already exists; not overwritten.`);
		process.exit(1);
	}
	mkdirSync(dirname(path), { recursive: true });
	writeFileSync(path, text);
	console.log(`Created ${relative(root, path).replace(/\\/g, '/')} as a draft.`);
	console.log('Next: fill it in from your sources, then run `npm run validate` and `npm run checklist`.');
}

if (resolve(process.argv[1] ?? '') === fileURLToPath(import.meta.url)) main(process.argv.slice(2));
