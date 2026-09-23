# Paper candidates for each dataset: review sheet

**Generated:** 2026-09-22. **Status: candidates.** Rows marked `verified` in the `status_2026_09_23` column were checked in full text and appear in section 6.4 of the research inventory; rows marked `checked and excluded` were rejected with a reason. Every other row is unverified. None of it may be imported into `src/data/study-uses/` until a reviewer has opened the paper and confirmed, in its methods, that the dataset was used, and recorded where.

The full list is [`paper-candidates.csv`](paper-candidates.csv), one row per dataset–paper pair. It opens in Excel with filters. Fill in `review_decision` (`keep`, `reject` or `unsure`), and for kept rows `role_if_used`, `train_test_role`, `method_used` and `evidence_locator` (section, table or page). This page lists the citation pages for each dataset and its strongest candidates.

## How candidates were found

1. **Semantic Scholar citations with citing sentences.** Every paper citing each dataset's descriptor or challenge paper was downloaded, including the sentence where the citation occurs and Semantic Scholar's citation-intent label. A sentence naming a specific edition (e.g. "KiTS23") is assigned to that edition, whichever paper it cites.
2. **Europe PMC Methods-section search.** Open-access papers whose *Methods* name the dataset, plus a whole-text search as weaker evidence.
3. **DataCite.** Papers that cite the dataset DOI itself (TCIA, Zenodo, Mendeley, Figshare).
4. **Semantic Scholar keyword search** for datasets without a paper.

### Evidence tiers

| Tier | Meaning |
|---|---|
| **A** | Strong: a citing sentence names the dataset and says the authors trained, tested, evaluated or used it |
| **B** | Probable: named in the Methods (Europe PMC), cites the dataset DOI (DataCite), or a citing sentence describes the data |
| **C** | Possible: cited in a methods context without naming the data, or named somewhere in the full text |
| **D** | Citation only: kept for small datasets so no user is missed; usually background |

Tiers only set the order of review; they are not verification. Automatic text matching makes mistakes both ways: a survey can describe a dataset in words that look like use, and a real user may cite only a website. Coverage is also limited: papers not indexed by these services, and paywalled Methods sections, can be missed. Use the citation pages below for an exhaustive check.

### How to verify a candidate

- Open the paper and find the dataset in the **Methods / Experiments / Datasets** section. A reference-list entry or a mention in the introduction is not use.
- Check it is **this release/edition** (KiTS19 vs KiTS21 vs KiTS23; FLARE21 vs 22 vs 23; TotalSegmentator dataset vs the TotalSegmentator model).
- Record the role: training, validation, test, external validation, or challenge entry. Also record the method or model, and the locator (section, table or figure).
- The dataset's own descriptor or challenge paper is already in the research inventory. It is a benchmark relationship, not downstream use.

## Summary

| ID | Dataset | Strong (A) | Probable (B) | Possible (C) | Citation only (D) | Total |
|---|---|---:|---:|---:|---:|---:|
| K01 | KiTS19 | 93 | 220 | 432 | 0 | 745 |
| K02 | KiTS21 | 32 | 90 | 177 | 0 | 299 |
| K03 | KiTS23 | 30 | 10 | 188 | 0 | 228 |
| K04 | Radboudumc Kidney Abnormality | 0 | 0 | 0 | 0 | 0 |
| K05 | CT Kidney Normal-Cyst-Tumor-Stone | 15 | 39 | 151 | 0 | 205 |
| K06-K08 | TCGA renal WSI (KIRC/KIRP/KICH) | 1 | 23 | 47 | 0 | 71 |
| K09 | TCGA-KIRC radiology (TCIA) | 0 | 100 | 0 | 0 | 100 |
| K10 | HuBMAP Hacking the Kidney | 1 | 28 | 91 | 11 | 131 |
| K11-K12 | HuBMAP+HPA Hacking the Human Body | 1 | 9 | 8 | 18 | 36 |
| K13 | TRUSTED | 1 | 0 | 12 | 8 | 21 |
| K14 | Axial CT kidney stone (Mendeley) | 0 | 5 | 1 | 0 | 6 |
| M01 | TotalSegmentator CT | 205 | 183 | 159 | 0 | 547 |
| M02 | TotalSegmentator MRI | 9 | 11 | 32 | 0 | 52 |
| M03 | AMOS22 | 149 | 104 | 37 | 0 | 290 |
| M04 | CHAOS | 124 | 176 | 113 | 0 | 413 |
| M05 | CT-ORG | 21 | 54 | 31 | 0 | 106 |
| M06 | WORD | 0 | 10 | 17 | 0 | 27 |
| M07 | AbdomenAtlas | 7 | 9 | 21 | 0 | 37 |
| M08 | FLARE21 | 16 | 16 | 27 | 0 | 59 |
| M09 | FLARE22 | 11 | 18 | 53 | 0 | 82 |
| M10 | FLARE23 | 2 | 6 | 18 | 0 | 26 |
| M11 | AbdomenAtlas 3.0 / RadGPT | 7 | 4 | 1 | 0 | 12 |
| M12 | AMOS-MM | 8 | 3 | 5 | 0 | 16 |
| M13 | SA-Med3D-140K | 0 | 0 | 62 | 0 | 62 |
| M14 | ULS23 | 1 | 5 | 21 | 20 | 47 |
| M15 | 3DLAND | 0 | 0 | 4 | 0 | 4 |
| M16 | DeepLesion | 80 | 62 | 84 | 0 | 226 |
| M17 | M3D-Data | 12 | 17 | 11 | 0 | 40 |
| G01 | UCSF RMaC | 1 | 0 | 1 | 0 | 2 |
| G02 | CPTAC-CCRCC imaging | 2 | 57 | 23 | 0 | 82 |
| G03 | RCC-AID | 0 | 0 | 2 | 0 | 2 |
| H01 | Open Kidney Ultrasound (kidneyUS) | 5 | 2 | 26 | 19 | 52 |
| H03 | KiPA22 | 8 | 6 | 59 | 72 | 145 |
| H04 | KPIs 2024 | 1 | 5 | 10 | 2 | 18 |
| H05 | AbdomenCT-1K | 40 | 67 | 92 | 0 | 199 |
| H06 | RAOS | 6 | 4 | 46 | 14 | 70 |
| H07 | BTCV / Synapse multi-organ | 16 | 162 | 153 | 0 | 331 |
| H09 | NEPTUNE multistain (Jayapandian) | 0 | 24 | 49 | 0 | 73 |
| H10 | Merlin Abdominal CT | 3 | 4 | 33 | 0 | 40 |
| H11 | RadImageNet-VQA | 1 | 0 | 2 | 2 | 5 |

*H08 (3D U-Net Xenopus microscopy) is not included: the method paper has over 10,000 citations and no dataset release was found.*

## Per-dataset citation pages and top candidates

