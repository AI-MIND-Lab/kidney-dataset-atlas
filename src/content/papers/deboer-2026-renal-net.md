---
id: deboer-2026-renal-net
slug: deboer-2026-renal-net
title: "Robust Renal Mass Segmentation on CT: A Validation Study of an AI-Based Framework"
authors:
  - Sarah de Boer
  - Hartmut Häntze
  - Kiran Vaidhya Venkadesh
  - Myrthe A. D. Buser
  - Gabriel E. Humpire Mamani
  - Lina Xu
  - Lisa C. Adams
  - Jawed Nawabi
  - Keno K. Bressem
  - Bram van Ginneken
  - Mathias Prokop
  - Alessa Hering
year: 2026
venue: Machine Learning for Biomedical Imaging
publicationStatus: peer_reviewed
doi: 10.59275/j.melba.2026-67g5
url: https://doi.org/10.59275/j.melba.2026-67g5
methodSummary: Renal-Net, an nnU-Net trained only on public data (KiTS23 and the Radboudumc kidney abnormality set), segments kidneys and renal masses on CT and is validated on three external test sets, one of them a TCGA-KIRC subset with radiologist-corrected BAMF masks.
linkedFigures:
  - label: Figure 1
    title: Overview of the research
    url: https://doi.org/10.59275/j.melba.2026-67g5
    summary: >-
      An nnU-Net that segments the kidney and any kidney lesions is trained on two public datasets, then validated on
      three test sets from three medical centres, with subgroups by patient sex, age, tumour subtype and contrast phase.
    reason: >-
      The paper is CC BY 4.0, so this figure may be reproduced, but it is a vector drawing that could not be extracted
      cleanly from the PDF. It is linked until a faithful copy is made.
models:
  - id: renal-net
    name: Renal-Net
    role: proposed
    task: segmentation
    evidence:
      sources: [deboer-2026-renal-net]
      locator: >-
        sections 2.1 to 2.3 (training data and framework), section 3.1 (evaluation) and Figure 1
      status: verified
      verifiedOn: 2026-09-26
    pipeline:
      - label: Abdominal CT
      - label: nnU-Net
        detail: Trained on KiTS23 (489) and Radboudumc (215) scans
      - label: Post-processing
        detail: Evaluated with and without it
      - label: Kidney + renal mass masks
    backbone: nnU-Net
    inputRepresentation: 3d
    outputs: Kidney and renal mass masks
    trainingInputs: KiTS23 (489 scans) and the Radboudumc public training set (215 scans)
    inferenceInputs: A CT scan
    code:
      status: present
      url: https://github.com/DIAGNijmegen/oncology-kidney-abnormality-segmentation
    weights:
      status: not_documented
  - id: renal-net-totalsegmentator-baseline
    name: TotalSegmentator (baseline)
    role: baseline
    originalPaper: wasserthal-2023
    task: segmentation
    evidence:
      sources: [deboer-2026-renal-net]
      locator: >-
        section 3.1 (comparison models); its architecture is on the TotalSegmentator paper page
      status: verified
      verifiedOn: 2026-09-26
    inputRepresentation: 3d
catalogStatus: draft
approvedBy: null
approvedOn: null
sources:
  - deboer-2026-renal-net
---

The TCGA-KIRC test set is the subset annotated under the AIMI initiative, where a model's masks
were corrected by a radiologist (Murugesan et al. 2024): 28 valid image-mask pairs after
incomplete pairs were excluded. The BAMF model is left out of the TCGA-KIRC comparison because
TCGA-KIRC was part of its training data. The same group later used this model to start the
RCC-AID annotations.
