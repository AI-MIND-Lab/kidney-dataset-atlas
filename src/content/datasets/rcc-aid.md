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
