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
figures:
  - id: tabibu-figure-1
    label: Figure 1
    title: Cancer classification pipeline
    path: /figures/tabibu-2019/figure-1.webp
    width: 1903
    height: 911
    alt: >-
      Pipeline diagram. Patches are cut from kidney whole-slide images; one CNN classifies patches as cancer or normal
      and marks high-probability tumour patches; a second CNN is trained on tumour patches of the three subtypes, and
      features from its penultimate layer go to a DAG-SVM that assigns the subtype.
    caption: >-
      Cancer Classification Pipeline. (1) Kidney Whole slide images. (2) 512*512 patches extracted from images with
      50% overlap and background removed using pixel thresholding. (3) Patches from normal and cancerous slides fed to
      the deep network. (4) Patches classified as cancerous or non-cancerous. (5) High probability patches identified
      by the trained network and binary mask is applied. (6) The patches from three subtypes used to train a similar
      deep architecture for a three-way classification. (7) Features extracted from the penultimate layer of the
      network and fed to DAG-SVM and a three-way classification is performed by it.
    mapsTo: >-
      The top row (steps 3 to 5) is the tumour-versus-normal classifier; the bottom row (steps 6 and 7) is the CNN
      with DAG-SVM. The figure labels the bottom model "KICH vs KIRC vs KICH"; the paper's text makes clear the three
      classes are KICH, KIRC and KIRP.
    credit: >-
      Tabibu S, Vinod PK, Jawahar CV. Pan-Renal Cell Carcinoma classification and survival prediction from
      histopathology images using deep learning. Scientific Reports 9, 10509 (2019), Figure 1. © The Author(s) 2019.
    license:
      name: CC BY 4.0
      url: https://creativecommons.org/licenses/by/4.0/
    changes: None to the content; converted to WebP.
    source: https://doi.org/10.1038/s41598-019-46718-3
models:
  - id: tabibu-cnn-tumour-vs-normal
    name: CNN tumour-versus-normal classifier
    role: proposed
    task: classification
    evidence:
      sources: [tabibu-2019]
      locator: >-
        Methods (data, background removal, training architecture and framework) and Figure 1
      status: verified
      verifiedOn: 2026-09-26
    pipeline:
      - label: Whole-slide image
      - label: 512 × 512 patches
        detail: 50% overlap; background removed by thresholding
      - label: ResNet-18 / ResNet-34
        detail: ImageNet-pretrained, fine-tuned; input resized to 224 × 224
      - label: Cancer or normal
        detail: Per patch; high-probability tumour patches kept
    backbone: ResNet-18 and ResNet-34 pretrained on ImageNet, fine-tuned with the final layer replaced by two outputs
    inputRepresentation: patch
    preprocessing: 512 × 512 patches with 50% overlap at 20× and 40×, background removed by pixel thresholding, resized to 224 × 224
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
    evidence:
      sources: [tabibu-2019]
      locator: >-
        Methods (DAG-SVM, training architecture and framework), Figures 1 and 2, and the subtype-classification results table
      status: verified
      verifiedOn: 2026-09-26
    pipeline:
      - label: Tumour patches
        detail: High-probability patches from the first model
      - label: ResNet (fine-tuned)
        detail: Trained for three-way subtype classification
      - label: Penultimate-layer features
      - label: DAG-SVM
        detail: Binary SVMs for each pair of classes
      - label: Subtype
        detail: Clear cell, papillary or chromophobe
    backbone: ResNet-18 or ResNet-34 pretrained on ImageNet, fine-tuned with the final layer replaced by three outputs
    inputRepresentation: patch
    preprocessing: Tumour patches selected by the tumour-versus-normal model, resized to 224 × 224
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

The catalog records the figures the authors themselves report: 93.39% (KIRC) and 87.34% (KICH)
patch-wise accuracy for tumour versus normal, best slide-wise AUCs of 0.98 and 0.95, and 94.07%
for subtype classification. The paper's tables hold further rows for other networks and
magnifications (for example 80.57% for KICH with ResNet-34 at 40×, and 92.62% patch-wise for the
subtypes with ResNet-18 and DAG-SVM); each result's note names the table row behind it, and where
the authors' summary differs from their tables (KIRC's AUC is 0.99 in Table 2), the note says so.
