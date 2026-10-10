---
id: crowds-cure-2017
slug: crowds-cure-2017
name: Crowds-Cure-2017 — Crowds Cure Cancer measurements from RSNA 2017
aliases:
  - Crowds-Cure-2017
  - Crowds Cure Cancer 2017
summary: Single-line lesion measurements that RSNA 2017 attendees drew on CT scans from four TCGA collections; the kidney part is 1,282 measurements on scans of 159 TCGA-KIRC patients.
diseaseTags:
  - renal_tumor
species: human
officialUrl: https://www.cancerimagingarchive.net/analysis-result/crowds-cure-2017/
doi: 10.7937/K9/TCIA.2018.OW73VLO2
sources:
  - tcia-crowds-cure-2017
  - tcia-crowds-cure-2018
---

Crowds Cure Cancer was a web application shown at the 2017 annual meeting of the Radiological
Society of North America (RSNA). Attendees opened CT scans from four TCGA collections on The
Cancer Imaging Archive (lung, kidney, liver and ovarian cancer) and were asked to draw one line
across the largest lesion. Each measurement records who drew it, under a nickname such as
misty_mandrill, and whether that person was a radiologist. The archive released the measurements as a table and
as DICOM structured reports, with a snapshot of the patients' GDC clinical records.

**This record describes the kidney part:** 1,282 of the 2,345 measurements, drawn on 237 CT
series of 159 TCGA-KIRC patients by 68 people, 770 of them by radiologists. The lung, liver and
ovarian parts are outside a kidney catalogue.

**These are lengths, not masks.** Each is a single line on one slice. The 2017 application
offered no way to say where the lesion was or what it looked like, so the file does not say
whether a measured lesion is the kidney tumour. Several people measured each patient (a median
of six measurements), but the file does not say whether they measured the same lesion.

**It is derived data, not new patients.** Every kidney measurement is on a series of the TCGA-KIRC
collection, and every patient is a TCGA-KIRC case, so its counts must never be added to those of
TCGA-KIRC.
