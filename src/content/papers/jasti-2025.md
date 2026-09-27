---
id: jasti-2025
slug: jasti-2025
title: Histopathology based AI model predicts anti-angiogenic therapy response in renal cancer clinical trial
authors:
  - Jay Jasti
  - Hua Zhong
  - Vandana Panwar
  - Vipul Jarmale
  - Jeffrey Miyata
  - Deyssy Carrillo
  - Alana Christie
  - Dinesh Rakheja
  - Zora Modrusan
  - Edward Ernest Kadel
  - Niha Beig
  - Mahrukh Huseni
  - James Brugarolas
  - Payal Kapur
  - Satwik Rajaram
year: 2025
venue: Nature Communications
publicationStatus: peer_reviewed
doi: 10.1038/s41467-025-57717-6
url: https://doi.org/10.1038/s41467-025-57717-6
methodSummary: A U-Net with a ResNet encoder predicts both a CD31 vascular mask and the RNA-based Angioscore from H&E patches of clear cell RCC; TCGA-KIRC slides with matched RNA supply the Angioscore training targets.
figures:
  - id: jasti-figure-1
    label: Figure 1
    title: Project and approach overview
    path: /figures/jasti-2025/figure-1.webp
    width: 1746
    height: 2369
    alt: >-
      Three panels. A: tumour patches from an H&E slide go into a deep learning model that predicts an Angioscore,
      validated against RNA Angioscores and applied to therapy response. B: an encoder-decoder model turns an H&E
      patch into a vascular mask, trained with RNA and CD31 immunohistochemistry data. C: a slide heat map of the
      predicted score with close-ups of the predicted vessels.
    caption: >-
      Project and approach overview. A Schematic outlining the H&E DL Model development, validation and practical
      application of the model. The model predicts Angioscores directly from an H&E-stained slide and is validated
      against the RNA-based Angioscore using multiple independent datasets. The validated model is applied to
      independent, previously unseen, clinical datasets where its predicted Angioscore is correlated with response to
      antiangiogenic (AA) therapy. B H&E DL Model is an interpretable machine learning model to predict Angioscore
      from H&E images. Given an input H&E image, the model predicts a vascular mask (green), and the proportion of
      positive pixels is the output H&E-based Angioscore. Training data consists of two datasets with H&E images
      matched with RNA-based Angioscores and CD31 IHC (basis of the vascular mask), providing the target ground truth.
      The model is trained to predict the vascular mask matching the CD31 and the RNA-based Angioscore (see
      Supplementary Fig 1 and methods for details). C Illustration of the model output on a ccRCC case with
      intra-slide heterogeneity and available multiregional RNA sequencing data. The central plot shows the model H&E
      Angioscore (blue-white-red colormap) applied to all tumor areas on the slide. To contrast against the output
      from patch level models (e.g., based on MIL), we calculated a local average of the percentage positive vascular
      mask prediction within a 416 x 416px grid, which show a far lower level of explainability than the pixel level
      vascular masks shown alongside. Three areas (circles) are marked where we had the ground truth RNA-based
      Angioscores (circle colors in yellow, red colormap). There is a broad qualitative agreement in the amount of
      vasculature and the H&E- based and RNA-based Angioscores, and both capture ITH which would have been missed by
      the standard slide-level bulk sequencing approaches.
    mapsTo: >-
      Panel B is the architecture in the table: the encoder-decoder (U-Net) with its two training targets. TCGA-KIRC
      supplies the RNA-based Angioscore half of the training data.
    credit: >-
      Jasti J, Zhong H, Panwar V, et al. Histopathology based AI model predicts anti-angiogenic therapy response in
      renal cancer clinical trial. Nature Communications 16, 2610 (2025), Figure 1. © The Author(s) 2025.
    license:
      name: CC BY 4.0
      url: https://creativecommons.org/licenses/by/4.0/
    changes: None to the content; converted to WebP.
    source: https://doi.org/10.1038/s41467-025-57717-6
models:
  - id: jasti-he-dl-angio
    name: H&E DL Angio
    role: proposed
    task: regression
    evidence:
      sources: [jasti-2025]
      locator: >-
        Results (model design), Methods (TCGA KIRC dataset, RNA training data), Figure 1 and Code availability
      status: verified
      verifiedOn: 2026-09-26
    pipeline:
      - label: H&E slide
        detail: Tumour regions, 20× magnification
      - label: Tumour patches
        detail: 416 × 416 px
      - label: U-Net, ResNet encoder
        detail: Shared encoder with two heads
      - label: Vascular mask
        detail: Pixels predicted CD31-positive
      - label: H&E DL Angioscore
        detail: Share of positive pixels
    fusion: The Angioscore head and the CD31 mask head share the encoder and are trained to agree
    backbone: U-Net with a ResNet backbone, shared by a CD31 mask arm and an Angioscore arm
    inputRepresentation: patch
    preprocessing: 416 × 416 pixel patches from pathologist-refined tumour regions, at 20× magnification (40× slides downsampled)
    outputs: A CD31-positive vascular mask and a predicted Angioscore for each patch
    trainingInputs: TCGA-KIRC H&E patches with the patient's RNA Angioscore; separate H&E/CD31 restained slides for the mask arm
    inferenceInputs: H&E slide patches
    code:
      status: present
      url: https://github.com/Rajaram-Lab/dl-angio-from-hne
    weights:
      status: present
      url: https://doi.org/10.5281/zenodo.14008281
catalogStatus: draft
approvedBy: null
approvedOn: null
sources:
  - jasti-2025
---

TCGA-KIRC is the training set for the Angioscore arm: 519 slides downloaded from the GDC, less
exclusions for frozen-section-like artefacts, non-clear-cell pathology, benign tissue and
imaging problems. Models are trained with three-fold cross-validation, and the held-out third of
the TCGA slides is used as an internal test. The model is then tested on independent cohorts
(UTSeq and the IMmotion150 trial) that are not part of this catalogue.
