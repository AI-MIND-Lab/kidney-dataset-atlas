# Research tools

Python scripts that produce or check the evidence behind catalogue records: data dictionaries built from released
files and APIs, preview images, paper figures, and the literature search behind the paper candidates. The site
itself does not use them; they are here so that any collaborator can reproduce, extend or re-check what the
records say.

## Set up

Python 3.10 or newer, then from the repository root:

```bash
pip install -r scripts/research/requirements.txt
```

Codespaces installs these for you. Optionally set `RESEARCH_CONTACT_EMAIL` to your email address: OpenAlex,
Crossref and Unpaywall ask for a contact address, and it is sent only to them (`verify_fulltext.py` needs it for
Unpaywall).

Everything the tools download (API responses, full texts, provider files) goes in `.research-cache/` at the
repository root. Git ignores it: it can always be fetched again, and much of it belongs to third parties. Delete a
folder in it to force a fresh download, for example after a provider publishes a new release.

## The tools

### Data dictionaries (`dictionary/`)

| Script | What it does | Writes |
|---|---|---|
| `build_kits19.py` | Builds the KiTS19 dictionary from `kits.json` at a pinned commit, with meanings from the KiTS19 data paper | `src/data/variables/kits19.json` |
| `build_tcga_gdc.py` | Builds the TCGA-KIRC, -KIRP and -KICH dictionaries from the GDC API and the GDC data dictionary: every clinical field with a real value, plus slide-file fields. Run `python scripts/research/dictionary/build_tcga_gdc.py KIRC` for one project | `src/data/variables/tcga-*-gdc-open.json` |
| `build_abdomenatlas3.py` | Builds the AbdomenAtlas 3.0 dictionary from the metadata table at a pinned Hugging Face revision (every column, recounted on all rows) and the mask file list, with meanings from the RadGPT paper and metadata script. Set `ABDOMENATLAS_CSV` to a local copy of the table to skip the 16 MB download | `src/data/variables/abdomenatlas-3-0-mini.json` |
| `build_deeptumorvqa.py` | Builds the DeepTumorVQA 2.0 dictionary from the question files, metadata table, subtype schema, leaderboard and agent files at a pinned Hugging Face revision (every column, recounted on all rows). Set `DEEPTUMORVQA_DIR` to a local copy of the text files to skip the download of about 290 MB, and `ABDOMENATLAS_CSV` to the AbdomenAtlas 3.0 metadata table, which it compares the report columns with | `src/data/variables/deeptumorvqa-2-0.json` |
| `build_amosmm.py` | Builds the AMOS-MM dictionary from the two JSON files of the Google Drive release (every field, recounted on all records; each file checked by sha256), with meanings from the Codabench page and the challenge design document. Set `AMOSMM_DIR` to a folder with local copies to skip the download of about 21 MB | `src/data/variables/amos-mm-2024.json` |
| `kits_files.py` | Helper: the KiTS clinical files pinned to the commits the dictionaries were built from | (used by the builders) |

A new dictionary builder belongs here too, so the dictionary can be regenerated; see "Building a dictionary from
the released files" in [docs/authoring.md](../../docs/authoring.md).

### Preview images (`previews/`)

`build_previews.py` compresses the full-size renderings in `figures/<folder>/` to WebP in
`public/previews/<release>/` and writes `src/data/samples/processed-figures.json`, with each preview's caption,
attribution and reuse terms. Rebuilding from the committed renderings gives byte-identical files. To add a preview,
put its PNG rendering in `figures/<folder>/` and add an entry with its caption and alt text in the script. See
[docs/previews.md](../../docs/previews.md) for how the renderings were made and how to read them.

### Paper figures (`figures/`)

`fetch_paper_figures.py` downloads the architecture figures of CC BY papers to `public/figures/<paper-id>/` as
WebP. For each DOI it checks the Crossref licence first and skips the paper if it is not CC BY; an arXiv figure
is listed only after checking the licence on its abstract page. Add a paper to its `FIGURES` list, run it, then add
the `figures` entry to the paper record (see "Architecture figures" in
[docs/authoring.md](../../docs/authoring.md)). Pass paper ids as arguments to fetch only those papers' figures.

### Literature search (`literature/`)

Finds papers that cite or name each dataset in the research inventory and turns them into the review sheet in
`docs/literature/`. The steps run in order; each reads the previous step's output from `.research-cache/literature/`.

| Step | Script | Source |
|---|---|---|
| 1 | `harvest_semantic_scholar.py` | Papers citing each dataset's anchor papers, with citing sentences |
| 2 | `search_europepmc.py` | Open-access papers naming each dataset in their Methods section or text |
| 3 | `harvest_openalex.py` | Citing works and abstracts from OpenAlex |
| 4 | `fetch_datacite.py` | Works citing dataset DOIs (TCIA, Zenodo, Mendeley, Figshare) |
| 5 | `classify_candidates.py` | Ranks dataset-paper candidates by how likely the paper used the data |
| 6 | `build_candidate_report.py` | Writes `docs/literature/paper-candidates.md` and `.csv` |
| 7 | `verify_fulltext.py` | For the shortlisted papers in `fulltext_checklist.py`, fetches the full text and shows where it names the dataset |

`anchors.json` lists, for each dataset, the papers whose citations are harvested and the names that mark a sentence
as naming the dataset. `verified_status.py` records which dataset-paper pairs were confirmed or excluded after a
full-text check, so the report can mark them.

The pipeline finds **candidates**. A paper becomes a record only after someone reads its full text and confirms
the paper actually used the data; see "Papers and their architectures" in
[docs/authoring.md](../../docs/authoring.md).

## Shared code

`common.py` holds the paths, the cache location, and an HTTP helper that retries politely on rate limits.
