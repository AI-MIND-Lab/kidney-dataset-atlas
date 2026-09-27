---
id: transmil-2021
slug: transmil-2021
title: "TransMIL: Transformer based Correlated Multiple Instance Learning for Whole Slide Image Classification"
authors:
  - Zhuchen Shao
  - Hao Bian
  - Yang Chen
  - Yifeng Wang
  - Jian Zhang
  - Xiangyang Ji
  - Yongbing Zhang
year: 2021
venue: NeurIPS 2021
publicationStatus: peer_reviewed
doi: null
url: https://arxiv.org/abs/2106.00908
methodSummary: A transformer aggregates ImageNet ResNet50 patch features across a whole slide, modelling correlations between patches, to classify renal cell carcinoma subtype from slide-level labels.
figures:
  - id: transmil-figure-3
    label: Figure 3
    title: Overview of TransMIL
    path: /figures/transmil-2021/figure-3.webp
    width: 1874
    height: 484
    alt: >-
      Architecture diagram. Patches cut from whole-slide images are embedded by a pretrained ResNet50; the sequence of
      feature tokens is squared and given a class token, passed through two multi-head self-attention layers with a
      pyramid position encoding generator (PPEG) between them, and the class token goes to an MLP head that outputs
      the class.
    caption: >-
      Overview of our TransMIL. Each WSI is cropped into patches (background is discarded), and embedded in feature
      vectors by ResNet50. Then the sequence is processed with the TPT module: 1) Squaring of sequence; 2) Correlation
      modelling of the sequence; 3) Conditional position encoding and local information fusion; 4) Deep feature
      aggregation; 5) Mapping of T → Y.
    mapsTo: >-
      Left: patching and the frozen ResNet50 (preprocessing and backbone). Middle: squaring, the two self-attention
      layers and PPEG (fusion). Right: the MLP head on the class token (output).
    credit: >-
      Shao Z, Bian H, Chen Y, Wang Y, Zhang J, Ji X, Zhang Y. TransMIL: Transformer based Correlated Multiple Instance
      Learning for Whole Slide Image Classification. NeurIPS 2021; arXiv:2106.00908, Figure 3. © The authors.
    license:
      name: CC BY 4.0
      url: https://creativecommons.org/licenses/by/4.0/
    changes: None to the content; extracted from the arXiv PDF and converted to WebP.
    source: https://arxiv.org/abs/2106.00908
models:
  - id: transmil
    name: TransMIL
    role: proposed
    task: classification
    evidence:
      sources: [transmil-2021]
      locator: >-
        section 3 (TransMIL, the TPT module and PPEG), section 4 (dataset and implementation details) and Figure 3
      status: verified
      verifiedOn: 2026-09-26
    pipeline:
      - label: Whole-slide image
        detail: Background discarded
      - label: Patches at 20×
      - label: ResNet50 (ImageNet)
        detail: Frozen; 1,024-d feature per patch
      - label: Squaring + class token
        detail: First tokens repeated so the length is a square number
      - label: Transformer + PPEG
        detail: Two self-attention layers, pyramid position encoding
      - label: MLP head
        detail: Subtype for the slide
    backbone: ResNet50 pretrained on ImageNet as a frozen patch encoder, followed by a transformer with a pyramid position encoding generator (PPEG)
    inputRepresentation: wsi
    preprocessing: Patches at 20× magnification, each embedded as a 1,024-dimensional feature vector
    fusion: Self-attention across all patch embeddings with a class token
    outputs: Kidney chromophobe, clear cell or papillary renal cell carcinoma for each slide
    trainingInputs: Slide-level subtype labels only
    inferenceInputs: A whole-slide image
    code:
      status: present
      url: https://github.com/szc19990412/TransMIL
    weights:
      status: not_documented
  - id: transmil-clam-mb-baseline
    name: CLAM-MB (baseline)
    role: baseline
    originalPaper: clam-2021
    task: classification
    evidence:
      sources: [transmil-2021]
      locator: >-
        Table 1, where the TransMIL authors report their own run of CLAM-MB; its architecture is on the CLAM paper page
      status: verified
      verifiedOn: 2026-09-26
    inputRepresentation: wsi
catalogStatus: draft
approvedBy: null
approvedOn: null
sources:
  - transmil-2021
---

TransMIL is evaluated on three public slide collections, one of them "TCGA-RCC": 884 diagnostic
slides from the three TCGA kidney cancer projects, the same slide counts CLAM reports. Results
are averaged over four-fold cross-validation, and the paper compares TransMIL with CLAM and
other multiple-instance learning methods on the same folds.
