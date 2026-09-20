---
id: totalsegmentator-ct
slug: totalsegmentator-ct
name: TotalSegmentator CT
aliases:
  - TotalSegmentator
summary: Routine clinical CT scans with segmentations of many anatomical structures, including both kidneys, released to train and evaluate whole-body segmentation.
diseaseTags:
  - other
species: human
officialUrl: https://github.com/wasserth/TotalSegmentator
doi: 10.5281/zenodo.6802613
sources:
  - totalsegmentator-ct-zenodo
---

A general anatomical segmentation dataset, not a kidney cohort. It earns a place here because
both kidneys are among the structures segmented in every scan, which makes it useful for
pre-processing, localisation and for pre-training kidney models.

The scans come from clinical routine across many scanners, protocols and institutions, and
include a range of pathologies. Nothing in the collection is selected for kidney disease, so a
kidney label here is an anatomical outline, not a diagnosis.

The published dataset has moved well beyond the paper that introduced it: the paper describes
104 structures in 1,204 examinations, while the current release holds 117 structures across
1,939 images. Anyone citing counts has to say which they mean.
