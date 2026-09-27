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
linkedFigures:
  - label: Figure 1b
    title: Iterative annotation workflow of the training dataset
    url: https://doi.org/10.1148/ryai.230024
    summary: >-
      A preliminary nnU-Net was trained on the first manually segmented patients, and its predictions were reviewed
      and corrected, with retraining after 5, 20 and 100 patients; the final model was then trained anew,
      independently of these intermediate models.
    reason: >-
      Not reproduced: the journal version is not published under an open licence, and the arXiv version carries
      arXiv's non-exclusive distribution licence, which does not permit reuse of its figures.
models:
  - id: totalsegmentator-model
    name: TotalSegmentator (nnU-Net)
    role: proposed
    task: segmentation
    evidence:
      sources: [totalsegmentator-paper]
      locator: >-
        the arXiv full text: sections 2.1 to 2.3 (dataset, annotation workflow, model) and Figure 1b
      status: verified
      verifiedOn: 2026-09-26
    pipeline:
      - label: CT scan
        detail: Routine clinical CT of any body region
      - label: Resample
        detail: 1.5 mm isotropic (a lighter model uses 3 mm)
      - label: nnU-Net
        detail: Self-configuring 3D U-Net
      - label: 104 structure masks
        detail: Organs, bones, muscles and vessels, including both kidneys
    backbone: nnU-Net, a U-Net implementation that configures its own hyperparameters from the dataset
    inputRepresentation: 3d
    preprocessing: All images resampled to 1.5 mm isotropic; a second model trained at 3 mm for lower memory and GPU needs
    outputs: Masks for 104 anatomical structures, including both kidneys
    trainingInputs: >-
      1,082 CT examinations (57 for validation, 65 for testing), annotated by an iterative workflow in which nnU-Net
      predictions were reviewed and corrected
    inferenceInputs: CT volume
    code:
      status: present
      url: https://github.com/wasserth/TotalSegmentator
    weights:
      status: not_documented
catalogStatus: draft
approvedBy: null
approvedOn: null
sources:
  - totalsegmentator-paper
  - totalsegmentator-paper-crossref
---

The paper that introduced the TotalSegmentator dataset and model, using 1,204 CT examinations
to segment 104 structures across 27 organs, 59 bones, 10 muscles and 8 vessels.

The model is a standard nnU-Net; the paper's contribution is the dataset and its annotation
workflow, in which intermediate nnU-Net models pre-segmented cases that were then corrected by
hand. Details come from the arXiv version; the ethics statement and per-structure results are not
recorded here. The published dataset has since grown to 117
structures across 1,939 images, so the paper's counts describe an earlier release than the one
catalogued here.
