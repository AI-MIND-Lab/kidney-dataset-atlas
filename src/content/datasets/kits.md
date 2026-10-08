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
---

KiTS releases pre-operative contrast-enhanced CT scans from patients who underwent partial
or radical nephrectomy, together with segmentations of three structures: kidney, tumour and
cyst. It exists to support automatic segmentation of kidneys and renal masses, and each
edition has been used as the basis of a MICCAI challenge.

The KiTS21 publication describes the cohort as patients treated at the University of
Minnesota for suspected renal malignancy, with an independent test set contributed by the
Cleveland Clinic. Annotation was done in three stages: medical trainees placed a bounding
box, then reference pins, and delineation was carried out by crowd workers following that
guidance, with three independent annotations collected for each region of interest.

KiTS23 also provides case-level clinical metadata in `dataset/kits23.json`, linked to the
images by case identifier. Release-specific cohort details and dictionary limitations are
described below; definitions from earlier editions should not be assumed unchanged.
