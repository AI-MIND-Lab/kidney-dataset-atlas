---
id: rcc-aid
slug: rcc-aid
name: RCC-AID — Renal Cell Carcinoma AI Dataset
aliases:
  - RCC-AID
  - Renal Cell Carcinoma AI Dataset for Medical Imaging Research
summary: Kidney, tumour and cyst masks for 129 contrast-enhanced CT scans from the three TCGA kidney cancer imaging collections, with the images converted to NIfTI.
diseaseTags:
  - renal_tumor
  - cysts
species: human
officialUrl: https://doi.org/10.5281/zenodo.20719257
doi: 10.5281/zenodo.20719257
sources:
  - rcc-aid-zenodo
  - rcc-aid-paper
  - rcc-aid-code
---

RCC-AID is an annotation set for the CT scans that The Cancer Imaging Archive holds for the
TCGA kidney cancer projects: clear cell (TCGA-KIRC), papillary (TCGA-KIRP) and chromophobe
(TCGA-KICH). The Radboudumc group behind it screened every CT series in the three collections,
generated kidney and lesion masks with their own segmentation model, and had trained students
correct them and pick out the primary tumour and any cysts, with a radiologist deciding
uncertain cases. A radiologist also labelled each scan's contrast phase.

**It is derived data, not new patients.** Every scan comes from the TCGA collections catalogued
on the TCGA-KIRC, TCGA-KIRP and TCGA-KICH pages, and each patient joins back to the TCGA
clinical records and slides by barcode. Counts from RCC-AID must never be added to counts from
those collections.

The images are redistributed under the TCIA collections' CC BY 3.0 licence and the masks under
CC BY 4.0, so both sources need attribution.

## RCC-AID v2 addendum

This catalogue's current RCC-AID release is **version 2.0.0**, published on June 16,
2026. Existing descriptions above are preserved; the following information supplements
them specifically for v2. The provider's documented changes from v1 are conversion
repairs, removal of irreparably broken files, and additional contrast-phase annotations.
The same TCGA-derived resource is being cleaned and supplemented, rather than a new
patient cohort being added. [Version log](https://zenodo.org/records/20719257)

| Release | CT scans | Unique patients |
| --- | --- | --- |
| Version 1.0.0 | 142 | 101 |
| Version 2.0.0 | 129 | 91 |
| Net reduction | 13 | 10 |

The paper's exclusion diagram counts patients represented in excluded scans, which
can include people who still have another retained scan. It does not mean that 13
unique patients disappeared between releases. The source TCGA collection populations
are also larger than the RCC-AID subset and must not be confused with its released
counts. [Paper, Figure 1 and Table 1](https://www.melba-journal.org/pdf/2026:039.pdf)

### V2 cohort and acquisition context

| Source collection | Histology | Released scans | Unique patients |
| --- | --- | --- | --- |
| TCGA-KIRC | Clear cell RCC | 85 | 65 |
| TCGA-KIRP | Papillary RCC | 26 | 16 |
| TCGA-KICH | Chromophobe RCC | 18 | 10 |
| Total | Three RCC subtypes | 129 | 91 |

These are the v2 subset counts, not the full TCIA collection counts.
[Repository cohort summary](https://github.com/DIAGNijmegen/oncology-RCC-AID-codebase)

The v2 metadata contains 26 arterial, 50 venous and 53 delayed series. Repeated scans
from the same patient need to remain in the same partition if the dataset is split.
The authors do not define a single official train/validation/test split or a hidden
challenge test set. Their dataset-description paper does not train a segmentation
benchmark model. [Paper, sections 3 and 6](https://www.melba-journal.org/pdf/2026:039.pdf)

### Files and metadata inspected for this addendum

The version-pinned download provides `images.zip` (about 4.1 GB), `labels.zip` (about
4.1 MB), `metadata.csv` (about 72.9 kB), and `manifest.tcia`. The manifest retrieves
original TCIA DICOM; the image and mask archives contain converted NIfTI volumes.
[V2 files](https://zenodo.org/records/20719257)

On October 8, 2026, all 41 columns and 129 rows of the v2 metadata CSV were inspected.
The atlas dictionary now includes the previously missing fields while retaining its
original entries. `PatientID` and `PatientName` are both present. The CSV also includes
study and series identifiers, source site and collection, scanner and acquisition
fields, licensing fields, and the added `phase_name` annotation.
[Inspected metadata](https://zenodo.org/records/20719257/files/metadata.csv?download=1)

The sum of `ImageCount` is **16,055 source-series images**. This is not a count of
patients or volumes, and the converted NIfTI slice counts were not independently
checked. Blank administrative columns do not imply absent segmentation masks.
`EthnicGroup` codes and `FileSize` units remain undocumented in the inspected file.
Study and series descriptions are not free-text radiology reports. The CSV does not
contain separate tumour-size columns; the paper's measurements and the analysis
code's derived output should be treated separately from the distributed metadata.
[Inspected metadata](https://zenodo.org/records/20719257/files/metadata.csv?download=1)

### Using v2 for external evaluation

For an external KiTS23 segmentation evaluation, keep RCC-AID frozen and out of
training or model selection. Check patient and scan overlap with any TCGA data used
elsewhere, including foundation-model pretraining. If RCC-AID is later added to
training, it no longer constitutes an independent external test cohort for that
experiment; reserve another patient-level test cohort. This is evaluation guidance,
not a provider-prescribed benchmark protocol.

RCC-AID and separately downloaded TCGA-KIRC, TCGA-KIRP or TCGA-KICH data can represent
the same patients. The subtype-balanced annotation selection also does not make the
final cohort equally balanced across subtypes. Compare scan counts and patient counts
separately. [Paper, sections 3 and 5](https://www.melba-journal.org/pdf/2026:039.pdf)
