# Kidney Dataset Atlas — Code Agent Implementation Brief

> **About this document.** This is the original product brief (version 1.0, 19 September 2026) from which the
> site was built. It was written as instructions to the AI coding agent that implemented the first version, which
> is why it is addressed to "you" and ends with a hand-off section. It is kept unchanged as the reference for what
> the atlas is meant to become: routes, page sections, data model, approval process and acceptance criteria.
>
> **What has changed since:** the repository became public on 23 September 2026, so the "private phase" in §1, §3
> and §13 is over; the site is still not hosted, and publishing it remains a manual step. Where this brief and the
> [README](../README.md), [CONTRIBUTING.md](../CONTRIBUTING.md) or [decisions.md](decisions.md) disagree, those
> files describe the current state and take precedence. [decisions.md](decisions.md) also records where the
> implementation deliberately departs from this brief.


Version: 1.0 | Prepared: 19 September 2026

## 1. Your task

Build a polished, interactive, open-source kidney research dataset catalog that can be hosted for free on GitHub Pages. Implement a working website, not just a design or a README. This brief is self-contained and captures the agreed product direction.

The central user journey is: find a dataset → open its dedicated page → inspect variables and sample images → discover papers and model architectures using it → compare it with another dataset.

Use the working title **Kidney Dataset Atlas** and description: “Explore open kidney research datasets, understand their variables, and discover the studies built with them.” Do not claim exhaustive coverage or that this is the first kidney atlas.

Inspect the target repository and applicable instructions first. Preserve unrelated work. Make routine implementation decisions autonomously and document meaningful deviations. Build and validate locally and provide a deployment-ready repository. Actual publication follows the user's deployment instructions; this brief does not supply credentials.

The repository owner is GitHub user `i-sababishraq`; the suggested repository name is `kidney-dataset-atlas`. The repository stays private for now. During this private phase the site is not hosted anywhere: GitHub users the owner adds as collaborators build and view it on their own computers. See §13.

## 2. Scope and non-negotiable content rules

The long-term subject scope includes renal tumors, segmentation, CKD, AKI, stones, cysts, transplantation, dialysis, and kidney outcomes. Modalities may include CT, MRI, ultrasound, pathology, clinical tables, and molecular data. The initial implementation should prioritize depth over breadth.

Only publish dataset releases that meet all applicable requirements:

- Publicly accessible through direct download or basic registration, without institutional approval, researcher credentialing, or controlled-access application review.
- Human data have authoritative documentation of de-identification; aggregate, synthetic, and nonhuman data are identified accurately where applicable.
- No PHI or identifiable patient records are collected or hosted by this website.
- Source provenance and terms permit the intended use.
- Each displayed sample has separately verified reuse permission and attribution.

HIPAA is a law, not an access credential. Do not label datasets “HIPAA-free” or imply that being downloadable proves de-identification. Use precise statements such as “Provider documents de-identification,” with a source. Licenses and institutional obligations can still apply to de-identified data.

Public and restricted portions of a collection must be evaluated separately. Unknown eligibility stays in draft; do not put it into the public catalog with an “open” badge. Basic registration must be visible to users. No need to acquire restricted datasets for this project.

Do not fabricate counts, variables, diagnoses, paired-case availability, paper usage, errors, model metrics, or citations. Distinguish “No,” “Not documented,” “Not verified,” and “Not applicable.” Preserve original variable names. Pathology labels do not prove WSI availability; collection-level CT and WSI availability does not prove same-patient or same-lesion pairing.

## 3. Technical approach

Recommended stack:

| Component | Decision |
| --- | --- |
| Site | Astro, static output, TypeScript |
| Content | Markdown descriptions plus schema-validated YAML/JSON |
| Dictionaries | Structured JSON; generated CSV exports |
| Interactivity | Small client components; React only where useful |
| Full-text search | Pagefind, generated after the static build |
| Structured filters | Client-side filtering of a generated compact catalog |
| Hosting | Private phase: not hosted; collaborators run it locally (§13). Public phase: GitHub Pages with the default github.io URL |
| Publishing | GitHub Actions |
| Contributions | GitHub issue forms and pull requests |
| Persistence | Optional browser localStorage for shortlist/preferences |

