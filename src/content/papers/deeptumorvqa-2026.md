---
id: deeptumorvqa-2026
slug: deeptumorvqa-2026
title: 'DeepTumorVQA: A Hierarchical 3D CT Benchmark for Stage-Wise Evaluation of Medical VLMs and Tool-Augmented Agents'
authors:
- Yixiong Chen
- Wenjie Xiao
- Pedro R. A. S. Bassi
- Boyan Wang
- Liang He
- Xinze Zhou
- Sezgin Er
- Ibrahim Ethem Hamamci
- Zongwei Zhou
- Alan Yuille
year: 2026
venue: arXiv
publicationStatus: preprint
doi: 10.48550/arXiv.2605.09679
url: https://arxiv.org/abs/2605.09679
methodSummary: 'Introduces DeepTumorVQA, 476K program-generated questions in four stages on 9,262 abdominal CTs. The paper
  evaluates over 30 configurations: zero-shot and fine-tuned 2D and 3D vision-language models, and tool-using agents, including
  a Meissa-4B agent trained on ground-truth tool traces.'
figures:
- id: deeptumorvqa-figure-1
  label: Figure 1
  title: Overview of the DeepTumorVQA benchmark
  path: /figures/deeptumorvqa-2026/figure-1.webp
  width: 1302
  height: 576
  alt: 'Six axial CT slices above example multiple-choice questions grouped into four panels: measurement, recognition, visual
    reasoning and medical reasoning.'
  caption: Overview of the DeepTumorVQA benchmark. The benchmark covers four diagnostic task types with 42 clinical subtypes,
    supports both 2D/3D inputs and both direct inference/agent reasoning, and evaluates along multiple dimensions including
    accuracy, latency, and agent trajectory quality.
  mapsTo: The four panels are the four task types behind the Recognition, Measurement, Visual reasoning and Medical reasoning
    results. The paper has no architecture figure for the models it evaluates.
  credit: 'Chen Y, Xiao W, Bassi PRAS, Wang B, He L, Zhou X, Er S, Hamamci IE, Zhou Z, Yuille A. DeepTumorVQA: A Hierarchical
    3D CT Benchmark for Stage-Wise Evaluation of Medical VLMs and Tool-Augmented Agents. arXiv:2605.09679 (2026), Figure 1.
    © The authors.'
  license:
    name: CC BY 4.0
    url: https://creativecommons.org/licenses/by/4.0/
  changes: None to the content. The figure was taken from the PNG in arXiv's HTML version of the paper and converted to WebP.
  source: https://arxiv.org/abs/2605.09679v1
linkedFigures: []
models:
- id: deeptumorvqa-2026-meissa-4b-sft-agent
  name: Meissa-4B agent trained on tool traces
  role: proposed
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Section 3.3 (tools and modes), section 4.2 and Table 4; Appendix e.4 (agent SFT data)
    status: verified
    verifiedOn: '2026-09-30'
    note: The paper gives the agents' input as "2D+tools" in Table 4, "img+tools" in Table 5 and "Full vol + tools" in Table
      10. The training conversations in Appendix e.4 start with "the 2D slice image". The paper says no more about which image
      reaches the model at test time.
  pipeline:
  - label: 2D image
    detail: 'Table 4: "2D+tools"'
  - &id002
    label: Multiple-choice question
  - label: Meissa-4B
    detail: Trained on 20K ground-truth tool traces
  - label: Tool calls
    detail: Up to 8 ReAct steps
  - &id001
    label: Option letter
  backbone: Meissa-4B
  inputRepresentation: multimodal
  fusion: A ReAct loop of up to 8 steps. The tools are segment_organ (statistics for 43 structures), measure (volume, mean
    HU, diameter, count), lookup_medical_knowledge (a curated knowledge base) and, in vision mode only, crop_region (organ
    crops). Evaluated with oracle and predicted (TotalSegmentator) tool outputs.
  trainingInputs: 20,000 conversations, made by running each subtype's ground-truth tool trace against the tool cache for
    training scans only. They cover 38 of the 42 subtypes.
  inferenceInputs: The 2D image, the question and the tool outputs.
  code:
    status: not_verified
    url: https://github.com/Schuture/DeepTumorVQA
    note: The repository holds the evaluation package. The script that the paper names for building the training data is not
      in it.
  weights:
    status: not_documented
