# Authoring records

Every page on the site is generated from the files described here. Two rules sit above all the others:

1. **Nothing is invented.** Counts, variables, licences, pairings, paper uses, metrics and citations come from a
   source, and the record names that source and where in it the claim appears.
2. **Unknown is written as unknown.** Never fill a gap with zero, "no", or a plausible guess.

## Complete examples

This guide explains the rules. For a complete, valid example of every record type, copy from the synthetic
fixtures, which the tests build into a working site:

| Record | Example |
| --- | --- |
| Dataset | `tests/fixtures/content/datasets/fixture-renal-ct.md` |
| Release | `tests/fixtures/content/releases/fixture-renal-ct-v2.yaml` |
| Paper and its models | `tests/fixtures/content/papers/fixture-paper.md` |
| Variables | `tests/fixtures/data/variables/fixture-renal-ct-v2.json` |
| Study uses | `tests/fixtures/data/study-uses/fixture-uses.json` |
| Sources | `tests/fixtures/data/sources/fixture-sources.json` |
| Samples | `tests/fixtures/data/samples/fixture-samples.json` |
| Quality findings | `tests/fixtures/data/quality/fixture-quality.json` |
| Relations and overlap | `tests/fixtures/data/relations/fixture-relations.json`, `tests/fixtures/data/overlap/fixture-overlap.json` |

The real records in `src/content/` and `src/data/` are also good models; `src/content/releases/kits23.yaml` is one
of the most complete. Fixture content is invented: copy the structure, never the values.

## Saying what you do not know

| Value | Use it when |
| --- | --- |
| `present` | The source states this is there. |
| `absent` | The source states this is not there. |
| `not_documented` | The source does not say. |
| `not_verified` | Someone claims it, but it has not been checked here. |
| `not_applicable` | The question does not apply to this release. |

Counts carry both a number and a state. `present` requires a non-negative integer. Every other state requires
`value: null`; an unknown count is never represented by `0`.
Patients, examinations, lesions, slices, slides and records are separate units and are never added together.

## Evidence

Any claim worth doubting carries an evidence object:

```yaml
evidence:
  sources: [kits23-challenge-page]   # ids from src/data/sources/
  locator: "Data section, paragraph 2"
  status: verified                   # or not_verified
  verifiedOn: 2026-09-19
```

Sources live in `src/data/sources/*.json` and carry a URL, title, locator and the date they were read.

## A dataset

`src/content/datasets/<id>.md`. Frontmatter holds the fields; the body is the prose shown under Overview.

```markdown
---
id: example-dataset
slug: example-dataset
name: Example Kidney Collection
aliases: [EKC]
summary: One sentence a researcher can scan in a list.
diseaseTags: [renal_tumor]
officialUrl: https://example.org/
sources: [example-source]
---

Purpose, cohort, inclusion and exclusion criteria, supported tasks, annotation
reference standard, strengths, limits, and what the collection does not contain.
```

## A release

`src/content/releases/<id>.yaml`. One release belongs to one dataset. Keep releases separate rather than
overwriting: the release URL is what people cite.

Required blocks: `counts`, `access`, `license`, `deidentification`, `dictionary`, `eligibility`, plus
`researchedBy`. Leave `catalogStatus: draft`, `approvedBy` and `approvedOn` alone — those belong to the curator.
Set `current: true` only on the release intended to be the dataset's canonical page. A dataset with published
releases must have exactly one published current release.

Access describes how the provider distributes a cohort; it does not itself decide whether the release may be
published. Use one of these values:

- `direct_open_download`
- `public_account_or_terms`
- `registration_gated`
- `application_or_manual_approval`
- `controlled_data_use_agreement`
- `partial_or_sample_release`
- `private_institutional`
- `access_unclear`

Only the first three can pass the public dataset eligibility gate. The others can still provide sourced context
on an approved paper page.