No paid services, runtime database, server-side rendering dependency, login system, API keys in the browser, or live external API dependency for core navigation. Source records live in Git. Generated pages, indexes, and exports derive from those records.

Use currently compatible stable dependencies, commit the lockfile, and document the supported Node version. Astro officially documents GitHub Pages deployment; Pagefind supports static search. Check current documentation when implementing rather than copying outdated version-specific configuration.

## 4. Information architecture and routes

All paths below are relative to the configured deployment base path.

| Route | Function |
| --- | --- |
| `/` | Dataset explorer homepage |
| `/datasets/[slug]/` | Dataset detail with current verified release |
| `/datasets/[slug]/releases/[release]/` | Stable release-specific detail |
| `/papers/` | Searchable paper explorer |
| `/papers/[slug]/` | Paper and model detail |
| `/compare/` | Compare two to four dataset releases |
| `/about/` | Scope, methodology, evidence definitions, limitations |
| `/contribute/` | Instructions and issue-form links |
| `/404.html` | Helpful not-found page |

Use actual pre-rendered routes so direct navigation and refresh work on GitHub Pages. Avoid relying on an SPA rewrite fallback. Dataset sections use stable anchors: overview, dictionary, samples, structure, papers, quality, access.

A dataset page and its current release's page render from the same record, so without care the site publishes the same content twice and search returns it twice. Handle this as follows:

1. The build determines each dataset's current release (its newest published release) from the records.
2. `/datasets/[slug]/` is the canonical page for the current release. The current release's page declares `/datasets/[slug]/` as its canonical URL; older release pages are canonical to themselves.
3. Search indexes dataset pages, older release pages (labeled "Older release" in results), and all other searchable pages, but not the current release's page. Once any page carries Pagefind's `data-pagefind-body` attribute, Pagefind skips every page without it, so mark every page that should be searchable.
4. Release pages show a banner. The current release links to the main dataset page; an older release links to the newer release.
5. A post-build check fails if two indexed pages describe the same release.

The release URL stays stable for citation, while the dataset URL always shows the current release.

Primary navigation: Datasets · Papers · Compare · About · Contribute. Include global search. Dataset and paper links must work in both directions.

## 5. Homepage explorer

Make the catalog immediately visible, with a short introduction rather than a large marketing hero.

Required controls:

- Search name, abbreviation, description, and aliases.
- Filter disease, modality, research task, annotations, pairing status, access mode, and documentation coverage.
- Card/table view switch, result count, active filter chips, reset, and helpful empty state.
- Sorting by name, last verified date, and verified patient count. Unknown patient counts go last in both sort directions. The patient sort uses patient counts only, never lesion, slice, slide, or record counts.
- Each card shows title, concise summary, modalities, release, verified patient count when known, access, preview where permitted, and View/Compare actions.
- Encode query, filters, and sorting in URL search parameters. Back/forward navigation restores state.
- Comparison tray shows selected releases, permits removal, and limits selection to four.

Never add patient counts across overlapping collections to advertise a total unique population. Catalog statistics must derive from published records, not hard-coded decoration.

## 6. Dataset detail page

Header: dataset name, summary, selected release, modality badges, access status, last verification date, count labels, official-source button, access instructions, citation copy button, and compare action.

Use a sticky section menu and normal scrollable sections. Maintain a readable no-JavaScript overview and usable anchors.

### Overview

Explain purpose, cohort, inclusion/exclusion criteria, supported tasks, modalities, annotation reference standard, strengths, limitations, and what is unavailable. Keep patients, examinations, lesions, slices, slides, and records as separate count types.

### Data dictionary

Search and filter by field name, meaning, clinical/imaging/pathology/outcome group, type, and observation level. Expand rows to show full coding, missing-value conventions, provenance, examples, and sources. Support pagination for large dictionaries, CSV/JSON download, and original names with optional normalized concepts.

Display completeness explicitly: complete for inspected release, partial, or documentation only. State what files/schema were inspected. Do not imply a partial dictionary lists every variable.

