---
id: wasserthal-2023
slug: wasserthal-2023
title: 'TotalSegmentator: Robust Segmentation of 104 Anatomic Structures in CT Images'
authors:
  - Jakob Wasserthal
  - Hanns-Christian Breit
  - Manfred T. Meyer
year: 2023
venue: 'Radiology: Artificial Intelligence'
publicationStatus: peer_reviewed
doi: 10.1148/ryai.230024
url: https://arxiv.org/abs/2208.05868
methodSummary: Introduces the TotalSegmentator dataset and a model trained on it to segment 104 anatomical structures, including both kidneys, in CT.
models:
  - id: totalsegmentator-model
    name: TotalSegmentator (nnU-Net based)
    role: proposed
    task: segmentation
    backbone: Not documented in the abstract read for this record
    inputRepresentation: 3d
    outputs: Masks for 104 anatomical structures, including both kidneys
    trainingInputs: 1,204 CT examinations with segmentations
    inferenceInputs: CT volume
    code:
      status: present
      url: https://github.com/wasserth/TotalSegmentator
    weights:
      status: not_documented
catalogStatus: draft
sources:
  - totalsegmentator-paper
  - totalsegmentator-paper-crossref
---

The paper that introduced the TotalSegmentator dataset and model, using 1,204 CT examinations
to segment 104 structures across 27 organs, 59 bones, 10 muscles and 8 vessels.

Only the abstract was read for this record, so the annotation procedure, the ethics statement
and the per-structure results are not recorded. The published dataset has since grown to 117
structures across 1,939 images, so the paper's counts describe an earlier release than the one
catalogued here.
