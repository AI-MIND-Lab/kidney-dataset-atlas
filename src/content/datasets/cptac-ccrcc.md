---
id: cptac-ccrcc
slug: cptac-ccrcc
name: CPTAC-CCRCC — Clear Cell Renal Cell Carcinoma
aliases:
  - CPTAC-CCRCC
  - CPTAC Clear Cell Renal Cell Carcinoma
summary: A public, longitudinally linkable collection of renal radiology and whole-slide pathology from the CPTAC clear-cell renal cell carcinoma cohort.
diseaseTags:
  - renal_tumor
  - outcomes
species: human
officialUrl: https://www.cancerimagingarchive.net/collection/cptac-ccrcc/
doi: 10.7937/K9/TCIA.2018.OBLAMN27
sources:
  - cptac-ccrcc-tcia
  - cptac-ccrcc-annotations
---

CPTAC-CCRCC is the kidney clear-cell carcinoma imaging collection from the National Cancer
Institute's Clinical Proteomic Tumor Analysis Consortium. The Cancer Imaging Archive distributes
CT and MRI in DICOM and pathology whole-slide images in SVS. Matching project identifiers connect
subjects to clinical, genomic, and proteomic records held in other Cancer Research Data Commons
systems; those external files can have access rules different from the imaging collection.

Version 14 is an ongoing collection. Its main radiology row contains 65 subjects and 85 studies;
the pathology row contains 222 subjects and 783 whole-slide images. These modality-specific counts
overlap and therefore must not be added as patient counts. TCIA reports 262 subjects for the
collection as a whole. The current release also contains a small non-CCRCC/rare-kidney-tumor
radiology add-on, so users building a pure clear-cell cohort must filter it explicitly.

The base collection does **not** itself provide tumor masks. TCIA publishes a separate derived
analysis result, CPTAC-CCRCC-Tumor-Annotations, with segmentations, seed points, and negative-finding
assessments for 60 subjects. It has its own DOI, version, licence and counts and should not be
silently treated as annotations for all 262 collection subjects.