Pre-render every documented variable into the page HTML, with each row's full details in a native `<details>` element. The dictionary then works without JavaScript, and Pagefind indexes it, so site-wide search finds variables: searching "eGFR" returns the datasets whose dictionaries document it, linked to their `#dictionary` section. JavaScript adds search, filters, and pagination on top of the rendered rows. Search results and the About page state that dictionary search covers documented variables only and identify partial dictionaries, so a missing hit is never read as a missing variable. If a release's dictionary exceeds about 2,000 variables, move it to a dedicated `/datasets/[slug]/releases/[release]/dictionary/` page rendered the same way.

### Samples

Show real, permitted dataset previews with captions and credit. Support gallery zoom. For compatible sample sets, provide a slice slider and segmentation visibility/opacity controls. Controls must only appear when actual assets support them. State whether a preview is an actual dataset sample or a published figure.

Use compressed previews, not complete datasets. No invented medical images, mismatched masks, or unrelated stock imagery. If permission or assets are unavailable, show an honest empty state and source link.

### Structure and pairing

Explain files, formats, identifiers, joins, observation levels, repeated scans/lesions/slides, and modality relationships. Use a small SVG or accessible diagram where it helps; provide equivalent text. Distinguish same-session phases from follow-up scans, and same-patient from same-lesion pairing. Document known cohort/release overlap.

### Papers and models

List papers by title. Each title links to that paper's page, which holds the method and every architecture. List the original dataset publication separately from downstream uses. Each row also shows year, task, release/subset used, and train/test role. Keep architecture details on the paper page, not the dataset page.

A paper mentioning a dataset is not evidence that it used it. Do not create a global score ranking across incompatible evaluations.

### Quality

Separate observed issues, published reports, and potential checks. Include affected scope, counts where known, source, detection method, and recommended handling. Valid outliers are not automatically errors. State inspection coverage; an empty issue list does not mean the data are error-free.

### Access and sources

Provide official access instructions, registration status, license and conditions, de-identification evidence, sample reuse permission, citation, and sources. Do not claim to grant access or permission on behalf of a provider.

## 7. Paper pages

Show title, authors, year, venue, `publicationStatus` (for example preprint or peer-reviewed), DOI/official URL, linked dataset releases, and original-versus-downstream role. Summarize the paper's method.

Document every architecture the paper presents and reports results for, each as its own model entry: proposed models, variants reported as separate models, and baselines. Mark each model's role (`proposed`, `variant`, or `baseline`) and list proposed models first. When a baseline comes from another paper in the catalog, link to it. For each model, describe task, backbone, input representation (2D/2.5D/3D/WSI/patch/tabular), preprocessing, fusion or distillation, loss if documented, outputs, and training versus deployment inputs. Include a concise original architecture diagram when supported by the paper; do not copy copyrighted figures without permission.

Evaluation entries must name the model they belong to and identify dataset subset, split, patient-level handling, metric, value, units, confidence interval if reported, and external/internal evaluation. Model code and pretrained weights are distinct per-model fields with separate verification status. Unknown details stay unknown.

## 8. Comparison page

Compare two to four releases with sticky dataset headers and rows for counts, disease, modalities, masks, CT phases, pathology labels, WSI, verified pairing, clinical information, follow-up, access, license, limitations, and overlap evidence.

Include Show differences only, remove/replace selection, shareable URL, and CSV export. Handle zero/one selection and malformed or retired IDs gracefully. Unknown is never converted to false. Avoid presenting two different grading systems or cohort counts as automatically equivalent.

Without JavaScript, the compare page shows a short notice that comparison needs JavaScript, followed by links to every published dataset page, where the same facts appear.

## 9. Data model

Use stable IDs independent of display names. Validate references at build time. Suggested collections:

