# Contributing

Thanks for helping build the Kidney Dataset Atlas. There are two ways to take part.

- **No code:** open an issue with one of the templates (suggest a dataset, a paper, or a correction). A curator
  checks the sources and turns it into a record.
- **Code or records:** follow the workflow below.

## Set up

1. Install [Node.js](https://nodejs.org) 24 (the version in `.nvmrc`; 22.12 or newer works) and git.
2. Clone the repository (you need collaborator access while it is private).
3. `npm ci`
4. `npm run preview:drafts` to see the current records as pages. The normal `npm run preview:site` shows
   approved records only, which may be none.

Or open the repository in GitHub Codespaces, which installs everything for you.

## Workflow

1. Create a branch from `main` named for the change: `dataset/<id>`, `paper/<id>`, `fix/<topic>`, `docs/<topic>`.
2. Make the change. Records follow [docs/authoring.md](docs/authoring.md): every claim names a source and where
   in it the claim appears, and unknown values are written as unknown, never as zero or a guess.
3. Before pushing, run the same checks CI runs:

   ```bash
   npm run validate
   npm run check
   npm test
   npm run build
   ```

4. Open a pull request against `main`. Say what changed and which sources you read. CI must pass before merging.
5. A curator reviews and merges. Only a curator listed in `src/data/curators.yaml` may approve a record for
   publication.

### Changes from outside the project team

The collaborators (the curators in `src/data/curators.yaml`, also listed in
[.github/CODEOWNERS](.github/CODEOWNERS)) can give final approval, and any one of them is enough. A change from
anyone else must be verified by one of them before it is merged or approved: the collaborator checks each new or
changed claim against its cited source and records that check by approving the pull request. GitHub enforces
this on `main` with a ruleset that requires one code-owner approval for pull requests from outside the team.
Collaborators can still push to `main` directly.

Write commit messages as a short, sentence-case summary of what the change does ("Add the KiPA22 release",
"Correct the DeepLesion DOI"), with detail in the body when it helps a reviewer.

## Rules that the build enforces

- **Never set approval fields yourself.** `approvedBy`, `permissionApprovedBy` and `catalogStatus: published` are
  set by a curator in their own commit. The validator rejects an approver who is not a curator.
- **Previews yes, raw data no.** Collaborators may add preview images: compressed renderings in
  `public/previews/<release-id>/`, each with a sample record giving its caption, attribution and reuse terms under
  the source dataset's licence (see [docs/previews.md](docs/previews.md) and the Samples section of
  [docs/authoring.md](docs/authoring.md)). Never commit raw scans, masks, archives or other downloads from a
  dataset. A preview shows on draft pages straight away; a curator approves its permission before a published
  page shows it.
- **No protected health information or credentials**, anywhere: records, issues, pull requests or commits.
- **Drafts stay drafts.** A normal build fails if a draft or fixture reaches its output.

## Terms for contributions

- Code and project documentation you contribute are licensed under the MIT License, like the rest of the
  software.
- Records and research content you contribute (anything under `src/content/`, `src/data/` or
  `docs/literature/`, and the research inventory) become part of the catalogue, which is not openly licensed. By
  opening a pull request you confirm that you have the right to submit the material and allow the maintainer to
  include, modify and publish it as part of the atlas.
- Preview images in `public/previews/` keep the licence of the dataset they come from. Each needs a sample record
  stating its attribution and terms, and a curator's permission approval before a published page shows it.

See [LICENSE](LICENSE) for the full terms.

## Useful references

- [README.md](README.md): running the site and the command list
- [docs/authoring.md](docs/authoring.md): record templates, evidence and unknown values
- [docs/decisions.md](docs/decisions.md): why the project works the way it does
- [docs/Kidney_Open_Datasets_and_CV_Papers.md](docs/Kidney_Open_Datasets_and_CV_Papers.md): the research inventory
  that new records come from
