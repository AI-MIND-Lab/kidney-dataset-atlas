# TCGA kidney data dictionary page

`tcga_data_dictionary.html` is a standalone data dictionary for the TCGA kidney family, built in the same format as
[`../ghazal/rmac_data_dictionary.html`](../ghazal/rmac_data_dictionary.html). It is not part of the atlas website: open
the file in a web browser. GitHub shows only its source, and at 4.1 MB it shows a "View raw" link instead.

## What it covers

- TCGA-KIRC, TCGA-KIRP and TCGA-KICH: the GDC open-access records (clinical, biospecimen, slide files) and the TCIA
  radiology collections.
- TCGA-KIRC-Radiogenomics and Crowds-Cure-2017, the two analysis results on TCGA-KIRC.
- The BAMF (AIMI) and RCC-AID masks for TCGA scans.
- The 16 atlas preview images of TCGA-KIRC and RCC-AID.

## How the format follows the RMaC page

The page reuses the RMaC page's stylesheet unchanged and the same structure:

| RMaC page | This page |
|---|---|
| Top bar with search, grouped sidebar, numbered sections | Same |
| Overview with count cards | Same: cases, patients with radiology, slide files, fields |
| Evidence badges (DOCUMENTED, OBSERVED, CALCULATED, UNVERIFIED, CONFLICTING) | Same labels |
| `[S01]`-style source links, with a numbered source list | Same, numbered in order of first use |
| Master field dictionary with presets, filters and a field details panel | Same, with filters for project, GDC entity, type and evidence |
| Codes and categories as folded tables | Same, with counts for each project |
| Data embedded as JSON in the page; JSON and CSV downloads | Same |
| Glossary with a search box and a domain filter | Same |
| Analysis notes | Same: a list of the inputs read |

Its sections are different where the data differ. It has whole-slide images, radiology series, masks and annotations,
shared patients across sources, reported limitations and papers that used the data. It has no image-size or intensity
profiling, because the TCIA DICOM headers were not read.

## Wording rule

Every sentence on the page is quoted, with its citation and section, from one of these:

- a provider: the GDC, TCIA, BAMF, RCC-AID, or the analysis-result pages;
- a paper that explains a term of the dataset.

Field definitions and code meanings are the GDC data dictionary's own text. Everything else is labels, counts and the
Analysis notes list.

Quotes are cut directly from saved copies of the source texts, and the build stops if a phrase is not found exactly.
The only change made to a quote is joining PDF line-break hyphens ("in- cludes" becomes "includes"); real hyphens such
as "board-certified" are kept. Oddities in the sources are kept as written, for example BAMF's reference number in
"TCGA-KIRC 15 collection" and "Cervical" in TCIA's TCGA-KIRP summary.

Two pieces of atlas wording remain, both from the preview format on main: the mask line under each preview, and the
folded "Credit and licence" text, which the CC BY licences require.

## Inputs

| Input | Used for |
|---|---|
| Atlas records in `src/content` and `src/data`: releases, variables, sources, overlaps, study uses, preview records | Structure, coverage and code counts, provider terms, preview captions |
| GDC data dictionary and case records, Data Release 46.0 (cached by `scripts/research/dictionary/build_tcga_gdc.py`) | Field definitions, code meanings, cohort counts |
| TCIA API series lists for the three collections | Patients, studies, series, images, modalities, manufacturers |
| BAMF `qa-results.csv` (Zenodo) and RCC-AID `metadata.csv` (Zenodo) | Mask counts for each collection |
| TCIA collection and analysis-result pages, the GDC access page, and the full texts of the cited papers | Quotes |
| `public/previews/tcga-kirc-tcia/` and `public/previews/rcc-aid-v2/` | The 16 preview images, embedded in the page |

## What is left out

- No patient-level records or identifier lists. Case IDs appear only in the preview captions, as on the site.
- Field values that are record IDs containing a patient barcode (KICH `diagnoses.tumor_of_origin`) are not listed; the
  field details panel gives how many were left out.
- Codes are limited to the 25 most frequent per field, as in the atlas dictionary.

## How it is built

The page is built from [`tcga_page.yaml`](tcga_page.yaml) by the scripts in
[`scripts/research/pages/`](../../../scripts/research/pages/). From the repository root:

```bash
pip install -r scripts/research/requirements.txt
python scripts/research/dictionary/build_tcga_gdc.py                              # GDC records and data dictionary
python scripts/research/pages/tcga_extras.py                                      # counts and GDC wording
python scripts/research/pages/fetch_texts.py docs/contributions/i-sababishraq/tcga_page.yaml
python scripts/research/pages/build_page.py docs/contributions/i-sababishraq/tcga_page.yaml
```

The downloads (GDC, TCIA, Zenodo, and the texts of the quoted pages and papers) go in `.research-cache/`, which git
ignores. A build from fresh downloads stops if any quote is no longer found word for word in its source.

The tables are written into the HTML, so they show when scripts are blocked. A small script inside the page adds the
filters, search, the field details panel and the downloads. The page was tested in a browser for errors, filters, the
field details panel, downloads, image enlarging, search, phone width, and viewing with scripts off.

To build a page like this for another dataset, see [the guide](../README.md).
