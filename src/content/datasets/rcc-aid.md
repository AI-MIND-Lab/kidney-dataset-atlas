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

RCC-AID provides contrast-enhanced CT and kidney, primary tumour and cyst masks for
renal cell carcinoma research. Its source images come from the TCGA-KIRC (clear cell),
TCGA-KIRP (papillary) and TCGA-KICH (chromophobe) collections on The Cancer Imaging Archive.
The released cohort includes 129 scans from 91 patients; some patients contribute more
than one scan. The overlap table below lists the contribution from each source collection.
[Dataset paper, sections 5.1 and 6.1, Table 3](https://www.melba-journal.org/pdf/2026:039.pdf)

The Radboudumc team screened the source CT series, generated initial kidney and renal-mass
masks with a segmentation model, and had trained students correct them and identify the
primary tumour and cysts. Uncertain cases were referred to a radiologist, and a second
radiologist assigned contrast phases. The Quality section describes the review outcomes
and the limits of these annotations.
[Dataset paper, sections 5.2.2-5.2.4](https://www.melba-journal.org/pdf/2026:039.pdf)

Version 2.0.0 was released on June 16, 2026. It repairs conversion errors, removes
irreparable files and adds contrast-phase annotations to the earlier release, which
contained 142 scans from 101 patients. The download includes converted NIfTI volumes,
matching masks, scan-level metadata and a manifest for retrieving the original TCIA DICOM.
[Zenodo release and version log](https://zenodo.org/records/20719257)
