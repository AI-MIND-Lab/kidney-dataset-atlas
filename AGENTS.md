# Instructions for coding agents

This file is for AI coding agents (Claude Code, Codex, Copilot and others) working in this repository. People
should start with [README.md](README.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

## What this project is

The Kidney Dataset Atlas is a static Astro site generated from curated records about kidney research datasets
and the papers that use them. The records are the product; every claim in them must be traceable to a source.
The original product brief is [docs/brief.md](docs/brief.md); [docs/decisions.md](docs/decisions.md) records
where the implementation departs from it.

## Rules you must not break

1. **Never approve anything.** Do not set `approvedBy`, `approvedOn`, `permissionApprovedBy`,
   `permissionApprovedOn` or `catalogStatus: published`, and never add anyone to `src/data/curators.yaml`.
   Records you write stay `catalogStatus: draft`, with `researchedBy: agent`. Approval is a person's decision,
   made in their own commit.
2. **Never invent.** Counts, variables, licences, pairings, paper uses, metrics and citations come from a source,
   and the record names the source and where in it the claim appears. A paper that mentions a dataset is not
   evidence that it used it.
3. **Unknown stays unknown.** Use `not_documented`, `not_verified` or `not_applicable` with `value: null`; never
   `0`, "no" or a plausible guess. See [docs/authoring.md](docs/authoring.md).
4. **Previews only, no raw data, no credentials.** Preview images may be added as compressed renderings in
   `public/previews/<release-id>/` with a sample record (see [docs/previews.md](docs/previews.md)), leaving
   `permissionApprovedBy` null. Never commit raw scans, masks, archives or other dataset downloads, protected
   health information or secrets.
5. **Fixtures stay fixtures.** Synthetic records live only in `tests/fixtures/` and must never be copied into
   `src/`.
6. **Paper figures only under CC BY or CC0, and describe models in your own words.** Copy a paper's figure into
   `public/figures/<paper-id>/` only when the paper's licence is CC BY or CC0, with the quoted caption and full
   credit; otherwise add a `linkedFigures` entry. Write model fields and pipelines from the full text in your own
   words, quote only captions and result values, and record where in the paper each model was read. See
   [docs/authoring.md](docs/authoring.md#architecture-figures).

## Before you finish

Run the same checks as CI, and report their results truthfully:

```bash
npm run validate
npm run check
npm test
npm run build
npm run test:browser   # whenever a page or component changed
```

`npm run validate` prints an approval checklist for draft releases; that output is for the curator, not a task
for you to complete by editing approval fields.

## Where things are

- Record formats: [docs/authoring.md](docs/authoring.md). Complete synthetic examples of every record type:
  `tests/fixtures/content/` and `tests/fixtures/data/`.
- Research backlog that new records come from, with verified paper relationships in section 6.4:
  [docs/Kidney_Open_Datasets_and_CV_Papers.md](docs/Kidney_Open_Datasets_and_CV_Papers.md).
- Unverified paper candidates for review: [docs/literature/](docs/literature/).
- Licensing: code and project documentation are MIT; catalogue data and research content are all rights
  reserved; preview images in `public/previews/` carry the licence of the dataset they come from. Keep new data
  files inside the paths listed in [LICENSE](LICENSE).

## Running the site

Use `npm run preview:drafts` to see draft records as pages; `npm run preview:site` shows approved records only.
`npm run dev` has live reload but no search index. To keep a dev server running in the background:

```
astro dev --background
```

Manage it with `astro dev stop`, `astro dev status` and `astro dev logs`.

## Astro documentation

Full documentation: https://docs.astro.build. Consult these guides before working on related tasks:

- [Adding pages, dynamic routes, or middleware](https://docs.astro.build/en/guides/routing/)
- [Working with Astro components](https://docs.astro.build/en/basics/astro-components/)
- [Adding or managing content](https://docs.astro.build/en/guides/content-collections/)
- [Adding styles](https://docs.astro.build/en/guides/styling/)
