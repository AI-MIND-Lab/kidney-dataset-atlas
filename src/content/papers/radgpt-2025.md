---
id: radgpt-2025
slug: radgpt-2025
title: "RadGPT: Constructing 3D Image-Text Tumor Datasets"
authors:
  - Pedro R. A. S. Bassi
  - Mehmet Can Yavuz
  - Ibrahim Ethem Hamamci
  - Sezgin Er
  - Xiaoxi Chen
  - Wenxuan Li
  - Bjoern Menze
  - Sergio Decherchi
  - Andrea Cavalli
  - Kang Wang
  - Yang Yang
  - Alan Yuille
  - Zongwei Zhou
year: 2025
venue: IEEE/CVF International Conference on Computer Vision (ICCV)
publicationStatus: peer_reviewed
doi: 10.1109/ICCV51701.2025.02202
url: https://doi.org/10.1109/ICCV51701.2025.02202
methodSummary: Introduces AbdomenAtlas 3.0 and RadGPT, a pipeline that turns organ and tumour masks into structured reports by fixed rules and into narrative reports with a language model. When run on a segmentation model's output instead of revised masks, RadGPT becomes a report generator. The paper compares it with five published models on the dataset's test set.
linkedFigures:
  - label: Figure 2
    title: The RadGPT 3-stage pipeline for report generation
    url: https://arxiv.org/abs/2501.04678v2
    summary: >-
      Three stages from left to right: segmentation (tumours, organs and vessels), rule-based measurement that fills a
      report template, and language-model rewriting into a hospital's narrative style. Arrows mark where radiologists
      revised the output when the dataset was built. Skipping these revisions gives the fully automatic generator.
    reason: >-
      The arXiv version is licensed CC BY-NC-SA 4.0 and the ICCV version is under IEEE copyright. Neither is CC BY or
      CC0, so the figure is linked rather than copied.
