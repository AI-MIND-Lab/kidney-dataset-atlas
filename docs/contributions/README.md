# Contributed data dictionary pages

Each folder here holds a collaborator's standalone data dictionary pages. A page is a single HTML file that opens in a
web browser. It holds its own styles, scripts, data and images, and it is not part of the atlas website. GitHub shows
only the source of an HTML file, so download the file or open it locally.

- [`ghazal/rmac_data_dictionary.html`](ghazal/rmac_data_dictionary.html): the UCSF RMaC page. It set the format the
  other pages follow.
- [`i-sababishraq/`](i-sababishraq/): the TCGA kidney page, with the config it is built from.

This guide shows how to build a page in the same format for another dataset, with the scripts in
[`scripts/research/pages/`](../../scripts/research/pages/).

## What the scripts do

| Script | What it does |
|---|---|
| `fetch_texts.py` | Downloads every page and paper the config quotes and saves their plain text in `.research-cache/pages/texts/` |
| `build_page.py` | Builds the page from the config, the atlas records and the saved texts, and writes it next to the config |
| `tcga_extras.py` | The TCGA page's "extras" script: counts from provider files and wording from the GDC data dictionary. Use it as a model if your page needs the same kind of thing |
| `quotes.py` | Used by `build_page.py`: cuts quotes from the saved texts, and stops the build if a quote is not found word for word |
| `page.js`, `page.css` | The page's scripts and the styles added to the RMaC page's stylesheet. `build_page.py` puts them inside the page |

The page takes its field list, coverage, codes, missing-value markers, previews, shared-patient counts and papers
from the atlas records in `src/`. Your dataset's releases, variables and sources therefore need to be in the atlas
first; see [docs/authoring.md](../authoring.md).

## Build a page