- id: deeptumorvqa-2026-m3d-llama2-ft
  name: M3D-LaMed (LLaMA2-7B), fine-tuned
  role: variant
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Table 15 (architectures), Table 16 (training), Appendix e.2 (3D inputs), Table 3; Table 10 (428K QA supervision)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - label: 3D CT volume
  - label: 3D ViT encoder
  - label: 3D pooling + MLP
    detail: 256 visual tokens
  - label: LLaMA2-7B
    detail: Fine-tuned on the training questions
  - *id001
  backbone: 3D ViT encoder with a LLaMA2-7B decoder
  inputRepresentation: 3d
  preprocessing: HU clipped to −1024…1024, resized to 64 × 256 × 256 (trilinear) and scaled to 0–1. The 3D ViT uses 2 × 16
    × 16 patches.
  trainingInputs: The 428K training questions with their CT volumes. LoRA (rank 16), learning rate 5e-5, AdamW, BF16, 33K
    iterations on 4 A6000 GPUs (about 48 hours).
  inferenceInputs: The CT volume and the multiple-choice question.
- id: deeptumorvqa-2026-m3d-phi3-ft
  name: M3D-LaMed (Phi-3-4B), fine-tuned
  role: variant
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Table 15 (architectures), Table 16 (training), Appendix e.2 (3D inputs), Table 3; Table 10 (428K QA supervision)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - label: 3D CT volume
  - label: 3D ViT encoder
  - label: 3D pooling + MLP
    detail: 256 visual tokens
  - label: Phi-3-4B
    detail: Fine-tuned on the training questions
  - *id001
  backbone: 3D ViT encoder with a Phi-3-4B decoder
  inputRepresentation: 3d
  preprocessing: HU clipped to −1024…1024, resized to 64 × 256 × 256 (trilinear) and scaled to 0–1. The 3D ViT uses 2 × 16
    × 16 patches.
  trainingInputs: The 428K training questions with their CT volumes. LoRA (rank 16), learning rate 5e-5, AdamW, BF16, 33K
    iterations on 4 A6000 GPUs (about 48 hours).
  inferenceInputs: The CT volume and the multiple-choice question.
- id: deeptumorvqa-2026-radfm-ft
  name: RadFM, fine-tuned
  role: variant
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Table 15 (architectures), Table 16 (training), Appendix e.2 (3D inputs), Table 3; Table 10 (428K QA supervision)
    status: verified
    verifiedOn: '2026-09-30'
    note: The input size is from Appendix e.2. Table 15 lists RadFM's input size as 256 × 256 × 64 instead.
  pipeline:
  - label: 3D CT volume
  - label: 3D ViT encoder
  - label: Perceiver resampler
    detail: 32 visual tokens
  - label: LLaMA2-13B
    detail: Fine-tuned on the training questions
  - *id001
  backbone: 3D ViT encoder with a LLaMA2-13B decoder
  inputRepresentation: 3d
  preprocessing: Resized to min(depth, 256) × 256 × 256, HU clipped to −1024…1024 and scaled to 0–1.
  trainingInputs: The 428K training questions with their CT volumes. Full tuning of the language model, learning rate 5e-6,
    8-bit AdamW, FP16, 25K iterations on 4 A5000 GPUs (about 48 hours).
  inferenceInputs: The CT volume and the multiple-choice question.
- id: deeptumorvqa-2026-merlin-ft
  name: Merlin, fine-tuned
  role: variant
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Table 15 (architectures), Table 16 (training), Appendix e.2 (3D inputs), Table 3; Table 10 (428K QA supervision)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - label: 3D CT volume
  - label: 3D ResNet encoder
  - label: One fully connected layer
    detail: 1 visual token
  - label: RadLLaMA-7B
    detail: Fine-tuned on the training questions
  - *id001
  backbone: 3D ResNet encoder with a RadLLaMA-7B decoder
  inputRepresentation: 3d
  preprocessing: Resampled to 1.5 × 1.5 × 3 mm, resized to 160 × 256 × 256, HU clipped to −1024…1024 and scaled to 0–1.
  trainingInputs: The 428K training questions with their CT volumes. LoRA (rank 128), learning rate 1e-4, AdamW, BF16, 25K
    iterations on 4 A5000 GPUs (about 48 hours). Merlin was pretrained on 14K 3D abdominal CTs (Table 15).
  inferenceInputs: The CT volume and the multiple-choice question.
