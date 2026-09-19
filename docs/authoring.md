# Authoring records

Every page on the site is generated from the files described here. Two rules sit above all the others:

1. **Nothing is invented.** Counts, variables, licences, pairings, paper uses, metrics and citations come from a
   source, and the record names that source and where in it the claim appears.
2. **Unknown is written as unknown.** Never fill a gap with zero, "no", or a plausible guess.

## Saying what you do not know

| Value | Use it when |
| --- | --- |
| `present` | The source states this is there. |
| `absent` | The source states this is not there. |
| `not_documented` | The source does not say. |
| `not_verified` | Someone claims it, but it has not been checked here. |
| `not_applicable` | The question does not apply to this release. |

Counts carry both a number and a state. An unknown count is `value: null` with a state, never `value: 0`.
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

## Papers and their architectures

`src/content/papers/<id>.md`. Document **every architecture the paper reports results for**: proposed models
first, then variants, then baselines, each with its own `id` and `role`. Evaluation results live with the
paper's use of a release and name the model they belong to.

A paper mentioning a dataset is not evidence that it used it. `actualUseEvidence` in the study-use record must
point at the place in the paper that shows the use.

## Samples

Each sample needs its own permission check, separate from the dataset licence, plus attribution and the terms
under which it is shown. Say whether the image is an actual dataset sample or a figure from a publication.
Never show an invented image, a mask that does not belong to its image, or unrelated stock imagery.

Preview files go in `public/previews/`, compressed. They live in git history forever, so keep them small.

## Before committing

```bash
npm run validate   # schemas, references, approval rules, draft checklist
npm test
```

Validation prints an approval checklist for every draft release. The curator reads the listed sources, then
sets `approvedBy`, `approvedOn` and `catalogStatus: published` in their own commit.
