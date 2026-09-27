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
methodSummary: MONAI's Auto3DSeg configures and trains 3D segmentation networks automatically; an ensemble of SegResNet and DiNTS trained on the KiTS23 training set won the KiTS 2023 challenge.
figures:
  - id: auto3dseg-figure-2
    label: Fig. 2
    title: SegResNet network configuration
    path: /figures/kits23-auto3dseg/figure-2.webp
    width: 1670
    height: 712
    alt: >-
      Diagram of SegResNet, a U-Net-shaped encoder-decoder built from repeated ResNet blocks, with outputs taken at
      several decoder levels for deep supervision.
    caption: >-
      SegResNet network configuration. The network uses repeated ResNet blocks with batch normalization and deep
      supervision
    mapsTo: >-
      This is one of the two networks in the ensemble (SegResNet in the table); the other, DiNTS, has no figure in
      the paper.
    credit: >-
      Myronenko A, Yang D, He Y, Xu D. Automated 3D Segmentation of Kidneys and Tumors in MICCAI KiTS 2023 Challenge.
      arXiv:2310.04110 (2023), Fig. 2. © The authors.
    license:
      name: CC BY 4.0
      url: https://creativecommons.org/licenses/by/4.0/
    changes: None to the content; extracted from the arXiv PDF and converted to WebP.
    source: https://arxiv.org/abs/2310.04110
models:
  - id: auto3dseg-kits23
    name: Auto3DSeg ensemble (SegResNet + DiNTS)
    role: proposed
    originalPaper: null
    task: segmentation
    evidence:
      sources: [kits23-winner-paper]
      locator: >-
        the arXiv v1 full text: section 2 (Methods: SegResNet, DiNTS, metrics, ensembling) and Fig. 2
      status: verified
      verifiedOn: 2026-09-26
    pipeline:
      - label: Abdominal CT
        detail: KiTS23 training set only (489 cases)
      - label: Auto3DSeg set-up
        detail: Data analysis picks intensity range and hyperparameters
      - label: SegResNet + DiNTS
        detail: Each trained with 5-fold cross-validation
      - label: Sliding-window ensemble
        detail: Probability maps resampled to the original spacing and combined
      - label: Three overlapping masks
        detail: Kidney+tumour+cyst, tumour+cyst, tumour
    backbone: >-
      SegResNet (a U-Net-shaped CNN of ResNet blocks with deep supervision, 5 levels, 3 × 3 × 3 convolutions) and
      DiNTS (a densely connected network found by differentiable topology search). SwinUNETR was also trained but
      left out of the final ensemble.
    inputRepresentation: 3d
    preprocessing: >-
      Intensities rescaled from [−54, 242] to [−1, 1] (range set automatically by the data analysis step); SegResNet
      trains on 256 × 256 × 256 crops, DiNTS on 96 × 96 × 96 crops later fine-tuned at larger sizes; random affine,
      flip, intensity, noise and blur augmentation
    fusion: The best checkpoints of SegResNet and DiNTS are ensembled at inference
    loss: Dice loss summed over the deep-supervision levels (SegResNet); Dice plus focal loss (DiNTS)
    outputs: >-
      Three sigmoid channels for the KiTS23 regions (kidney + tumour + cyst, tumour + cyst, tumour), so a voxel can
      carry more than one label
    trainingInputs: KiTS23 training CT with segmentations, split into 5 random folds
    inferenceInputs: CT volume
    code:
      status: present
      url: https://github.com/Project-MONAI/MONAI
      note: The paper points to MONAI's Auto3DSeg; no repository for this specific submission is given.
    weights:
      status: not_documented
catalogStatus: draft
approvedBy: null
approvedOn: null
sources:
  - kits23-winner-paper
---

The authors run MONAI's Auto3DSeg on the KiTS23 training set with a few lines of configuration:
it analyses the data, trains three network types with 5-fold cross-validation, and ensembles
them. The final submission keeps only SegResNet and DiNTS, which did better in cross-validation,
and the authors report that it ranked first in the challenge (average Dice 0.835, surface Dice
0.723).

Details come from the arXiv version (v1, October 2023).