| Entity | Required concepts |
| --- | --- |
| Dataset | id, slug, name, aliases, description, disease tags, official URL, release IDs |
| Release | id, dataset ID, version label, date if known, counts by unit, modalities, cohort, tasks, access, license, de-identification evidence, pairing, verification date, `catalogStatus`, eligibility checks, `researchedBy`, `approvedBy`, `approvedOn` |
| Variable | id, release ID, original name, file/table, definition, type, unit, coding, missing values, observation level, time point, role, group, raw/derived, provenance, evidence |
| Paper | id, slug, title, authors, year, venue, `publicationStatus`, DOI/URL, method summary, model IDs |
| Model | id, paper ID, name, role (`proposed`/`variant`/`baseline`), original paper ID for baselines, task, backbone, input representation, preprocessing, fusion/distillation, loss, outputs, training/inference inputs, code, weights, diagram; may be stored inside its paper's record |
| StudyUse | id, paper ID, release ID, role, actual-use evidence, subset, preprocessing, task, split, evaluation results (each naming a model ID) |
| Sample | id, release ID, asset paths, kind, caption, alt text, source, attribution, reuse terms, `permissionApprovedBy`, `permissionApprovedOn`, image/mask alignment metadata |
| QualityFinding | id, release ID, evidence category, description, inspected scope, affected count, detection, impact, handling, source |
| Source | id, URL, title, locator/page/section, accessed date |
| Overlap | release IDs, overlap type, known count or unknown, explanation, evidence |

Model evidence at the claim or field level where needed, not only as a single bibliography. A useful evidence object has source IDs, locator, status, verification date, and optional note.

Use explicit state enums such as `present`, `absent`, `not_documented`, `not_verified`, `not_applicable`. Numerical unknowns use null plus status; never zero. A release's catalog state is a field named `catalogStatus` with values `draft` or `published`, with eligibility checked separately. It is distinct from a paper's `publicationStatus` (for example `preprint` or `peer_reviewed`); never use one name for the other. Exclude drafts from generated public assets, search, exports, and routes.

A release belongs to one dataset; variables, samples, and findings belong to releases. A paper has one or more models. StudyUse provides the many-to-many paper/release link. The same paper must not be duplicated per dataset.

## 10. Suggested repository organization

| Path | Purpose |
| --- | --- |
| `src/content/datasets/` | Dataset descriptions/records |
| `src/content/releases/` | Release metadata |
| `src/content/papers/` | Paper descriptions/records, including their models |
| `src/data/variables/` | Release-specific dictionaries |
| `src/data/study-uses/` | Paper/release relationships |
| `src/data/samples/` | Preview manifests |
| `src/data/quality/` | Evidence-backed issues |
| `src/data/sources/` | Source records |
| `src/data/overlap/` | Cohort/release overlap |
| `src/data/curators.yaml` | GitHub usernames allowed to approve releases and samples |
| `src/components/` | Reusable UI and interactive components |
| `src/layouts/` and `src/pages/` | Templates and routes |
| `src/lib/` | Validation, filters, comparison, URL helpers |
| `public/previews/` | Approved lightweight preview assets |
| `scripts/` | Validation, index/export generation |
| `tests/` | Focused behavior and deployment tests |
| `.github/workflows/` | CI and Pages deployment |
| `.devcontainer/` | Codespaces setup for collaborators |
| `.github/ISSUE_TEMPLATE/` | Dataset, paper, and correction submissions |
| `docs/` | Content-authoring and maintenance instructions |

Treat this structure as a guide, not a reason to fight current Astro conventions. Do not manually maintain a second copy of counts or paper relationships in UI code.

## 11. Visual and accessibility requirements

Use a restrained academic style: white/off-white surfaces, dark navy text, teal accents, modest borders, generous readable spacing, and clear typography. Prefer real dataset previews and informative tables. Avoid oversized gradients, decorative dashboard charts, or irrelevant imagery.

Responsive desktop/tablet/mobile layouts are required. Tables may scroll within their container without breaking the page. Filters become a labeled mobile panel. Provide keyboard operation, visible focus, semantic headings, labeled inputs, captions, alt text, sufficient contrast, reduced-motion support, and accessible dialog focus handling.

Do not communicate evidence status by color alone. Surface useful empty, loading, and error states. Content should remain understandable without JavaScript even if advanced filtering is unavailable.

## 12. Content seeding and research boundary

Start with three verified releases where feasible, covering imaging with masks, pathology, and clinical tables. These are coverage goals, not permission to invent suitable datasets. KiTS23 is a candidate to investigate, not a blanket preapproval of every asset or release. Verify every selected release against the scope.

Research official sites, original papers, documentation, and original repositories. Use the same records to render all linked pages. For each seeded release, aim for sourced overview, accessible dictionary fields with honest completeness, at least one verified paper relationship, and permitted previews if available.

