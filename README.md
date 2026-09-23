# Kidney Dataset Atlas

Explore open kidney research datasets, understand their variables, and discover the studies built with them.

The catalog is a set of files in this repository. Pages, search and exports are generated from those files, so
every number on the site traces back to a record with a source.

**Status: public repository, site not yet hosted.** Anyone can read the source and run the site on their own
machine, as described below. Records in the repository are drafts until a curator approves them: drafts are
visible here as files, but they never appear on the built site, in its search index or in its exports.

## Run the site

You need [Node.js](https://nodejs.org) 22.12 or newer (the project uses 24, pinned in `.nvmrc`) and git. Then:

```bash
git clone https://github.com/i-sababishraq/kidney-dataset-atlas.git
cd kidney-dataset-atlas
npm ci
npm run preview:site
```

The last command validates the records, builds the site, generates the search index, and serves the result.
Open the address it prints (usually <http://localhost:4321>).

**Seeing an empty site?** That is expected while every record is still a draft: the normal build shows
approved records only. To read the drafts as pages, run:

```bash
npm run preview:drafts
```

Every page in that build is marked as a draft, and the output check refuses to publish it.

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
| `npm run test:browser` | Browser smoke test against the fixtures (first run `npx playwright install chromium`) |
| `npm run build` | Validate → build → **generate search** → check output |
| `npm run preview:site` | Build as above, then serve it locally (approved records only) |
| `npm run preview:drafts` | Build including drafts, marked as such, then serve it locally |
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

The rules for records and unknown values are in [docs/authoring.md](docs/authoring.md), which also points to a
complete synthetic example of every record type in `tests/fixtures/` to copy from. The original product brief is
[docs/brief.md](docs/brief.md).

## Approval

Records start as `catalogStatus: draft` and stay out of the site, its search index and its exports until a
curator approves them. `npm run validate` prints a checklist for every draft, listing each eligibility check
with its sources.

An agent may research and write records, but must never set `approvedBy`, `permissionApprovedBy` or
`catalogStatus: published`. Approval is a person reading the sources and committing that decision themselves.
Curators are listed in `src/data/curators.yaml`; the build fails if anyone else appears as an approver.

## Deployment

The site is not deployed yet. `.github/workflows/deploy.yml` holds the GitHub Pages deployment and starts only
when triggered by hand from the Actions tab; the repository is public, so it can now run, and it publishes
approved records only. `.github/workflows/ci.yml` validates, checks, tests and builds every push, including a
build under the project sub-path.

## Layout

```
src/content/      dataset, release and paper records
src/data/         variables, study uses, samples, quality, sources, overlap, curators
src/lib/          schemas, catalog queries, display rules, URL helpers
src/pages/        routes
scripts/          record validation, build output checks
tests/            tests and synthetic fixtures
docs/             authoring guide, recorded decisions, product brief, research inventory
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the branch and pull-request workflow. To suggest a dataset, paper or
correction without writing code, open an issue using one of the templates.

## Licence

The software (site source, scripts, tests, configuration and project documentation) is under the MIT License. The catalogue data and
research content (`src/content/`, `src/data/`, `public/previews/`, the research inventory and `docs/literature/`)
are **not** openly licensed: all rights reserved. See [LICENSE](LICENSE) for the exact scope and for the
attribution required for third-party material.
