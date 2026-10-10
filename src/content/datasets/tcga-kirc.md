---
id: tcga-kirc
slug: tcga-kirc
name: TCGA-KIRC — Kidney Renal Clear Cell Carcinoma
aliases:
  - TCGA-KIRC
  - KIRC
summary: Whole-slide pathology images and clinical records for clear cell renal cell carcinoma cases from The Cancer Genome Atlas, with CT and MR for about half of them in The Cancer Imaging Archive.
diseaseTags:
  - renal_tumor
  - outcomes
species: human
officialUrl: https://portal.gdc.cancer.gov/projects/TCGA-KIRC
sources:
  - gdc-kirc-summary
  - tcia-tcga-kirc
---

TCGA-KIRC is the clear cell renal cell carcinoma project of The Cancer Genome Atlas. The
Genomic Data Commons distributes its data in two tiers, and **the GDC release covers the
open-access tier only**: clinical and biospecimen records, and whole-slide tissue and
diagnostic slide images. The controlled-access tier, which includes low-level sequencing
data and germline variants, needs dbGaP authorisation and is deliberately outside this
record.

A case is a patient, identified by a TCGA barcode. Cases carry demographic fields,
one or more diagnoses, follow-up records, and slide images in SVS format.

**Radiology is a second release.** The Cancer Imaging Archive holds CT and MR for 267 of
the 537 cases (237 with CT). Its patient identifiers are the same TCGA barcodes, and every
imaging patient matches a case in the GDC release, so imaging joins to slides and clinical
records by barcode. The imaging patients are a subset of the GDC cases, not extra ones.

The archive distributes images, with a copy of the TCGA clinical spreadsheets; it holds no masks.
Masks for some of the CT scans come from two separate sources: BAMF's AI-generated kidney, tumour and cyst masks under the AIMI Annotations
initiative (156 scans, 39 of them scored by a radiologist), and RCC-AID, catalogued as its own
dataset, whose student-corrected masks cover 85 scans.

Two analysis results listed on the archive's collection page are also catalogued as their own
datasets: TCGA-KIRC-Radiogenomics, with imaging features scored by three radiologists and
mutation status for 103 patients, and Crowds-Cure-2017, with single-line lesion measurements
drawn at RSNA 2017 on scans of 159 patients. Both describe these patients' scans and add no
new patients.