If a content category cannot be verified, keep it in a clearly documented draft backlog while implementing its UI with test fixtures outside the public build. Synthetic test fixtures must never masquerade as real catalog entries. Report missing content as a release limitation. Do not block the entire software build because research coverage is incomplete.

Existing sites offer inspiration, not evidence of novelty: KPMP, Kidney Cell Atlas, and KiTS. Do not copy their branding or assert they lack features without checking.

### Curator approval

A person, not an agent, decides what the site publishes. `src/data/curators.yaml` lists the GitHub usernames allowed to approve; it starts with `i-sababishraq`.

- Each release records `researchedBy` (`agent` or a GitHub username), `approvedBy`, and `approvedOn`, plus the five eligibility checks from §2, each with a status and sources. Each sample records `permissionApprovedBy` and `permissionApprovedOn`, because sample reuse permission is checked separately.
- An agent writes every record it researches as `draft`. It never sets `approvedBy`, `permissionApprovedBy`, or `catalogStatus: published`.
- Validation prints an approval checklist for each draft release: every eligibility check with its source links, the headline counts with their sources, and each sample's reuse terms.
- The curator opens those sources. If they hold up, the curator fills in the approval fields and switches the release to `published` in their own commit.
- The build fails if a published release has an empty `approvedBy` or one not listed in `curators.yaml`, if any of its eligibility checks has not passed, or if it displays a sample without permission approval.

Approval covers the eligibility checks, sample permissions, and a spot-check of headline counts. Other fields rely on their cited sources and locators, which readers can check themselves. The About page explains what approval does and does not cover.

This is a process control, not a lock. When an agent commits with the owner's git credentials, git history cannot show who checked what, so the approval fields and the reviewed diff are the record.

## 13. Build, search, exports, and deployment

Suggested pipeline: validate records, references, and curator approval → generate compact indexes and exports → build static pages → run Pagefind on output → check routes, assets, and duplicate search entries → publish artifact.

Configure `site` and `base` for both user sites and project sites. All internal links, previews, downloads, Pagefind assets, and query-driven navigation must respect the base path. Verify direct navigation to nested routes under a non-root path.

Keep external paper metadata and official APIs out of runtime-critical paths. Visitors should be able to browse curated content even if source sites are down. External source failures should not silently delete curated records.

Provide commands for development, content validation, type checking, production build, production preview, and focused tests. Document which command generates search. A development server alone is insufficient to verify Pagefind.

Use least-privilege GitHub Actions permissions and the official Pages deployment pattern. PR checks must not deploy unreviewed changes. Production publication should come from the configured branch/manual workflow, consistent with user authorization. Do not embed credentials. Keep the deployment URL configurable.

Private phase: a GitHub Pages site is publicly visible on the internet even when its repository is private, and restricting viewers requires GitHub Enterprise Cloud. The private phase therefore has no hosted site. The owner adds viewers as collaborators on the private repository, and they run the site on their own computers:

- Provide one command that builds the production site, including Pagefind search, and serves it locally (for example `npm run preview:site`). The development server is not enough, because it does not include search.
- Write a README section for collaborators who are not developers: install the supported Node version and git, clone the repository, install dependencies from the lockfile, run the command, and open the printed URL.
- Add a dev container configuration so collaborators can instead open the repository in GitHub Codespaces and install nothing. Each collaborator's Codespaces use counts against their own free monthly allowance.
- CI validates, builds, and tests every push. Include the GitHub Pages deployment workflow for the public phase, but give it a manual trigger only and document that it works once the repository is public.
- Keep `site` and `base` configurable so the move to GitHub Pages is a configuration change.

The build reports total output size and file count. The private phase has no hosting limit, but the public GitHub Pages site will be limited to 1 GB, so the build warns when output passes 1 GB. Preview assets also live in git, which keeps every committed version of every file. GitHub recommends repositories stay under 1 GB (under 5 GB at most) and blocks files over 100 MiB. Compress previews, and avoid repeatedly committing regenerated binary assets.

Downloads must derive from canonical records and include release IDs, completeness, and source references. Escape CSV correctly, including spreadsheet formula-injection handling for text fields. Render text safely; do not inject arbitrary HTML from records or query parameters.

## 14. Implementation milestones

