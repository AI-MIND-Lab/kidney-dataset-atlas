---
id: deeptumorvqa
slug: deeptumorvqa
name: "DeepTumorVQA — question answering on abdominal CT"
aliases:
  - DeepTumorVQA 2.0
  - DeepTumorVQA v2
summary: Computer-generated questions and answers about organs and lesions on the 9,262 AbdomenAtlas 3.0 CT scans, with a 10,000-question benchmark, 2D images, videos and tool-use traces for evaluating vision-language models and agents.
diseaseTags:
  - renal_tumor
  - cysts
  - other
species: human
officialUrl: https://huggingface.co/datasets/tumor-vqa/DeepTumorVQA_2.0
doi: null
sources:
  - deeptumorvqa-paper
  - deeptumorvqa-hf-card
  - deeptumorvqa-question-files
---

DeepTumorVQA is a benchmark from Johns Hopkins University for testing how well AI models answer questions about 3D
abdominal CT. The questions come in four stages: recognising organs and lesions, measuring them, combining several
findings, and applying clinical rules. There are 42 kinds of question, from "Is there at least one cysts in the
kidney?" to "Identify whether the largest kidney lesion is a cyst or tumor." (paper, section 3.1 and Figure 1).

The questions are not written by people. A program for each kind of question reads a table of values measured on
each scan (organ volumes, lesion counts, sizes, attenuation) and fills one of up to 10 sentence templates. For organ
volume and organ aggregation questions, the wrong options of a multiple-choice question lie between 0.7 and 1.3 times
the true value. For organ HU questions they almost always do, and for lesion counts, diameters and volumes they often do
not. The scans are the 9,262 AbdomenAtlas 3.0 CTs, under the same `BDMAP_` IDs. The release also holds per-scan PNG
slices, videos, pre-computed tool outputs and training conversations for tool-using agents.

Two things are easy to misread. First, DeepTumorVQA adds questions to existing scans rather than new patients. Its PNGs
and videos are renderings of those scans, and the release re-hosts CT volumes only for the 991 benchmark scans. The CT
volumes of the other scans are on AbdomenAtlas. DeepTumorVQA's counts must never be added to AbdomenAtlas's. Second, its
sources disagree on where the underlying masks came from. The dataset card says the questions are generated from the
AbdomenAtlas masks and reports. The paper instead says all masks were drawn again in-house by 23 radiologists (see the
quality findings on the release page).