- id: deeptumorvqa-2026-meissa-4b-lora
  name: Meissa-4B, LoRA fine-tuned
  role: variant
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Appendix e.3 (2D LoRA fine-tuning), Table 3; Table 23 caption (option-letter targets)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - label: Organ png
  - *id002
  - label: Meissa-4B
    detail: LoRA fine-tuned
  - label: Answer
    detail: option letters
  backbone: Meissa-4B (Qwen3-VL architecture)
  inputRepresentation: 2d
  trainingInputs: All 428K training questions with organ PNGs, answers as option letters. LoRA rank 16, alpha 32, on the attention
    and MLP projections of all 32 blocks (about 26M trainable parameters), with the image encoder frozen. AdamW, learning
    rate 2e-5, cosine schedule, effective batch 64, 3 epochs (about 20K steps) with per-subtype loss reweighting, on 4 A5000
    GPUs (about 12 hours).
  inferenceInputs: Organ PNG and the question.
- id: deeptumorvqa-2026-meissa-4b-lora-wv
  name: Meissa-4B, LoRA fine-tuned on whole-scan images
  role: variant
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Appendix e.3 (2D LoRA fine-tuning), Table 3; Table 23 caption (option-letter targets) (WV train+infer row)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - label: Whole-scan png
  - *id002
  - label: Meissa-4B
    detail: LoRA fine-tuned
  - label: Answer
    detail: option letters
  backbone: Meissa-4B (Qwen3-VL architecture)
  inputRepresentation: 2d
  trainingInputs: All 428K training questions with whole-scan PNGs, answers as option letters. Appendix ab says they used
    "the same 428K LoRA recipe" as the option-letter models (Appendix e.3). The GitHub free-form leaderboard says "LoRA on
    50K open-ended" instead.
  inferenceInputs: Whole-scan PNG and the question.
- id: deeptumorvqa-2026-qwen3-vl-4b-lora
  name: Qwen3-VL-4B, LoRA fine-tuned
  role: variant
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Appendix e.3 (2D LoRA fine-tuning), Table 3; Table 23 caption (option-letter targets)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - label: Organ png
  - *id002
  - label: Qwen3-VL-4B
    detail: LoRA fine-tuned
  - label: Answer
    detail: option letters
  backbone: Qwen3-VL-4B (Qwen3-VL architecture)
  inputRepresentation: 2d
  trainingInputs: All 428K training questions with organ PNGs, answers as option letters. LoRA rank 16, alpha 32, on the attention
    and MLP projections of all 32 blocks (about 26M trainable parameters), with the image encoder frozen. AdamW, learning
    rate 2e-5, cosine schedule, effective batch 64, 3 epochs (about 20K steps) with per-subtype loss reweighting, on 4 A5000
    GPUs (about 12 hours).
  inferenceInputs: Organ PNG and the question.
- id: deeptumorvqa-2026-meissa-4b-lora-ff
  name: Meissa-4B, LoRA fine-tuned for free-form answers
  role: variant
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Table 23 and its caption; Appendix ab; Appendix e.3
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - label: Organ png
  - *id002
  - label: Meissa-4B
    detail: LoRA fine-tuned
  - label: Answer
    detail: open-ended answers
  backbone: Meissa-4B (Qwen3-VL architecture)
  inputRepresentation: 2d
  trainingInputs: All 428K training questions with organ PNGs and open-ended answers. Appendix ab says they used "the same
    428K LoRA recipe" as the option-letter models (Appendix e.3). The GitHub free-form leaderboard says "LoRA on 50K open-ended"
    instead.
  inferenceInputs: Organ PNG and the question.