On de-identification, write what the provider documents and cite it, for example
`statement: "Provider documents de-identification of all DICOM headers."` Never write "HIPAA-free", and never
treat being downloadable as evidence that data were de-identified.

`eligibility` holds the five gates. Each is `pass`, `fail` or `unknown`, with evidence:

| Check | Question |
| --- | --- |
| `publicAccess` | Direct download or basic registration, with no approval committee? |
| `deidentification` | Does the provider document de-identification of human data? |
| `noPhiHosted` | Does this site avoid hosting any patient records? |
| `termsPermitUse` | Do the provider's terms permit what this site does with the material? |
| `samplePermission` | Has reuse permission been checked for every image shown? |

## Variables

`src/data/variables/<release-id>.json`, an array. Keep the provider's original names; add
`normalizedConcept` only as an extra. Set the release's `dictionary.completeness` honestly:

- `complete_for_inspected_release` — every variable in the files that were inspected
- `partial` — a subset, and the page will say so
- `documentation_only` — taken from documentation, not from the files

`dictionary.inspectedScope` says what was actually opened, for example "clinical.csv and the v2 release notes".

### Building a dictionary from the released files

`src/data/variables/kits19.json` is the worked example: 63 clinical fields plus the segmentation labels.

1. **Pin the file.** Download the provider's own metadata file (for KiTS19, `data/kits.json`), and add a source in
   `src/data/sources/` whose URL names the exact commit or version you read.
2. **One entry per field,** named exactly as in the file (`originalName`), including nested keys such as
   `comorbidities.copd`.
3. **Meanings come from the provider's documentation** (for KiTS19, section 3 of the data paper). If a field is not
   documented, say so in `definition`; do not infer its meaning from its name.
4. **Observed facts come from the file:** the value type, the codes that actually occur with their counts, ranges,
   and each missing-value marker with how many records use it (for example `null: not available (57 of 210 cases)`).
5. **Units only where a source states them.** Leave `unit: null` rather than assume centimetres or millimetres.
6. **Record every mismatch between documentation and file** as a quality finding in `src/data/quality/`: renamed
   fields, numbers stored as text, value sets that differ. `src/data/quality/kits19.json` shows the form.
7. Set `dictionary.completeness` to `complete_for_inspected_release` only when every field of the inspected file is
   present, and say in `inspectedScope` what was and was not opened (for example, "imaging volumes not downloaded").

## Papers and their architectures

`src/content/papers/<id>.md`. Document **every architecture the paper reports results for**: proposed models
first, then variants, then baselines, each with its own `id` and `role`. Evaluation results live with the
paper's use of a release and name the model they belong to.

A paper mentioning a dataset is not evidence that it used it. `actualUseEvidence` in the study-use record must
point at the place in the paper that shows the use. A study use targets exactly one of:

- a published `release`, which receives a dataset route; or
- an `externalCohort` with its own access class and verified evidence, which is shown as text and receives no
  dataset route.

Published papers require `approvedBy` and `approvedOn`, independently of release approval. A public study-use
edge requires verified evidence, and a published endpoint may never point through that edge to a draft endpoint.

A result that covers several releases (one classifier evaluated on three TCGA projects together) is recorded in
each release's study use, with a note in its evidence saying the figure belongs to the releases jointly. The paper
page shows it once and lists the releases.

### Describing a model

Write the model fields in your own words from the full text, so papers can be compared; quote only figure
captions and result values. The paper page says so under the architecture table.

- **`pipeline`**: the model from input to output as three to six short steps, each with a `label` and an
  optional `detail` ("ResNet50 (ImageNet)", "Frozen; 1,024-d feature per patch"). The page draws it as a diagram,
  so every model has a picture even when the paper's figure may not be copied.
- **`backbone`, `preprocessing`, `fusion`, `loss`, `outputs`, `trainingInputs`, `inferenceInputs`**: leave a field
  out rather than guess. `fusion` is how patches, phases or features are combined (attention pooling, averaging
  patch scores, an ensemble).
