# Decisions

Choices that a reader of the brief would not predict from the brief alone, and why they were made.

## Releases are not listed on the dataset record

The brief lists "release IDs" among a dataset's fields. Instead, each release names its dataset, and the
dataset's releases are derived at build time. Keeping the list in both places would mean maintaining a second
copy of a relationship, which the brief rules out elsewhere.

## One canonical page per release

`/datasets/<slug>/` and `/datasets/<slug>/releases/<current>/` render the same content. The dataset page is
canonical; the current release's page points at it and is left out of the search index, while older releases
are indexed and labelled. `scripts/check-output.mjs` fails the build if two indexed pages share a canonical URL.

Pagefind skips every page without `data-pagefind-body` as soon as one page has it, so the marker is set in the
base layout for all pages, and only the duplicate opts out.

## Data records are read through Vite, not content collections

Datasets, releases and papers are content collections, because they have prose or benefit from per-file
frontmatter. Variables, study uses, samples, quality findings, sources and overlaps are arrays inside JSON
files, which does not fit one-entry-per-file collections, so they are loaded with `import.meta.glob` and
validated against the same schemas at build time.

## Schemas are shared JavaScript

`src/lib/schemas.mjs` is plain JavaScript using `astro/zod`, so both the Astro content config and the standalone
validation script use exactly the same definitions. TypeScript still infers record types from them.

## Fixtures replace the catalog rather than joining it

`ATLAS_FIXTURES=1` points the loaders at `tests/fixtures/` instead of the real directories, so synthetic records
can never appear beside real ones. Fixture pages carry a `data-atlas-fixture` marker, and the output check fails
if that marker appears in a normal build.

## The validator, not the platform, enforces approval

GitHub cannot require reviews on a private repository on the free plan, and an agent commits with the owner's
credentials, so git history alone cannot show who checked what. `npm run validate` refuses to build a published
release whose `approvedBy` is empty or is not listed in `src/data/curators.yaml`, whose eligibility checks have
not all passed, or that displays a sample without its own permission approval.

## Search is not wired up yet

Pagefind runs in the build and the index is generated, but the search interface lands with the explorer in
milestone 2. `npm run dev` therefore has no search; `npm run preview:site` builds the real thing.

## Deployment is prepared but disabled

`deploy.yml` starts only by hand. A GitHub Pages site is public even from a private repository, and viewer
restrictions need GitHub Enterprise Cloud, so during the private phase collaborators run the site locally.
