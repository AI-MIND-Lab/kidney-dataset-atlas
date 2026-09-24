"""Papers to check in full text: (dataset ID, arxiv:ID or doi:DOI, pattern that must appear in the paper body).

This is the list checked on 2026-09-23 for docs/Kidney_Open_Datasets_and_CV_Papers.md section 6.4. Add rows to check more papers."""
V = [
 # KiTS19
 ('K01', 'arxiv:1904.08128', r'KiTS'), ('K01', 'arxiv:2102.04525', r'KiTS\s?-?19'), ('K01', 'arxiv:2102.10365', r'KiTS\s?-?19'),
 ('K01', 'arxiv:2106.00817', r'KiTS\s?-?19'), ('K01', 'arxiv:2303.09975', r'KiTS\s?-?19'), ('K01', 'arxiv:2004.08108', r'KiTS\s?-?19'),
 # KiTS21
 ('K02', 'arxiv:2306.13465', r'KiTS\s?-?21'), ('K02', 'doi:10.1007/978-3-030-98385-7_8', r'KiTS'), ('K02', 'arxiv:2302.02125', r'KiTS\s?-?21'),
 # KiTS23
 ('K03', 'arxiv:2404.09556', r'KiTS\s?-?(20)?23'), ('K03', 'arxiv:2312.17183', r'KiTS\s?-?(20)?23'), ('K03', 'arxiv:2509.06830', r'KiTS\s?-?(20)?23'),
 ('K03', 'arxiv:2406.03323', r'KiTS\s?-?(20)?23'), ('K03', 'arxiv:2309.02001', r'KiTS\s?-?(20)?23'),
 # CT Kidney Normal-Cyst-Tumor-Stone
 ('K05', 'doi:10.1038/s41598-024-71410-6', r'12,?446|Cyst'), ('K05', 'doi:10.7717/peerj-cs.1717', r'12,?446|Islam'), ('K05', 'doi:10.1016/j.jksuci.2024.102130', r'CT KIDNEY DATASET|Kaggle'),
 ('K05', 'doi:10.1007/s13721-023-00431-4', r'Islam|Dhaka'),
 # TCGA renal WSI
 ('K06-K08', 'arxiv:2004.09666', r'RCC|renal'), ('K06-K08', 'arxiv:2106.00908', r'TCGA-RCC|RCC'), ('K06-K08', 'doi:10.1371/journal.pone.0272656', r'TCGA'),
 ('K06-K08', 'doi:10.1038/s41467-025-57717-6', r'TCGA'),
 # TCGA-KIRC/KIRP/KICH radiology (TCIA)
 ('K09', 'doi:10.1038/s41698-021-00195-y', r'TCGA|TCIA'), ('K09', 'doi:10.1016/j.ejrad.2018.08.014', r'TCGA|TCIA'), ('K09', 'doi:10.1007/s00330-021-08344-4', r'TCGA|TCIA'),
 ('K09', 'doi:10.1007/s00261-015-0386-z', r'TCGA|TCIA'),
 # HuBMAP Hacking the Kidney
 ('K10', 'doi:10.1038/s41467-023-36960-9', r'HuBMAP'), ('K10', 'doi:10.1007/s10278-022-00764-y', r'HuBMAP'), ('K10', 'doi:10.1016/j.jpi.2022.100140', r'HuBMAP'),
 ('K10', 'arxiv:2604.14263', r'HuBMAP'),
 # HuBMAP + HPA
 ('K11-K12', 'doi:10.1109/ACCTCS66275.2025.00050', r'HuBMAP'),
 # TRUSTED
 ('K13', 'arxiv:2606.25009', r'TRUSTED'),
 # Kidney stone Mendeley
 ('K14', 'doi:10.1016/j.dib.2025.111446', r'stone'), ('K14', 'doi:10.1155/acis/5844438', r'fwhytt5mzd|Mendeley|Abdalla|axial'), ('K14', 'doi:10.1007/s11255-026-05057-9', r'fwhytt5mzd|Mendeley|Abdalla|axial'),
 # TotalSegmentator CT
 ('M01', 'arxiv:2304.06716', r'TotalSegmentator'), ('M01', 'arxiv:2312.17183', r'TotalSegmentator'), ('M01', 'arxiv:2312.07381', r'TotalSegmentator'),
 ('M01', 'arxiv:2403.09827', r'TotalSegmentator'), ('M01', 'arxiv:2411.02372', r'TotalSegmentator'),
 # TotalSegmentator MRI
 ('M02', 'doi:10.1007/s10278-025-01716-y', r'TotalSegmentator'), ('M02', 'arxiv:2602.08717', r'TotalSegmentator'),
 # AMOS
 ('M03', 'arxiv:2304.12620', r'AMOS'), ('M03', 'arxiv:2209.15076', r'AMOS'), ('M03', 'arxiv:2309.08842', r'AMOS'), ('M03', 'arxiv:2311.13385', r'AMOS'),
 ('M03', 'arxiv:2404.09556', r'AMOS'), ('M03', 'arxiv:2303.09975', r'AMOS'),
 # CHAOS
 ('M04', 'arxiv:2007.09886', r'CHAOS'), ('M04', 'doi:10.1109/TMI.2022.3192303', r'CHAOS'), ('M04', 'arxiv:2311.13385', r'CHAOS'), ('M04', 'arxiv:2112.04489', r'CHAOS'),
 # CT-ORG
 ('M05', 'arxiv:2304.06716', r'CT-?ORG'), ('M05', 'arxiv:2207.11225', r'CT-?ORG'), ('M05', 'arxiv:2312.04964', r'CT-?ORG'),
 # WORD
 ('M06', 'doi:10.3390/s23218739', r'WORD'), ('M06', 'doi:10.1109/ojemb.2024.3397623', r'WORD'), ('M06', 'arxiv:2307.12591', r'WORD'),
 # AbdomenAtlas
 ('M07', 'arxiv:2411.03670', r'AbdomenAtlas'), ('M07', 'arxiv:2501.04678', r'AbdomenAtlas'), ('M07', 'arxiv:2510.14831', r'AbdomenAtlas'),
 # FLARE21
 ('M08', 'arxiv:2207.11225', r'FLARE'), ('M08', 'arxiv:2109.10601', r'FLARE'),
 # FLARE22
 ('M09', 'arxiv:2304.06716', r'FLARE\s?-?(20)?22'), ('M09', 'arxiv:2403.07332', r'FLARE'), ('M09', 'arxiv:2406.07085', r'FLARE\s?-?(20)?22'), ('M09', 'arxiv:2407.06468', r'FLARE\s?-?(20)?22'),
 # FLARE23
 ('M10', 'arxiv:2408.12534', r'FLARE\s?-?(20)?23|FLARE 2023'), ('M10', 'arxiv:2406.01264', r'FLARE\s?-?(20)?23'),
 # AbdomenAtlas 3.0
 ('M11', 'arxiv:2603.00479', r'AbdomenAtlas\s?3'), ('M11', 'arxiv:2605.22619', r'AbdomenAtlas\s?3'), ('M11', 'arxiv:2507.05582', r'AbdomenAtlas'),
 # AMOS-MM
 ('M12', 'arxiv:2410.08588', r'AMOS-MM'), ('M12', 'arxiv:2503.13330', r'AMOS-MM'), ('M12', 'arxiv:2506.21535', r'AMOS-MM'),
 # ULS23
 ('M14', 'arxiv:2508.06453', r'ULS23'),
 # DeepLesion (kidney relevance checked separately)
 ('M16', 'arxiv:1908.04373', r'DeepLesion'), ('M16', 'arxiv:2504.03600', r'DeepLesion'),
 # M3D-Data
 ('M17', 'arxiv:2506.19665', r'M3D-Cap'), ('M17', 'arxiv:2503.15892', r'M3D-Cap'), ('M17', 'arxiv:2601.09879', r'M3D-Seg'),
 # UCSF RMaC
 ('G01', 'doi:10.23919/SpliTech70133.2026.11685485', r'RMaC'),
 # CPTAC-CCRCC imaging
 ('G02', 'doi:10.1016/j.xcrm.2025.102299', r'CPTAC'), ('G02', 'arxiv:2609.04071', r'CPTAC'), ('G02', 'doi:10.1038/s41591-024-02857-3', r'CPTAC'),
 # kidneyUS
 ('H01', 'doi:10.1177/20552076241291306', r'Open Kidney|kidneyUS'), ('H01', 'doi:10.3390/diagnostics15151978', r'Open Kidney|OKUD'), ('H01', 'arxiv:2503.06976', r'KidneyUS|Open Kidney'),
 # KiPA22
 ('H03', 'arxiv:2311.13385', r'KiPA'), ('H03', 'doi:10.1007/s40747-024-01751-2', r'KiPA'), ('H03', 'arxiv:2208.05241', r'KiPA'), ('H03', 'arxiv:2309.02001', r'KiPA'),
 # KPIs
 ('H04', 'arxiv:2509.25594', r'KPIs'),
 # AbdomenCT-1K
 ('H05', 'arxiv:2311.13385', r'AbdomenCT-?1[kK]'), ('H05', 'arxiv:2307.12591', r'AbdomenCT-?1[kK]'), ('H05', 'arxiv:2312.04964', r'AbdomenCT-?1[kK]'), ('H05', 'arxiv:2503.04106', r'AbdomenCT-?1[kK]'),
 # RAOS
 ('H06', 'arxiv:2501.12844', r'RAOS'), ('H06', 'arxiv:2505.04899', r'RAOS'), ('H06', 'arxiv:2608.18193', r'RAOS'),
 # BTCV
 ('H07', 'arxiv:2102.04306', r'Synapse'), ('H07', 'arxiv:2103.10504', r'BTCV'), ('H07', 'arxiv:2111.14791', r'BTCV'), ('H07', 'arxiv:2109.03201', r'Synapse'),
 ('H07', 'arxiv:2105.05537', r'Synapse'), ('H07', 'arxiv:2007.09886', r'Synapse|BTCV|Cranial Vault'),
 # Merlin
 ('H10', 'arxiv:2511.17803', r'Merlin'), ('H10', 'arxiv:2606.09400', r'Merlin'), ('H10', 'arxiv:2510.14803', r'Merlin'),
 # RadImageNet-VQA
 ('H11', 'arxiv:2601.23220', r'RadImageNet-VQA'),
]