- id: deeptumorvqa-2026-qwen3-vl-4b-lora-ff
  name: Qwen3-VL-4B, LoRA fine-tuned for free-form answers
  role: variant
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Table 23 and its caption; Appendix ab; Appendix e.3
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - label: Organ png
  - *id002
  - label: Qwen3-VL-4B
    detail: LoRA fine-tuned
  - label: Answer
    detail: open-ended answers
  backbone: Qwen3-VL-4B (Qwen3-VL architecture)
  inputRepresentation: 2d
  trainingInputs: All 428K training questions with organ PNGs and open-ended answers. Appendix ab says they used "the same
    428K LoRA recipe" as the option-letter models (Appendix e.3). The GitHub free-form leaderboard says "LoRA on 50K open-ended"
    instead.
  inferenceInputs: Organ PNG and the question.
- id: deeptumorvqa-2026-huatuogpt-7b
  name: HuatuoGPT (7B)
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Section 4.1 and Table 3 (direct inference); Table 10 (input protocol); Appendix e.1 (organ slices); Appendices
      n and v.3 (greedy decoding)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - &id003
    label: Organ PNG
    detail: 5 axial slices across the organ, window −150 to 250, side by side
  - *id002
  - label: HuatuoGPT (7B)
    detail: Used as released, greedy decoding
  - *id001
  backbone: Medical vision-language model, 7B parameters (listed as HuatuoGPT-Qwen2.5VL in the leaderboard)
  inputRepresentation: 2d
  trainingInputs: Not trained on DeepTumorVQA. Used as released.
  inferenceInputs: The organ PNG and the multiple-choice question.
- id: deeptumorvqa-2026-internvl3-8b
  name: InternVL3-8B
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Section 4.1 and Table 3 (direct inference); Table 10 (input protocol); Appendix e.1 (organ slices); Appendices
      n and v.3 (greedy decoding)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - *id003
  - *id002
  - label: InternVL3-8B
    detail: Used as released, greedy decoding
  - *id001
  backbone: General vision-language model, 8B parameters
  inputRepresentation: 2d
  trainingInputs: Not trained on DeepTumorVQA. Used as released.
  inferenceInputs: The organ PNG and the multiple-choice question.
- id: deeptumorvqa-2026-llava-med-7b
  name: LLaVA-Med 7B
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Section 4.1 and Table 3 (direct inference); Table 10 (input protocol); Appendix e.1 (organ slices); Appendices
      n and v.3 (greedy decoding)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - *id003
  - *id002
  - label: LLaVA-Med 7B
    detail: Used as released, greedy decoding
  - *id001
  backbone: Medical vision-language model, 7B parameters
  inputRepresentation: 2d
  trainingInputs: Not trained on DeepTumorVQA. Used as released.
  inferenceInputs: The organ PNG and the multiple-choice question.
- id: deeptumorvqa-2026-llava-onevision-7b
  name: LLaVA-OneVision 7B
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Section 4.1 and Table 3 (direct inference); Table 10 (input protocol); Appendix e.1 (organ slices); Appendices
      n and v.3 (greedy decoding)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - *id003
  - *id002
  - label: LLaVA-OneVision 7B
    detail: Used as released, greedy decoding
  - *id001
  backbone: General vision-language model, 7B parameters
  inputRepresentation: 2d
  trainingInputs: Not trained on DeepTumorVQA. Used as released.
  inferenceInputs: The organ PNG and the multiple-choice question.
- id: deeptumorvqa-2026-medgemma-4b
  name: MedGemma 1.5 4B
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Section 4.1 and Table 3 (direct inference); Table 10 (input protocol); Appendix e.1 (organ slices); Appendices
      n and v.3 (greedy decoding); Appendix k, "MedGemma 3D analysis"
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - *id003
  - *id002
  - label: MedGemma 1.5 4B
    detail: Used as released, and also run in its "3D mode"
  - *id001
  backbone: Medical vision-language model with a 2D image encoder, 4B parameters
  inputRepresentation: 2d
  preprocessing: In "3D mode" it receives up to 85 axial slices as separate RGB images, about 21,760 visual tokens. Each channel
    is a different window (R −1024 to 1024 HU, G −135 to 215 HU, B 0 to 80 HU).
  trainingInputs: Not trained on DeepTumorVQA. Used as released.
  inferenceInputs: The organ PNG, or 85 axial slices in 3D mode, and the multiple-choice question.
