---
id: abdomenatlas
slug: abdomenatlas
name: "AbdomenAtlas — abdominal CT with organ and lesion masks"
aliases:
  - AbdomenAtlas 3.0
  - AbdomenAtlas3.0Mini
summary: Abdominal CT scans gathered from 17 public datasets, with per-voxel organ and lesion masks and, in version 3.0, radiology reports written from those masks by the RadGPT pipeline.
diseaseTags:
  - renal_tumor
  - other
species: human
officialUrl: https://huggingface.co/datasets/AbdomenAtlas/AbdomenAtlas3.0Mini
doi: null
sources:
  - radgpt-paper
  - abdomenatlas3-hf-card
  - radgpt-repo-readme
---

AbdomenAtlas is a collection of abdominal CT scans published by a group at Johns Hopkins University. The scans were
not acquired for it: they come from 17 public datasets, among them KiTS'23, CT-ORG, AMOS, WORD, FLARE'23 and six
Medical Segmentation Decathlon CT tasks, and span 138 institutions (RadGPT paper, Table 1). Earlier versions added
organ masks (AbdomenAtlas 1.1); version 3.0 keeps the same 9,262 CT scans and adds masks of liver, kidney and pancreatic
lesions, liver and pancreas sub-regions, and blood vessels, together with a radiology report for each scan.

One case is one CT scan, identified as `BDMAP_` followed by eight digits. It has the CT volume, one mask file per
structure, a row in the metadata table, and structured and narrative reports. The reports were not written by the
hospitals that made the scans. RadGPT, the paper's pipeline, measures each lesion from the masks with fixed rules
and fills a template (the structured report). A language model then rewrites that text in a hospital's style
(the narrative report). Radiologists revised the lesion masks and checked the reports (paper, sections 3.1–3.2 and
Appendix C).

Three things are easy to misread. The kidney lesion mask does not say whether a lesion is a tumour or a cyst, although
KiTS'23, one of the sources, labels the two separately. Counts must never be added to those of
the source datasets, because the same scans appear in both; this catalogue records that overlap for KiTS23,
CT-ORG, TotalSegmentator and CPTAC-CCRCC. And the numbers in the metadata table were read back out of the report
text, not measured from the masks (see the quality findings on the release page).