- **`code` and `weights`**: `status`, the `url`, and a `note` for any restriction ("academic research use only").
- **`originalPaper`** on a baseline: the id of the paper that introduced it, when that paper is in the catalogue.
- **`evidence`**: the sources and the sections and figures the model was read from, for example
  "section 3 (TransMIL, the TPT module and PPEG), section 4 and Figure 3". Read the full text; an abstract is not
  enough to describe an architecture.

`tests/fixtures/content/papers/fixture-paper.md` shows every field.

### Architecture figures

A paper's figure may be copied onto the site **only if the paper is CC BY or CC0**. Check the licence at the
source: the Crossref `license` field or the publisher's page for a journal article, and the licence link on the
arXiv abstract page for a preprint (arXiv's default "non-exclusive distribution" licence does not permit reuse).
The validator refuses a `figures` entry under any other licence.

- **Reproduced (`figures`)**: fetch the image with `scripts/research/figures/fetch_paper_figures.py`, which
  checks the Crossref licence first and saves WebP to `public/figures/<paper-id>/`. The entry quotes the caption
  unchanged, adds `alt` text, a `mapsTo` note tying the figure to the model table, the `credit` (authors, title,
  venue, year, figure number and copyright holder), the `license`, what was changed (`changes`; "None" is an
  answer) and the `source`. The page prints all of this under the figure, as CC BY requires.
- **Not reproducible (`linkedFigures`)**: name the figure, summarise it in your own words, link to it, and give the
  reason it is not shown.
- Figures from a paper can contain patient images; a curator looks at them when approving the paper.

## Samples

Each sample needs its own permission check, separate from the dataset licence, plus attribution and the terms
under which it is shown. Say whether the image is an actual dataset sample or a figure from a publication.
Never show an invented image, a mask that does not belong to its image, or unrelated stock imagery.

Preview files go in `public/previews/`, compressed. They live in git history forever, so keep them small.

`src/data/samples/processed-figures.json` is the worked example. For each preview:

- **Folder and format.** Put the file in `public/previews/<release-id>/` as WebP (quality around 80 keeps outlines
  sharp at a fraction of the PNG size). Keep the full-size PNG rendering in `figures/<folder>/`, which is committed
  so anyone can rebuild the previews with `scripts/research/previews/build_previews.py`; add a rendering there only
  when a preview uses it. Raw scans, masks and other dataset files never go in the repository.
- **Caption.** Start with who drew the mask ("Mask: BAMF (AI-generated), corrected by a radiologist.",
  "Mask: KiTS23's own reference labels…"), then describe what the image shows in neutral terms, then point to
  [previews.md](previews.md), which explains how the previews were made and who drew each mask.
- **Attribution.** Name the image source and the mask source separately when they differ (a TCIA collection with
  BAMF or RCC-AID masks), with DOIs, and say who rendered the preview and what was changed (windowed, cropped,
  outlined).
- **Reuse terms.** A preview is an adaptation, so it carries the source dataset's licence, with a link to the
  official licence page. A share-alike licence (such as KiTS23's CC BY-NC-SA 4.0) passes on to the preview.
- **Approval.** Leave `permissionApprovedBy` and `permissionApprovedOn` null for a curator, and set the release's
  `eligibility.samplePermission` to `unknown` until they approve every preview it shows.

## Before committing

Run the same checks CI runs (also listed in [CONTRIBUTING.md](../CONTRIBUTING.md)):

```bash
npm run validate   # schemas, references, approval rules, draft checklist
npm run check      # TypeScript and Astro checks
npm test
npm run build      # the full build, including search and the output checks
npm run test:browser  # clicks through the pages; run `npx playwright install chromium` once first
```

Run the browser test whenever you change a page or component: it is the only check that looks at the rendered
pages.

`npm run checklist` prints an approval checklist for every draft release. The curator reads the listed sources, then
sets `approvedBy`, `approvedOn` and `catalogStatus: published` in their own commit.