- id: deeptumorvqa-2026-meissa-4b
  name: Meissa-4B
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Section 4.1 and Table 3 (direct inference); Table 10 (input protocol); Appendix e.1 (organ slices); Appendices
      n and v.3 (greedy decoding); Table 9 (video input)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - *id003
  - *id002
  - label: Meissa-4B
    detail: Used as released, greedy decoding
  - *id001
  backbone: Medical agent model built on the Qwen3-VL architecture, 4B parameters
  inputRepresentation: 2d
  trainingInputs: Not trained on DeepTumorVQA. Used as released.
  inferenceInputs: The organ PNG and the multiple-choice question. Also evaluated with MP4 videos of the axial slices.
- id: deeptumorvqa-2026-qwen3-vl-4b
  name: Qwen3-VL-4B
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Section 4.1 and Table 3 (direct inference); Table 10 (input protocol); Appendix e.1 (organ slices); Appendices
      n and v.3 (greedy decoding); Table 9 (video input)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - *id003
  - *id002
  - label: Qwen3-VL-4B
    detail: Used as released, greedy decoding
  - *id001
  backbone: General vision-language model, 4B parameters
  inputRepresentation: 2d
  trainingInputs: Not trained on DeepTumorVQA. Used as released.
  inferenceInputs: The organ PNG and the multiple-choice question. Also evaluated with MP4 videos of the axial slices.
- id: deeptumorvqa-2026-qwen3-vl-8b
  name: Qwen3-VL-8B
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Section 4.1 and Table 3 (direct inference); Table 10 (input protocol); Appendix e.1 (organ slices); Appendices
      n and v.3 (greedy decoding); Table 9 (video input)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - *id003
  - *id002
  - label: Qwen3-VL-8B
    detail: Used as released, greedy decoding
  - *id001
  backbone: General vision-language model, 8B parameters
  inputRepresentation: 2d
  trainingInputs: Not trained on DeepTumorVQA. Used as released.
  inferenceInputs: The organ PNG and the multiple-choice question. Also evaluated with MP4 videos of the axial slices.
- id: deeptumorvqa-2026-qwen35-9b
  name: Qwen3.5-9B
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Section 4.1 and Table 3 (direct inference); Table 10 (input protocol); Appendix e.1 (organ slices); Appendices
      n and v.3 (greedy decoding)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - *id003
  - *id002
  - label: Qwen3.5-9B
    detail: Used as released, greedy decoding
  - *id001
  backbone: General vision-language model, 9B parameters
  inputRepresentation: 2d
  trainingInputs: Not trained on DeepTumorVQA. Used as released.
  inferenceInputs: The organ PNG and the multiple-choice question.
- id: deeptumorvqa-2026-qwen35-35b-a3b
  name: Qwen3.5-35B-A3B
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Section 4.1 and Table 3 (direct inference); Table 10 (input protocol); Appendix e.1 (organ slices); Appendices
      n and v.3 (greedy decoding)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - *id003
  - *id002
  - label: Qwen3.5-35B-A3B
    detail: Used as released, greedy decoding
  - *id001
  backbone: Mixture-of-experts vision-language model, 35B parameters with 3B active
  inputRepresentation: 2d
  trainingInputs: Not trained on DeepTumorVQA. Used as released.
  inferenceInputs: The organ PNG and the multiple-choice question.
- id: deeptumorvqa-2026-gemini-3-flash
  name: Gemini-3-Flash
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Section 4.1 and Table 3 (direct inference); Table 10 (input protocol); Appendix e.1 (organ slices); Appendices
      n and v.3 (greedy decoding)
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - label: 2D image
  - *id002
  - label: Gemini-3-Flash
    detail: Commercial API
  - *id001
  backbone: Commercial model accessed through an API, size not given
  inputRepresentation: 2d
  trainingInputs: Not trained on DeepTumorVQA. Used as released.
  inferenceInputs: A 2D image and the multiple-choice question.
