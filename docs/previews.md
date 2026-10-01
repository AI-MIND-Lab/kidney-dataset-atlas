# Preview images: how they were made and how to read them

Preview images on dataset pages are compressed renderings of each dataset's own images and masks. They are there
so a reader can see what the data look like; they are not results, and each shows one randomly chosen scan.

Every preview has a sample record in `src/data/samples/` giving its caption, attribution, licence and sources.
The rules for adding one are in the Samples section of [authoring.md](authoring.md).

## Where the current previews come from

The previews in `src/data/samples/processed-figures.json` (KiTS23, UCSF RMaC, CPTAC-CCRCC, TCGA-KIRC and RCC-AID)
were rendered by the Kidney-VLM project as visual quality checks of its processed data, then compressed to WebP for
the atlas by [scripts/research/previews/build_previews.py](../scripts/research/previews/build_previews.py), which
also writes the sample records. The full-size renderings it reads are committed in `figures/<folder>/`, so the
previews can be rebuilt from the repository; the rendering code itself belongs to the Kidney-VLM project and is
not part of this repository.
Captions were written from that project's description of each figure and checked against the images.

The AbdomenAtlas 3.0 preview was made later and differently. The Kidney-VLM project rendered it with a separate script
(`RadGPT/tools/render_preview.py` in the project's dataset folder, also not in this repository), written to follow the
four-panel conventions below. It reads the release's own CT and mask files directly, and its caption was written
from the release's report for that scan.

The DeepTumorVQA 2.0 preview is different again: it is not a rendering by the Kidney-VLM project but one of
DeepTumorVQA's own released images (an organ PNG of five axial slices), downloaded from the release and only
compressed to WebP. It carries no outlines, and its caption comes from that scan's DeepTumorVQA metadata and questions.

The AMOS-MM preview was rendered by the Kidney-VLM project with `AMOS-MM/tools/render_preview.py` (in the project's
dataset folder, not in this repository), adapted from the AbdomenAtlas script. AMOS-MM releases no masks: the scan
shown, amos_0088, is one of its 228 CTs that are AMOS22 files, so it is drawn with AMOS22's kidney labels. It was
picked because its report describes a kidney finding, and its caption comes from that report and its questions.

The TCGA-KIRC previews show the project's own conversion of the TCIA scans with BAMF or RCC-AID masks placed on
them; the RCC-AID previews show RCC-AID's released images and labels directly. In TCGA-KIRC captions, the phase
comes from a reader's label, because the TCIA collection does not record phase in a structured field.

What was changed from the source data, for every preview: the intensity was windowed, the view cropped and
zoomed, and the mask drawn as outlines. Nothing was added to or removed from the anatomy.

## How to read a four-panel preview (KiTS23, CPTAC-CCRCC, TCGA, RCC-AID, AbdomenAtlas 3.0, AMOS-MM)

| Panel | What it shows |
|---|---|
| Axial | The whole axial slice where the label the view is centred on is largest (a tumour by default, a cyst in previews marked "centred on a cyst") |
| Axial zoom | The same slice, cropped to the labelled structures plus a margin |
| Coronal | A front-to-back cut through the centre of that label, superior at the top |
| Sagittal | A side-to-side cut through the same point, superior at the top and anterior on the left |

- **Outline colours:** kidney green, tumour red, cyst yellow. The kidney outline often has small interior loops
  where the renal sinus fat and collecting system are excluded from the kidney label. AbdomenAtlas 3.0 has one
  kidney lesion mask that does not say whether a lesion is a tumour or a cyst, so its lesion is outlined in orange.
  Its kidney and lesion masks are separate files that can overlap, so the kidney outline may also run around the lesion.
- **Intensity window:** level 50 HU, width 500 HU (−200 to 300 HU). Fat appears dark, soft tissue mid-grey,
  enhancing tissue and bone bright.
- **Orientation:** radiological. In axial and coronal views the patient's left is on the viewer's right.
- **Scale:** coronal and sagittal views are shown at true physical proportions, so scans with 5 mm slices look
  blocky in those views.
- **Title line inside the image:** dataset and case, contrast phase where known, scanner manufacturer, voxel size
  (x × y × slice, in mm), and the mask source. The AbdomenAtlas 3.0 preview labels the voxel size mm only when the
  CT header states that unit, and otherwise says "unit not stated".

## How to read a multi-phase preview (UCSF RMaC)

Each panel is one contrast phase (non-contrast, arterial, portal venous, delayed) at the same slice and zoom. Only
phases that the release registers to the non-contrast scan are shown, because only those share the annotation's
grid; a missing panel means that exam has no registered volume for that phase. The red outline is the dataset's
own annotation of the mass. In these previews it is a bounding box, not an outline of the tumour.

## Who drew the masks

Every caption starts by naming the mask source. They differ a great deal in how the masks were made:

| Mask source | How the masks were made | Source |
|---|---|---|
| **KiTS23 reference labels** | Trained annotators (residents, medical students and pre-medical undergraduates) placed 3D boxes and then 2D contours, consulting experts when in doubt; each region was annotated once, and experts reviewed cases where a baseline nnU-Net disagreed with the labels | [KiTS23 challenge page](https://kits-challenge.org/kits23/) |
| **UCSF RMaC annotations** | A radiology resident with three years' experience annotated each lesion in MD.ai, mostly as bounding boxes (53%) or a centre-slice box with end-slice points (41%), with polygons for 6%; an attending abdominal radiologist with over 15 years' experience reviewed every annotation | [Sahin et al. 2026, preprint](https://doi.org/10.64898/2026.02.11.26346096) |
| **BAMF (AIMI Annotations)** | AI-generated segmentations released for NCI Imaging Data Commons collections, including CPTAC-CCRCC and the TCGA kidney collections. A portion was reviewed and corrected by a radiologist; captions say whether a mask was corrected or is uncorrected AI output, which can contain small stray regions | [Murugesan et al. 2024](https://doi.org/10.1038/s41597-024-03977-8); [Zenodo release, CC BY 4.0](https://doi.org/10.5281/zenodo.8345959) |
| **AbdomenAtlas 3.0** | Kidney masks from AbdomenAtlas 1.1, made by AI with radiologists in the loop. The kidney lesion mask was drawn by AI (DiffTumor and nnU-Net) and then checked and corrected by radiologists one by one, using the source datasets' ground truth where it existed. It does not say whether a lesion is a tumour or a cyst | [Bassi et al. 2025, ICCV](https://doi.org/10.1109/ICCV51701.2025.02202); [Hugging Face release, CC BY-NC-SA 4.0 on the dataset card](https://huggingface.co/datasets/AbdomenAtlas/AbdomenAtlas3.0Mini) |
| **AMOS22 (shown on AMOS-MM)** | AMOS22's organ masks, which are not part of AMOS-MM. 50 CT and 20 MRI scans were annotated by hand; the rest were pre-labelled by models (3D-UNet, VNet), checked case by case by five junior radiologists and then reviewed by three senior radiologists. The kidneys are labelled as right and left kidney; there are no lesion labels | [Ji et al. 2022, AMOS paper](https://arxiv.org/abs/2206.08023); [Zenodo release](https://doi.org/10.5281/zenodo.7262581) |
| **RCC-AID** | An automated segmentation model produced initial kidney and lesion masks on TCGA-KIRC, -KIRP and -KICH CT; two trained students checked and corrected them and added tumours and cysts, and a board-certified radiologist reviewed uncertain cases | [de Boer et al. 2026](https://doi.org/10.59275/j.melba.2026-2dg2); [Zenodo release, CC BY 4.0](https://doi.org/10.5281/zenodo.20719257) |

None of these is a mask drawn from scratch by a radiologist for every case. Where a preview shows a quality
problem in a mask (for example stray fragments in an uncorrected AI mask), the caption says so, and the problem is
recorded as a quality finding when it applies to the release as a whole.

## Licences

A preview is an adaptation of its source dataset and carries that dataset's licence: KiTS23 previews are
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/); UCSF RMaC and CPTAC-CCRCC (with BAMF masks)
previews are [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). TCGA-KIRC and RCC-AID previews combine
[CC BY 3.0](https://creativecommons.org/licenses/by/3.0/) images from TCIA with CC BY 4.0 masks, so they need
attribution to both. The AbdomenAtlas 3.0 preview carries CC BY-NC-SA 4.0, the licence on its dataset card; the
RadGPT repository's own LICENSE says CC BY-NC-ND 4.0, and a curator has to settle which applies before approving it.
The DeepTumorVQA 2.0 preview falls under the same source CT licence, according to the DeepTumorVQA card; by
DeepTumorVQA's ID mapping its scan is a KiTS case, so KiTS23's CC BY-NC-SA 4.0 applies as well.
The AMOS-MM preview's licence is unresolved: its CT is an AMOS22 file (AMOS22's Zenodo record says CC BY 4.0, its
dataset.json CC-BY-SA 4.0 and the AMOS paper CC BY-NC-SA), AMOS-MM's own files say CC BY-ND 4.0, which does not
allow adaptations, and the challenge's application form asked applicants not to share the dataset. A curator has to
settle it before approving the preview.
See [LICENSE](../LICENSE).
