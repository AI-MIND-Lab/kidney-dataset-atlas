---
id: ucsf-rmac
slug: ucsf-rmac
name: UCSF RMaC — Renal Mass CT
aliases:
  - UCSF RMaC
  - UCSF Renal Mass CT Dataset
summary: 831 pre-operative multiphase 3D CT examinations of small renal masses, with tumor localization and surgical pathology labels.
diseaseTags:
  - renal_tumor
species: human
officialUrl: https://imagingdatasets.ucsf.edu/dataset/3
doi: 10.58078/C2WC74
sources:
  - ucsf-rmac-repo
  - ucsf-rmac-aws
  - ucsf-rmac-preprint
---

UCSF RMaC is a renal-mass classification and localization resource assembled from CT
examinations acquired at the University of California, San Francisco between 2002 and 2018.
The cohort is limited to surgically treated renal masses no larger than 7 cm (T1 stage), so it
does not represent the full spectrum of renal cancer.

Each examination has an unenhanced CT volume and may have arterial/corticomedullary, portal
venous/nephrogenic, and delayed/excretory volumes. Post-contrast volumes were registered to the
unenhanced volume when registration succeeded. The release includes a tumor outline or bounding
box, postoperative pathology, tumor type and—where applicable—pathology grade.

The downloadable files are HDF5 containers rather than the source DICOM studies. One container
holds the available CT phases, a mask, selected patient and scanner attributes, and pathology
labels. A separate CSV records whether each phase is absent, present but unregistered, or present
and registered.

The provider reports **831 examinations**. This atlas does not relabel that as 831 unique patients:
the public documentation uses both “exam” and patient-keyed filenames without explicitly stating
that the patient count and examination count are identical.
