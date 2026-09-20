---
id: ct-org
slug: ct-org
name: CT-ORG — multiple organ segmentation in CT
aliases:
  - CT-ORG
summary: CT scans with masks for six organ categories including kidneys, drawn from mixed abdominal, full-body and PET-CT sources.
diseaseTags:
  - other
species: human
officialUrl: https://www.cancerimagingarchive.net/collection/ct-org/
doi: null
sources:
  - ct-org-tcia
---

A multi-organ segmentation collection with kidney masks among six organ categories: lung,
bones, liver, kidneys, bladder, and brain in part of the scans.

Its usefulness for kidney work lies in the variety of its sources — abdominal and full body,
contrast and non-contrast, low dose and high dose, including nine scans from PET-CT
examinations. That variety is also its weakness for kidney-specific work: nothing here was
selected for the kidney, and the masks are anatomical outlines.

How the masks were made differs by organ and by split, which matters if you evaluate against
them. Lungs and bones were segmented automatically in the training set and manually in the
test set; every other organ, kidneys included, was segmented by hand.