- id: deeptumorvqa-2026-m3d-llama2
  name: M3D-LaMed (LLaMA2-7B), pretrained
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Table 15 (architectures), Table 16 (training), Appendix e.2 (3D inputs), Table 3
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - label: 3D CT volume
  - label: 3D ViT encoder
  - label: 3D pooling + MLP
    detail: 256 visual tokens
  - label: LLaMA2-7B
  - *id001
  backbone: 3D ViT encoder with a LLaMA2-7B decoder
  inputRepresentation: 3d
  preprocessing: HU clipped to −1024…1024, resized to 64 × 256 × 256 (trilinear) and scaled to 0–1. The 3D ViT uses 2 × 16
    × 16 patches.
  trainingInputs: Not trained on DeepTumorVQA. Pretrained on 120K 3D CT by its authors.
  inferenceInputs: The CT volume and the multiple-choice question.
- id: deeptumorvqa-2026-m3d-phi3
  name: M3D-LaMed (Phi-3-4B), pretrained
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Table 15 (architectures), Table 16 (training), Appendix e.2 (3D inputs), Table 3
    status: verified
    verifiedOn: '2026-09-30'
  pipeline:
  - label: 3D CT volume
  - label: 3D ViT encoder
  - label: 3D pooling + MLP
    detail: 256 visual tokens
  - label: Phi-3-4B
  - *id001
  backbone: 3D ViT encoder with a Phi-3-4B decoder
  inputRepresentation: 3d
  preprocessing: HU clipped to −1024…1024, resized to 64 × 256 × 256 (trilinear) and scaled to 0–1. The 3D ViT uses 2 × 16
    × 16 patches.
  trainingInputs: Not trained on DeepTumorVQA. Pretrained on 120K 3D CT by its authors.
  inferenceInputs: The CT volume and the multiple-choice question.
- id: deeptumorvqa-2026-radfm
  name: RadFM, pretrained
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Table 15 (architectures), Table 16 (training), Appendix e.2 (3D inputs), Table 3
    status: verified
    verifiedOn: '2026-09-30'
    note: The input size is from Appendix e.2. Table 15 lists RadFM's input size as 256 × 256 × 64 instead.
  pipeline:
  - label: 3D CT volume
  - label: 3D ViT encoder
  - label: Perceiver resampler
    detail: 32 visual tokens
  - label: LLaMA2-13B
  - *id001
  backbone: 3D ViT encoder with a LLaMA2-13B decoder
  inputRepresentation: 3d
  preprocessing: Resized to min(depth, 256) × 256 × 256, HU clipped to −1024…1024 and scaled to 0–1.
  trainingInputs: Not trained on DeepTumorVQA. Pretrained on 16M 2D and 3D images by its authors.
  inferenceInputs: The CT volume and the multiple-choice question.
- id: deeptumorvqa-2026-gemini-3-flash-agent
  name: Gemini-3-Flash agent
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Section 3.3 (tools and modes), section 4.2 and Table 4
    status: verified
    verifiedOn: '2026-09-30'
    note: The paper gives the agents' input as "2D+tools" in Table 4, "img+tools" in Table 5 and "Full vol + tools" in Table
      10. The training conversations in Appendix e.4 start with "the 2D slice image". The paper says no more about which image
      reaches the model at test time.
  pipeline:
  - label: 2D image
    detail: 'Table 4: "2D+tools"'
  - *id002
  - label: Gemini-3-Flash
    detail: Not trained on DeepTumorVQA
  - label: Tool calls
    detail: Up to 8 ReAct steps
  - *id001
  backbone: Gemini-3-Flash
  inputRepresentation: multimodal
  fusion: A ReAct loop of up to 8 steps. The tools are segment_organ (statistics for 43 structures), measure (volume, mean
    HU, diameter, count), lookup_medical_knowledge (a curated knowledge base) and, in vision mode only, crop_region (organ
    crops). Evaluated in oracle and vision modes. Tool outputs come from the ground-truth masks (oracle), TotalSegmentator
    (predicted) or crops only (vision).
  trainingInputs: Not trained on DeepTumorVQA. Used as released.
  inferenceInputs: The 2D image, the question and the tool outputs.
