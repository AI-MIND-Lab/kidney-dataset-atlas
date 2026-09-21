# Kidney Dataset Atlas

Explore open kidney research datasets, understand their variables, and discover the studies built with them.

The catalog is a set of files in this repository. Pages, search and exports are generated from those files, so
every number on the site traces back to a record with a source.

**Status: private.** The site is not hosted anywhere yet. People invited to this repository run it on their own
machine, as described below. Nothing is published until a curator has approved it.

## Run the site

You need [Node.js](https://nodejs.org) 22.12 or newer and git. Then:

```bash
git clone https://github.com/i-sababishraq/kidney-dataset-atlas.git
cd kidney-dataset-atlas
npm ci
npm run preview:site
```

The last command validates the records, builds the site, generates the search index, and serves the result.
Open the address it prints (usually <http://localhost:4321>).

Prefer not to install anything? Open the repository in GitHub Codespaces instead (Code → Codespaces → Create),
then run `npm run preview:site` in its terminal. Codespaces usage counts against your own free allowance.

### Working on the interface

`npm run dev` starts the development server with live reload, but it has **no search index**: Pagefind runs
against the built site, so use `npm run preview:site` whenever search matters.

Because no real records are approved yet, use the synthetic fixtures to see a populated interface:

```bash
npm run dev:fixtures
```

Fixture records are clearly labelled in the page, live outside `src/`, and can never reach a real build: the
output check fails if a fixture marker appears in `dist/`.

## Commands

| Command | What it does |
| --- | --- |
| `npm run dev` | Development server, live reload, no search index |
| `npm run dev:fixtures` | Development server against the synthetic fixtures |
| `npm run validate` | Checks every record: schema, references, curator approval |
| `npm run check` | TypeScript and Astro checks |
| `npm test` | Focused tests (approval gate, unknown-value semantics) |
| `npm run build` | Validate → build → **generate search** → check output |
| `npm run preview:site` | Build as above, then serve it locally |
| `npm run search:index` | Regenerate the Pagefind index over `dist/` |

To build the site as it will be published later, under a repository sub-path:

```bash
SITE_URL=https://i-sababishraq.github.io BASE_PATH=/kidney-dataset-atlas npm run build
```

## Adding to the catalog

The broad research inventory is versioned at
[`docs/Kidney_Open_Datasets_and_CV_Papers.md`](docs/Kidney_Open_Datasets_and_CV_Papers.md). It is a backlog, not a
publication feed: records are imported individually only after evidence review and curator approval. Citation
counts and unapproved preview images are not public site metadata.

| What you are adding | Where it goes |
| --- | --- |
| Dataset | `src/content/datasets/<id>.md` — description in the body, fields in the frontmatter |
| Release | `src/content/releases/<id>.yaml` — counts, access, licence, eligibility |
| Variable | `src/data/variables/<release-id>.json` — an array of variables |
| Paper and its architectures | `src/content/papers/<id>.md` — every model the paper reports |
| Paper's use of a release | `src/data/study-uses/<name>.json` — role, subset, split, results |
| Sample image | `src/data/samples/<name>.json` plus the file in `public/previews/` |
| Quality finding | `src/data/quality/<name>.json` |
| Source | `src/data/sources/<name>.json` — every claim cites one of these |
| Correction | Change the record and its source; `npm run validate` before committing |

Templates and the rules for unknown values are in [docs/authoring.md](docs/authoring.md).

## Approval

Records start as `catalogStatus: draft` and stay out of the site, its search index and its exports until a
curator approves them. `npm run validate` prints a checklist for every draft, listing each eligibility check
with its sources.

An agent may research and write records, but must never set `approvedBy`, `permissionApprovedBy` or
`catalogStatus: published`. Approval is a person reading the sources and committing that decision themselves.
Curators are listed in `src/data/curators.yaml`; the build fails if anyone else appears as an approver.

## Deployment

Nothing is deployed during the private phase. A GitHub Pages site would be visible to anyone with its address
even from a private repository, and restricting viewers needs GitHub Enterprise Cloud, so the site stays local
for now.

`.github/workflows/deploy.yml` holds the Pages deployment and starts only when triggered by hand. It works once
the repository is public. `.github/workflows/ci.yml` validates, checks, tests and builds every push, including a
build under the project sub-path.

## Layout

```
src/content/      dataset, release and paper records
src/data/         variables, study uses, samples, quality, sources, overlap, curators
src/lib/          schemas, catalog queries, display rules, URL helpers
src/pages/        routes
scripts/          record validation, build output checks
tests/            tests and synthetic fixtures
docs/             authoring guide and recorded decisions
```
