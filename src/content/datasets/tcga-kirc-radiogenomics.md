---
id: tcga-kirc-radiogenomics
slug: tcga-kirc-radiogenomics
name: TCGA-KIRC-Radiogenomics — radiologist-read imaging features of clear cell RCC
aliases:
  - TCGA-KIRC-Radiogenomics
  - Radiogenomics of Clear Cell Renal Cell Carcinoma (TCGA-RCC)
summary: One table of imaging features that three radiologists scored on the CT or MRI of 103 TCGA-KIRC patients, with each patient's mutation status for six genes and a few clinical variables; no images or masks of its own.
diseaseTags:
  - renal_tumor
species: human
officialUrl: https://www.cancerimagingarchive.net/analysis-result/tcga-kirc-radiogenomics/
doi: 10.7937/K9/TCIA.2014.K6M61GDW
sources:
  - tcia-tcga-kirc-radiogenomics
  - shinagare-2015
---

TCGA-KIRC-Radiogenomics is an analysis result that The Cancer Imaging Archive lists beside the
TCGA-KIRC collection. The TCGA Renal Cell Carcinoma Imaging Research Group took the first 103
patients of the TCGA clear cell project with pre-surgical CT or MRI, and had each tumour scored
by three radiologists, blinded to the clinical and mutational data, on a feature set the group
agreed beforehand: size, margin, composition, necrosis, growth pattern and calcification. The
study (Shinagare et al. 2015) then related those features to mutations in VHL, PBRM1, BAP1,
SETD2, KDM5C and MUC4.

**What it distributes is one table.** Each row is a patient, keyed by TCGA barcode, with one
summary value per feature (the readers' median, or their most common answer), the six mutation
flags, and age, sex, grade, stage and days to last follow-up. The individual readers' scores are
not released. The scans themselves are TCGA-KIRC's; the analysis-result page links a list of
the 738 series involved.

**It is derived data, not new patients.** All 103 patients are in the TCGA-KIRC collection on
The Cancer Imaging Archive and in the GDC release of TCGA-KIRC, and they join to both by
barcode. Its counts must never be added to those of TCGA-KIRC.

For model work it supplies radiologist-read labels and genotype for a small cohort: 52 patients
have a VHL mutation, but only 5 have BAP1, so per-gene analyses are thin.
