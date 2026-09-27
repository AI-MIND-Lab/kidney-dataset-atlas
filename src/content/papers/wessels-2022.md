---
id: wessels-2022
slug: wessels-2022
title: Deep learning can predict survival directly from histology in clear cell renal cell carcinoma
authors:
  - Frederik Wessels
  - Max Schmitt
  - Eva Krieghoff-Henning
  - Jakob N. Kather
  - Malin Nientiedt
  - Maximilian C. Kriegmair
  - Thomas S. Worst
  - Manuel Neuberger
  - Matthias Steeg
  - Zoran V. Popovic
  - Timo Gaiser
  - Christof von Kalle
  - Jochen S. Utikal
  - Stefan Fröhling
  - Maurice S. Michel
  - Philipp Nuhn
  - Titus J. Brinker
year: 2022
venue: PLOS ONE
publicationStatus: peer_reviewed
doi: 10.1371/journal.pone.0272656
url: https://doi.org/10.1371/journal.pone.0272656
methodSummary: A ResNet18 trained on tumour patches from one representative H&E slide per patient predicts 5-year overall survival in clear cell RCC; trained on TCGA-KIRC and validated on an in-house cohort.
figures:
  - id: wessels-figure-1
    label: Figure 1
    title: Preprocessing and workflow
    path: /figures/wessels-2022/figure-1.webp
    width: 2100
    height: 1230
    alt: >-
      Workflow diagram. Annotated slides from TCGA and from the in-house cohort are cut into patches (A), all patches
      are colour-normalised to one target (B), a CNN is trained on the TCGA patches (C) and evaluated on the in-house
      patches, shown as an ROC curve (D).
    caption: >-
      Preprocessing and workflow. (A) All annotated whole slide images from TCGA (training set) and from the
      validation cohort from our institution (independent test set) were tessellated into patches and downscaled as
      appropriate. Blurry patches were discarded. All patches were saved with a reference to their original WSI.
      TCGA = The Cancer Genome Atlas. (B) All patches were normalized with the same target, using the method as
      described by Macenko et al. (C) After preprocessing, the TCGA cohort was used to train the CNN. CNN =
      convolutional neural network. (D) The trained CNN was evaluated on the independent validation cohort from our
      institution (in-house).
    mapsTo: >-
      Panels A and B are the preprocessing row of the table, panel C is the training on TCGA-KIRC, and panel D is the
      external evaluation.
    credit: >-
      Wessels F, Schmitt M, Krieghoff-Henning E, et al. Deep learning can predict survival directly from histology in
      clear cell renal cell carcinoma. PLOS ONE 17: e0272656 (2022), Figure 1. © 2022 Wessels et al.
    license:
      name: CC BY 4.0
      url: https://creativecommons.org/licenses/by/4.0/
    changes: None to the content; converted to WebP.
    source: https://doi.org/10.1371/journal.pone.0272656
models:
  - id: wessels-resnet18-5y-os
    name: ResNet18 5-year survival classifier
    role: proposed
    task: survival
    evidence:
      sources: [wessels-2022]
      locator: >-
        Methods (pre-processing and model training) and Figure 1
      status: verified
      verifiedOn: 2026-09-26
    pipeline:
      - label: H&E slide
        detail: One representative slide per patient
      - label: Tumour patches
        detail: 512 × 512 px from annotated tumour; blurry patches dropped
      - label: Stain normalisation
        detail: Macenko method, one target for all patches
      - label: ResNet18
        detail: ImageNet-pretrained, fine-tuned per patch
      - label: Slide average
        detail: Mean patch score, threshold 0.5
      - label: 5-year survival
        detail: Likely alive or likely deceased
    backbone: ResNet18 pretrained on ImageNet
    inputRepresentation: patch
    preprocessing: >-
      Pathologist-annotated tumour regions tessellated in QuPath, keeping patches that overlap the annotation by at
      least half; patches rescaled to 512 × 512 px (0.2527 µm/px), blurry patches discarded (Laplacian variance below
      170), and all patches stain-normalised with the Macenko method
    fusion: Patch probabilities averaged over the slide; above 0.5 means likely deceased within five years
    outputs: Binary 5-year overall survival for each slide, from patch predictions
    trainingInputs: One H&E slide per TCGA-KIRC patient with the 5-year survival label
    inferenceInputs: Tumour patches from one H&E slide
    code:
      status: not_documented
    weights:
      status: not_documented
catalogStatus: draft
approvedBy: null
approvedOn: null
sources:
  - wessels-2022
---

The model is trained and tuned with ten-fold cross-validation on 254 TCGA-KIRC patients, one
slide each, stratified by outcome, metastasis, grade and tumour size, and then tested on 99
patients from the authors' institution. The paper also combines the model's prediction with
age, stage and metastasis in a logistic regression, and relates it to survival with Cox
regression.
