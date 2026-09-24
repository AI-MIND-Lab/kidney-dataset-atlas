# Decisions

Choices that a reader of the [project brief](brief.md) would not predict from the brief alone, and why they were made.

## Releases are not listed on the dataset record, but the current one is declared

The brief lists "release IDs" among a dataset's fields. Instead, each release names its dataset, and the
dataset's releases are derived at build time. Keeping the list in both places would mean maintaining a second
copy of a relationship, which the brief rules out elsewhere.

Which release is **current** is the exception: it is stated, not derived. A release carries `current: true`,
and validation requires exactly one current release among a dataset's published releases. Deriving it from
dates looked simpler until several releases turned out to have no documented date, at which point the
canonical page for a dataset would have depended on a sort over nulls.

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

An agent commits with the owner's credentials, so git history alone cannot show who checked what; and
repository settings such as required reviews can change. (The repository started private, where the free plan
cannot require reviews at all.) `npm run validate` refuses to build a published
release whose `approvedBy` is empty or is not listed in `src/data/curators.yaml`, whose eligibility checks have
not all passed, or that displays a sample without its own permission approval.

## Search runs against the built site, not the development server

`/search/` queries the Pagefind index, and the header carries a search field. Because Pagefind runs over
`dist/` after the build, `npm run dev` has no index: the page says so rather than appearing broken. Use
`npm run preview:site` whenever search matters. The query stays in the address bar so a result page can be
shared, and the index is loaded from a path that respects the configured base.

## Deployment is prepared but disabled

`deploy.yml` starts only by hand, so publishing the site is a separate, deliberate step, and it publishes
approved records only. On GitHub's free plan it can run only while the repository is public; and a Pages site is
visible to anyone with its address even from a private repository, because viewer restrictions need GitHub
Enterprise Cloud. While the repository is private, collaborators run the site locally.