models:
  - id: radgpt-2025-radgpt
    name: RadGPT (fully automatic)
    role: proposed
    task: report_generation
    evidence:
      sources: [radgpt-paper]
      locator: >-
        sections 3.1-3.2 and Figure 2 (pipeline), footnote 1 (structures and vessel model), Appendix B.2 and
        Algorithms 2-4 (measurement, staging, noise reduction), section 4 (fully automatic use)
      status: verified
      verifiedOn: 2026-09-30
    pipeline:
      - label: CT volume
      - label: Segmentation
        detail: DiffTumor and nnU-Net, 26 structures (tumours, organs, vessels)
      - label: Noise removal
        detail: Erosion, dilation and a minimum tumour volume per organ
      - label: Rule-based measurement
        detail: WHO diameters, volume, HU, location, pancreatic T stage
      - label: Structured report
        detail: Radiologist-designed template
      - label: Narrative report
        detail: Llama 3.1 70B (AWQ) rewrites it in a hospital's style
    backbone: DiffTumor and nnU-Net for segmentation, and Llama 3.1 70B (AWQ quantised) for the narrative text
    inputRepresentation: 3d
    preprocessing: >-
      Segmentation output is cleaned by erosion (3×3×3), dilation (4×4×4) and a voxel-wise AND with the original mask.
      An organ counts as having a tumour only above a volume threshold: 1 mm³ in the pancreas, 150 mm³ in the kidneys,
      100 mm³ in the liver and 50 mm³ for metastases. The thresholds were chosen for F1 on a validation set.
    fusion: >-
      The structured report is made by rules. Measurements taken from the masks fill a fixed template. The language
      model is then given 10 example reports with the same kind of tumour and is told not to change findings. It checks
      its output against the structured report.
    outputs: A structured report and a narrative report; the paper reports one result for both, as they carry the same diagnoses.
    trainingInputs: >-
      Not trained end to end. The segmentation models were trained separately. DiffTumor is public, the liver sub-region
      nnU-Net was fine-tuned on 131 LiTS scans, and the vessel model was trained on private data. The language model is
      used without fine-tuning.
    inferenceInputs: A CT scan. When AbdomenAtlas 3.0 was built, radiologist-revised masks replaced the segmentation step.
    code:
      status: present
      url: https://github.com/MrGiovanni/RadGPT
      note: Report generation from masks, report fusion and the LLM labeller.
    weights:
      status: not_verified
      note: >-
        The file generate_reports/README.md ("Perform tumor and organ segmentation") links a DiffTumor tumour model and
        an organ model (RSuperMaskPretrained) on Hugging Face for segmenting new data. The top-level README links a
        separate AbdomenAtlasNet model. Whether these are the exact weights behind Table 2 is not stated.
  - id: radgpt-2025-ct-chat
    name: CT-CHAT (baseline)
    role: baseline
    task: report_generation
    evidence:
      sources: [radgpt-paper]
      locator: Appendix B.1 (training on AbdomenAtlas 3.0); Table 2
      status: verified
      verifiedOn: 2026-09-30
    pipeline:
      - label: CT volume
        detail: 1.5 mm isotropic, cropped or padded to 300 × 300 × 600 mm
      - label: CT-CLIP encoder
        detail: Patch size 20
      - label: Attention pooling
        detail: 256 learned query tokens
      - label: Linear projection
      - label: Llama 3.1 8B
        detail: Report text
    inputRepresentation: 3d
    trainingInputs: >-
      AbdomenAtlas 3.0 CT scans and structured reports only, without the masks. Training followed the original authors'
      code and settings. It ran for 20,000 iterations with batch size 16 on four A100 GPUs, then 100 epochs of visual
      instruction fine-tuning.
    inferenceInputs: A CT scan
  - id: radgpt-2025-ct2rep
    name: CT2Rep (baseline)
    role: baseline
    task: report_generation
    evidence:
      sources: [radgpt-paper]
      locator: Appendix B.1 (training on AbdomenAtlas 3.0); Table 2
      status: verified
      verifiedOn: 2026-09-30
    pipeline:
      - label: CT volume
        detail: 1.5 mm isotropic
      - label: CT2Rep
        detail: The original authors' architecture and settings
      - label: Report text
        detail: Sub-word tokens, up to 600
    inputRepresentation: 3d
    trainingInputs: >-
      AbdomenAtlas 3.0 CT scans and structured reports only, without the masks. The model was selected by validation
      loss, with 30% of the data held out for validation.
    inferenceInputs: A CT scan
  - id: radgpt-2025-merlin
    name: Merlin (baseline)
    role: baseline
    task: report_generation
    evidence:
      sources: [radgpt-paper]
      locator: Appendix B.1 (training on AbdomenAtlas 3.0); section 4; Table 2
      status: verified
      verifiedOn: 2026-09-30
      note: >-
        Appendix B.1 and the Table 2 caption say Merlin was trained on AbdomenAtlas 3.0, but section 4 lists it with the
        models trained elsewhere. Its report-generation weights were not available, so only its pretrained image
        encoder was reused.
    pipeline:
      - label: CT volume
      - label: Merlin image encoder
        detail: Pretrained on abdominal CT
      - label: Linear projection
      - label: Rad Llama2 7B
        detail: Report text
    inputRepresentation: 3d
    trainingInputs: AbdomenAtlas 3.0 CT scans and structured reports only, without the masks. Training was 100 epochs of visual instruction fine-tuning.
    inferenceInputs: A CT scan
  - id: radgpt-2025-m3d
    name: M3D (baseline)
    role: baseline
    task: report_generation
    evidence:
      sources: [radgpt-paper]
      locator: Section 4 and the Table 2 caption (evaluated zero-shot); Table 2
      status: verified
      verifiedOn: 2026-09-30
    pipeline:
      - label: CT volume
      - label: M3D
        detail: Public release, not retrained
      - label: Report text
    inputRepresentation: 3d
    trainingInputs: Not trained on AbdomenAtlas 3.0. It was used as released by its authors.
    inferenceInputs: A CT scan
  - id: radgpt-2025-radfm
    name: RadFM (baseline)
    role: baseline
    task: report_generation
    evidence:
      sources: [radgpt-paper]
      locator: The Table 2 caption (evaluated zero-shot); Table 2
      status: verified
      verifiedOn: 2026-09-30
    pipeline:
      - label: CT volume
      - label: RadFM
        detail: Public release, not retrained
      - label: Report text
    inputRepresentation: 3d
    trainingInputs: Not trained on AbdomenAtlas 3.0. It was used as released by its authors.
    inferenceInputs: A CT scan
catalogStatus: draft
approvedBy: null
approvedOn: null
sources:
  - radgpt-paper
  - radgpt-iccv
  - radgpt-repo-readme
  - radgpt-generate-readme
---

The paper is the dataset's own publication. It builds AbdomenAtlas 3.0 from the 9,262 CT scans of AbdomenAtlas 1.1.
AI proposes the lesion masks, radiologists correct them, and RadGPT turns the corrected masks into reports.

To compare report generators, a language model reads each report and says whether it describes a liver, kidney or
pancreatic tumour. Those answers are compared with the same reading of the reference reports. Radiologists checked this
reading on 447 reports and found it right 96% of the time. The results are tumour-detection sensitivity and specificity
by organ, not text similarity. The paper also tests every model on a private set from UCSF. That set is not part of this
catalogue, and its results are not recorded here.
