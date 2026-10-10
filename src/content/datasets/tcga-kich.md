---
id: tcga-kich
slug: tcga-kich
name: TCGA-KICH — Kidney Chromophobe
aliases:
  - TCGA-KICH
  - KICH
summary: Whole-slide pathology images and clinical records for chromophobe renal cell carcinoma cases from The Cancer Genome Atlas, with CT and MR for 15 of them in The Cancer Imaging Archive.
diseaseTags:
  - renal_tumor
  - outcomes
species: human
officialUrl: https://portal.gdc.cancer.gov/projects/TCGA-KICH
doi: null
sources:
  - gdc-kich-summary
  - tcia-tcga-kich
---

The chromophobe renal cell carcinoma project of The Cancer Genome Atlas, and the smallest of
its three renal projects at 113 cases. **The GDC release covers the open-access tier only**:
clinical and biospecimen records and whole-slide images.

Its size matters when reading results: a subtype classifier trained across the three renal
projects sees far fewer chromophobe cases than clear cell ones, and the imbalance is a
property of the cohorts rather than of any method applied to them.

**Radiology is a second release.** The Cancer Imaging Archive holds imaging for 15 of the 113
cases (12 with CT), identified by the same TCGA barcodes, so it joins to the slides and
clinical records here. The archive distributes images, with a copy of the TCGA clinical spreadsheets, but no
masks; RCC-AID, catalogued as its own dataset, adds kidney, tumour and cyst masks for 18 of these CT scans.
