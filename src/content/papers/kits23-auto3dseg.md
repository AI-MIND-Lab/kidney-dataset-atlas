---
id: kits23-auto3dseg
slug: kits23-auto3dseg
title: Automated 3D Segmentation of Kidneys and Tumors in MICCAI KiTS 2023 Challenge
authors:
  - Andriy Myronenko
  - Dong Yang
  - Yufan He
  - Daguang Xu
year: 2023
venue: MICCAI 2023 Kidney and Kidney Tumor Segmentation Challenge
publicationStatus: preprint
doi: null
url: https://arxiv.org/abs/2310.04110
methodSummary: Automated 3D segmentation built with Auto3DSeg in MONAI, submitted to the KiTS 2023 challenge and reported by its authors as the winning entry.
models:
  - id: auto3dseg-kits23
    name: Auto3DSeg (MONAI)
    role: proposed
    originalPaper: null
    task: segmentation
    backbone: Not documented in the abstract read for this record
    inputRepresentation: 3d
    preprocessing: Not documented in the abstract read for this record
    outputs: Kidney, tumour and cyst segmentation on CT
    trainingInputs: KiTS23 training CT with segmentations
    inferenceInputs: CT volume
    code:
      status: not_documented
      note: Auto3DSeg is part of MONAI, but no repository for this specific submission was recorded here.
    weights:
      status: not_documented
catalogStatus: draft
approvedBy: null
approvedOn: null
sources:
  - kits23-winner-paper
---

The authors report an automated segmentation pipeline built with Auto3DSeg in MONAI and
submitted to the 2023 Kidney Tumor Segmentation Challenge.

Only the abstract was read for this record, so the architecture details, preprocessing and
training configuration are marked as not documented rather than guessed. A curator adding the
full text should fill those in and replace this note.
