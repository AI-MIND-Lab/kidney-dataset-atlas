---
id: kits
slug: kits
name: KiTS — Kidney Tumor Segmentation Challenge
aliases:
  - KiTS
  - KiTS23
summary: Contrast-enhanced CT of nephrectomy patients with kidney, tumour and cyst segmentations, released for the Kidney Tumor Segmentation Challenge.
diseaseTags:
  - renal_tumor
species: human
officialUrl: https://kits-challenge.org/kits23/
sources:
  - kits23-challenge-page
  - kits19-data-paper
  - kits21-paper
  - kits23-clinical-metadata
  - c4kc-kits-tcia
---

KiTS (Kidney Tumor Segmentation Challenge) provides preoperative contrast-enhanced CT,
segmentation masks and clinical metadata for research on kidneys and renal masses.
The editions build on overlapping cohorts, so their patient counts should not be added together.

**KiTS19 / C4KC-KiTS:** KiTS19 introduced kidney and tumour segmentation using preoperative CT.
The challenge included 300 cases, with 210 released for training and 90 held out for testing.
C4KC-KiTS archives those same 210 training cases on TCIA, with DICOM images,
DICOM SEG masks and clinical data; it is not an additional cohort.
[KiTS19 data paper](https://arxiv.org/html/1904.00445#S2) ·
[TCIA collection](https://www.cancerimagingarchive.net/collection/c4kc-kits/)

**KiTS21:** This edition provides separate kidney, tumour and cyst labels, with three
independent delineations per region of interest. Its 300 public training cases reuse the
same patients as the full KiTS19 cohort (210 training plus 90 test cases), with new
annotations. It also introduced a separate 100-case test cohort.
[KiTS21 challenge paper](https://arxiv.org/html/2307.01984#S2.SS1)

**KiTS23:** This edition expands the public training set to 489 cases and uses a new
110-case challenge test set. It retains the 300 KiTS19/KiTS21 cases in its training set and adds
nephrogenic-phase CT alongside corticomedullary-phase CT. It includes kidney, tumour and
cyst masks, plus case-level clinical metadata in `dataset/kits23.json`.
[KiTS23 challenge page](https://kits-challenge.org/kits23/) ·
[Clinical metadata](https://github.com/neheller/kits23/blob/main/dataset/kits23.json)