1. Inspect repository; scaffold framework, navigation, styles, configuration, schemas, and build validation.
2. Implement explorer and complete dataset template with empty states and release handling.
3. Implement paper pages and StudyUse relationships; build dictionary, comparison, and sample interactions.
4. Seed verified content and permitted previews; generate exports and search.
5. Validate accessibility, mobile layout, core interactions, and project-base deployment; finish CI and documentation.

Do not defer central requested features as decorative placeholders. Where research evidence is unavailable, distinguish content incompleteness from an unimplemented function.

## 15. Acceptance criteria

- [ ] A fresh install using the lockfile can validate and build the static website.
- [ ] A collaborator can follow the README from clone to a running local site with working search, on their own computer or in Codespaces.
- [ ] Every published dataset opens its own page and release-specific URL.
- [ ] Filters, sorting, URL restoration, result count, and reset work together.
- [ ] Dictionary search, expansion, pagination, and CSV/JSON exports work.
- [ ] Dataset-to-paper and paper-to-dataset navigation agree and identify train/test roles.
- [ ] Paper pages document every architecture the paper presents, and every evaluation result names its model.
- [ ] Comparison supports two to four releases, difference mode, sharing, and export.
- [ ] Samples have accurate captions and provenance; applicable image controls work.
- [ ] Unknown values, incomplete dictionaries, and inspection scope are explicit.
- [ ] Drafts and ineligible datasets never leak into public output or indexes.
- [ ] The build fails when a published release or a displayed sample lacks curator approval.
- [ ] Search returns each release once, and each dataset page and its current release's page declare the same canonical URL.
- [ ] Schema checks catch duplicate IDs and broken relationships.
- [ ] Site-wide search works against the production build.
- [ ] Nested routes, assets, search, and exports work under a repository base path.
- [ ] Main journeys are keyboard accessible and readable on mobile.
- [ ] No paid runtime dependency, backend credential, PHI upload, or full-dataset mirroring is required.
- [ ] No unsupported dataset/model claims or fabricated preview images are published.
- [ ] README explains run/build/deploy and how to add a dataset, variable, paper, sample, or correction.

Use focused tests for filtering and unknown-state semantics, relationship integrity, URL persistence, comparison, and base-path routing. Include a browser smoke test through explorer → detail → dictionary → paper → comparison. Avoid excessive tests that merely duplicate implementation.

## 16. Final handoff from the implementing agent

Provide repository changes, local preview instructions, build/test results, deployment configuration and remaining account setup, seeded dataset inventory, drafts awaiting curator approval with their checklists, missing-content list, and a short maintenance guide. Report whether the site is actually deployed or only deployment-ready. Never claim exhaustive catalog coverage or completed verification when it is partial.

## 17. Future work, outside the first release

Cross-dataset variable harmonization, guided dataset selection, interactive full-volume/WSI viewers, richer cohort-overlap visualization, automated literature-update suggestions, and expanded disease coverage. Automated research suggestions should enter review rather than directly overwrite verified claims. Accounts, patient uploads, paid AI assistants, and runtime databases are not part of the agreed first release.

## 18. Official implementation references

These references support platform choices; they are not sources for unverified dataset records. Checked or discussed during planning on 19 September 2026. Recheck current instructions during implementation.

- [Astro: deploy to GitHub Pages](https://docs.astro.build/en/guides/deploy/github/) — official static deployment and Actions setup.
- [Astro: content collections](https://docs.astro.build/en/guides/content-collections/) — structured content and schema validation.
- [Pagefind](https://pagefind.app/) — search for static sites without a search server.
- [GitHub Pages overview](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) — static hosting and public-repository availability on GitHub Free.
- [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits) — verify current storage/bandwidth limits; planning assumed a 1 GB published-site ceiling.
- [HHS de-identification guidance](https://www.hhs.gov/hipaa/for-professionals/special-topics/de-identification/index.html) — properly de-identified information is no longer PHI under the HIPAA Privacy Rule; this is distinct from licensing.
- [KiTS23](https://kits-challenge.org/kits23/) — candidate dataset and example of dataset/annotation/method documentation; verify applicable license and previews.
- [Kidney Cell Atlas](https://www.kidneycellatlas.org/) — example of kidney dataset exploration.
- [KPMP](https://www.kpmp.org/) — example of a kidney research atlas initiative.