- id: deeptumorvqa-2026-meissa-4b-agent
  name: Meissa-4B agent
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Section 3.3 (tools and modes), section 4.2 and Table 4
    status: verified
    verifiedOn: '2026-09-30'
    note: The paper gives the agents' input as "2D+tools" in Table 4, "img+tools" in Table 5 and "Full vol + tools" in Table
      10. The training conversations in Appendix e.4 start with "the 2D slice image". The paper says no more about which image
      reaches the model at test time.
  pipeline:
  - label: 2D image
    detail: 'Table 4: "2D+tools"'
  - *id002
  - label: Meissa-4B
    detail: Not trained on DeepTumorVQA
  - label: Tool calls
    detail: Up to 8 ReAct steps
  - *id001
  backbone: Meissa-4B
  inputRepresentation: multimodal
  fusion: A ReAct loop of up to 8 steps. The tools are segment_organ (statistics for 43 structures), measure (volume, mean
    HU, diameter, count), lookup_medical_knowledge (a curated knowledge base) and, in vision mode only, crop_region (organ
    crops). Evaluated in oracle and vision modes. Tool outputs come from the ground-truth masks (oracle), TotalSegmentator
    (predicted) or crops only (vision).
  trainingInputs: Not trained on DeepTumorVQA. Used as released.
  inferenceInputs: The 2D image, the question and the tool outputs.
- id: deeptumorvqa-2026-qwen35-9b-agent
  name: Qwen3.5-9B agent
  role: baseline
  task: other
  evidence:
    sources:
    - deeptumorvqa-paper
    locator: Section 3.3 (tools and modes), section 4.2 and Table 4
    status: verified
    verifiedOn: '2026-09-30'
    note: The paper gives the agents' input as "2D+tools" in Table 4, "img+tools" in Table 5 and "Full vol + tools" in Table
      10. The training conversations in Appendix e.4 start with "the 2D slice image". The paper says no more about which image
      reaches the model at test time.
  pipeline:
  - label: 2D image
    detail: 'Table 4: "2D+tools"'
  - *id002
  - label: Qwen3.5-9B
    detail: Not trained on DeepTumorVQA
  - label: Tool calls
    detail: Up to 8 ReAct steps
  - *id001
  backbone: Qwen3.5-9B
  inputRepresentation: multimodal
  fusion: A ReAct loop of up to 8 steps. The tools are segment_organ (statistics for 43 structures), measure (volume, mean
    HU, diameter, count), lookup_medical_knowledge (a curated knowledge base) and, in vision mode only, crop_region (organ
    crops). Evaluated in oracle, predicted and vision modes. Tool outputs come from the ground-truth masks (oracle), TotalSegmentator
    (predicted) or crops only (vision).
  trainingInputs: Not trained on DeepTumorVQA. Used as released.
  inferenceInputs: The 2D image, the question and the tool outputs.
catalogStatus: draft
approvedBy: null
approvedOn: null
sources:
- deeptumorvqa-paper
- deeptumorvqa-github
- deeptumorvqa-metadata-files
---

The paper is the dataset's own publication. It evaluates every model on the 10,000-question benchmark: directly, on
2D slice images, videos or 3D volumes, and as agents that call segmentation, measurement and knowledge tools. Its main
finding is that measurement is the bottleneck. Open zero-shot 2D models score 23–32% on four-option measurement
questions (Table 3), although section 4.1 says 24–32%. Gemini-3-Flash scores 35.7% on these questions. With oracle
tools, Meissa-4B and Qwen3.5-9B rise from 29–31% to 64–65% (Tables 3 and 4).

Two radiologists also answered a 200-question subset (45.0% and 54.5%, Table 3). They are not models, so their scores
are not recorded here. The atlas records the five accuracy scores of each configuration in Tables 3, 4 and 23, but not
Table 4's trajectory-quality columns (steps, tool choice, parameters, validity, time). Tables 9, 10, 15 and 16 are used
only to describe the models and their inputs. The paper's other analyses and the latency figures are not recorded. Those
analyses, in Tables 5, 8, 11–13 and 18–22, include ablations and annotation-quality checks.