### K01 — KiTS19

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *The KiTS19 Challenge Data: 300 Kidney Tumor Cases with Clinical Context, CT Semantic Segmentations, and Surgical Outcomes* (503 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/2bc472478247173b25aaf5e12f2604a74a8d2063>
- Semantic Scholar citations of *The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 challenge* (653 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/4d55dfb3db28064d0313332fce937e036a2f72a3>
- OpenAlex works citing *The KiTS19 Challenge Data: 300 Kidney Tumor Cases with Clinical Context, CT Semantic Segmentations, and Surgical Outcomes* (332): <https://openalex.org/works?filter=cites:W2933796343>
- OpenAlex works citing *The state of the art in kidney and kidney tumor segmentation in contrast-enhanced CT imaging: Results of the KiTS19 challenge* (56): <https://openalex.org/works?filter=cites:W2993476821>
- DataCite Commons, works citing the dataset DOI `10.7937/TCIA.2019.IX49E8NX`: <https://commons.datacite.org/doi.org/10.7937/TCIA.2019.IX49E8NX>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22KiTS19%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22KiTS19%22%20OR%20%22KiTS%202019%22%20OR%20%22C4KC-KiTS%22%20OR%20%22KiTS-19%22%29>
- KiTS19 leaderboard (Grand Challenge): <https://kits19.grand-challenge.org/evaluation/challenge/leaderboard/>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [LAW & ORDER: Adaptive Spatial Weighting for Medical Diffusion and Segmentation](https://doi.org/10.48550/arXiv.2603.04795) | 2026 | Compared to training on real data only, LAW-generated synthetic data improves Dice by 4.9% on Polyps and 1.5% on KiTS19. |
| A | [Spine-anchored active contour-based renal spatial prioritization for precision-constrained volumetric segmentation of bilateral nephric tumors via spine-guided 3D deep encoders in abdominopelvic tomographic data](https://doi.org/10.1007/s12194-026-01115-0) | 2026 | We used abdomen computed tomography scans drawn from the archive of the KiTS19 challenge, which had 310 volumes of humans [36]. |
| A | [Joint Medical Image Enhancement and Segmentation with Diffusion-based Symbiotic Information Interaction](https://doi.org/10.48550/arXiv.2607.00058) | 2026 | To evaluate our DiSIINet model’s performance, we conduct experiments on several medical image segmentation datasets including ACDC [Bernard et al. , 2018], KiTS19 [Heller et al. , 2021], and TN3K [Gong et al. , 2021]. |
| A | [Adaptively Distilled ControlNet: Accelerated Training and Superior Sampling for Medical Image Synthesis](https://doi.org/10.48550/arXiv.2507.23652) | 2025 | We evaluate our method on two publicly available medical datasets: Polyps [12,1] ( RGB ) and KiTS19 [6] ( CT , 2D slices), referred to as Real Datasets . |
| A | [DSEA-Net: a dual-stream edge-aware network for kidney tumor segmentation](https://doi.org/10.1007/s11760-025-04385-0) | 2025 | To further evaluate the generalization ability of DSEA-Net beyond our constructed dataset, additional experiments were conducted on the KiTS19 dataset [ 11]. |
| A | [Automated Renal Tumor Segmentation in Computed Tomography Images Using a Global Attention–Based DeepLabV3+ Model: Algorithm Development and Validation](https://doi.org/10.2196/78523) | 2025 | The annotations include 2 categories: background and renal tumor, as illustrated in Figure 2A. Additionally, experiments were conducted on the publicly available KiTS19 dataset from the 2019 Kidney and Kidney Tumor Segmentation Challenge [33]. |
| A | [Hybrid 3D Medical Image Segmentation Using CNN and Frequency Transformer Fusion](https://doi.org/10.1007/s13369-024-09602-5) | 2024 | Regarding of the conﬁguration details related to the dataset used for training and evaluating proposed network, we employed two 3D datasets, namely KiTS 2019[72] and BraTS21[73]. |
| A | [CoCPF: Coordinate-based Continuous Projection Field for Ill-Posed Inverse Problem in Imaging](https://doi.org/10.48550/arXiv.2406.14976) | 2024 | Comprehensive experiments on two simulated datasets: COVID-19 [23] and KiTS19 [24], and a real projection dataset: AAPM-LDCT-PD [25] demonstrate that CoCPF outperforms state-of-the-art INR-and CNN-based methods for 2D and 3D SVCT reconstructions, achieving con… |
| A | [CuNeRF: Cube-Based Neural Radiance Field for Zero-Shot Medical Image Arbitrary-Scale Super Resolution](https://doi.org/10.1109/ICCV51070.2023.01937) | 2023 | More specifically, we select T1-weighted MRI volumes from the Medical Segmentation Decathlon (MSD) [33] while we also take CT volumes from the 2019 Kidney Tumor Segmentation Challenge (KiTS19) [13] datasets, respectively. |
| A | [AI-Driven Robust Kidney and Renal Mass Segmentation and Classification on 3D CT Images](https://doi.org/10.3390/bioengineering10010116) | 2023 | Comparison with the State-of-the-Art Methods Our model predicts remarkably accurate kidney segmentation on the KiTs19 testing set, with an average Dice metric of 96.7% and 86.6% for kidney and renal mass regions, respectively. |
| A | [Ring Artifact Correction in Photon-Counting Spectral CT Using a Convolutional Neural Network With Spectral Loss](https://arxiv.org/abs/2302.00921) | 2023 | 3 we have formed 40 keV virtual monoenergetic images from an example slice in the KiTS19 test set. |
| A | [APRF: Anti-Aliasing Projection Representation Field for Inverse Problem in Imaging](https://doi.org/10.48550/arXiv.2307.05270) | 2023 | Comprehensive experiments on COVID-19 [7] and KiTS19 [21] datasets demonstrate the superiority of our APRF, whose reconstruction quality surpasses state-of-the-art methods on parallel-, fan- and conebeam SVCT images. |

733 more candidate(s) in the CSV.

### K02 — KiTS21

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *The KiTS21 Challenge: Automatic segmentation of kidneys, renal tumors, and renal cysts in corticomedullary-phase CT* (167 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/f8c16510ef80ba70ead16f4349179aceee6d1e43>
- OpenAlex works citing *The KiTS21 Challenge: Automatic segmentation of kidneys, renal tumors, and renal cysts in corticomedullary-phase CT* (35): <https://openalex.org/works?filter=cites:W4383472689>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22KiTS21%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22KiTS21%22%20OR%20%22KiTS%202021%22%20OR%20%22KiTS-21%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Correction-aware interactive 3D tumor segmentation with sparse and revisable prompts](https://doi.org/10.1007/s00371-026-04560-5) | 2026 | We evaluate on two public 3D tumor segmentation benchmarks: MSD-Colon [2] and KiTS21 kidney tumor segmentation [8]. |
| A | [Conformal Lesion Segmentation for 3D Medical Images](https://doi.org/10.48550/arXiv.2510.17897) | 2025 | To further illustrate this limitation, we evaluate the pretrained Med3D model (Chen, Ma, and Zheng 2019) on the KiTS21 dataset (Heller et al. 2023), and present the average value distribution of elements in the output probability matrices in Figure 3a. Notably… |
| A | [Aggressiveness classification of clear cell renal cell carcinoma using registration-independent radiology-pathology correlation learning](https://doi.org/10.1002/mp.17476) | 2024 | We used publicly available data from the 2021 Kidney and Kidney Tumor Segmentation Challenge (KiTS21) and TCIA: The Cancer Genome Atlas Kidney Renal Clear Cell Carcinoma Collection (TCGA-KIRC). |
| A | [An Integrated Deep Learning Model to Analyze CT Scans for Minimally Invasive Accurate Classification of T1a Small Renal Masses](https://doi.org/10.1145/3707172.3707173) | 2024 | Currently, our model has been tested, based upon the availability of the test data in KiTS 19 and KiTS 21 challenge dataset , to classify SRMs greater than 1.2 cm from axial slices [35, 36]. |
| A | [A Densely Connected Attention Spatiotemporal U-Net for Kidney and Renal Artery Segmentation in CT Images](https://doi.org/10.1109/ISBI53787.2023.10230479) | 2023 | RESULTS AND DISCUSSION We selected 35 volumes from KiTS19 and KiTS21 [17] with arterial phase of abdominal CT scans of unique kidney cancer patients. |
| A | [Topology-Preserving Segmentation Network: A Deep Learning Segmentation Framework for Connected Component](https://doi.org/10.48550/arXiv.2210.03299) | 2022 | In this paper, the simply-connected and doubly connected object segmentation models are evaluated on the KiTS21[10] and ACDC[11] dataset, respectively. |
| A | [Enhanced VGG16 Model for Kidney Tumor Classification](https://www.semanticscholar.org/paper/8bc8186d2af6040e111e552572502561a85fd0e1) |  | The cohort is geographically concentrated (predominantly Jordanian), limiting generalizability; external validation on multi-ethnic datasets such as KiTS-21 [14] is therefore planned. |
| A | [End-to-End Differentiable Photon Counting CT.](https://doi.org/10.1109/TMI.2026.3720353) | 2026 | After the phantom-based calibration, we applied the corrected thresholds to a simulated PCCT scan of an abdomen, using an axial image from the KiTS21 dataset [28]. |
| A | [Volumetric Directional Diffusion: Anchoring Uncertainty Quantification in Anatomical Consensus for Ambiguous Medical Image Segmentation](https://doi.org/10.48550/arXiv.2603.04024) | 2026 | We evaluated VDD on three multi-rater datasets: LIDC-IDRI [27], KiTS21 [28], and ISBI 2015 [29]. |
| A | [SAM-Med3D: A Vision Foundation Model for General-Purpose Segmentation on Volumetric Medical Images](https://doi.org/10.1109/TNNLS.2025.3586694) | 2025 | Since KiTS21 [39] and BraTS21 [19] did not release annotations for the o ﬃ cial test set, we randomly selected 90 cases from the training set of each dataset for our evaluation and used the remaining annotated data for training. |
| A | [An efficient automated diagnosis of kidney tumors by integrating image processing based localization and enhanced U-Net-based semantic segmentation](https://doi.org/10.1117/12.3071689) | 2025 | We used publicly available KiTS 19 and KiTS 21 Challenge datasets [25, 26]. |
| A | [MedNeXt-v2: Scaling 3D ConvNeXts for Large-Scale Supervised Representation Learning in Medical Image Segmentation](https://doi.org/10.48550/arXiv.2512.17774) | 2025 | In this work, we propose validating our backbone against existing state of the art architectures on 4 public validation datasets – BTCV [37], AMOS22 [33], KITS21 [27] and ACDC [5] (more in Sec. |

287 more candidate(s) in the CSV.

### K03 — KiTS23

> KiTS23 has no challenge report yet. Candidates come from sentences naming KiTS23 in papers citing the KiTS19/KiTS21 reports, plus Europe PMC.

**Where to find every paper that cites or uses it:**

- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22KiTS23%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22KiTS23%22%20OR%20%22KiTS%202023%22%20OR%20%22KiTS-23%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Advancing Generalizable Tumor Segmentation with Anomaly-Aware Open-Vocabulary Attention Maps and Frozen Foundation Diffusion Models](https://doi.org/10.1109/CVPR52734.2025.02419) | 2025 | In this setup, we used KiTS23 [18] and four CT tumor segmentation datasets from the MSD [3], including colon, pancreas, lung, and hepatic vessel tumors, to train the models and then tested them on three MRI datasets, including an in-house MRI liver tumor datas… |
| A | [Exploiting Scale-Variant Attention for Segmenting Small Medical Objects](https://doi.org/10.1109/TNNLS.2025.3645355) | 2024 | To validate the effectiveness of SvANet, we conducted tests alongside seven state-of-the-art (SOTA) models for small medical object segmentation across seven benchmark datasets: FIVES [1], ISIC 2018 [2], PolypGen [3], ATLAS [6], KiTS23 [4], TissueNet [7], and … |
| A | [Unleashing the Potential of Vision-Language Pre-Training for 3D Zero-Shot Lesion Segmentation via Mask-Attribute Alignment](https://doi.org/10.48550/arXiv.2410.15744) | 2024 | We conducted ablation experiments to assess the segmentation performance of unseen lesions using different numbers of mask tokens on the KiTS23 dataset (Heller et al., 2023) and our in-house dataset. |
| A | [SvANet: A Scale-variant Attention-based Network for Small Medical Object Segmentation](https://doi.org/10.48550/arXiv.2407.07720) | 2024 | …Protocol 1) Dataset: To validate the effectiveness of SvANet, we conducted tests alongside seven state-of-the-art (SOTA) models for small medical object segmentation across seven benchmark datasets: FIVES [1], ISIC 2018 [2], PolypGen [3], ATLAS [6], KiTS23 [4… |
| A | [Optimizing Inference Distribution for Efficient Kidney Tumor Segmentation Using a UNet-PWP Deep-Learning Model with XAI on CT Scan Images](https://doi.org/10.3390/diagnostics13203244) | 2023 | Our extensive evaluation, conducted on the KiTs19, KiTs21, and KiTs23 variant datasets [23,25], illustrates the efﬁcacy of our approach in addressing the challenges inherent to medical image analysis. |
| A | [SvANet: A Scale-variant Attention-based Network for Small Medical Object Segmentation](https://www.semanticscholar.org/paper/dc626a3ecc3d4ef57155dc060b27282aa85dcc08) |  | …Protocol 1) Dataset: To validate the effectiveness of SvANet, we conducted tests alongside seven state-of-the-art (SOTA) models for small medical object segmentation across seven benchmark datasets: FIVES [1], ISIC 2018 [2], PolypGen [3], ATLAS [6], KiTS23 [4… |
| A | [GenMed: A Pairwise Generative Reformulation of Medical Diagnostic Tasks](https://doi.org/10.48550/arXiv.2605.10645) | 2026 | For evaluation, we use KiTS23 [79], which contains 599 contrast-enhanced abdominal CT scans with semantic annotations, from which we extract the left kidney label of each case. |
| A | [Preoperative prediction of preserved renal parenchymal volume via multilevel CT feature fusion: a proof-of-concept study](https://doi.org/10.1007/s00261-026-05381-9) | 2026 | We utilized the nnUNetv2 [ 21] architecture as the foundational segmentation engine, initialized with weights pre-trained on the KITS2023 [ 22] dataset. |
| A | [MedSIGHT: Towards Grounded Visual Comprehension in Medical Large Vision-Language Models](https://doi.org/10.48550/arXiv.2606.06760) | 2026 | Specifically, we sample image–mask–description triples from the following datasets: Breast Ultrasound (Al-Dhabyani et al., 2020), ISIC (Codella et al., 2019), CESM (Khaled et al., 2022), KiTS23 (Heller et al., 2023), MSD (Antonelli et al., 2022), LIDC-IDRI (Ar… |
| A | [LOCBAM: Advancing 3D Patch-Based Image Segmentation by Integrating Location Context](https://doi.org/10.1109/ISBI61048.2026.11515865) | 2026 | We evaluate the impact of incorporating location context on three publicly available 3D medical imaging datasets: BTCV-Abdomen [15], AMOS22-CT [16], and KiTS23 [17]. |
| A | [Curia: A Multi-Modal Foundation Model for Radiology](https://doi.org/10.48550/arXiv.2509.06830) | 2025 | We used the KITS23 dataset [38] to create the Kidney Lesion Malignancy benchmark. |
| A | [Large-scale generative tumor synthesis in computed tomography images for improving tumor recognition](https://doi.org/10.1038/s41467-025-66071-6) | 2025 | To evaluate the effectiveness of scaling up datasets, we conduct ablation studies on ﬁ ve segmentation datasets, i.e., LiTS 61 (liver tumors), MSD07 10 (pancreas tumors), KiTS23 66 , MSD06 10 (lung tumors), and CV19-20 69 (COVID-19 infection). |

216 more candidate(s) in the CSV.

### K04 — Radboudumc Kidney Abnormality

> The dataset paper is not indexed by Semantic Scholar and OpenAlex records no citations. Check Google Scholar.

**Where to find every paper that cites or uses it:**

- OpenAlex works citing *Kidney abnormality segmentation in thorax-abdomen CT scans* (0): <https://openalex.org/works?filter=cites:W4386554882>
- DataCite Commons, works citing the dataset DOI `10.5281/zenodo.8014289`: <https://commons.datacite.org/doi.org/10.5281/zenodo.8014289>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22kidney%20abnormality%20segmentation%22%20Radboud>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22zenodo.8014289%22%29>

_No strong or probable candidates were found automatically. Use the citation pages above._

### K05 — CT Kidney Normal-Cyst-Tumor-Stone

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *Vision transformer and explainable transfer learning models for auto detection of kidney cyst, stone and tumor from CT-radiography* (290 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/5c1b7e400ba8b3c3b04522f7bb3af17ad68d0585>
- OpenAlex works citing *Vision transformer and explainable transfer learning models for auto detection of kidney cyst, stone and tumor from CT-radiography* (311): <https://openalex.org/works?filter=cites:W4284890590>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22CT%20KIDNEY%20DATASET%3A%20Normal-Cyst-Tumor%20and%20Stone%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22CT%20KIDNEY%20DATASET%22%20OR%20%22Normal-Cyst-Tumor%22%20OR%20%28%2212%2C446%22%20AND%20kidney%29%29>
- Kaggle "Code" tab (notebooks, not papers): <https://www.kaggle.com/datasets/nazmul0087/ct-kidney-dataset-normal-cyst-tumor-and-stone/code>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [CLIP-SVD: Efficient and Interpretable Vision-Language Adaptation via Singular Values](https://arxiv.org/abs/2509.03740) | 2025 | For the biomedical domain, we follow Koleilat et al. (2025b) and evaluate the performance of our method on 10 diverse medical imaging datasets covering 9 different organs and 8 imaging modalities: Computerized Tomography (CTKidney (Islam et al., 2022)), Endosc… |
| A | [Explainable Deep Learning for Kidney CT Scan Classification](https://doi.org/10.1109/MoSICom67153.2025.11398278) | 2025 | The dataset used in this study was put together by Is-lam et al. [8] and includes 12,446 abdominal CT images. |
| A | [UGPL: Uncertainty-Guided Progressive Learning for Evidence-Based Classification in Computed Tomography](https://doi.org/10.1109/ICCVW69036.2025.00105) | 2025 | We conduct experiments on three CT image datasets: the kidney disease diagnosis dataset [36] (multi-class: normal, cyst, tumor, stone), the IQ-OTH/NCCD lung cancer dataset [3, 4, 22] (multiclass: benign, malignant, normal), and the UCSD-AI4H COVID-CT dataset [… |
| A | [Convnext-PCA: A Parameter-Efficient Model for Accurate Kidney Abnormality Classification](https://doi.org/10.1109/MLSP58920.2024.10734811) | 2024 | Table 2 compares our model with other studies classifying kidney stones, cysts, and tumors using Kaggle dataset [15]. |
| A | [IR-CNN: Inception residual network for detecting kidney abnormalities from CT images](https://doi.org/10.1007/s13721-023-00431-4) | 2023 | To evaluate the classification performance of our proposed IR-CNN model, we used a publicly available CT kidney dataset (Islam et al. 2022) from a hospital in Dhaka, Bangladesh, which includes four different categories, i.e., kidney stones, cysts, tumors, and … |
| A | [Kidney CT Image Analysis Using CNN](https://doi.org/10.5121/csit.2023.131403) | 2023 | To evaluate the performance of the proposed model, we used a test set of 6,223 images from the CT KIDNEY DATASET. |
| A | [Neural Network Pipeline for Kidney Stone Detection and Segmentation from CT Images](https://doi.org/10.1109/AQTR70159.2026.11577676) | 2026 | In this study, the CT KIDNEY DATASET (Normal-Cyst-Tumor and Stone) was used, containing CT images extracted from hospitals in Dhaka, Bangladesh [14]. |
| A | [A Deep Learning Approach for Automated Kidney Tumor Classification](https://doi.org/10.24271/psr.2026.244506) | 2026 | The second dataset utilized in this study, the CT-Kidney dataset, originally comprises 12,446 CT images obtained from various hospitals in Dhaka, Bangladesh, using urogram-based scanning protocols [19] . |
| A | [Fine-tuned deep transfer learning: an effective strategy for the accurate chronic kidney disease classification](https://doi.org/10.7717/peerj-cs.2800) | 2025 | The dataset utilized in this study is the “ CT Kidney ” dataset ( Islam et al., 2022 ; https:// www.kaggle.com/datasets/nazmul0087/ct-kidney-dataset-normal-cyst-tumor-and-stone) comprising 12,446 data samples with four classes of popular kidney diseases namely… |
| A | [Optimized ROI Extraction and Pixel Reduction Methods for Kidney Abnormality Detection](https://doi.org/10.1109/SoutheastCon56624.2025.10971551) | 2025 | We used the “CT KIDNEY DATASET: Normal-Cyst-Tumor and Stone” [12] which included four different classes with a significant number of images in each. |
| A | [Artificial intelligence in diagnostic medicine: a case study of kidney disease applications](https://doi.org/10.11591/ijeecs.v40.i3.pp1232-1240) | 2025 | The dataset used in this paper, titled “CT Kidney Dataset: Normal-Cyst-Tumor and Stone,” was collected from the picture archiving and communication system (PACS) of various hospitals in Dhaka, Bangladesh [16]. |
| A | [An optimized fusion of deep learning models for kidney stone detection from CT images](https://doi.org/10.1016/j.jksuci.2024.102130) | 2024 | To conduct this assessment, we collected 254 samples of CT images from the Kaggle repository “ CT KIDNEY DATASET, ” sourced from various hospitals in Dhaka, Bangladesh (Islam et al., 2022). |

193 more candidate(s) in the CSV.

### K06-K08 — TCGA renal WSI (KIRC/KIRP/KICH)

> The three TCGA renal slide projects share one candidate list. Record which project(s) each paper used when verifying.

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *Pan-Renal Cell Carcinoma classification and survival prediction from histopathology images using deep learning* (215 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/034740d392e536793c03c2c6792e82b2ebf2804f>
- OpenAlex works citing *Pan-Renal Cell Carcinoma classification and survival prediction from histopathology images using deep learning* (269): <https://openalex.org/works?filter=cites:W2964324957>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22TCGA-KIRC%22%20OR%20%22TCGA-KIRP%22%20OR%20%22TCGA-KICH%22%20whole-slide%20deep%20learning>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%28%22TCGA-KIRC%22%20OR%20%22TCGA-KIRP%22%20OR%20%22TCGA-KICH%22%20OR%20%22TCGA%20KIRC%22%29%20AND%20%28%22whole%20slide%22%20OR%20%22whole-slide%22%29%20AND%20%28%22deep%20learning%22%20OR%20%22convolutional%22%29%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Artificial intelligence for renal cancer: From imaging to histology and beyond](https://doi.org/10.1016/j.ajur.2022.05.003) | 2022 | Tabibu et al. [74] trained convolutional neural networks (CNNs) with hematoxylin and eosin (H&E) whole-slide images from The Cancer Genome Atlas (TCGA) to detect clear cell and chromophobe RCC. |
| B | [Deep representation learning for temporal inference in cancer omics: a systematic literature review.](https://doi.org/10.1093/bib/bbag147) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [A pathomics-based pyroptosis signature predicts survival in clear cell renal cell carcinoma.](https://doi.org/10.1007/s12672-026-04685-y) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Deep spatial proteomics reveals a suppressive immune niche linked to immune evasion in renal cell carcinoma.](https://doi.org/10.20517/cdr.2026.27) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [A spatial multi-omic portrait of survival outcome for clear cell renal cell carcinoma](https://doi.org/10.64898/2026.03.02.26347390) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Hybrid DenseNet-U-Net framework for automated grading of renal cell carcinoma.](https://doi.org/10.1177/20552076261453125) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Deep-learning-based artificial intelligence approaches for grading and progression prediction of clear cell renal cell carcinoma.](https://doi.org/10.1016/j.isci.2026.116182) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [BPX-Net: biomarker-preserved explainable networks for disease diagnosis and prognosis.](https://doi.org/10.1186/s13040-026-00537-1) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [ALPaCA: Adapting Llama for Pathology Context Analysis to enable slide-level question answering.](https://doi.org/10.1038/s41467-026-76372-z) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Pan-cancer atlas of cellular architecture reveals a nearest-neighbour distance-associated biomechanical-immune axis involving CD4+ memory T cells.](https://doi.org/10.1002/ctm2.70742) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [A foundation model for generalizable cancer diagnosis and survival prediction from histopathological images.](https://doi.org/10.1038/s41467-025-57587-y) | 2025 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Histopathology based AI model predicts anti-angiogenic therapy response in renal cancer clinical trial.](https://doi.org/10.1038/s41467-025-57717-6) | 2025 | Europe PMC: named in Methods; Europe PMC: named in full text |

59 more candidate(s) in the CSV.

### K09 — TCGA-KIRC radiology (TCIA)

> Candidates cover TCIA radiology for TCGA-KIRC, -KIRP and -KICH. Radiogenomics studies use the images; genomics-only papers that cite the collection DOI do not.

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *AI-Generated Annotations Dataset for Diverse Cancer Radiology Collections in NCI Image Data Commons* (10 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/cf0f4d8d5934e41d000df7223c6c514b949e942a>
- OpenAlex works citing *AI-Generated Annotations Dataset for Diverse Cancer Radiology Collections in NCI Image Data Commons* (1): <https://openalex.org/works?filter=cites:W4387946320>
- DataCite Commons, works citing the dataset DOI `10.7937/K9/TCIA.2016.V6PBVTDR`: <https://commons.datacite.org/doi.org/10.7937/K9/TCIA.2016.V6PBVTDR>
- DataCite Commons, works citing the dataset DOI `10.7937/K9/TCIA.2016.ACWOGBEF`: <https://commons.datacite.org/doi.org/10.7937/K9/TCIA.2016.ACWOGBEF>
- DataCite Commons, works citing the dataset DOI `10.7937/K9/TCIA.2016.YU3RBCZN`: <https://commons.datacite.org/doi.org/10.7937/K9/TCIA.2016.YU3RBCZN>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22TCGA-KIRC%22%20TCIA%20CT%20segmentation>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%28%22TCGA-KIRC%22%20OR%20%22TCGA%20KIRC%22%29%20AND%20%28%22TCIA%22%20OR%20%22Cancer%20Imaging%20Archive%22%29%20AND%20%28CT%20OR%20%22computed%20tomography%22%29%29>
- TCIA publication list: <https://www.cancerimagingarchive.net/publications/>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| B | [Robust Renal Mass Segmentation on CT: A Validation Study of an AI-Based Framework](https://doi.org/10.59275/j.melba.2026-67g5) | 2025 | Under the AIMI Annotations initiative, a subset of The Cancer Genome Atlas Kidney Renal Clear Cell Carcinoma Collection (TCGA-KIRC) (Akin et al., 2016) is annotated for kidney, tumor and cyst regions, first by a trained AI model and corrected by an experienced… |
| B | [Biomedical Imaging Robust Renal Mass Segmentation on CT: A Validation Study of an AI-Based Framework](https://www.semanticscholar.org/paper/6129e7d10b4532a364ef3d63c3306a9996dce744) |  | Under the AIMI Annotations initiative, a subset of The Cancer Genome Atlas Kidney Renal Clear Cell Carcinoma Collection (TCGA-KIRC) (Akin et al., 2016) is annotated for kidney, tumor and cyst regions, first by a trained AI model and corrected by an experienced… |
| B | [A Tertiary Lymphoid Structure-Derived Prognostic Signature Integrates Immune Microenvironment and Mutational Landscapes in Clear Cell Renal Cell Carcinoma.](https://doi.org/10.1155/humu/8446751) | 2026 | Europe PMC: named in Methods |
| B | [Synthesizing 4D image phantoms spanning multiple respiratory cycles from heterogeneous data sources](https://doi.org/10.1088/1361-6560/ae4afe) | 2026 | Cites the dataset DOI 10.7937/K9/TCIA.2016.V6PBVTDR (DataCite) |
| B | [Deciphering mitotic catastrophe-associated transcriptomic patterns in renal cell carcinoma: prognostic significance and immunotherapy-related associations.](https://doi.org/10.1186/s13062-026-00863-8) | 2026 | Europe PMC: named in Methods |
| B | [Angiogenesis-Informed Preoperative CT Radiogenomics Predicts Overall Survival in Clear Cell Renal Cell Carcinoma: Development and External Validation.](https://doi.org/10.3390/cancers18050768) | 2026 | Europe PMC: named in Methods |
| B | [Multimodal deep learning model for multiclass classification of renal tumors.](https://doi.org/10.1038/s41746-026-02697-0) | 2026 | Europe PMC: named in Methods |
| B | [Revealing hidden material composition via physics-induced deep learning for precision clinical diagnosis.](https://doi.org/10.1016/j.patter.2026.101620) | 2026 | Europe PMC: named in Methods |
| B | [PPP4C-related metastasis genes serve as a prognostic signature and potential therapeutic target in renal cell carcinoma.](https://doi.org/10.1007/s12672-026-04930-4) | 2026 | Europe PMC: named in Methods |
| B | [UCSF RMaC: University of California San Francisco 3D Multi-Phase Renal Mass CT Dataset with Tumor Segmentations](https://doi.org/10.64898/2026.02.11.26346096) | 2026 | Cites the dataset DOI 10.7937/K9/TCIA.2016.V6PBVTDR (DataCite) |
| B | [CT Radiogenomics Provides a Novel Factor for cM0(i+) Risk Stratification in Localized Renal Cell Carcinoma: A Model Linked to a Circulating Tumor Cell-Related Gene Signature](https://doi.org/10.1016/j.acra.2026.02.016) | 2026 | Cites the dataset DOI 10.7937/K9/TCIA.2016.V6PBVTDR (DataCite) |
| B | [Tumor morphology on CT radiomics is largely driven by the local anatomical environment, not the primary tumor type](https://doi.org/10.1186/s41747-026-00691-5) | 2026 | Cites the dataset DOI 10.7937/K9/TCIA.2016.V6PBVTDR (DataCite) |

88 more candidate(s) in the CSV.

### K10 — HuBMAP Hacking the Kidney

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *Segmentation of human functional tissue units in support of a Human Reference Atlas* (16 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/5c41352a6a1c86c43d1eda33c0525ae0ba5cdcb0>
- OpenAlex works citing *Segmentation of human functional tissue units in support of a Human Reference Atlas* (14): <https://openalex.org/works?filter=cites:W4384820854>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22Hacking%20the%20Kidney%22%20HuBMAP>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22Hacking%20the%20Kidney%22%20OR%20%28%22HuBMAP%22%20AND%20glomerul%2A%29%29>
- Kaggle competition "Code" tab: <https://www.kaggle.com/competitions/hubmap-kidney-segmentation/code>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [A Deep Learning Framework for Glomeruli Segmentation with Boundary Attention](https://doi.org/10.1109/ISBI61048.2026.11516050) | 2026 | We evaluated our method in comparison with the top three models on the Kaggle HuBMAP challenge leaderboard [18]. |
| B | [A MEF2C transcription factor network regulates proliferation of glomerular endothelial cells in diabetic kidney disease.](https://doi.org/10.1016/j.kint.2026.03.020) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [GlomNet: glomeruli segmentation network for WSI with diverse staining protocols for kidney disease diagnosis.](https://doi.org/10.3389/fmed.2026.1785037) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [StainStyleSampler: clustering-based sampling of whole slide image appearances.](https://doi.org/10.1186/s13000-026-01752-4) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Human BioMolecular Atlas Program (HuBMAP): 3D Human Reference Atlas construction and usage](https://doi.org/10.1038/s41592-024-02563-5) | 2025 | Abstract/title: Human BioMolecular Atlas Program (HuBMAP): 3D Human Reference Atlas construction and usage. |
| B | [Integration of spatial protein imaging and transcriptomics in the human kidney tracks the regenerative potential of proximal tubules.](https://doi.org/10.1126/sciadv.adv8918) | 2025 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Spatial top-down proteomics for the functional characterization of human kidney.](https://doi.org/10.1186/s12014-025-09531-x) | 2025 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [miRNA and mRNA Signatures in Human Acute Kidney Injury Tissue.](https://doi.org/10.1016/j.ajpath.2024.08.013) | 2025 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Three dimensional multiscalar neurovascular nephron connectivity map of the human kidney across the lifespan.](https://doi.org/10.1038/s41467-025-60435-8) | 2025 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [FUSION: a web-based application for in-depth exploration of multi-omics data with brightfield histology.](https://doi.org/10.1038/s41467-025-63050-9) | 2025 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Histology image analysis of 13 healthy tissues reveals molecular-histological correlations.](https://doi.org/10.1038/s41598-025-11853-7) | 2025 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [GNCnn: A QuPath extension for glomerulosclerosis and glomerulonephritis characterization based on deep learning.](https://doi.org/10.1016/j.csbj.2024.11.049) | 2025 | Europe PMC: named in Methods; Europe PMC: named in full text |

119 more candidate(s) in the CSV.

### K11-K12 — HuBMAP+HPA Hacking the Human Body

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *Segmenting functional tissue units across human organs using community-driven development of generalizable machine learning algorithms* (19 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/0a63cc935e8d0ed032e90b106130d0352a7e1e1e>
- OpenAlex works citing *Segmenting functional tissue units across human organs using community-driven development of generalizable machine learning algorithms* (26): <https://openalex.org/works?filter=cites:W4385551808>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22Hacking%20the%20Human%20Body%22%20HuBMAP>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22Hacking%20the%20Human%20Body%22%20OR%20%28%22HuBMAP%22%20AND%20%22Human%20Protein%20Atlas%22%20AND%20segmentation%29%29>
- Kaggle competition "Code" tab: <https://www.kaggle.com/competitions/hubmap-organ-segmentation/code>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Yet another STAin NORmalization Method: Point Set Registration for Color Space Alignment in Histological Images](https://doi.org/10.1109/EMBC58623.2025.11253721) | 2025 | MedSAM was originally trained using HuBMAP dataset [22]. |
| B | [GlomNet: glomeruli segmentation network for WSI with diverse staining protocols for kidney disease diagnosis.](https://doi.org/10.3389/fmed.2026.1785037) | 2026 | Europe PMC: named in Methods |
| B | [Human BioMolecular Atlas Program (HuBMAP): 3D Human Reference Atlas construction and usage](https://doi.org/10.1038/s41592-024-02563-5) | 2025 | Abstract/title: Human BioMolecular Atlas Program (HuBMAP): 3D Human Reference Atlas construction and usage. |
| B | [Antibody-Based Multiplex Image Analysis: Standard Analytical Workflows and Artificial Intelligence Tools for Pathologists.](https://doi.org/10.1016/j.labinv.2025.104220) | 2025 | Europe PMC: named in Methods |
| B | [Flexible and robust cell-type annotation for highly multiplexed tissue images.](https://doi.org/10.1016/j.cels.2025.101374) | 2025 | Europe PMC: named in Methods |
| B | [Human Organ Functional Tissue Units Image Segmentation Based on UNeXt50](https://doi.org/10.1109/ACCTCS66275.2025.00050) | 2025 | Abstract/title: Experimental results on the HuBMAP + HPA dataset demonstrate that UNeXt50 achieves an optimal Dice coefficient of 83.7% with a threshold of 0.51, outperforming traditional U-Net variants in handling complex tissue boundaries and cross-organ var… |
| B | [Human BioMolecular Atlas Program (HuBMAP): 3D Human Reference Atlas Construction and Usage](https://doi.org/10.1101/2024.03.27.587041) | 2024 | Abstract/title: Human BioMolecular Atlas Program (HuBMAP): 3D Human Reference Atlas Construction and Usage. |
| B | [Flexible and robust cell type annotation for highly multiplexed tissue images](https://doi.org/10.1101/2024.09.12.612510) | 2024 | Europe PMC: named in Methods |
| B | [Segmenting functional tissue units across human organs using community-driven development of generalizable machine learning algorithms.](https://doi.org/10.1038/s41467-023-40291-0) | 2023 | Abstract/title: We present the setup and results of the Hacking the Human Body machine learning algorithm development competition hosted by the Human Biomolecular Atlas (HuBMAP) and the Human Protein Atlas (HPA) teams on the Kaggle platform. |
| B | [Spatial omics technologies at multimodal and single cell/subcellular level.](https://doi.org/10.1186/s13059-022-02824-6) | 2022 | Europe PMC: named in Methods |

26 more candidate(s) in the CSV.

### K13 — TRUSTED

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *TRUSTED: The Paired 3D Transabdominal Ultrasound and CT Human Data for Kidney Segmentation and Registration Research* (10 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/ed4bb08b90edaa3345e282d2dbb4b94527ff5467>
- OpenAlex works citing *TRUSTED: The Paired 3D Transabdominal Ultrasound and CT Human Data for Kidney Segmentation and Registration Research* (7): <https://openalex.org/works?filter=cites:W4409391010>
- DataCite Commons, works citing the dataset DOI `10.6084/m9.figshare.27981050`: <https://commons.datacite.org/doi.org/10.6084/m9.figshare.27981050>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22TRUSTED%22%20kidney%20ultrasound%20CT%20dataset>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22TRUSTED%22%20AND%20kidney%20AND%20ultrasound%20AND%20CT%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Noise-Aware Boundary-Enhanced Generative Learning for Ultrasound Speckle Reduction](https://doi.org/10.48550/arXiv.2606.25009) | 2026 | …the applicability of NBGL to a different anatomical region and acquisition setting, additional experiments were conducted on the TRUSTED dataset (Ndzimbong et al., 2025), a transabdominal kidney ultrasound dataset with expert anatomical landmark annotations, … |

20 more candidate(s) in the CSV.

### K14 — Axial CT kidney stone (Mendeley)

**Where to find every paper that cites or uses it:**

- DataCite Commons, works citing the dataset DOI `10.17632/fwhytt5mzd.2`: <https://commons.datacite.org/doi.org/10.17632/fwhytt5mzd.2>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22Axial%20CT%20Imaging%20Dataset%20for%20AI-Powered%20Kidney%20Stone%20Detection%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22fwhytt5mzd%22%20OR%20%22Axial%20CT%20Imaging%20Dataset%20for%20AI-Powered%20Kidney%20Stone%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| B | [Prospective pilot evaluation of a deep learning model for kidney stone detection on CT using a web-based workflow platform](https://doi.org/10.1007/s11255-026-05057-9) | 2026 | Cites the dataset DOI 10.17632/fwhytt5mzd.2 (DataCite) |
| B | [A Comprehensive Analysis of Deep and Traditional Machine Learning for Kidney Diseases and Lung Cancer CT Interpretation](https://doi.org/10.1007/978-3-032-23716-3_24) | 2026 | Cites the dataset DOI 10.17632/fwhytt5mzd.2 (DataCite) |
| B | [KidneyStoneNet: A Deep Learning Approach for Kidney Stone Detection with Transfer Learning and Explainable AI](https://doi.org/10.1007/978-3-032-27708-4_22) | 2026 | Cites the dataset DOI 10.17632/fwhytt5mzd.2 (DataCite) |
| B | [Kidney stone detection via axial CT imaging: A dataset for AI and deep learning applications.](https://doi.org/10.1016/j.dib.2025.111446) | 2025 | Cites the dataset DOI 10.17632/fwhytt5mzd.2 (DataCite) |
| B | [Contour‐Detected Normalized Residual Model for Kidney Stone Classification](https://doi.org/10.1155/acis/5844438) | 2025 | Cites the dataset DOI 10.17632/fwhytt5mzd.2 (DataCite) |

1 more candidate(s) in the CSV.

### M01 — TotalSegmentator CT

> Most papers citing TotalSegmentator run the released **model** on their own scans. That is not use of the dataset. Rows marked `check_model_vs_dataset_use` look (by a text heuristic) like runs of the model; they are sorted last. The flag is a hint, not a verdict.

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *TotalSegmentator: Robust Segmentation of 104 Anatomic Structures in CT Images.* (1982 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/586f5754f6825d445afa5026c0fede55a65290a1>
- OpenAlex works citing *TotalSegmentator: Robust Segmentation of 104 Anatomic Structures in CT Images* (1484): <https://openalex.org/works?filter=cites:W4383218413>
- DataCite Commons, works citing the dataset DOI `10.5281/zenodo.6802613`: <https://commons.datacite.org/doi.org/10.5281/zenodo.6802613>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22TotalSegmentator%20dataset%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22TotalSegmentator%20dataset%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [A prospective multicenter trial of deep learning auto-segmentation for organs at risk in thoracic radiotherapy](https://doi.org/10.1038/s41467-026-70863-9) | 2026 | We benchmarked the performance of iCurveE model on our ﬁ ve-center cohort against an nnU-Net model trained from scratch (using the identical development images) and the open-source TotalSegmentator 21,33 . |
| A | [Annotating anatomy and pathology in the National Lung Screening Trial computed tomography images](https://arxiv.org/abs/2609.10858) | 2026 | To enrich the NLST collection with anatomic organ segmentations, we used TotalSegmentator 17 , a deep learning model capable of segmenting over 100 anatomical regions in CT images, trained on a diverse dataset of patients with multiple pathologies, and collect… |
| A | [Do Medical Vision Models Reason About Anatomy? Probing the Spatial Inductive Biases of Learned Visual Representations](https://arxiv.org/abs/2608.28092) | 2026 | A regularity common to abdominal CT would survive our probe-level controls, so we evaluate every trained configuration on TotalSegmentator [27] without re-6 training, deriving labels by the procedure of Section 3.1. |
| A | [A Few Cases Are All You Need: An Empirical Study of Annotation-Efficient LoRA Fine-Tuning of MedSAM3](https://arxiv.org/abs/2608.18731) | 2026 | TotalSegmentator was trained on 1,204 CT scans and can segment 104 anatomical structures [14]. |
| A | [MedSAM2-Anatomy: Training-Free Inference-Time Optimization for Musculoskeletal Segmentation](https://arxiv.org/abs/2608.00195) | 2026 | TotalSegmentator [3] is the frozen expert CNN, MedSAM2 [8] the frozen promptable foundation model, and MedSAM2-Anatomy our training-free inference-time optimisation of the two. |
| A | [Organ Segmentation with Machine Learning Models](https://doi.org/10.3390/jimaging12080335) | 2026 | Third, we validate the ranking zero-shot on the independent TotalSegmentator dataset [16], determining whether the AMOS conclusions transfer off-distribution. |
| A | [Customized 3D-printed breast prostheses using patient imaging at the point of care: feasibility and proof-of-concept study](https://doi.org/10.1088/2057-1976/ae8af5) | 2026 | …scope, segmentation tools such as TotalSegmentator achieve Dice coefficients of 0.943 on CT imaging across 104 anatomic structures using nnU-Net trained on over 1200 diverse scans [37], contextualizing Restora’s performance within the inherent challenges of b… |
| A | [Potential of Image2Image translation in reducing AI bias attributed to differences in CT reconstruction methods: proof-of-concept study on a paired dataset](https://doi.org/10.3389/fradi.2026.1875867) | 2026 | In addition, we assess anatomical structure segmentation using Body Composition Analysis (BCA) and TotalSegmentator (16), providing a downstream clinical validity evaluation alongside task-agnostic distribution metrics. |
| A | [Patient-Specific Articulated Digital Twins from a Single Full-Body CT Scan](https://doi.org/10.48550/arXiv.2607.02156) | 2026 | Specifically, we use TotalSegmentator [16] to extract semantic segmentations of the body, bones, and organs. |
| A | [An Uncertainty Estimation Framework for Dose Accumulation in Adaptive Radiotherapy: Application to CBCT-Guided Radiotherapy for Cervical Cancer](https://doi.org/10.48550/arXiv.2606.11012) | 2026 | We selected TotalSegmentator [34], a state-of-the-art segmentation model based on five nnU-Net architectures trained on a large CT dataset. |
| A | [Automated Prediction of Postoperative Pancreatic Fistula Using Preoperative Computed Tomography](https://doi.org/10.48550/arXiv.2605.31539) | 2026 | To objectively stratify CT scans by contrast timing, we used a TotalSegmentator [13]-based phase prediction pipeline in which the median Hounsfield Unit (HU) intensity within each structure is extracted as a feature vector. |
| A | [Whole-body CT attenuation and volume charts from routine clinical scans via evidence-grounded LLM report filtering](https://doi.org/10.48550/arXiv.2605.05933) | 2026 | We used TotalSegmentator version 2.2.1 [1] for the automated segmentation of 106 anatomical structures, including 23 organs, 58 bones, 8 muscles, and 17 major vessels (see supplement S1); segmentation quality on our PACS data was previously validated [14]. |

535 more candidate(s) in the CSV.

### M02 — TotalSegmentator MRI

> As with M01, citing papers usually run the model rather than train or test on the MRI dataset.

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *TotalSegmentator MRI: Robust Sequence-independent Segmentation of Multiple Anatomic Structures in MRI.* (154 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/18362723e36cfdcd5ef1526360ffbbdc4695fd51>
- OpenAlex works citing *TotalSegmentator MRI: Robust Sequence-independent Segmentation of Multiple Anatomic Structures in MRI* (100): <https://openalex.org/works?filter=cites:W4407677889>
- DataCite Commons, works citing the dataset DOI `10.5281/zenodo.11367004`: <https://commons.datacite.org/doi.org/10.5281/zenodo.11367004>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22TotalSegmentator%20MRI%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22TotalSegmentator%20MRI%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Liver Segment and Lesion Segmentation on CT and MRI: An Open-Source Contribution to TotalSegmentator](https://doi.org/10.1007/s10278-025-01716-y) | 2025 | The first model (SMMRI) was trained on a dataset of MRIs only, labelled “D-MRI”, derived from a subset of data employed in the TotalSegmentator MRI Project [2], where “abdomen” and “liver” served as inclusion criteria. |
| A | [nnSAM2: nnUNet-Enhanced One-Prompt SAM2 for Few-shot Multi-Modality Segmentation and Composition Analysis of Lumbar Paraspinal Muscles](https://doi.org/10.48550/arXiv.2510.05555) | 2025 | For benchmarking, we compared nnsam2 against (i) vanilla SAM2 (18) and its medical fine-tuned variants (19,20), representing promptable foundation-model approaches; (ii) FAMNet (16), the state-of-the-art CD-FSMIS method; and (iv) TotalSegmentator (12,15), a fu… |
| A | [MAGnet: synthesis of CT images from MRI data with guided segmentation masks](https://doi.org/10.1117/12.3086114) | 2026 | …texture, mitigating the trade-offs common to uniform translators; (ii) a label-efficient guidance strategy that leverages TotalSegmentator 19,20 masks to scale anatomy-aware conditioning without manual contouring; and (iii) comprehensive validation on public … |
| A | [Automated Prostate Gland Segmentation in MRI Using nnU-Net](https://doi.org/10.48550/arXiv.2604.01964) | 2026 | TotalSegmentator was originally developed as a large-scale, multi-organ segmentation framework trained on heterogeneous MRI and CT datasets to segment a wide range of anatomical structures (up to 80) across varying imaging conditions [4] . |
| A | [Standardizing ACL tunnel placement: an automated method for knee quadrant computation](https://doi.org/10.1007/s11548-026-03578-3) | 2026 | Therefore, weﬁne-tunedtheTotalSegmentator[26,27],annUNet-based [26] foundation model pretrained on 1139 CT and 561 MRI images. |
| A | [Zero-shot System for Automatic Body Region Detection for Volumetric CT and MR Images](https://doi.org/10.48550/arXiv.2602.08717) | 2026 | Our analysis was conducted on 887 medical volumes (465 CT, 422 MR) from the TotalSegmentator public datasets [13], [14]. |
| A | [LISP-Net: Context-Aware and Lightweight Interactive Medical Segmentation](https://doi.org/10.1109/ACCESS.2026.3727306) | 2026 | Since one of the evaluation datasets (TotalSegmentator MRI) [27] was part of UniverSeg’s original training corpus, results on this dataset should be interpreted as a partial in-distribution comparison for UniverSeg rather than a fully held-out generalization s… |
| A | [Biomechanical Constraints Assimilation in Deep-Learning Image Registration: Application to sliding and locally rigid deformations](https://doi.org/10.48550/arXiv.2504.05444) | 2025 | Specifically, we used TotalSegmentator [56, 57, 58] in our work to obtain more than 100 labels associated with each image. |
| B | [A comprehensive framework for planning pedicle screw trajectory using ANTs template-based registration approach](https://doi.org/10.1007/s00586-026-10295-7) | 2026 | Cites the dataset DOI 10.5281/zenodo.11367004 (DataCite) |
| A (model use?) | [Learning like a radiologist: a medical vision-language model for radiological image analysis via curriculum learning](https://doi.org/10.1038/s41746-026-02713-3) | 2026 | For MR imaging, we conducted a ten-organ multi-label classi ﬁ cation task on MR scans using the TotalSegmentator-MR dataset, which includes . |
| B (model use?) | [Location-Aware Fine-Grained Representation Learning for Medical Vision Foundation Models](https://arxiv.org/abs/2608.00976) | 2026 | TotalSegmentator CT contains 1,204 CT scans with 104 annotated anatomical structures, and TotalSegmentator MRI contains 616 MRI scans with 50 annotated anatomical regions. |
| B (model use?) | [Automatically Measuring Kidney, Liver, and Cyst Volumes in Autosomal Dominant Polycystic Kidney Disease](https://doi.org/10.1681/ASN.0000000904) | 2025 | TraceOrg model performance on the internal and external validation datasets was further compared with five open source models that are publicly available: TotalSegmentator, 33 MRAnnotator, 34 Kim et al., 7 Woznicki et al., 32 and the kidney cyst segmentation m… |

40 more candidate(s) in the CSV.

### M03 — AMOS22

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *AMOS: A Large-Scale Abdominal Multi-Organ Benchmark for Versatile Medical Image Segmentation* (610 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/27d5abc68c2e5555bca47a3aff3f074b01f35b8c>
- OpenAlex works citing *AMOS: A Large-Scale Abdominal Multi-Organ Benchmark for Versatile Medical Image Segmentation* (201): <https://openalex.org/works?filter=cites:W4283072464>
- DataCite Commons, works citing the dataset DOI `10.5281/zenodo.7262581`: <https://commons.datacite.org/doi.org/10.5281/zenodo.7262581>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22AMOS22%22%20OR%20%22AMOS%20dataset%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22AMOS22%22%20OR%20%22AMOS%202022%22%20OR%20%28%22AMOS%22%20AND%20%22abdominal%20multi-organ%22%29%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Organ Segmentation with Machine Learning Models](https://doi.org/10.3390/jimaging12080335) | 2026 | We use the CT split of the Multi-Modality Abdominal Multi-Organ Segmentation (AMOS) dataset [20], which we obtained in its labelled training release of 300 CT volumes. |
| A | [SAM-Med3D: A Vision Foundation Model for General-Purpose Segmentation on Volumetric Medical Images](https://doi.org/10.1109/TNNLS.2025.3586694) | 2025 | A. Experimental Setup 1) Preliminary Experiment Details: For the preliminary experiment, we trained all the models on the training set of AMOS [37] for 400 epochs, with the implementation details consistent with those described in Section V-A.2. |
| A | [Decipher-MR: a vision-language foundation model for 3D MRI representations](https://doi.org/10.1038/s41746-026-02596-4) | 2025 | For AMOS, we used the official train/validation split[22], reported the mean Dice across all organs on the validation set, and referenced the nnUNet performance from the original AMOS paper[22]. |
| A | [MaskSAM: Auto-Prompt SAM with Mask Classification for Volumetric Medical Image Segmentation](https://doi.org/10.1109/ICCV51701.2025.02264) | 2025 | We use three publicly available datasets: AMOS22 Abdominal CT Organ Segmentation [29], Synapse Multiorgan Segmentation [31], and the Automatic Cardiac Diagnosis Challenge (ACDC) [3]. |
| A | [A dual self-attentive transformer U-Net model for precise pancreatic segmentation and fat fraction estimation](https://doi.org/10.1186/s12880-025-01852-5) | 2025 | We test our approach on five distinct datasets: The AMOS dataset [34] contains 200 scans with segmentation masks of multiple organs, including the pancreas; WORD [35] includes 120 pancreas segmentations of healthy persons; BTCV [36] Here, identical experimenta… |
| A | [SAM-aware Test-time Adaptation for Universal Medical Image Segmentation](https://doi.org/10.48550/arXiv.2506.05221) | 2025 | …Cancer Segmentation Tasks: To assess in-distribution versus out-of-distribution (OOD) performance, we evaluate the Pancreas task from AMOS 2022 [47], which was used to train MedSAM [11] and SAM-Med2D [21], and the Pancreatic cancer task from MSWAL [48], which… |
| A | [UKBOB: One Billion MRI Labeled Masks for Generalizable 3D Medical Image Segmentation](https://doi.org/10.1109/ICCV51701.2025.02006) | 2025 | We also rely on the zero-shot segmentation performance of a model trained solely on those collected labels to be evaluated on a similar domain, namely the AMOS Abdomen MRI dataset [32] and on MRI on BTCV dataset [16] in Table 5. |
| A | [Boosting Semi-Supervised Medical Image Segmentation via Masked Image Consistency and Discrepancy Learning](https://doi.org/10.48550/arXiv.2503.14013) | 2025 | A. Experimental Setup 1) Dataset: Our proposed semi-supervised medical image segmentation method has been validated on the AMOS [17] and Synapse [18] datasets. |
| A | [Learning General-Purpose Biomedical Volume Representations using Randomized Synthesis](https://doi.org/10.48550/arXiv.2411.02372) | 2024 | Notably, while PrimGeoSeg had originally outperformed our method on the AMOS-CT few-shot segmentation experiment in the main paper, its performance drops below ours by 5 mean Dice points when matched in parameter count, suggesting that the performance gap is a… |
| A | [Clustering Propagation for Universal Medical Image Segmentation](https://doi.org/10.1109/CVPR52733.2024.00323) | 2024 | To comprehensively evaluate our method, we experiment S2VNet on three volumetric datasets, i.e ., WORD [23], BTCV [24], and AMOS [25]. |
| A | [FreeTumor: Advance Tumor Segmentation via Large-Scale Tumor Synthesis](https://doi.org/10.48550/arXiv.2406.01264) | 2024 | Thanks to the previous efforts, we can collect large-scale CT datasets with organ labels, i.e. , CHAOS [30], Pancreas-CT [55], BTCV [34], Amos22 [26], WORD [41], Flare22 [44], Abdomenct-1k [43], AbdomenAtlas [50], and Flare23 [44]. |
| A | [Children Are Not Small Adults: Addressing Limited Generalizability of an Adult Deep Learning CT Organ Segmentation Model to the Pediatric Population](https://doi.org/10.1007/s10278-024-01273-w) | 2024 | For our adult CT dataset, we used 300 CT scans of the abdomen and pelvis from the Abdominal Multi-Organ Segmentation (AMOS) dataset provided in NIfTI format with voxel-level annotations for up to 15 abdominal organs [18] (Table 1). |

278 more candidate(s) in the CSV.

### M04 — CHAOS

> CHAOS kidney labels exist only in the MRI part. Papers using only CHAOS-CT (liver) are not kidney uses.

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *CHAOS Challenge - Combined (CT-MR) Healthy Abdominal Organ Segmentation* (911 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/6d38bdd172cdbccb11745f5f031f848679117f25>
- OpenAlex works citing *CHAOS Challenge - combined (CT-MR) healthy abdominal organ segmentation* (825): <https://openalex.org/works?filter=cites:W3002569343>
- DataCite Commons, works citing the dataset DOI `10.5281/zenodo.3362844`: <https://commons.datacite.org/doi.org/10.5281/zenodo.3362844>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22CHAOS%20challenge%22%20kidney>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22CHAOS%20challenge%22%20OR%20%22CHAOS%20dataset%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [MedCLIPSeg: Probabilistic Vision-Language Adaptation for Data-Efficient and Generalizable Medical Image Segmentation](https://doi.org/10.48550/arXiv.2602.20423) | 2026 | We validate this on the CHAOS CT Liver dataset [39] following the M3D-Seg data split and achieve a DSC of 88.72% , demonstrating that MedCLIPSeg generalizes beyond 2D. |
| A | [Learning like a radiologist: a medical vision-language model for radiological image analysis via curriculum learning](https://doi.org/10.1038/s41746-026-02713-3) | 2026 | Spatial localization performance was tested on the internal CT dataset, AMOS-CT, CT-ORG, and CHAOS-MR datasets. |
| A | [Morphogenetic Field Loss for Unified Medical Image Segmentation](https://doi.org/10.1109/ISBI61048.2026.11515683) | 2026 | We evaluate MFLoss on six benchmarks ISIC 2017 [2], CHAOS CT/MRI [1], Retinal OCT [3], Intra-Operative In-struments [4], and MRBrainS18 [15], demonstrating improved boundary coherence, regional stability, and convergence across CNNs, hybrid models, and transfo… |
| A | [Neural architecture search with Deep Radon Prior for sparse‐view CT image reconstruction](https://doi.org/10.1002/mp.17685) | 2025 | We selected images from the CHAOS and Lung-PET-CT-Dx datasets as the test set to comprehensively evaluate the reconstruction performance of different methods. |
| A | [CoMed-SAM: Collaborative Medical SAM for Multi-Modality Image Segmentation](https://doi.org/10.1109/ACCESS.2025.3626037) | 2025 | The effectiveness of CoMed-SAM has been validated through extensive experiments on the IVDM3Seg dataset [32] for lumbar intervertebral disc segmentation and the CHAOS dataset [33] for abdominal organ segmentation. |
| A | [FreeTumor: Advance Tumor Segmentation via Large-Scale Tumor Synthesis](https://doi.org/10.48550/arXiv.2406.01264) | 2024 | Thanks to the previous efforts, we can collect large-scale CT datasets with organ labels, i.e. , CHAOS [30], Pancreas-CT [55], BTCV [34], Amos22 [26], WORD [41], Flare22 [44], Abdomenct-1k [43], AbdomenAtlas [50], and Flare23 [44]. |
| A | [Attention Based Cross-Domain Synthesis and Segmentation From Unpaired Medical Images](https://doi.org/10.1109/TETCI.2023.3296499) | 2024 | Firstly, we introduce the used four datasets: MRI-CT abdomen dataset CHAOS [10], MRI T1-T2 brain datasetiSeg-2017[11],andtwoOCTretinaldatasets,Data-Duke [35] and Data-Hopkins [36], as well as implementation details. |
| A | [Dimensionality Reduction and Nearest Neighbors for Improving Out-of-Distribution Detection in Medical Image Segmentation](https://doi.org/10.59275/j.melba.2024-g93a) | 2024 | MRI+ UNETR was trained on 48 scans from the AMOS dataset, 172 scans from the DLDS dataset, 38 scans from the CHAOS dataset, 44 scans from the Tumor and Liver Automatic Segmentation (ATLAS) dataset (Quinton et al., 2023), and 69 scans from MD Anderson, for a to… |
| A | [Med3DInsight: Enhancing 3D Medical Image Understanding with 2D Multi-Modal Large Language Models](https://doi.org/10.48550/arXiv.2403.05141) | 2024 | In this experiment, we use CTs, consist of 177 to 363 slices with 512 × 512 pixels and voxel spacing ranging from 0.3 to 0.6 mm. CHAOS [15]. |
| A | [Cross-Modal Learning via Adversarial Loss and Covariate Shift for Enhanced Liver Segmentation](https://doi.org/10.1109/TETCI.2024.3369868) | 2024 | We use the CHAOS Challenge dataset [16], which contains both MR and CT scans of the upper abdominal region. |
| A | [S2S2: Semantic Stacking for Robust Semantic Segmentation in Medical Imaging](https://doi.org/10.48550/arXiv.2412.13156) | 2024 | For 3D images (Synapse, CHAOS T2-SPIR, LGE, and bSSFP datasets), these metrics are calculated over the entire 3D volume, whereas for 2D images in the Kvasir-SEG and CVC-ClinicDB datasets, evaluations are performed on individual images. |
| A | [Bayesian uncertainty estimation for detection of long-tailed and unseen conditions in medical images](https://doi.org/10.1117/1.JMI.10.5.054501) | 2023 | On the other hand, our objective of using CHAOS segmentation was to test the model ’ s ability for multi-organ semantic segmentation. |

401 more candidate(s) in the CSV.

### M05 — CT-ORG

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *CT-ORG, a new dataset for multiple organ segmentation in computed tomography* (168 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/f3859b9f09b4b6ccbd3423659a6e56fe592d3691>
- OpenAlex works citing *CT-ORG, a new dataset for multiple organ segmentation in computed tomography* (145): <https://openalex.org/works?filter=cites:W3098715541>
- DataCite Commons, works citing the dataset DOI `10.7937/tcia.2019.tt7f4v7o`: <https://commons.datacite.org/doi.org/10.7937/tcia.2019.tt7f4v7o>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22CT-ORG%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22CT-ORG%22%29>
- TCIA publication list: <https://www.cancerimagingarchive.net/publications/>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [MambaMIM: Pre-training Mamba with state space token interpolation and its application to medical image segmentation](https://doi.org/10.1016/j.media.2025.103606) | 2024 | For CT-ORG and KiTS 23, we adopt an 80 / 20 train-validation split. |
| A | [NERONE: The Fast Way to Efficiently Execute Your Deep Learning Algorithm at the Edge](https://doi.org/10.1109/JBHI.2023.3296142) | 2023 | We employed a 2D FCN based on the U-Net [26] architecture for the CT-ORG dataset [19], [20], while for the Prostate-3T dataset [24], we chose a network based on the V-Net [27] architecture. |
| A | [Leveraging Self-Supervised Vision Transformers for Neural Transfer Function Design](https://doi.org/10.48550/arXiv.2309.01408) | 2023 | Then we present a quantitative evaluation based on the CT-ORG [44] segmentation dataset, where we also compare our approach to related work. |
| A | [Robust Prototypical Few-Shot Organ Segmentation With Regularized Neural-ODEs](https://doi.org/10.1109/TMI.2023.3258069) | 2022 | We show R-PNODE’s efﬁcacy by repeating these experiments on three publicly available multi-organ segmentation datasets BCV [35], CT-ORG [36] and DECATHLON [37] for both in-domain and cross-domain settings on novel classes. |
| A | [Adversarially Robust Prototypical Few-Shot Segmentation with Neural-ODEs](https://doi.org/10.1007/978-3-031-16452-1_8) | 2022 | We experiment on three publicly available multi-organ segmentation datasets, BCV [3], CT-ORG [25], and Decathlon [23] to evaluate the generalisability of our method. |
| A | [On How to Push Efficient Medical Semantic Segmentation to the Edge: the SENECA approach](https://doi.org/10.1109/IPDPSW55747.2022.00027) | 2022 | Then, we select the best configuration among all the ones presented, and we will further analyze it by exploiting more metrics and comparing it with the CT-ORG work [17]. |
| A | [An Optimized U-Net for Unbalanced Multi-Organ Segmentation](https://doi.org/10.1109/EMBC48229.2022.9871288) | 2022 | We test our model with CT-ORG [3], [7], [8], [9], an open-source data set, which includes the segmentation of lungs, liver, bladder, bones, kidneys, and brain. |
| A | [Hierarchical Random Walker Segmentation for Large Volumetric Biomedical Images](https://doi.org/10.1109/TIP.2022.3185551) | 2021 | Subsequently, an evaluation on synthetic data, the CT-ORG dataset and real data from current biomedical research is presented and discussed, followed by the conclusion. |
| A | [Interpretable Auto Window Setting for Deep-Learning-Based CT Analysis](https://doi.org/10.1016/j.compbiomed.2025.110994) | 2025 | In this study, we primarily utilize several widely recognized public datasets, including Totalsegmentator [8], FLARE 2023 [21], CT-ORG [26], AbdomenCT-1K [22], KiTS23 [14, 15], and ImageTBAD [35]. |
| A | [Render-FM: Feedforward Model for Real-time Photorealistic Volumetric Rendering](https://arxiv.org/abs/2505.17338) | 2025 | …to GPU memory constraints) or lacking orthonormal directionality, we used 991 scans for training and 46 for in-domain ( ID ) testing; 2) CT-ORG [25]: This dataset includes 140 CT scans from diverse sources, featuring both large organs ( e.g ., lungs) and smal… |
| A | [Unleashing Diffusion and State Space Models for Medical Image Segmentation](https://doi.org/10.48550/arXiv.2506.12747) | 2025 | The data are split into training, testing, and inference sets as follows: • Training set (2,860 images): In Stage 1, we use 8 public datasets (2,668 images) to train organ labels, including BTCV (Landman et al., 2015), CHAOS (Kavur et al., 2021), Pancreas-CT (… |
| A | [VELVET-Med: Vision and Efficient Language Pre-training for Volumetric Imaging Tasks in Medicine](https://doi.org/10.48550/arXiv.2508.12108) | 2025 | Experiments are conducted on public datasets: AbdomenCT-1K [55] with 1000 annotated CT scans and CT-Organ [56] with 140 annotated CT scans, using the official splits. |

94 more candidate(s) in the CSV.

### M06 — WORD

> The WORD paper is not indexed by Semantic Scholar, so there are no citing sentences. Candidates come from OpenAlex abstracts and Europe PMC; use the OpenAlex and Google Scholar links for the full list.

**Where to find every paper that cites or uses it:**

- OpenAlex works citing *WORD: A large scale dataset, benchmark and clinical applicable study for abdominal organ segmentation from CT image* (173): <https://openalex.org/works?filter=cites:W4298110661>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22WORD%20dataset%22%20abdominal>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22WORD%20dataset%22%20AND%20%28abdominal%20OR%20organ%29%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| B | [Demographic-aware deep learning for multi-organ segmentation: Mitigating gender and age biases in CT images.](https://doi.org/10.1002/mp.70322) | 2026 | Abstract/title: We validate the generalizability and effectiveness of our framework on an external dataset (WORD, 150 adults, 62 females). |
| B | [DBANet: Dual Boundary Awareness With Confidence-Guided Pseudo Labeling for Medical Image Segmentation.](https://doi.org/10.1109/jbhi.2025.3592873) | 2026 | Abstract/title: Similarly, on the WORD dataset, DBANet achieves average Dice score improvements of 1.72%, 0.97%, and 0.65% under 2%, 5%, and 10% labeled data settings, respectively. |
| B | [Surface Mesh Reconstruction From Medical Images via Enrichment Feature Learning and Mesh Contour Loss](https://doi.org/10.1109/tmrb.2026.3654256) | 2026 | Abstract/title: Moreover, we evaluate our RFENet on rectum surface mesh reconstruction in the WORD dataset for the first time, achieving favorable outcomes and highlighting the potential advantages of our proposed method. |
| B | [Anatomy as a guide: Using learned priors for precise organ segmentation](https://doi.org/10.1016/j.craph.2025.100017) | 2026 | Abstract/title: We trained and evaluated our model on the Whole Abdominal Organ Dataset (WORD), a large-scale benchmark with 150 CT scans and 16 annotated organs, comparing its performance against state-of-the-art baselines using Dice Similarity Coefficient (D… |
| B | [Enhancing feature discrimination with pseudo-labels for foundation model in segmentation of 3D medical images](https://doi.org/10.1016/j.neunet.2025.107979) | 2025 | Abstract/title: Experimental results demonstrate that PESF achieves a 6.8% improvement in the overall average Dice Similarity Coefficient (DSC) compared to the baseline SAM-Med3D on (Amos, FLARE22, WORD, BTCV), with particularly gains in challenging anatomical… |
| B | [SALT: Introducing a framework for hierarchical segmentations in medical imaging using label trees.](https://doi.org/10.1038/s41598-025-31639-1) | 2025 | Abstract/title: Dice scores across SAROS, CT-ORG, FLARE22, LCTSC, LUNA16, and WORD datasets measured performance, with 95% confidence intervals (CI) from 1000 bootstrapping rounds. |
| B | [Rectal cancer segmentation via HHF-SAM: a hierarchical hypercolumn-guided fusion segment anything model.](https://doi.org/10.3389/frai.2025.1696984) | 2025 | Abstract/title: The model was evaluated on two public abdominal CT datasets (CARE and WORD) using mean Dice coefficient (mDice) and mean Intersection over Union (mIoU) as metrics. |
| B | [Alleviating Class Imbalance in Semi-Supervised Multi-Organ Segmentation via Balanced Subclass Regularization](https://doi.org/10.1109/lsp.2024.3451962) | 2024 | Abstract/title: Extensive experiments conducted on two publicly available datasets, i.e., the MICCAI FLARE 2022 dataset and the WORD dataset, verify the superior performance of our method compared with other methods. |
| B | [An Efficient Spatial Modeling Conv-ViT using Mask Supervision for 3D Medical Image Segmentation](https://doi.org/10.1109/ijcnn60899.2024.10650648) | 2024 | Abstract/title: We conducted experiments on two authoritative abdominal multi-organ segmentation datasets, AMOS2022 and WORD. |
| B | [CFANet: Context Feature Fusion and Attention Mechanism Based Network for Small Target Segmentation in Medical Images.](https://doi.org/10.3390/s23218739) | 2023 | Abstract/title: Extensive experiments are conducted on four challenging medical image datasets, namely ADAM, LUNA16, Thoracic OAR, and WORD. |

17 more candidate(s) in the CSV.

### M07 — AbdomenAtlas

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *AbdomenAtlas: A large-scale, detailed-annotated, & multi-center dataset for efficient transfer learning and open algorithmic benchmarking* (99 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/3c81dffa975311b21c45d601de1f1f445699a82f>
- Semantic Scholar citations of *AbdomenAtlas: A large-scale, detailed-annotated, & multi-center dataset for efficient transfer learning and open algorithmic benchmarking* (99 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/3c81dffa975311b21c45d601de1f1f445699a82f>
- OpenAlex works citing *AbdomenAtlas: A large-scale, detailed-annotated, & multi-center dataset for efficient transfer learning and open algorithmic benchmarking* (51): <https://openalex.org/works?filter=cites:W4401115924>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22AbdomenAtlas%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22AbdomenAtlas%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Large-Scale Label Quality Assessment for Medical Segmentation Via a Vision-Language Judge and Synthetic Data](https://doi.org/10.1109/ISBI61048.2026.11515717) | 2026 | We assess whether SegAE improves sample selection on To-talSegmentator [1] and AbdomenAtlas-Tumors [3] using a pretrained SwinUNETR [18]. |
| A | [RadGPT: Constructing 3D Image-Text Tumor Datasets](https://doi.org/10.1109/ICCV51701.2025.02202) | 2025 | Given the small size of this dataset, we fine-tuned an nnU-Net pre-trained on 9,262 CT scans in AbdomenAtlas 1.1 [31]. |
| A | [Scaling Tumor Segmentation: Best Lessons from Real and Synthetic Data](https://doi.org/10.1109/ICCV51701.2025.02225) | 2025 | We train ResEncM [45] with the annotated tumor data in AbdomenAtlas 2.0 and compare with the following state-of-the-art medical image segmentation models: UNETR [32], Swin UNETR [92], nnU-Net [44], ResEncM [45] and STU-Net [43], SegRes-Net [76], Universal Mode… |
| A | [AdaViT: Adaptive Vision Transformer for Flexible Pretrain and Finetune with Variable 3D Medical Image Modalities](https://doi.org/10.48550/arXiv.2504.03589) | 2025 | Zhou et al. [24] applied it to both CNN and transformer based 3D models using the AbdomenAtlas 1.1 dataset [25] (CT images) for supervised pretrain and achieved excellent finetune performance on the TotalSegmentator v1 dataset [37] as well as a proprietary dat… |
| A | [A Two-Stage Contrastive Learning Framework Grounded in Label-Specific Features for Low-Frequency Labels in Chest X-Ray Multi-Label Classification](https://doi.org/10.3390/bioengineering13050553) | 2026 | AbdomenAtlas [24] is pre-trained on abdominal CT datasets and then transferred to small-scale tasks such as liver tumor segmentation. |
| A | [3D Venous Anatomy Analysis for Pancreatic Surgery Using Large Vision-Language Model](https://doi.org/10.1109/BIBM66473.2025.11356698) | 2025 | The dataset consists of 123 thin-slice contrast-enhanced CT scans from AbdomenAtlas [42] and our in-house collection from Peking University Third Hospital. |
| A | [ShapeKit](https://arxiv.org/abs/2506.24003) | 2025 | We used a subset of the JHH dataset [28,34] (denoted as Dataset A) and a subset of AbdomenAtlasPro [20,3,19] (denoted as Dataset B) to evaluate the ShapeKit pipeline. |
| B | [Touchstone Benchmark: Are We on the Right Way for Evaluating AI Algorithms for Medical Segmentation?](https://doi.org/10.48550/arXiv.2411.03670) | 2024 | However, due to the growing need for more annotated data in the medical domain, even MSD/BTCV test sets have been annotated and integrated into recent public datasets, like FLARE [53, 54, 56] and AbdomenAtlas [60, 44, 43]. |
| B | [VIBESegmentator: full body MRI segmentation for the NAKO and UK Biobank.](https://doi.org/10.1007/s00330-025-12035-9) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Text-Driven Tumor Synthesis.](https://doi.org/10.1109/tmi.2026.3658596) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [State of abdominal CT datasets: A critical review of bias, clinical relevance, and real-world applicability.](https://doi.org/10.1371/journal.pdig.0001567) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Primus: Enforcing Attention Usage for 3D Medical Image Segmentation](https://doi.org/10.48550/arXiv.2503.01835) | 2025 | More recently the TotalSegmentator dataset [77], AbdomenAtlas [43, 59], FLARE 2023 [53] and multi-dataset training [73] have taken a step in the right direction, tackling the data-sparsity that plagues the medical image domain. |

25 more candidate(s) in the CSV.

### M08 — FLARE21

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *Fast and Low-GPU-memory abdomen CT organ segmentation: The FLARE challenge* (202 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/23cec82d60dab39f3fef87bad564adca54e365e9>
- OpenAlex works citing *Fast and Low-GPU-memory abdomen CT organ segmentation: The FLARE challenge* (163): <https://openalex.org/works?filter=cites:W4294605033>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22FLARE21%22%20OR%20%22FLARE%202021%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22FLARE21%22%20OR%20%22FLARE%202021%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Efficient automatic segmentation for multi-level pulmonary arteries: The PARSE challenge](https://doi.org/10.48550/arXiv.2304.03708) | 2023 | Therefore, motivated by FLARE challenge(Ma et al., 2022), we adopted accuracy-oriented and e ffi ciency-oriented evaluation metrics. |
| A | [GeoLS: Geodesic Label Smoothing for Image Segmentation](https://www.semanticscholar.org/paper/20b9fffa3a53b1440f40788f0b7cb416f4bc210f) | 2023 | To validate our GeoLS, we use two publicly available benchmarks: a) the Brain Tumour Segmentation dataset from the BraTS 2019 challenge (Bakas et al., 2017, 2018) and b) the abdomen multi-organ segmentation dataset from the FLARE challenge (Ma et al., 2022). |
| A | [Revisiting nnU-Net for Iterative Pseudo Labeling and Efficient Sliding Window Inference](https://doi.org/10.1007/978-3-031-23911-3_16) | 2022 | We summarized the main efficiency takeoffs from the winning methods in FLARE21: (1) use a small model and low-resolution images; (2) input whole volume image and use two-stage segmentation. |
| A | [Medical Image Analysis](https://www.semanticscholar.org/paper/d6a9029c028272612cbbd2d72f4db0403a7d9749) |  | The performance of our method is validated on two publicly available benchmarks: (a) the left atrium (LA) binary segmentation dataset from the 2018 atrial challenge (Xiong et al., 2021), and (b) the abdominal multi-organ segmentation dataset from the FLARE cha… |
| A | [MIS-HCC: Hierarchical Channel Clustering for Efficient Medical Image Segmentation](https://doi.org/10.48550/arXiv.2607.17329) | 2026 | For 3D segmentation, we conduct experiments on the MICCAI FLARE 2021 [63] dataset using the Med-SAM2 [64] For performance evaluation, we adopt Dice coefficient and Intersection over Union (IoU) metrics to assess both 2D and 3D segmentation performance. |
| A | [GSToken: Geometry-Structured Gaussian Tokens for Compact 3D Medical Image Representation](https://arxiv.org/abs/2608.17425) | 2026 | It consistently outperforms the evaluated Transformer-based methods on the FLARE2021 [21], FeTA2021 [22], and AMOS2022 [23] datasets. |
| A | [VoxShield: Protecting 3D Medical Datasets from Unauthorized Training via Frequency-Aware Inter-Slice Disruption](https://doi.org/10.48550/arXiv.2605.17345) | 2026 | We evaluated the protection effectiveness of VoxShield on two 3D MIS datasets: BraTS19 [15] (brain tumor MRI) and FLARE21 [14] (abdominal (5) TAP [7]; (6) PUE [21]; (7) UMed [12]. |
| A | [BENet: a boundary-enhanced network for medical image segmentation](https://doi.org/10.1117/12.3115706) | 2026 | Experiments were conducted on two public CT datasets, FLARE21 [2] and LiTS17 [15] . |
| A | [Volumetric Axial Disentanglement Enabling Advancing in Medical Image Segmentation](https://doi.org/10.24963/ijcai.2025/134) | 2025 | To substantiate the efficacy of our method, we conducted experiments across three publicly available datasets: FLARE2021 [Ma et al. , 2022] , OIMHS [ Ye et al. , 2023 ] , and SegTHOR [ Lambert et al. , 2020]. |
| A | [Drl-Stnet⁺⁺ Uncertainty-Aware Self-Training For Cross-Modality Segmentation With Generative Translation](https://doi.org/10.1109/ICIPW68931.2025.11386045) | 2025 | We conduct our experiments on the FLARE 2024 Task 3 dataset 1 [12]. |
| A | [Good Enough? An Investigation on the Impact of Label Quality in Large-Scale Medical Datasets](https://arxiv.org/abs/2505.20928) | 2025 | We now turn towards the scenario of pre-training models on the generated noisy dataset before fine-tuning them on one of two different clean target datasets: SegThor [11] and Flare [17]. |
| A | [MMedAgent: Learning to Use Medical Tools with Multi-modal Agent](https://doi.org/10.48550/arXiv.2407.02483) | 2024 | Our first step is to collect multiple medical image segmentation datasets, including FLARE2021 (Ma et al., 2022), WORD (Luo et al., 2022), BRATS (Menze et al., 2015), Montgomery County X-ray Set (MC) (Jaeger et al., 2014; Candemir et al., 2014), VinDr-CXR (Ngu… |

47 more candidate(s) in the CSV.

### M09 — FLARE22

> The FLARE22 summary paper is in The Lancet Digital Health (2024; arXiv:2308.05862).

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *Unleashing the Strengths of Unlabeled Data in Pan-cancer Abdominal Organ Quantification: the FLARE22 Challenge* (92 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/1b27c5c5d5e0a26234da8cc4284471d0c543b855>
- OpenAlex works citing *Unleashing the Strengths of Unlabeled Data in Pan-cancer Abdominal Organ Quantification: the FLARE22 Challenge* (19): <https://openalex.org/works?filter=cites:W4385825439>
- DataCite Commons, works citing the dataset DOI `10.5281/zenodo.7860267`: <https://commons.datacite.org/doi.org/10.5281/zenodo.7860267>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22FLARE22%22%20OR%20%22FLARE%202022%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22FLARE22%22%20OR%20%22FLARE%202022%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [STU-Net: Scalable and Transferable Medical Image Segmentation Models Empowered by Large-Scale Supervised Pre-training](https://doi.org/10.48550/arXiv.2304.06716) | 2023 | We ﬁne-tune the pre-trained STU-Net with different scales on three downstream datasets that contain novel anatomical structures, modalities and domains: AutoPET22 [11] (with lesions and PET modality), AMOS22 [19] (with MR modality), and FLARE22 [28] (with mult… |
| A | [Multimodal foundation model for 3D genito-pelvic structure segmentation in image-guided radiotherapy](https://doi.org/10.1117/12.3087514) | 2026 | In the first stage, self-supervised pretraining is performed on a large collection of CT datasets, including FLARE22[21], HNSCC[22], RibFrac[23], ACRIN 6664[22], and TCIA COVID[24], allowing the model to learn foundational anatomical representations without re… |
| A | [OpenVocabCT: Towards Universal Text-driven CT Image Segmentation](https://doi.org/10.1109/TMI.2025.3646046) | 2025 | We also evaluate the segmentation model’s generalization capabilities on the FLARE22 [47] and SegTHOR [48] datasets. |
| A | [RoMedFormer: A Rotary-Embedding Transformer Foundation Model for 3D Genito-Pelvic Structure Segmentation in MRI and CT](https://doi.org/10.48550/arXiv.2503.14304) | 2025 | In the first stage, self-supervised pretraining is performed on a large collection of CT datasets, including FLARE22 [22], HNSCC [23], RibFrac [24], ACRIN 6664[25], and TCIA COVID [26], allowing the model to learn foundational anatomical representations withou… |
| A | [Lifting Wavelet Transform-Based Network for Liver Segmentation in CT Scans](https://doi.org/10.1109/BIBM66473.2025.11356169) | 2025 | Datasets: To evaluate the effectiveness of the proposed method, experiments were conducted on two publicly available liver segmentation datasets: LiTS17 [18] and FLARE22 [19]. |
| A | [CAT: Coordinating Anatomical-Textual Prompts for Multi-Organ and Tumor Segmentation](https://doi.org/10.48550/arXiv.2406.07085) | 2024 | For evaluating the accuracy of organ segmentation, we employ FLARE22 [60] as the external test set. |
| A | [AnatoMask: Enhancing Medical Image Segmentation with Reconstruction-guided Self-masking](https://doi.org/10.48550/arXiv.2407.06468) | 2024 | We adopt a previous SOTA architecture STU-Net [20] and evaluate the pretraining efficacy by finetuning on TotalSegmenta-tor [40], FLARE22 [26], AMOS22 [22] and AutoPETII [11]. |
| A | [MLLA-UNet: Mamba-like Linear Attention in an Efficient U-Shape Model for Medical Image Segmentation](https://doi.org/10.48550/arXiv.2410.23738) | 2024 | Our experiments leveraged six diverse medical image segmentation datasets: FLARE22 [40] (13 abdominal organs, CT, 50 labeled cases), AMOS22 [26] (15 abdominal organs, CT and MRI, 500 CT and 100 MRI scans), ATLAS23 [50] (liver and liver tumor, T1 CE-MRI, 60 tra… |
| A | [Anatomical Positional Embeddings](https://doi.org/10.1007/978-3-031-72117-5_7) | 2024 | To evaluate APE and baselines, we use the labeled part of FLARE2022 [7]. |
| A | [TG-LMM: Enhancing Medical Image Segmentation Accuracy through Text-Guided Large Multi-Modal Model](https://doi.org/10.48550/arXiv.2409.03412) | 2024 | We used data from the FLARE(Ma et al., 2023), SegTHOR(T. |
| A | [Class-wise restructured knowledge distillation for medical image segmentation](https://doi.org/10.1117/12.3035297) | 2024 | We validated our method on two public datasets: Synapse [6] and Flare2022 [7] . |
| B | [Robust and Label-Efficient Adrenal Gland Segmentation in Abdominal CT](https://doi.org/10.1109/PAEE71887.2026.11660675) | 2026 | Large abdominal multi organ benchmarks such as AMOS22 [1], BTCV [2], FLARE22 [3], and WORD [4] have driven progress in CT segmentation, but they are scored as an average over many organs at once, so small structures are easily lost in that average and their in… |

70 more candidate(s) in the CSV.

### M10 — FLARE23

**Where to find every paper that cites or uses it:**

- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22FLARE23%22%20OR%20%22FLARE%202023%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22FLARE23%22%20OR%20%22FLARE%202023%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [FreeTumor: Advance Tumor Segmentation via Large-Scale Tumor Synthesis](https://doi.org/10.48550/arXiv.2406.01264) | 2024 | Thanks to the previous efforts, we can collect large-scale CT datasets with organ labels, i.e. , CHAOS [30], Pancreas-CT [55], BTCV [34], Amos22 [26], WORD [41], Flare22 [44], Abdomenct-1k [43], AbdomenAtlas [50], and Flare23 [44]. |
| A | [Conformal Risk Control for Semantic Uncertainty Quantification in Computed Tomography](https://doi.org/10.48550/arXiv.2503.00136) | 2025 | We evaluate our method on quantile regression for CT denoising and a simple FBP-UNet reconstruction pipeline using two real-world datasets: TotalSegmentator [30] and FLARE23 [18]. |
| B | [Automatic Organ and Pan-cancer Segmentation in Abdomen CT: the FLARE 2023 Challenge](https://doi.org/10.48550/arXiv.2408.12534) | 2024 | Title/abstract: Organ and cancer segmentation in abdomen Computed Tomography (CT) scans is the prerequisite for precise cancer diagnosis and treatment. Most existing benchmarks and algorithms are tailored to specific cancer types, limiting their ability to pro… |
| B | [State of abdominal CT datasets: A critical review of bias, clinical relevance, and real-world applicability.](https://doi.org/10.1371/journal.pdig.0001567) | 2026 | Europe PMC: named in Methods |
| B | [Local ancestry-informed GWAS of warfarin dose requirement in African Americans identifies a CYP2C19 splicing QTL.](https://doi.org/10.1016/j.ajhg.2025.09.006) | 2025 | Europe PMC: named in Methods |
| B | [A multi-stage training and deep supervision based segmentation approach for 3D abdominal multi-organ segmentation](https://doi.org/10.1177/08953996251355806) | 2025 | Experimental data are derived from the FLARE 2023 Challenge that is an extension of FLARE 2021 – 2022, 33,34 aiming at advancing foundational models for abdominal disease analysis. |
| B | [Fast, Low-resource, and Accurate Organ and Pan-cancer Segmentation in Abdomen CT: MICCAI Challenge, FLARE 2023, Held in Conjunction with MICCAI 2023, Vancouver, BC, Canada, October 8, 2023, Proceedings](https://doi.org/10.1007/978-3-031-58776-4) | 2024 | Title/abstract: Fast, Low-resource, and Accurate Organ and Pan-cancer Segmentation in Abdomen CT: MICCAI Challenge, FLARE 2023, Held in Conjunction with MICCAI 2023, Vancouver, BC, Canada, October 8, 2023, Proceedings |
| B | [Prediction of fetal loss in Chinese pregnant patients with systemic lupus erythematosus: a retrospective cohort study.](https://doi.org/10.1136/bmjopen-2018-023849) | 2019 | Europe PMC: named in Methods |

18 more candidate(s) in the CSV.

### M11 — AbdomenAtlas 3.0 / RadGPT

> RadGPT/AbdomenAtlas 3.0 is both a report-generation method and a dataset. Confirm that the data were used.

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *RadGPT: Constructing 3D Image-Text Tumor Datasets* (46 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/6d3cac0ebcdf869fd83da0ca58391b9c60b10a9f>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22AbdomenAtlas%203.0%22%20OR%20%22RadGPT%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22AbdomenAtlas%203.0%22%20OR%20%22RadGPT%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Photon: Speedup Volume Understanding with Efficient Multimodal Large Language Models](https://doi.org/10.48550/arXiv.2603.25155) | 2026 | …pairs of CT-RATE (we use 47,141 out of 50,188 pairs, reconstructed from 25,692 volumes belonging to 21,304 patients for training) (Hamamci et al., 2024b), AbdomenAtlas 3.0 (we use 8,334 out of 9,262 pairs for training) (Li et al., 2024a), and our internal dat… |
| A | [U-VLM: Hierarchical Vision Language Modeling for Report Generation](https://doi.org/10.48550/arXiv.2603.00479) | 2026 | To validate U-VLM, we train on CT-RATE [10] (25,692 chest CTs) and AbdomenAtlas 3.0 [3] (9,262 abdominal CTs). |
| A | [RadSight: Towards Perceptually Reliable Multimodal Radiology Image Understanding](https://doi.org/10.48550/arXiv.2607.22293) | 2026 | For 3D CT, we use report-associated data from CT-RATE (Hamamci et al., 2024b), Merlin (Blankemeier et al., 2024b), INSPECT (Huang et al., 2023), AMOS-MM (Ji et al., 2022a), and AbdomenAtlas 3.0 (Bassi et al., 2025), together with additional low-dose CT volumes… |
| A | [Large-Scale Multi-Cancer Detection by Learning Segmentation from Reports](https://doi.org/10.21203/rs.3.rs-10131590/v1) | 2026 | To create these organ masks, we used an organ segmentation model, an nnU-Net [37] trained in AbdomenAtlas [10] (made public). |
| A | [GLeVE: Graph-Guided Lesion Grounding with Proposal Verification in 3D CT](https://doi.org/10.48550/arXiv.2605.22619) | 2026 | We conduct experiments on AbdomenAtlas 3.0 [6], comprising 9,262 cases across 138 institutions. |
| A | [Learning Segmentation from Radiology Reports](https://doi.org/10.48550/arXiv.2507.05582) | 2025 | We trained R-Super using the UCSF-Train reports, in addition to few (50), medium (344) or many (1.7K) tumor segmentation masks (sourced from AbdomenAtlas 2.0 [3]). |
| A | [ShapeKit](https://arxiv.org/abs/2506.24003) | 2025 | We used a subset of the JHH dataset [28,34] (denoted as Dataset A) and a subset of AbdomenAtlasPro [20,3,19] (denoted as Dataset B) to evaluate the ShapeKit pipeline. |
| B | [PHASOR: Anatomy- and Phase-Consistent Volumetric Diffusion for CT Virtual Contrast Enhancement](https://doi.org/10.48550/arXiv.2604.01053) | 2026 | First, to bridge the domain gap between video and CT images, we initialize the DiT from WAN 2.1 and perform warm-up pretraining on the AbdomenAtlas 3.0 [39] dataset for 50 epochs, with the VAE encoder and decoder, as well as the T5 text encoder frozen. |
| B | [RadGPT: A System Based on a Large Language Model That Generates Sets of Patient-Centered Materials to Explain Radiology Report Information.](https://doi.org/10.1016/j.jacr.2025.06.013) | 2025 | Europe PMC: named in Methods |
| B | [Visual-language artificial intelligence system for knee radiograph diagnosis and interpretation: a collaborative system with humans.](https://doi.org/10.1093/radadv/umaf027) | 2025 | Europe PMC: named in Methods |
| B | [A generalist vision-language foundation model for diverse biomedical tasks.](https://doi.org/10.1038/s41591-024-03185-2) | 2024 | Europe PMC: named in Methods |

1 more candidate(s) in the CSV.

### M12 — AMOS-MM

**Where to find every paper that cites or uses it:**

- DataCite Commons, works citing the dataset DOI `10.5281/zenodo.10992155`: <https://commons.datacite.org/doi.org/10.5281/zenodo.10992155>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22AMOS-MM%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22AMOS-MM%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [RadSight: Towards Perceptually Reliable Multimodal Radiology Image Understanding](https://doi.org/10.48550/arXiv.2607.22293) | 2026 | For 3D CT, we use report-associated data from CT-RATE (Hamamci et al., 2024b), Merlin (Blankemeier et al., 2024b), INSPECT (Huang et al., 2023), AMOS-MM (Ji et al., 2022a), and AbdomenAtlas 3.0 (Bassi et al., 2025), together with additional low-dose CT volumes… |
| A | [Regulating Anatomy-Aware Rewards via Trajectory-Integral Feedback for Volumetric Computed Tomography Analysis](https://doi.org/10.48550/arXiv.2605.20277) | 2026 | We evaluate our method on two public multimodal CT datasets: CT-RATE (Hamamci et al., 2024c) and AMOS-MM (Ji et al., 2022). |
| A | [A Vision-language Framework for Comparative Reasoning in Radiology](https://doi.org/10.48550/arXiv.2606.06407) | 2026 | For internal validation, we used four public datasets (MIMIC-CXR [25], CT-RATE [15], AMOS-MM [22], and CURG [28]), following their official train-test splits, along with an in-house brain MRI dataset [26] split 9:1 for training and testing. |
| A | [MedPruner: Training-Free Hierarchical Token Pruning for Efficient 3D Medical Image Understanding in Vision-Language Models](https://doi.org/10.48550/arXiv.2603.11625) | 2026 | In our experiments, we evaluate our approach on three 3D medical benchmarks: M3D [2], 3D-RAD [7], and AMOS-MM [10]. |
| A | [LEAVS: An LLM-based Labeler for Abdominal CT Supervision](https://doi.org/10.48550/arXiv.2503.13330) | 2025 | To test our labeler, we annotated 200 reports from the validation set of AMOS-MM [12], a public dataset of abdominal CT volumes and reports with unspecified license. |
| A | [Exploring the Design Space of 3D MLLMs for CT Report Generation](https://doi.org/10.48550/arXiv.2506.21535) | 2025 | All the experiments are conducted using the MICCAI24 AMOS-MM challenge 8 , originally from the AMOS dataset [10], which includes 1287 and 400 cases for training and validation. |
| A | [Radiologist Copilot: An Agentic Framework Orchestrating Specialized Tools for Reliable Radiology Reporting](https://arxiv.org/abs/2512.02814) | 2025 | We utilize the publicly available 3D CT dataset AMOS-MM [9] and its medical report generation task, which contains 1,287 training cases and 400 validation cases. |
| A | [ViT3D Alignment of LLaMA3: 3D Medical Image Report Generation](https://doi.org/10.48550/arXiv.2410.08588) | 2024 | In this work, we propose a novel method for MICCAI2024 AMOS-MM Challenge [4] about automatic MRG using a multimodal large language model. |
| B | [ReportQA: QA-Based Radiology Report Evaluation](https://doi.org/10.48550/arXiv.2606.15037) | 2026 | 5 shows relatively competitive results, while Hulu-Med [25] performs best among medical VLMs. CT-CHAT [17], which is specifically trained for chest CT, demonstrates strong performance on the chest CT dataset CT-RATE [17], as well as on AMOS-MM [20], which part… |
| B | [Large multimodal models evaluation: a survey](https://doi.org/10.1007/s11432-025-4676-4) | 2025 | Benchmarks like AMOS-MM [280], RP3D-DiagDS [281], and PubMedQA [272], although focus on diagnostic or domain-speciﬁc question-answering tasks, typically employ relatively simple modalities with insuﬃcient ﬁdelity to real clinical scenarios. |
| B | [Radiologist Copilot: An Agentic Assistant with Orchestrated Tools for Radiology Reporting with Quality Control](https://doi.org/10.48550/arXiv.2512.02814) | 2025 | We utilize the publicly available 3D CT dataset AMOS-MM [9] and its medical report generation task, which includes more than 2,000 CT scans with comprehensive radiology reports. |

5 more candidate(s) in the CSV.

### M13 — SA-Med3D-140K

> The SAM-Med3D paper introduces both a model and the SA-Med3D-140K data. Only sentences naming the data are kept; many papers only compare against the SAM-Med3D model.

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *SAM-Med3D: Towards General-Purpose Segmentation Models for Volumetric Medical Images* (204 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/fa5249099d638317f8b659ddb39ee13afaea4d44>
- OpenAlex works citing *SAM-Med3D: Towards General-purpose Segmentation Models for Volumetric Medical Images* (11): <https://openalex.org/works?filter=cites:W4387929840>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22SA-Med3D-140K%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22SA-Med3D%22%20OR%20%22SAM-Med3D%22%29>
- Hugging Face dataset page: <https://huggingface.co/datasets/blueyo0/SA-Med3D-140K>

_No strong or probable candidates were found automatically. Use the citation pages above._

### M14 — ULS23

> Includes the 34 Semantic Scholar citations of the ULS23 challenge paper. Only papers using its kidney-lesion or KiTS21-derived component matter here.

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *The ULS23 Challenge: a Baseline Model and Benchmark Dataset for 3D Universal Lesion Segmentation in Computed Tomography* (34 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/738f25d09b24872aa4dfd5bba77836a47838517c>
- OpenAlex works citing *The ULS23 challenge: A baseline model and benchmark dataset for 3D universal lesion segmentation in computed tomography* (19): <https://openalex.org/works?filter=cites:W4408108565>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22ULS23%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22ULS23%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [RAPS-3D: Efficient interactive segmentation for 3D radiological imaging](https://doi.org/10.48550/arXiv.2507.07730) | 2025 | Our training dataset comprised 12,628 CT scans sourced from publicly available datasets: Abdom-enAtlas [10], TotalSegmentator v1 [12], KiTS23 [4], MSD [1] (specifically Liver, Lung, Pancreas, and Colon), and the ULS23 challenge datasets [3]. |
| B | [U‐VQVAE‐CTLesionNet: A Generalized Deep Learning Framework for Multi‐Organ Lesion Detection and Segmentation in Medical Imaging](https://doi.org/10.1111/coin.70168) | 2026 | In addition, the ULS23 benchmark offers quite minimal database segmentation of lesions in abdominal, thoracic, and pelvic CT images into 3D CT volumes for investigating more general ignition foundation [16]. |
| B | [DPMT-Net: a dual-prompt attention multi-task 3D network for joint nodule segmentation and malignancy prediction in lung CT scans](https://doi.org/10.1007/s40747-026-02337-w) | 2026 | In the next year, De Grauw et al. [42] utilized introduced the ULS23 benchmark for 3D universal lesion segmentation in chest-abdomen-pelvis CT examinations. |
| B | [3DLAND: 3D Lesion Abdominal Anomaly Localization Dataset](https://doi.org/10.48550/arXiv.2602.12820) | 2026 | More recent efforts, such as the ULS23 challenge (de Grauw et al., 2025), advance 3D lesion segmentation by providing a universal benchmark. |
| B | [Text Embedded Swin-UMamba for DeepLesion Segmentation](https://doi.org/10.1117/12.3086299) | 2025 | The ULS23 DeepLesion dataset 17 was utilized as validated labels were available in this dataset. |
| B | [Unstable Prompts, Unreliable Segmentations: A Challenge for Longitudinal Lesion Analysis](https://doi.org/10.48550/arXiv.2507.19230) | 2025 | This paper presents an in-depth evaluation of the baseline model from the ULS23 challenge on longitudinal CT scans with annotated metastases [3]. |

41 more candidate(s) in the CSV.

### M15 — 3DLAND

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *3DLAND: 3D Lesion Abdominal Anomaly Localization Dataset* (0 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/0bba6a14521fca26135d2d40e8513bcacf2c852d>
- OpenAlex works citing *3DLAND: 3D Lesion Abdominal Anomaly Localization Dataset* (0): <https://openalex.org/works?filter=cites:W7129024326>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%223DLAND%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%223DLAND%22%29>

_No strong or probable candidates were found automatically. Use the citation pages above._

### M16 — DeepLesion

> DeepLesion is body-wide. Only papers that use or report the kidney lesions matter for this atlas.

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *DeepLesion: automated mining of large-scale lesion annotations and universal lesion detection with deep learning* (583 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/98a68e8148d380120924d5c2810e3e0f513a75b2>
- OpenAlex works citing *DeepLesion: automated mining of large-scale lesion annotations and universal lesion detection with deep learning* (587): <https://openalex.org/works?filter=cites:W2883683269>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22DeepLesion%22%20kidney>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22DeepLesion%22%20AND%20%28kidney%20OR%20renal%29%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Universal CT Representations from Anatomy to Disease Phenotype through Agglomerative Pretraining](https://doi.org/10.48550/arXiv.2605.21906) | 2026 | We evaluated FlexiCT-2D as a frozen feature extractor for cancer and disease classification on KiTS Heller et al. [2023], DeepLesion Yan et al. [2018], LUNA16 Setio et al. [2017], and COVIDx-CT Gunraj et al. [2022], following the Curia evaluation protocol Danc… |
| A | [MedRoute: RL-Based Dynamic Specialist Routing in Multi-Agent Medical Diagnosis](https://doi.org/10.48550/arXiv.2604.06180) | 2026 | We also evaluate on image-text multimodal medical datasets (PMC-VQA (Zhang et al., 2024b), DeepLesion (Yan et al., 2018) and PathVQA (He et al., 2020)). |
| A | [3DLAND: 3D Lesion Abdominal Anomaly Localization Dataset](https://doi.org/10.48550/arXiv.2602.12820) | 2026 | We compared three approaches: (1) manual 3D masks by clinicians, (2) semi-automated masks generated via MedSAM2 (Ma et al., 2025) propagation from expert-drawn 2D slices, and (3) fully automated 3D masks from our pipeline using MedSAM2 with DeepLesion slice ra… |
| A | [LiMT: A Multi-Task Liver Image Benchmark Dataset](https://doi.org/10.1109/JBHI.2025.3637798) | 2025 | Other studies [6], [14], [15] evaluated detection methods on the DeepLesion dataset [16]. |
| A | [Depth-Aware Networks for Multi-Organ Lesion Detection in Chest CT Scans](https://doi.org/10.3390/bioengineering11100998) | 2024 | We have evaluated the proposed method on the publicly-available DeepLesion dataset [22], which contains 32,735 lesions from 32,120 axial CT slices from 10,594 CT scan studies of a total of 4427 patients. |
| A | [Non-Invasive Assessment of Lung Water Content Using Chest Patch RF Sensors: A Computer Study Using NIH Patients CT Scan Database and AI Classification Algorithms](https://doi.org/10.1109/ACCESS.2023.3238969) | 2023 | We use the pixel to mm conversion provided by DeepLesion to ensure the correct sizes of our lung model. |
| A | [Confidence-Aware and Self-Supervised Image Anomaly Localisation](https://doi.org/10.48550/arXiv.2303.13227) | 2023 | Note that the models are trained on healthy tissue of ill patients for the datasets LIDC-IDRI and DeepLesion, which is different to the dataset JSRT for which we only differentiate between ill and healthy patients/samples. |
| A | [DiffULD: Diffusive Universal Lesion Detection](https://doi.org/10.1007/978-3-031-43904-9_10) | 2023 | To validate the effectiveness of our method, we conduct experiments against seven state-of-the-art ULD methods on the public dataset DeepLesion [1]. |
| A | [RetinexFlow for CT metal artifact reduction](https://doi.org/10.48550/arXiv.2306.10520) | 2023 | Notice that all the deep-learning-based methods are trained on the DeepLesion [42] dataset, not the clinical data "CT pelvic1K dataset [24]". |
| A | [Super-Resolution Swin Transformer and Attention Network for Medical CT Imaging](https://doi.org/10.1155/2022/4431536) | 2022 | We used the largest medical CT medical image dataset, DeepLesion [36], for training and testing the model. |
| A | [An Efficient Anchor-Free Universal Lesion Detection in Ct-Scans](https://doi.org/10.1109/ISBI52829.2022.9761698) | 2022 | Dataset and Metric: All the experiments are performed on standard DeepLesion 1 dataset consisting of 32, 735 lesions bounding-box instances on 32, 120 axial key CT slices of 4, 427 unique patients [9]. |
| A | [DKMA-ULD: Domain Knowledge augmented Multi-head Attention based Robust Universal Lesion Detection](https://doi.org/10.48550/arXiv.2203.06886) | 2022 | 90% by training on 4 heterogeneous datasets, namely LUNA [20], LiTS [4], NIH-Lymph [1] and DeepLesion [33]. |

214 more candidate(s) in the CSV.

### M17 — M3D-Data

> The M3D paper introduces both a model (M3D-LaMed) and the M3D-Data sets. Only sentences naming the data components are kept.

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *M3D: Advancing 3D Medical Image Analysis with Multi-Modal Large Language Models* (193 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/2af15dd679b9c3c91030e2bf2047abbca0194d94>
- OpenAlex works citing *M3D: Advancing 3D Medical Image Analysis with Multi-Modal Large Language Models* (18): <https://openalex.org/works?filter=cites:W4393904064>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22M3D-Seg%22%20OR%20%22M3D-Cap%22%20OR%20%22M3D-VQA%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22M3D-Cap%22%20OR%20%22M3D-VQA%22%20OR%20%22M3D-Seg%22%20OR%20%22M3D-Data%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [OmniCT: Towards a Unified Slice-Volume LVLM for Comprehensive CT Analysis](https://doi.org/10.48550/arXiv.2602.16110) | 2026 | As shown in Figure 4 (b), even though M3D-CLIP (Bai et al., 2024) is pretrained with contrastive learning on the M3D dataset, it does not exhibit a clear advantage over 2D encoders such as DINOv3 (245 tokens) (Sim ´ eoni et al., 2025) and SigLIP (405 tokens) (… |
| A | [A data-efficient 3D medical vision-language model using only a 2D encoder](https://doi.org/10.1038/s41598-026-39526-z) | 2026 | To ensure fairness in our experiments and to facilitate comparison with existing studies, we adopt two subsets of the M3D-Data dataset 4 , as used in previous research: • M3D-Cap : This subset consists of image-text pairs for medical report generation. |
| A | [MedVol-R1: Reward-Driven Evidence Grounding for Volumetric Reasoning Segmentation](https://doi.org/10.48550/arXiv.2605.26621) | 2026 | Datasets and Evaluation Metrics We evaluate our framework on three CT sub-datasets from the M3D-Seg [1] benchmark: CT-ORG, AbdomenCT-1K, and KiTS23. |
| A | [UMIT: Unifying Medical Imaging Tasks via Vision-Language Models](https://doi.org/10.48550/arXiv.2503.15892) | 2025 | For medical report generation, we collect chest X-ray images IU-Xray [6], CT images from M3D-Cap [2], and clinical photos from PEIR GROSS [23]. |
| A | [Feature Decomposition via Shared Low-Rank Matrix Recovery for CT Report Generation](https://doi.org/10.1109/TMI.2025.3628159) | 2025 | In this work, we use the M3D-Cap 1 [10] and CT-RATE [62] datasets to evaluate our approach, with their detailed statistics provided in Table I. |
| A | [Recurrent Visual Feature Extraction and Stereo Attentions for CT Report Generation](https://doi.org/10.1109/BIBM66473.2025.11356692) | 2025 | In our experiments, we utilize the M3D-Cap [15] dataset, which focuses on CT scans of various body parts, including the chest, abdomen, and pelvis. |
| A | [VELVET-Med: Vision and Efficient Language Pre-training for Volumetric Imaging Tasks in Medicine](https://doi.org/10.48550/arXiv.2508.12108) | 2025 | We adopt three baseline models for the retrieval task: PMC-CLIP [67] (2D model), the M3D retrieval model [15] trained on the full M3D-CAP dataset, and our own implementation of [15], called as CLIP-3D, pre-trained on M3D-CAP-filtered. |
| A | [Rad-JEPA 3D: Radiology Joint-Embedding Predictive Model for 3D Computed Tomography](https://doi.org/10.48550/arXiv.2607.26196) | 2026 | Rad-JEPA 3D is trained on the publicly available M3D dataset [Bai et al., 2024], collected with informed consent and ethical approval by the original work. |
| A | [Venice-H1: Failure-Aware Query Re-Ranking with Multi-Scale Grid Signatures for Referring Image Segmentation](https://doi.org/10.48550/arXiv.2606.22546) | 2026 | To assess generality, we evaluate Venice-H1’s zero-shot transfer to two medical referring segmentation benchmarks: (1) MS-CXR [3] (1,000 chest X-rays) and (2) M3D-RefSeg-2D [7] (2,010 3D medical slices). |
| A | [REAF: a Region-Enhanced Volume-Slice Hierarchical Attention Fusion Vision-Language Model for CT-Report Retrieval](https://doi.org/10.1109/ISBI61048.2026.11515779) | 2026 | …REAF against six SOTA models on volume-report cross retrieval tasks: 1) Merlin [9] that is a 3D VLM using EHR and report supervision, 2) M3D-CLIP [6] trained on the M3D-Data instruction dataset, 3) Med3DVLM [14], featuring an efficient DCFormer encoder and Si… |
| A | [MV-MambaNet: multiscale and multiview visual question answering network for 3D medical images](https://doi.org/10.1117/12.3095778) | 2025 | The experimental data set used in this paper is M3D-VQA, which is a subset of M3D-Data [19] . |
| A | [MedBLIP: Bootstrapping Language-Image Pre-training from 3D Medical Images and Texts](https://doi.org/10.48550/arXiv.2305.10799) | 2023 | …and text descriptions and also provides some reasons for making such decision; and (3) zero-shot close-ended VQA on AD-related disease in the M3D-VQA dataset [2], which applies our MedBLIP to select answers from a set of possible choices when presenting with … |

28 more candidate(s) in the CSV.

### G01 — UCSF RMaC

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *UCSF RMaC: University of California San Francisco 3D Multi-Phase Renal Mass CT Dataset with Tumor Segmentations* (1 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/47ad7afc62d86bdd1a8cf4aaf6d17b2ef71bf755>
- OpenAlex works citing *UCSF RMaC: University of California San Francisco 3D Multi-Phase Renal Mass CT Dataset with Tumor Segmentations* (0): <https://openalex.org/works?filter=cites:W7128742238>
- DataCite Commons, works citing the dataset DOI `10.58078/C2WC74`: <https://commons.datacite.org/doi.org/10.58078/C2WC74>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22UCSF%20RMaC%22%20OR%20%22UCSF-RMaC%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22UCSF-RMaC%22%20OR%20%22RMaC%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [PhaseDiff: Conditional Latent Diffusion for Multi-Phase Renal CT Synthesis](https://doi.org/10.23919/SpliTech70133.2026.11685485) | 2026 | We used the University of California, San Francisco 3D multi-phase renal mass CT dataset (UCSF RMaC) [3], [26], [27] which comprises 831 multi-phase 3D CT studies, each containing up to three contrast-enhanced phases. |

1 more candidate(s) in the CSV.

### G02 — CPTAC-CCRCC imaging

> The anchor is the proteogenomic Cell paper, which is mostly cited for genomics. Only imaging/pathology users belong here; sentences without an imaging term were moved to tier C.

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *Integrated Proteogenomic Characterization of Clear Cell Renal Cell Carcinoma* (651 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/bac20b777cb57af5cb5cd0c141170b406233df26>
- OpenAlex works citing *Integrated Proteogenomic Characterization of Clear Cell Renal Cell Carcinoma* (793): <https://openalex.org/works?filter=cites:W2982402173>
- DataCite Commons, works citing the dataset DOI `10.7937/K9/TCIA.2018.OBLAMN27`: <https://commons.datacite.org/doi.org/10.7937/K9/TCIA.2018.OBLAMN27>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22CPTAC-CCRCC%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%28%22CPTAC-CCRCC%22%20OR%20%22CPTAC%20ccRCC%22%20OR%20%22CPTAC-ccRCC%22%29%20AND%20%28%22whole%20slide%22%20OR%20%22whole-slide%22%20OR%20%22deep%20learning%22%20OR%20radiomics%29%29>
- TCIA publication list: <https://www.cancerimagingarchive.net/publications/>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [AI-driven multimodal algorithm predicts immunotherapy and targeted therapy outcomes in clear cell renal cell carcinoma](https://doi.org/10.1016/j.xcrm.2025.102299) | 2025 | Three experienced pathologists examined sarcomatoid and rhabdoid features for all cases from the CPTAC-ccRCC and TCGA-KIRC cohorts with available histological images. |
| A | [TAP-Path: Task-Adaptive Structural and Token Pruning for Efficient and Trustworthy Pathology Foundation Models](https://arxiv.org/abs/2609.04071) | 2026 | For independent external evaluation, we used 433 whole-slide images (WSIs) from the Clinical Proteomic Tumor Analysis Consortium (CPTAC), comprising 209 clear cell renal cell carcinoma (CCRCC) images [33] and 224 uterine corpus endometrial carcinoma (UCEC) ima… |
| B | [Integrated multi-omic profiling reveals macrophage-driven prognostic signatures in clear cell renal cell carcinoma through machine learning optimization](https://doi.org/10.3389/fimmu.2025.1612262) | 2026 | Abstract/title: Based on seven hub genes from the Mac-M2 module, RSF model was constructed, achieving robust prognostic performance and effectively stratifying patients into high- and low-risk groups (log-rank p < 0.0001) in both the TCGA and CPTAC cohorts. |
| B | [Practical guidelines for multiple instance learning in computational pathology: how embedding choice impacts overall survival prediction.](https://doi.org/10.3389/fbinf.2026.1809049) | 2026 | Abstract/title: We compare four representative tile embedding strategies (ResNet50, ProvGigaPath, UNI, and CONCH) across five The Cancer Genome Atlas (TCGA) cohorts: bladder urothelial carcinoma (BLCA), breast invasive carcinoma (BRCA), colon adenocarcinoma (C… |
| B | [Artificial intelligence empowers full-stack histopathological diagnosis and prognosis of renal cell tumor: a multi-center study with external validation.](https://doi.org/10.1186/s12916-026-05110-5) | 2026 | Cites the dataset DOI 10.7937/K9/TCIA.2018.OBLAMN27 (DataCite) |
| B | [A toolkit for generating virtual brightfield images of histological and immunohistochemical stains from multiplexed data with AI-based channel selection and image enhancement.](https://doi.org/10.3389/fbinf.2026.1765143) | 2026 | Cites the dataset DOI 10.7937/K9/TCIA.2018.OBLAMN27 (DataCite) |
| B | [Tumor morphology on CT radiomics is largely driven by the local anatomical environment, not the primary tumor type](https://doi.org/10.1186/s41747-026-00691-5) | 2026 | Cites the dataset DOI 10.7937/K9/TCIA.2018.OBLAMN27 (DataCite) |
| B | [MultiOmicsXplorer, a tool to browse, access and analyse multi-omics data](https://doi.org/10.1186/s12859-026-06460-w) | 2026 | Abstract/title: The first, OncoXplorer, enables the systematic inference and comparison of protein activities from 1492 samples corresponding to approximately 1000 patients across ten cancer types, leveraging harmonized datasets from the CPTAC portal to provid… |
| B | [Retroelement Hypomethylation Links Hypoxia Signaling, Immune Phenotypes, and Survival in Clear Cell Renal Cell Carcinoma](https://doi.org/10.64898/2026.05.01.722263) | 2026 | Abstract/title: Key findings were then externally validated in CPTAC-ccRCC and independently replicated in an institutional Dartmouth Cancer Center (DCC) cohort with matched methylation and RNA-sequencing data. |
| B | [The Deubiquitinating Enzyme USP9X Regulates the Protein Stability of the FAM49B in Clear Cell Renal Cell Carcinoma](https://doi.org/10.1021/acs.jproteome.6c00329) | 2026 | Abstract/title: Analysis of TCGA and CPTAC data sets revealed a significantly upregulated FAM49B protein in ccRCC tissues that positively correlated with pathological grade, while the mRNA level was unchanged. |
| B | [Pan‐Cancer Quantification of Driver Alteration Transmission Across Molecular Layers Reveals Limited Propagation to Protein Abundance](https://doi.org/10.1002/ijc.70657) | 2026 | Abstract/title: Applying this framework to matched genomic, transcriptomic, proteomic, and phosphoproteomic data from 754 Clinical Proteomic Tumor Analysis Consortium (CPTAC) tumors across seven cancer types, I analyzed 86 driver gene–cancer type pairs, of whi… |
| B | [Inflammatory reprogramming of the solid tumor microenvironment by infiltrating clonal hematopoiesis is associated with adverse outcomes](https://doi.org/10.1016/j.xcrm.2025.101989) | 2025 | Abstract/title: Here, we report the effects of CH on the tumor microenvironment (TME) using 1,550 treatment-naive patient samples from the Clinical Proteomics Tumor Analysis Consortium (CPTAC) cohort. |

70 more candidate(s) in the CSV.

### G03 — RCC-AID

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *Accessible and Reproducible Renal Cell Carcinoma Research Through Open-Sourcing Data and Annotations* (1 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/dfbb3d0bd7a89747202aa20f85efe9882d814433>
- OpenAlex works citing *RCC-AID: Renal Cell Carcinoma AI Dataset for Medical Imaging Research* (0): <https://openalex.org/works?filter=cites:W7155419210>
- OpenAlex works citing *RCC-AID: Renal Cell Carcinoma AI Dataset for Medical Imaging Research* (0): <https://openalex.org/works?filter=cites:W7164991237>
- DataCite Commons, works citing the dataset DOI `10.5281/zenodo.20719257`: <https://commons.datacite.org/doi.org/10.5281/zenodo.20719257>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22RCC-AID%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22RCC-AID%22%29>

_No strong or probable candidates were found automatically. Use the citation pages above._

### H01 — Open Kidney Ultrasound (kidneyUS)

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *The Open Kidney Ultrasound Data Set* (49 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/11d9b866b273c48fc56fc93e1f27bef9fddd5a19>
- OpenAlex works citing *The Open Kidney Ultrasound Data Set* (0): <https://openalex.org/works?filter=cites:W4282974564>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22Open%20Kidney%20Ultrasound%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22Open%20Kidney%20Ultrasound%22%20OR%20%22kidneyUS%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Comparative Analysis of Segmentation Architectures for Kidney Ultrasound Imaging](https://doi.org/10.1109/IICC69623.2026.11582510) | 2026 | This study investigates these questions by evaluating six architectures spanning three paradigms, under identical training conditions on the Open Kidney Ultrasound Dataset [17]. |
| A | [MLAU-Net: Deep supervised attention and hybrid loss strategies for enhanced segmentation of low-resolution kidney ultrasound](https://doi.org/10.1177/20552076241291306) | 2024 | In addition, through performing more evaluation on MLAU-Net using Open Kidney Dataset which is an open access dataset used to further con ﬁ rm its ability. |
| A | [Defining Robust Ultrasound Quality Metrics via an Ultrasound Foundation Model](https://arxiv.org/abs/2604.19512) | 2026 | Experimental Setup: We use thyroid and kidney ultrasound images for Dice-based segmentation evaluation, including thyroid nodule segmentation from DDTI [16] and kidney capsule segmentation from the Open Kidney Ultrasound Data Set [19]. |
| A | [A Segmentation Network with Two Distinct Attention Modules for the Segmentation of Multiple Renal Structures in Ultrasound Images](https://doi.org/10.3390/diagnostics15151978) | 2025 | In our experiments, we utilize the Open Kidney US Data Set (OKUD) [28] which comprises 534 ultrasound images along with their corresponding labels. |
| A | [SSL-CL-RUS - A Semi-Supervised Framework for Renal Ultrasound Segmentation in CKD: Combining Pseudo-Label Guided Contrastive Learning with ST++](https://doi.org/10.1109/EMBC58623.2025.11253499) | 2025 | To evaluate the generalization capability of the proposed SSL-CL framework, we conducted an external validation using the publicly available Open Kidney Dataset [11]. |
| B | [MK-Net: A Multi-Scale Semantic Propagation and Base-Channel Distillation Network for Multi-Class Kidney Ultrasound Segmentation](https://doi.org/10.1109/ISCAS66217.2026.11562078) | 2026 | The Open Kidney Ultrasound Dataset [5], which is the first publicly available high-quality B-mode kidney ultrasound dataset comprising of 514 2D images collected from over 500 adult patients between 2015 and 2019, will be studied. |
| B | [Task-Specific Knowledge Distillation from the Vision Foundation Model for Enhanced Medical Image Segmentation](https://doi.org/10.48550/arXiv.2503.06976) | 2025 | These datasets enable a robust evaluation of our method’s generalizability and effectiveness: • KidneyUS Dataset [45] |

45 more candidate(s) in the CSV.

### H03 — KiPA22

> Includes citations of the two papers the KiPA22 organizers ask users to cite (He et al., MedIA 2020 and 2021).

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *Boundary-Aware Network for Kidney Parsing* (5 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/5d498bad96a0a2b15c78aee97a90da254e353d4e>
- Semantic Scholar citations of *Meta grayscale adaptive network for 3D integrated renal structures segmentation* (65 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/089c41a83b6a12000f8606b8aebc746e58d7a44c>
- Semantic Scholar citations of *Dense biased networks with deep priori anatomy and hard region adaptation: Semi-supervised learning for fine renal artery segmentation* (73 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/f29ea3187a4b843c109f9d91f424d3e542cbe3f4>
- OpenAlex works citing *Boundary-Aware Network for Kidney Parsing* (0): <https://openalex.org/works?filter=cites:W4293830395>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22KiPA22%22%20OR%20%22KiPA%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22KiPA22%22%20OR%20%22KiPA%202022%22%20OR%20%22Kidney%20Parsing%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Triad: Vision Foundation Model for 3D Magnetic Resonance Imaging](https://doi.org/10.21203/rs.3.rs-6129856/v1) | 2025 | We evaluate Triad on 17 extensive 3D MRI and CT semantic segmentation datasets, including five MRI datasets for within-domain tasks: BraTS21[26], MSD[27]-BrainTumour, BreastDM[28], Prostate158[29], and MSD-Prostate; and 12 datasets covering different organs or… |
| A | [Vector Contrastive Learning for Pixel-Wise Pretraining in Medical Vision](https://doi.org/10.1109/ICCV51701.2025.01844) | 2025 | These pretrained models are fine-tuned on four tasks (SCR 25% S [68] (X-ray), PDCXR C [37] (X-ray), FIVES S [35] (fundus), KiPA22 2 DS [24] (CT)). b) 3D evaluation: It pretrained networks on 837 3D T1 brain MR images from the PPMI database [45]. |
| A | [MedVision: Benchmarking Quantitative Medical Image Analysis](https://arxiv.org/abs/2511.18676) | 2025 | We collected 22 datasets, summarized in Table 1, covering a diverse range of anatomies and modalities: AbdomenAtlas (Li et al., 2024b), AbdomenCT-1K (Ma et al., 2022), ACDC (Bernard et al., 2018), AMOS22 (Ji et al., 2022), autoPET-III 1 , BCV15 2 , BraTS24 (de… |
| A | [MBD-Net: Multi-Branch Dilated Convolutional Network With Cyst Discriminator for Renal Multi-Structure Segmentation](https://doi.org/10.1109/EMBC40787.2023.10341054) | 2023 | Dataset : Our experiments are conducted on the 2022 Kidney Parsing for Renal Cancer Treatment Challenge (KiPA2022) dataset [8], which contains abdominal CTA images from 70 patients who have a tumor in their unilateral kidney. |
| A | [COMMA: Coordinate-Aware Modulated Mamba Network for 3D Dispersed Vessel Segmentation](https://doi.org/10.1109/TIP.2026.3682121) | 2025 | Six vessel segmentation datasets are used for evaluation in this study, including three CT datasets and three MRI datasets: • KiPA : The dataset is sourced from “the Kidney Parsing Challenge 2022” [43]. aiming to segment cerebrovascular structures from MRA ima… |
| A | [SegVol: Universal and Interactive Volumetric Medical Image Segmentation](https://doi.org/10.48550/arXiv.2311.13385) | 2023 | …we collected 25 open-source segmentation CT datasets, including CHAOS [27–29], HaN-Seg [43], AMOS22 [25], AbdomenCT-1k [38], KiTS23 [21], KiPA22 [17, 18, 54, 55], KiTS19 [20], BTCV [31], Pancreas-CT [7, 48, 49], 3D-IRCADB [58], AbdomenCT-12organ [39,57], Tota… |
| A | [Analyzing domain shift when using additional data for the MICCAI KiTS23 Challenge](https://doi.org/10.1007/978-3-031-54806-2_4) | 2023 | In addition to the official KiTS23 data, our submission made use of the public KiPA22 competition training set [3] The KiTS23 training dataset contains 489 CTs which include at least one kidney and tumor region and usually include both kidneys and optionally o… |
| A | [CANet: Channel Extending and Axial Attention Catching Network for Multi-structure Kidney Segmentation](https://doi.org/10.1007/978-3-031-27324-7_4) | 2022 | We use kidney multi-structure data (KiPA22 dataset [7,15,16,6]) to evaluate the proposed method. |
| B | [Vision foundation model for 3D magnetic resonance imaging segmentation, classification, and registration](https://doi.org/10.1016/j.media.2026.103992) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text; OpenAlex: citing work (no dataset mention in abstract); S2 citation (no sentence available) |
| B | [Development of an Artificial Intelligence–Driven Three‐Dimensional Reconstruction Model of Renal Vasculature for Surgical Planning in Robot‐Assisted Partial Nephrectomy](https://doi.org/10.1002/rcs.70207) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text; OpenAlex: citing work (no dataset mention in abstract); S2 citation (no sentence available) |
| B | [RenalSegNet: automated segmentation of renal tumor, veins, and arteries in contrast-enhanced CT scans](https://doi.org/10.1007/s40747-024-01751-2) | 2025 | Abstract/title: Evaluated on the KiPA dataset, RenalSegNet achieved remarkable performance, with an average dice score of 86.25%, IOU of 76.75%, Recall of 86.69%, Precision of 86.48%, HD of 15.78 mm, and AVD of 0.79 mm. |
| B | [Source free domain adaptation for kidney and tumor image segmentation with wavelet style mining.](https://doi.org/10.1038/s41598-024-75972-3) | 2024 | Europe PMC: named in Methods; Europe PMC: named in full text |

133 more candidate(s) in the CSV.

### H04 — KPIs 2024

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *KPIs 2024 Challenge: Advancing Glomerular Segmentation from Patch- to Slide-Level* (11 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/224f38037d35e1b4922d27b8a45bdd860e14b565>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22KPIs%202024%22%20glomerular>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22KPIs%202024%22%20OR%20%22KPIs%20challenge%22%20OR%20%22KPIs%20dataset%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Organism-scale annotation with Pan-human Azimuth](https://doi.org/10.64898/2026.07.16.738997) | 2026 | To independently validate their specific localization to glomeruli, we generated glomerular masks and outlines using an existing SegFormer B5 70 model trained on Kidney Pathology Image Segmentation (KPIs) data 71,72 (Supplementary Fig.8B bottom, Supplementary … |
| B | [K-Prism: A Knowledge-Guided and Prompt Integrated Universal Medical Image Segmentation Model](https://doi.org/10.48550/arXiv.2509.25594) | 2025 | The KPIs dataset was released as part of the MICCAI 2024 Challenge to benchmark glomeruli segmentation performance in chronic kidney disease (CKD) pathology. |
| B | [StainStyleSampler: clustering-based sampling of whole slide image appearances.](https://doi.org/10.1186/s13000-026-01752-4) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Who initiates price competition when generic entrants are introduced into the South Korean pharmaceutical market?](https://doi.org/10.3389/fpubh.2022.934161) | 2022 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Smartphone-Based Accurate Analysis of Retinal Vasculature towards Point-of-Care Diagnostics.](https://doi.org/10.1038/srep34603) | 2016 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Retinal vessel diameter measurement using unsupervised linear discriminant analysis.](https://doi.org/10.5402/2012/151369) | 2012 | Europe PMC: named in Methods; Europe PMC: named in full text |

12 more candidate(s) in the CSV.

### H05 — AbdomenCT-1K

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *AbdomenCT-1K: Is Abdominal Organ Segmentation a Solved Problem?* (487 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/8aefc1469ba378389e1742340d25a24ba21a94a6>
- OpenAlex works citing *AbdomenCT-1K: Is Abdominal Organ Segmentation a Solved Problem?* (415): <https://openalex.org/works?filter=cites:W3183302989>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22AbdomenCT-1K%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22AbdomenCT-1K%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [A medical image watermarking method based on the combination of DTCWT and PSO optimization](https://doi.org/10.1007/s44443-026-00480-5) | 2026 | Inertia weight w 0.8 abdomen images from the AbdomenCT-1K dataset (Ma et al. 2021), and ﬁnger and eyeball images from the Kag-gle platform (https://www.kaggle.com/). |
| A | [Pancreas segmentation using AI developed on the largest CT dataset with multi-institutional validation and implications for early cancer detection](https://doi.org/10.1038/s41598-025-01802-9) | 2025 | The model’s generalizability was further evaluated using CTs from the international multi-institutional public dataset AbdomenCT-1K 33 , which consists of 1062 CT scans from 12 medical centers. |
| A | [FreeTumor: Advance Tumor Segmentation via Large-Scale Tumor Synthesis](https://doi.org/10.48550/arXiv.2406.01264) | 2024 | Thanks to the previous efforts, we can collect large-scale CT datasets with organ labels, i.e. , CHAOS [30], Pancreas-CT [55], BTCV [34], Amos22 [26], WORD [41], Flare22 [44], Abdomenct-1k [43], AbdomenAtlas [50], and Flare23 [44]. |
| A | [Devil is in Details: Locality-Aware 3D Abdominal CT Volume Generation for Self-Supervised Organ Segmentation](https://doi.org/10.1145/3664647.3680588) | 2024 | As shown in Figure 1a, the dice scores of the self-supervised segmentation model SSL-ALPNet [22] trained on the augmented AbdomenCT-1K [20] dataset with synthetic abdominal CT volumes generated by Medical Diffusion [14], achieve an improvement of mean dice sco… |
| A | [MiniGPT-Pancreas: Multimodal Large Language Model for Pancreas Cancer Observation and Localization in CT Images](https://doi.org/10.1007/s41666-025-00224-6) | 2024 | It was finally tested on the AbdomenCT-1k dataset for the multi-organ detection task of the abdomen [18]. |
| A | [Neural Annotation Refinement: Development of a New 3D Dataset for Adrenal Gland Analysis](https://doi.org/10.48550/arXiv.2206.15328) | 2022 | Here, we use the public AbdomenCT-1K [15], an abdominal CT organ segmentation dataset, |
| A | [Fully Perturbed Self-Ensemble Framework Using Cascaded Parallel CNN-Transformer for Semisupervised Medical Image Segmentation](https://doi.org/10.1109/TAI.2025.3644335) | 2026 | In this work, all experiments are conducted on the ACDC [41] dataset, the semisupervised subtask 1 dataset of AbdomenCT-1K [42], and ISIC2018 [43] dataset. |
| A | [Reliable Multi-Prototypical Contrastive Learning for Semi-Supervised Heterogeneous and Multi-Organ Medical Image Segmentation](https://doi.org/10.1109/TMI.2026.3692692) | 2026 | To rigorously test TP-Net’s cross-source generalization ability, we tested the model trained on the Abdomenct-1k dataset [30] on the WORD dataset [45], aiming to evaluate the model’s generalization ability across di ﬀ erent scanning protocols and devices. |
| A | [Weight Group-wise Post-Training Quantization for Medical Foundation Model](https://doi.org/10.48550/arXiv.2604.07674) | 2026 | Dataset We validate the performance of permutation-COMQ on AbdomenCT1K as the test dataset, which contains more than 1000 CT scans from 12 medical centers [17]. |
| A | [AdamFlow: Adam-based Wasserstein Gradient Flows for Surface Registration in Medical Imaging](https://doi.org/10.48550/arXiv.2604.02290) | 2026 | For the AbdomenCT-1K dataset, we collect 360 ground-truth segmentation maps of abdominal CT scans that include the liver and pancreas. |
| A | [WeakMedSAM: Weakly-Supervised Medical Image Segmentation via SAM With Sub-Class Exploration and Prompt Affinity Mining](https://doi.org/10.1109/TMI.2025.3549433) | 2025 | E XPERIMENTS A. Experimental Settings 1) Datasets: We conducted our research by utilizing three widely used datasets: BraTS 2019 [55], AbdomenCT-1K [56], and MSD Cardiac dataset [57]. |
| A | [Communication Efficient Federated Learning for Multi-Organ Segmentation via Knowledge Distillation With Image Synthesis](https://doi.org/10.1109/TMI.2025.3525581) | 2025 | We trained local models for each of the four organs (liver, kidney, pancreas, and spleen) using AbdomenCT-1K dataset [59] and generated synthetic images as shown in Fig. |

187 more candidate(s) in the CSV.

### H06 — RAOS

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *Rethinking Abdominal Organ Segmentation (RAOS) in the clinical scenario: A robustness evaluation benchmark with challenging cases* (33 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/be240a8bacf886cea71f0093846962858bdfc36e>
- OpenAlex works citing *Rethinking Abdominal Organ Segmentation (RAOS) in the clinical scenario: A robustness evaluation benchmark with challenging cases* (0): <https://openalex.org/works?filter=cites:W4399911088>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22RAOS%22%20abdominal%20organ%20segmentation>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22RAOS%22%20AND%20abdominal%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [GAMED-Snake: Gradient-aware Adaptive Momentum Evolution Deep Snake Model for Multi-organ Segmentation](https://doi.org/10.1109/ICME59968.2025.11209898) | 2025 | A. Experimental Settings 1) Dataset Introduction: For our experiments, we utilize four multi-organ datasets, including the private multi-organ spinal dataset MR AVBCE [1] and three public datasets: the spinal dataset VerSe [14], the abdominal multi-organ segme… |
| A | [Large-Scale Multimodality via Dual-Path Cooperative Feature Fusion Strategy for Medical Image Segmentation](https://doi.org/10.1109/TMI.2026.3667954) | 2026 | We conducted experiments on six datasets, Synapse [31], SegTHOR [32], ImageTBAD [33], MM-WHS2017, RAOS [34], and MRSpineSeg2021, focusing on segmentation processing of ﬁne-grained details of the segmented regions in all images. |
| A | [Bound-Aware Per-Organ Recall Risk Control for Multi-Organ CT Segmentation under Clinical Domain Shift](https://arxiv.org/abs/2608.18193) | 2026 | We study an AMOS-trained [2] nnU-Net on RAOS [3], an extension of WORD [4] that labels organ presence and absence across a graded surgical-shift ladder. |
| A | [Text-to-Conditioned Abdominal CT Image Generation with ControlNet](https://doi.org/10.1007/978-3-032-29912-3_22) | 2026 | We employed the RAOS CT dataset [17][18], which consists of 413 real clinical scans annotated for 19 different organs. |
| A | [Assisting embodied AI: a survey of 3D segmentation models for medical CT images](https://doi.org/10.1007/s42486-025-00203-1) | 2025 | We selected eight data-sets corresponding to different anatomical regions, including HaN-Seg (Podobnik et al. 2023), BraTS 2019 (Menze et al. 2014; Bakas et al. 2017, 2018), AeroPath (Støverud et al. 2023), MSD (Antonelli et al. 2022), MM-WHS 2017 (Zhuang 2018… |
| A | [OWT: A Foundational Organ-Wise Tokenization Framework for Medical Imaging](https://doi.org/10.48550/arXiv.2505.04899) | 2025 | We conduct experiments on four 3D medical datasets: two CT sets (Abdomen1k [42] and the CT volumes from Au-toPet [21]) and two synthetic MRI sequences (delay and pre-artery) from RAOS dataset [41]. |
| B | [Learning like a radiologist: a medical vision-language model for radiological image analysis via curriculum learning](https://doi.org/10.1038/s41746-026-02713-3) | 2026 | Speci ﬁ cally, MR images were sourced from CHAOS 30 , AMOS 31 , TotalSegmentator-MR 32 , and RAOS 33 , CTimageswereobtainedfromCT-ORG 34 andTotalSegmentator-CT 35 ,and DR images were drawn from an internal clinical archive (as detailed in Supplementary Table S… |
| B | [Unified Medical Image Segmentation with State Space Modeling Snake](https://doi.org/10.1145/3746027.3755148) | 2025 | Datasets This study evaluates the performance of the Mamba Snakemodelusingfiveprominentmulti-organsegmentationdatasets: MR_AVBCE (spine, MRI) [47], VerSe (spine, CT) [33], RAOS (abdomen, CT) [25], BTCV (abdomen, CT) [18], and PanNuke (cells, microscopy) [9]. |
| B | [XRadNet: A Radiomics-Guided Breast Cancer Molecular Subtype Prediction Network With a Radiomics Explanation](https://doi.org/10.1109/JBHI.2025.3552072) | 2025 | These datasets, AbdomenCT-1K [63], AMOS [64], BTCV [65], and RAOS [66], include a total of 1640 samples used for segmentation task pretraining. |
| B | [Towards Reliable Medical Image Segmentation by Modeling Evidential Calibrated Uncertainty](https://arxiv.org/abs/2301.00349) | 2023 | …strong calibration and robustness across diverse segmentation settings (2D, 3D, and multi-modal), including semi-supervised scenarios and OOD detection, its applicability to highly heterogeneous clinical edge cases, as represented in RAOS [53], remains an imp… |

60 more candidate(s) in the CSV.

### H07 — BTCV / Synapse multi-organ

> BTCV has no indexed dataset paper. Candidates come from papers citing UNETR (WACV 2022) that name BTCV/Synapse, plus Europe PMC. TransUNet citations were not harvested.

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *UNETR: Transformers for 3D Medical Image Segmentation* (3034 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/7519a1e9e7371df79bd8a21cee871feb0ec597a5>
- OpenAlex works citing *UNETR: Transformers for 3D Medical Image Segmentation* (214): <https://openalex.org/works?filter=cites:W3137561054>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22BTCV%22%20multi-organ>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22BTCV%22%20OR%20%22Beyond%20the%20Cranial%20Vault%22%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Benchmarking CNN-based Models against Transformer-based Models for Abdominal Multi-Organ Segmentation on the RATIC Dataset](https://doi.org/10.48550/arXiv.2603.18616) | 2026 | For instance, the UNETR [3] model which is commonly used as a base-line yields reported DSC scores ranging from 0.6888 [6] to 0.8910 [3, 7], with intermediate results of 0.7835 [8], 0.8027 [9], and 0.8129 [10] while trained on the BTCV dataset [11] with compar… |
| A | [Fake It Right: Injecting Anatomical Logic into Synthetic Supervised Pre-training for Medical Segmentation](https://doi.org/10.48550/arXiv.2603.00979) | 2026 | We systematically evaluate our framework on BTCV [8] MSD [1] datasets on UNETR [4] and SwinUNETR [3] backbones, outperforming state-of-the-art FDSL baselines and SSL methods by over 1.45% and up to 1.67%. |
| A | [Pre-Trained LLM is a Semantic-Aware and Generalizable Segmentation Booster](https://doi.org/10.48550/arXiv.2506.18034) | 2025 | Following pervious work [29,5,36,21], we utilize IoU and F1 score for BUSI, TNSCUI, ISIC, and Kvasir, while adopting the Dice for BTCV as [13,35,28]. |
| A | [TDFormer: Top-Down Token Generation for 3D Medical Image Segmentation](https://doi.org/10.1109/JBHI.2025.3567590) | 2025 | Pretrained Weights: In BTCV experiments, we leverage pre-trained weights, a strategy in line with previous studies [11], [12]. |
| A | [Accurate 3D Medical Image Segmentation with Mambas](https://doi.org/10.1109/ISBI60581.2025.10981167) | 2025 | Following the literature on medical image segmentation [9, 13, 31], experiments have been carried out on three different well-known datasets: MSD BrainTumour [32], Synapse Multi-organ [33], and ACDC [34]. |
| A | [Self Pre-Training with Topology- and Spatiality-Aware Masked Autoencoders for 3D Medical Image Segmentation](https://doi.org/10.1109/BIBM66473.2025.11356706) | 2024 | We conduct experiments on five segmentation datasets: Synapse multi-organ CT segmentation (Synapse CT Dataset) [15], BTCV multi-organ CT segmentation (BTCV CT Dataset) [15], ACDC automated cardiac diagnosis (ACDC) [3], and Medical Segmentation Decathlon (MSD) … |
| A | [Anatomical Invariance Modeling and Semantic Alignment for Self-supervised Learning in 3D Medical Image Analysis](https://doi.org/10.1109/ICCV51070.2023.01453) | 2023 | We fine-tune these widely used ViT-based medical image segmentation frameworks following [19, 40, 53] with our pre-trained weights on two publicly available benchmarks: Fast and Low-resource semi-supervised Abdominal oRgan sEgmentation in CT (FLARE 2022) * , a… |
| A | [DeepEdit: Deep Editable Learning for Interactive Segmentation of 3D Medical Images](https://doi.org/10.1007/978-3-031-17027-0_2) | 2023 | A second set of experiments using the UNETR [6] as backbone were performed on the BTCV dataset. |
| A | [Frequency Domain Adversarial Training for Robust Volumetric Medical Segmentation](https://doi.org/10.48550/arXiv.2307.07269) | 2023 | Implementation Details: We demonstrate the effectiveness of our approach using two medical segmentation models: UNETR[12], UNETR++[24] and two datasets: Synapse (18-12 split) [17], and ACDC [2]. |
| A | [Anatomical Invariance Modeling and Semantic Alignment for Self-supervised Learning in 3D Medical Image Segmentation](https://doi.org/10.48550/arXiv.2302.05615) | 2023 | We fine-tune these widely used ViT-based medical image segmentation frameworks following [59, 20, 44] with our pre-trained weights on two publicly available benchmarks: Fast and Lowresource semi-supervised Abdominal oRgan sEgmentation in CT (FLARE 2022)∗, and … |
| A | [A Comparison of Applying Image Processing and Deep Learning in Acne Region Extraction](https://doi.org/10.18178/joig.10.4.166-171) | 2022 | Then the performance was tested with a data set combined with Multi Atlas Labeling Beyond The Cranial Vault (BTCV) dataset for multi-organ segmentation and the Medical Segmentation Decathlon (MSD) dataset for brain tumor and spleen segmentation tasks with bett… |
| A | [nnFormer: Volumetric Medical Image Segmentation via a 3D Transformer](https://doi.org/10.1109/TIP.2023.3293771) | 2021 | Moreover, nnFormer is able to surpass the second best method, i.e., UNETR, by large margins in 2 Similar to Synapse, we also follow the evaluation setting of TransUNet. |

319 more candidate(s) in the CSV.

### H09 — NEPTUNE multistain (Jayapandian)

> Citations of Jayapandian et al. Most use their own cohorts, not NEPTUNE data. Verify the data source.

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *Development and evaluation of deep learning–based segmentation of histologic structures in the kidney cortex with multiple histologic stains* (179 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/9ea745a7d0e58fef274f0af0b3a92f9945147561>
- OpenAlex works citing *Development and evaluation of deep learning–based segmentation of histologic structures in the kidney cortex with multiple histologic stains* (202): <https://openalex.org/works?filter=cites:W3080677331>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=NEPTUNE%20%22whole%20slide%22%20deep%20learning%20kidney>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22NEPTUNE%22%20AND%20%28%22deep%20learning%22%20OR%20segmentation%29%20AND%20%28%22whole%20slide%22%20OR%20WSI%29%29>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| B | [Computational Characterization of Lymphocyte Topology on Whole Slide Images of Glomerular Diseases.](https://doi.org/10.1681/asn.0000000889) | 2026 | Abstract/title: Methods NEPhrotic syndrome sTUdy NEtwork (NEPTUNE) ( N =333)/Cure Glomerulonephropathy (CureGN) participants ( N =155 focal segmental glomerulosclerosis, N =178 minimal change disease) with available clinical/demographic data and one hematoxyli… |
| B | [GlomNet: glomeruli segmentation network for WSI with diverse staining protocols for kidney disease diagnosis.](https://doi.org/10.3389/fmed.2026.1785037) | 2026 | Abstract/title: Experimental results demonstrate that GlomNet achieves state-of-the-art performance across multiple benchmarks, including NEPTUNE, HuBMAP-1, and HuBMAP-2, showcasing its robustness across diverse histological conditions, with significant potent… |
| B | [A deep learning and morphometric hybrid model for automated quantification of kidney interstitial fibrosis in trichrome-stained whole-slide image.](https://doi.org/10.1016/j.jpi.2026.100649) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Explainable Pathomics Feature Visualization via Correlation-aware Conditional Feature Editing.](https://europepmc.org/article/MED/42764993) | 2026 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Analysis of Correlated Image Features Using Scalar‐On‐Matrix Regression](https://doi.org/10.1002/sam.70078) | 2026 | Abstract/title: Finally, we applied Random CLUSSO to predict kidney function using image features from kidney biopsies of subjects with glomerular disease from the Nephrotic Syndrome Study Network (NEPTUNE) and Cure Glomerulonephropathy (CureGN) studies. |
| B | [Segment Anything Model (SAM) for Digital Pathology: Assess Zero-shot Segmentation on Whole Slide Imaging.](https://doi.org/10.2352/ei.2025.37.14.coimg-132) | 2025 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Clinical Relevance of Computational Pathology Analysis of Interplay between Kidney Microvasculature and Interstitial Microenvironment.](https://doi.org/10.2215/cjn.0000000597) | 2025 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Clinical relevance of computationally derived tubular features and their spatial relationships with the interstitial microenvironment in minimal change disease/focal segmental glomerulosclerosis.](https://doi.org/10.1016/j.kint.2025.04.026) | 2025 | Abstract/title: METHODS: Deep-learning and image-analysis approaches were employed on 254/266 Periodic acid Schiff-stained whole slide image (WSI) kidney biopsies from participants in the NEPTUNE/CureGN prospective observational cohort studies (135/153 with fo… |
| B | [Assessment of Cell Nuclei AI Foundation Models in Kidney Pathology.](https://doi.org/10.1117/12.3047301) | 2025 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Novel Scalar-on-matrix Regression for Unbalanced Feature Matrices.](https://doi.org/10.1007/s12561-025-09476-7) | 2025 | Europe PMC: named in Methods; Europe PMC: named in full text |
| B | [Clinical Relevance of Computationally Derived Attributes of Arteries and Arterioles in focal segmental glomerulosclerosis and minimal change disease](https://doi.org/10.1101/2025.10.08.25336276) | 2025 | Abstract/title: Methods: We utilized one trichrome-stained WSI from 225 participants in the NEPTUNE/CureGN studies, comprising 127 cases of focal segmental glomerulosclerosis (FSGS) and 98 cases of minimal change disease (MCD). |
| B | [Computational characterization of lymphocyte topology on whole slide images of glomerular diseases](https://doi.org/10.1101/2025.04.12.25325548) | 2025 | Abstract/title: N=333 NEPTUNE/CureGN participants (N=155 focal segmental glomerulosclerosis (FSGS) and N=178 Minimal Change Disease (MCD) with available clinical/demographic data and 1 Hematoxylin & Eosin-stained whole slide image (WSI), were included. |

61 more candidate(s) in the CSV.

### H10 — Merlin Abdominal CT

> Merlin is both a model and a dataset. Only sentences naming the dataset are kept; most citing papers use the model.

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *Merlin: A Computed Tomography Vision-Language Foundation Model and Dataset* (171 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/5fd4b58f2bc9de5f3b1c8b59026b524678f309fa>
- Semantic Scholar citations of *Merlin: A Computed Tomography Vision-Language Foundation Model and Dataset* (171 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/5fd4b58f2bc9de5f3b1c8b59026b524678f309fa>
- OpenAlex works citing *Merlin: a computed tomography vision–language foundation model and dataset* (34): <https://openalex.org/works?filter=cites:W7133527361>
- OpenAlex works citing *Merlin: A Computed Tomography Vision-Language Foundation Model and Dataset* (9): <https://openalex.org/works?filter=cites:W4399554476>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22Merlin%22%20abdominal%20CT%20dataset>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22Merlin%22%20AND%20%28CT%20OR%20%22computed%20tomography%22%29%20AND%20%28%22vision-language%22%20OR%20%22foundation%20model%22%29%29>
- Hugging Face dataset page: <https://huggingface.co/datasets/stanfordmimi/Merlin>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Pillar-0: A New Frontier for Radiology Foundation Models](https://doi.org/10.48550/arXiv.2511.17803) | 2025 | For external evaluation, we used the Merlin Abdominal CT Dataset [15], which comprises 25,494 abdomen-pelvis CT–report pairs from 18,317 patients. |
| A | [vesselFM-CT: Segmenting All Blood Vessels in CT Images for System-Level Cardiovascular Analysis](https://doi.org/10.48550/arXiv.2606.09400) | 2026 | Both experiments are conducted on the Merlin dataset [2], which consists of abdominal CT scans, matching radiology reports, and relevant metadata. |
| A | [Structured Spectral Graph Representation Learning for Multi-label Abnormality Analysis from 3D CT Scans](https://doi.org/10.59275/j.melba.2026-87e3) | 2025 | : There are atheromat-Generation Evaluation protocol To assess cross-anatomy generalization, we evaluate CT-SSG chest-pretrained model on the Merlin Abdominal CT dataset (Blankemeier et al., 2024). |
| B | [Report Supervision.](https://doi.org/10.1016/j.media.2026.104257) | 2026 | Hospitals therefore hold hundreds of thousands of reports, and the public Merlin dataset alone contains over 25,000 CT-Report pairs (Blankemeier et al., 2026). |
| B | [RadLite: Multi-Task LoRA Fine-Tuning of Small Language Models for CPU-Deployable Radiology AI](https://doi.org/10.48550/arXiv.2605.00421) | 2026 | Data sourced from the Merlin dataset [34], a large-scale CT vision-language dataset; reports were screened for explicit lymph node descriptors to extract staging labels. |
| B | [Scaling Artificial Intelligence for Multi-Tumor Early Detection with More Reports, Fewer Masks](https://doi.org/10.48550/arXiv.2510.14803) | 2025 | Our dataset also includes the public Merlin dataset [18] (25,494 CTs, Stanford Hospital, from 2012 to 2018). |
| B | [ReCo: a self-configuring and self-extending agentic framework for biomedical research](https://doi.org/10.64898/2026.07.14.26358025) | 2026 | Abstract/title: Self-extension was evaluated using five heterogeneous systems: the Merlin computed tomography foundation model, MAISI-v2 medical image synthesis framework, asari liquid chromatography-mass spectrometry workflow, DosimeTron agentic radiation-dos… |

33 more candidate(s) in the CSV.

### H11 — RadImageNet-VQA

**Where to find every paper that cites or uses it:**

- Semantic Scholar citations of *RadImageNet-VQA: A Large-Scale CT and MRI Dataset for Radiologic Visual Question Answering* (5 citing works; filter by "Methods" intent): <https://www.semanticscholar.org/paper/e80f4d0ac4278dedcc49a6e11f34faabbdd511a4>
- OpenAlex works citing *RadImageNet-VQA: A Large-Scale CT and MRI Dataset for Radiologic Visual Question Answering* (0): <https://openalex.org/works?filter=cites:W7116970580>
- Google Scholar full-text search for the dataset name: <https://scholar.google.com/scholar?q=%22RadImageNet-VQA%22>
- Europe PMC, open-access papers naming it in Methods: <https://europepmc.org/search?query=METHODS%3A%28%22RadImageNet-VQA%22%29>
- Hugging Face dataset page: <https://huggingface.co/datasets/raidium/RadImageNet-VQA>

| Tier | Paper | Year | Evidence |
|---|---|---|---|
| A | [Med-Scout: Curing MLLMs' Geometric Blindness in Medical Perception via Geometry-Aware RL Post-Training](https://doi.org/10.48550/arXiv.2601.23220) | 2026 | Second, we assess standard radiological VQA using RadImageNet-VQA (Butsanets et al., 2025), VQA-RAD (Lau et al., 2018), and SLAKE (Liu et al., 2021), alongside MIMIC-CXR and IU-Xray for report generation. |

4 more candidate(s) in the CSV.
