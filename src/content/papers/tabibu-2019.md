---
id: tabibu-2019
slug: tabibu-2019
title: Pan-Renal Cell Carcinoma classification and survival prediction from histopathology images using deep learning
authors:
  - Sairam Tabibu
  - P. K. Vinod
  - C. V. Jawahar
year: 2019
venue: Scientific Reports
publicationStatus: peer_reviewed
doi: 10.1038/s41598-019-46718-3
url: https://pmc.ncbi.nlm.nih.gov/articles/PMC6642160/
methodSummary: Convolutional networks classify renal cell carcinoma subtypes and separate tumour from normal tissue on whole-slide images, and morphological features extracted from predicted tumour regions are related to survival.
models:
  - id: tabibu-cnn-tumour-vs-normal
    name: CNN tumour-versus-normal classifier
    role: proposed
    task: classification
    backbone: Not documented in the sections read for this record
    inputRepresentation: patch
    preprocessing: Patches taken from whole-slide images at 40x
    outputs: Tumour or normal for each patch
    trainingInputs: TCGA renal whole-slide images
    inferenceInputs: Whole-slide image patches
    code:
      status: not_documented
    weights:
      status: not_documented
  - id: tabibu-cnn-dag-svm
    name: CNN with directed acyclic graph SVM
    role: proposed
    task: classification
    backbone: Not documented in the sections read for this record
    inputRepresentation: patch
    preprocessing: Patches taken from whole-slide images
    fusion: A directed acyclic graph of binary SVMs breaks the three-subtype problem into binary decisions
    outputs: Clear cell, papillary or chromophobe
    trainingInputs: TCGA renal whole-slide images from three projects
    inferenceInputs: Whole-slide image patches
    code:
      status: not_documented
    weights:
      status: not_documented
catalogStatus: draft
approvedBy: null
approvedOn: null
sources:
  - tabibu-2019
---

The paper trains convolutional networks on whole-slide images from three TCGA renal projects,
separating tumour from normal tissue and classifying the subtype, then relates shape and
nuclei features from predicted tumour regions to survival in the clear cell cohort.

Two sets of figures appear for the same models: the abstract reports 93.39% and 87.34% for
tumour versus normal, and 94.07% for subtype classification, while the results section reports
patch-wise figures of 93.39%, 80.57% and 92.62%. The level at which each figure was aggregated
was not established here, so the catalog records the patch-wise figures with their locator and
notes the difference rather than choosing between them.