1. Set up the research tools once, as in [scripts/research/README.md](../../scripts/research/README.md#set-up):

   ```bash
   pip install -r scripts/research/requirements.txt
   ```

2. Make a folder `docs/contributions/<your GitHub username>/`. Copy
   [`i-sababishraq/tcga_page.yaml`](i-sababishraq/tcga_page.yaml) into it and rename the copy, for example
   `kits23_page.yaml`.

3. Edit the config (see [The config](#the-config) below). Start small: the title, `columns`, `texts`, and a few
   sections. Add more sections once that much builds.

4. Save the texts you quote:

   ```bash
   python scripts/research/pages/fetch_texts.py docs/contributions/<you>/<page>.yaml
   ```

   Some sources refuse downloads, for example a page behind a login or a publisher that blocks scripts. For those, the
   script prints `MISSING` and the path to use. Save the PDF, HTML or text file at that path yourself and run the
   script again. Texts already saved are kept; `--refresh` downloads them all again.

5. If your page shows counts from provider files, or wording from a provider's own dictionary, write an extras script
   and run it (see [Extras](#extras)). Skip this step if the atlas records are enough.

6. Build the page:

   ```bash
   python scripts/research/pages/build_page.py docs/contributions/<you>/<page>.yaml
   ```

   The build stops at the first quote it cannot find, and names the text and the phrase. Fix the phrase in the config
   and build again.

7. Open the page in a browser and check it (see [Check the page](#check-the-page)).

To serve the folder locally instead of opening the file:

```bash
python -m http.server 8000 --directory docs/contributions/<you>
```

Then open `http://localhost:8000/<page>.html`.

## Wording rule

Every sentence on a page is quoted word for word, with its citation and locator, from one of these:

- the provider of the dataset: its website, data page, dictionary or files;
- a paper that explains a term of the dataset.

Everything else is a label (a heading or column name), a number counted from the provider's records, or the
"Analysis notes" list of inputs. Do not write your own descriptions. If no source explains something, leave it out,
or mark the field UNVERIFIED.

The scripts enforce the quoting part. A quote is cut from the saved text of its source, so it cannot drift from the
source, and it is always shown with its source number (`[S01]`), which links to the numbered source list.

**How to write a phrase.** The saved texts are cleaned once when loaded, and phrases must be written in that clean
form:

- Line breaks and runs of spaces become one space.
- A hyphen that a PDF put at a line break is joined, so "in- cludes" is written as `includes`. Real compounds keep the
  hyphen ("board-certified"). The list of compound first parts is `COMPOUND` in `quotes.py`; add to it if a real
  hyphen is lost.
- Spaces before `.,;:)` and after `(` are removed, so "(TCGA) ." is written as `(TCGA).`.

To find the exact text, search the saved file in `.research-cache/pages/texts/<key>.txt`.

## The config

The config is a YAML file. Keys at the top level:

| Key | Meaning |
|---|---|
| `title` | Page title. A `\|` marks the line break in the big heading: `KiTS23\|Data Dictionary` |
| `brand` | Short name in the top bar |
| `description` | One sentence for the page's description tag |
| `slug` | File name for the JSON and CSV downloads |
| `output` | The page's file name, written next to the config |
| `style` | The page whose `<style>` is reused. Keep `docs/contributions/ghazal/rmac_data_dictionary.html` |
| `extras` | Path, from the repository root, of an extras file (optional) |
| `embed_images` | `true` puts the preview images inside the page; `false` links to them in `public/` |
| `definitions` | `atlas` (the default): field definitions and code meanings come from the atlas variables. `extras`: they come only from `field_overrides` in the extras file |
| `hide_codes_matching` | A regular expression. Stored values that match it are not listed, for example values that contain a patient identifier |
| `field_layer` | Small label above a field's name in its details panel, for example `Field` or `GDC field` |
| `labels` | Optional wording of a few labels: `column` (the filter name for columns, default `Release`), `all_columns`, `absent` (shown when a field is not in a column), `entity`, `entity_prefix`, `meaning` |
| `columns` | One entry per release shown side by side: `{label, release, title?, sources?}`. `label` heads the columns, `release` is an atlas release id, `title` is a longer name for cards, and `sources` are added to every field's sources |
| `family` | Release ids whose shared-patient counts and papers are shown. Defaults to the `columns` releases |
| `names` | Short release names for tables, as `{release id: name}`. Without one, a release is shown as "dataset name (version label)" |
| `texts` | Every source a quote is cut from, as `{key: {source, cite?, url?}}`. `source` is the atlas source id it is cited as. `cite` is the short citation shown under a quote. It defaults to the source's title. `url` defaults to the source record's URL |
| `lede` | A quote shown under the title |
| `cards` | Count cards under the title, as `[{value, label, detail?}]`. Usually these come from the extras file instead |
| `overview_caption` | `{text, sources}` under the cards. It can also come from the extras file |
| `overview_group` | Sidebar group of the Overview (default `Dataset`) |
| `links` | Buttons under the title, as `[{label, to: section id}]` |
| `group_order` | Order of field groups in the dictionary (default: administrative, clinical, pathology, outcome) |
| `analysis_tables` | Derived or analysis tables whose columns get their own list: `[{label, release, files_matching?, definitions?}]`. `files_matching` is a regular expression on the variable's file. `definitions` maps a column name to a quote |
| `sections` | The page's sections, in order: `[{id, title, group, layer?, heading?, blocks}]`. `group` is the sidebar heading. `layer` is the small label above the title, as `[text, source\|profile]`. `blocks` is a list of blocks |

A **quote** is written one of three ways:

```yaml
{text: rccaid, phrase: 'RCC-AID provides publicly available', loc: Section 3}   # the whole sentence containing the phrase
{text: rccaid, first: 'For RCC, TCGA in', last: '2016a).', loc: Section 1}       # from `first` to the end of `last`
{text: page_tcga-kirc, value: 'CC BY 3.0', loc: Data Access}                       # exactly this value (quote_table rows only)
```

`loc` is where in the source the quote is: a section, a heading or a table name. It is shown after the citation.
Always give it for a long source.

**Blocks** (each is a one-key mapping):

| Block | Shows |
|---|---|
| `h3: text` | A sub-heading |
| `evidence: DOCUMENTED` (with optional `sources: [...]`) | An evidence badge: DOCUMENTED, OBSERVED, CALCULATED, UNVERIFIED or CONFLICTING |
| `quote: {...}` | One quote |
| `quotes: [{...}, ...]` | Several quotes |
| `quote_table: {columns?, rows}` | A two-column table of labels and quotes. A row is a quote with a `label`, or `{label, extras: key}` for a value from the extras file |
| `caption: text` (with optional `sources`) | A small caption. Use it only for labels and file names |
| `field_dictionary: {}` | The master field table, with presets, filters, the details panel and downloads |
| `analysis_columns: {}` | The list of `analysis_tables` columns |
| `codebooks: [field names]` | Folded tables of stored values, meanings and counts. The first two are open |
| `code_bars: [field names]` | Bar charts of the commonest values of each field, one card per column |
| `previews: [{release, title?}]` | The atlas preview images of each release, with the provider's captions |
| `overlaps: {}` | Shared-patient counts between the `family` releases |
| `missing: {}` | How many records have a value, per field and column |
| `papers: {quotes: {study-use id: [quotes]}}` | Papers that used the `family` releases, with what their authors write |
| `terms: [{label, release}]` | The provider's annotation terms (`annotationTerms`) of each release |
| `glossary: [...]` | Glossary entries: `{term, category?, quote}` or `{extras: key}`. The category is `Medical` or `Technical` |
| `extras_table: key` | A table from the extras file |
| `extras_bars: key` | Bar-chart cards from the extras file |
| `notes: [{input, what, sources?}]` | The Analysis notes table. `{key}` in `what` is replaced by an extras value |
| `sources: {}` | The numbered source list. Put it in the last section |

The TCGA config uses most of these blocks, and YAML anchors (`&name`, `*name`) to reuse a quote.

## Extras

An extras file is JSON that a script writes from provider files. Write the script in `scripts/research/pages/`; the
JSON goes in `.research-cache/pages/`, which git ignores. [`tcga_extras.py`](../../scripts/research/pages/tcga_extras.py)
is the example. Any of these keys can be present:

| Key | Shape | Used by |
|---|---|---|
| `values` | `{key: {value, cite?, sources?}}` | `quote_table` rows with `extras:`, `{key}` in notes |
| `cards`, `overview_caption` | As in the config | The overview |
| `field_overrides` | `{field name: {entity?, property?, definition?, source?, locator?, codes?: {stored value: meaning}}}` | Field definitions and code meanings in the provider's own words |
| `analysis_overrides` | `{analysis table label: {column: {definition, source, locator?}}}` | Analysis column definitions |
| `tables` | `{key: {columns, rows, evidence?, sources?, numcols?, format?: {column index: code\|quote}, caption?}}` | `extras_table` |
| `bars` | `{key: [[{title, rows: [[label, count], ...], total?}, ...], ...]}`: one list per card | `extras_bars` |
| `glossary` | `{key: [{term, definition, cite, source, category?}]}` | `glossary` with `extras:` |

Every `source` must be an atlas source id. Every definition and meaning must be the provider's text, copied exactly.
The file holds counts and dictionary text only, never patient-level records.

## What not to put on a page

- No patient-level records, and no lists of patient or case identifiers. A case ID may appear in a preview caption,
  as on the site. Use `hide_codes_matching` for stored values that contain identifiers.
- No images other than the atlas previews, which carry their credit and licence.
- No text of yours presented as the provider's.
- No PHI, secrets or raw data files in the repository. Saved texts and downloads stay in `.research-cache/`.

## Check the page

Before you share a page, open it in a browser and check that:

- the console shows no errors;
- the field filters, presets and search work, and clicking a field opens its details panel;
- the JSON and CSV downloads work;
- the preview images open larger when clicked;
- the page fits a phone-width window without scrolling sideways;
- the tables still show with JavaScript turned off. They are written into the HTML for that case.

Then read every quote once against its source, especially the `loc` you gave it.
