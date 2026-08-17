# Data Manifest — Hematology AI System

Cập nhật: 2026-08-16 (v2). Ghi lại nguồn gốc, trạng thái từng bộ dữ liệu để tránh nhầm lẫn khi dùng lại sau này.

## Đã tải, sẵn sàng dùng

### tabular/anemia_cbc_ml_repo/
- **Nguồn gốc**: Kaggle `abdelrhmankaram/complete-blood-count-cbc-test`, lấy lại qua repo GitHub `Pfuglo1/anemia-detection-cbc-ml`.
- **File chính**: `cbc information.xlsx` — 500 dòng × 21 cột: ID, WBC, LYMp, MIDp, NEUTp, LYMn, MIDn, NEUTn, RBC, HGB, HCT, MCV, MCH, MCHC, RDWSD, RDWCV, PLT, MPV, PDW, PCT, PLCR.
- **Nhãn**: không có cột target sẵn — cần tự sinh (VD ngưỡng HGB/HCT theo giới) hoặc dùng notebook `Project_7_Anemia_Detection_using_Complete_Blood_Count_(CBC)_Parameters.ipynb` trong cùng thư mục làm tham khảo.
- **Giấy phép**: theo LICENSE của repo GitHub gốc — kiểm tra trước khi dùng thương mại.

### tabular/anemia_ml_basic_repo/
- **Nguồn gốc**: Kaggle `biswaranjanrao/anemia-dataset`, lấy lại qua repo GitHub `maladeep/anemia-detection-with-machine-learning`.
- **File chính**: `anemia data from Kaggle.csv` — 1.421 dòng, cột: Gender, Hemoglobin, MCH, MCHC, MCV, Result (nhãn nhị phân).
- **Đã có sẵn**: model đã train (`random_forest_model.pkl`), 2 notebook minh hoạ, script `anemia.py`.

### images/mds_bone_marrow/
- **Nguồn gốc**: figshare, DOI 10.6084/m9.figshare.28737170.v1 — bài báo "A large dataset of bone marrow cells in myelodysplastic syndrome for classification systems" (Scientific Data, 2025).
- **Nội dung**: `dataset_BM_cell_MDS.zip` (giữ nguyên gốc) + đã giải nén vào `extracted/` — 33 thư mục lớp tế bào (Blast NOC, Myeloblast, Dysplastic erythroblast, Micromegakaryocyte, Segmented neutrophil...), tổng 25.067 ảnh JPEG.
- **Lưu ý**: phân bố lớp lệch mạnh — cần EDA đếm ảnh/lớp trước khi train (xem `eda/report_images.txt`).

### images/txl_pbc_repo/
- **Nguồn gốc**: GitHub `lugan113/TXL-PBC_Dataset` — dữ liệu gộp/re-annotate từ BCCD, BCDD, PBC (Barcelona), Raabin-WBC.
- **Nội dung**: `TXL-PBC/images/{train,val,test}` + `TXL-PBC/labels/{train,val,test}` — ảnh + bounding box annotation dạng **YOLO detection**, chỉ 3 lớp: WBC, RBC, Platelet (KHÔNG phân loại tiếp neutrophil/eosinophil...).
- **Đã có sẵn**: script `dataset_splits.py`, `baseline_model.py`, `dataset_statistical_analysis.py` của tác giả gốc.

### tabular/physionet_sepsis_2019/
- **Nguồn gốc**: PhysioNet/Computing in Cardiology Challenge 2019 — [physionet.org/content/challenge-2019/1.0.0](https://physionet.org/content/challenge-2019/1.0.0/), CC BY 4.0, **không cần credential** (khác MIMIC).
- **Nội dung**: `training_setA/` (20.336 file) + `training_setB/` (20.000 file) = **40.336 file `.psv`** (pipe-separated), mỗi file là 1 bệnh nhân, các dòng là chuỗi thời gian theo giờ (ICULOS).
- **Cột quan trọng cho dự án**: `HR, O2Sat, Temp, SBP, MAP, DBP, Resp` (sinh hiệu), `Bilirubin_total/direct, AST, Alkalinephos` (sinh hóa gan), `Hct, Hgb, WBC, Platelets` (CBC), **`PTT, Fibrinogen`** (đông máu), `Age, Gender` (thông tin bệnh nhân), **`SepsisLabel`** (nhãn outcome nhị phân theo từng giờ).
- **Lưu ý**: dữ liệu dạng time-series đa biến, rất nhiều `NaN` (đo không đều theo giờ) — cần chiến lược xử lý missing riêng (forward-fill, hoặc lấy lát cắt tại 1 thời điểm) trước khi dùng như dữ liệu bảng tĩnh. Không có PT/INR/D-Dimer/CRP/ESR/Ferritin — chỉ bù được 1 phần đông máu (PTT, Fibrinogen).

### tabular/kaggle_cbc_vizeno/
- **Nguồn gốc**: Kaggle `vizeno/complete-blood-count-cbc-dataset` — người dùng tự tải tay, tôi đã sắp xếp lại.
- **File chính**: `blood_count_dataset.csv` — 417 dòng × 9 cột: Age, Gender, Hemoglobin, Platelet_Count, White_Blood_Cells, Red_Blood_Cells, MCV, MCH, MCHC.
- **Cảnh báo chất lượng**: **323/417 dòng bị trùng lặp hoàn toàn (77.5%)** — chỉ còn ~94 dòng thật sự khác nhau. Không có cột nhãn bệnh.

### tabular/kaggle_covid_cbc/
- **Nguồn gốc**: Kaggle `tawsifurrahman/covid19-complete-blood-count-clinical-database` — người dùng tự tải tay.
- **File chính**: `COVID-19_CBC_Data.csv` — 103 dòng × 14 cột: Admission/Discharge date, **Outcome** (Recovered 61 / Not Recovered 42), Age, Gender, Treatment, Ventilated, RDW, Monocytes%, WBC, PLT, Lymphocyte, Neutrophils.
- **Lưu ý**: rất nhỏ (103 dòng), không có missing value; nhãn Outcome là kết quả điều trị COVID chứ không phải chẩn đoán bệnh huyết học; thiếu RBC/Hgb/HCT/MCV/MCH/MCHC so với CBC đầy đủ.

### tabular/rheumatic_dataverse/
- **Nguồn gốc**: Harvard Dataverse, DOI 10.7910/DVN/VM4OR3 — người dùng tự tải tay (bị AWS WAF chặn khi tôi thử tự động).
- **File chính**: `Rheumatic and Autoimmune Disease Dataset.xlsx` — **12.085 dòng × 15 cột**: Age, Gender, **ESR, CRP**, RF, Anti-CCP, HLA-B27, ANA, Anti-Ro, Anti-La, Anti-dsDNA, Anti-Sm, C3, C4, **Disease** (nhãn 7 lớp: Rheumatoid Arthritis, Ankylosing Spondylitis, Sjögren's Syndrome, Psoriatic Arthritis, Normal, Systemic Lupus Erythematosus, Reactive Arthritis).
- **Chất lượng**: 0 dòng trùng lặp, có missing value ở các cột huyết thanh học (ESR thiếu 9%, CRP thiếu 20%, các marker khác thiếu 15-43%) — bình thường vì không phải bệnh nhân nào cũng làm đủ panel xét nghiệm.
- **Lưu ý quan trọng**: đây là dataset **bệnh tự miễn/thấp khớp**, KHÔNG phải bệnh huyết học trong taxonomy gốc — chỉ dùng được để bù chỉ số CRP/ESR làm dữ liệu tham chiếu/huấn luyện phụ, không dùng làm nhãn chính.

### images/pbc_barcelona/
- **Nguồn gốc**: Mendeley Data (Acevedo et al.), DOI liên kết snkd93bnjr — người dùng tự tải tay.
- **Nội dung**: `PBC_dataset_normal_DIB/` — **17.093 ảnh**, 8 lớp: eosinophil (3.117), neutrophil (3.330), ig - immature granulocytes (2.895), platelet (2.348), erythroblast (1.551), monocyte (1.420), basophil (1.218), lymphocyte (1.214).
- **Điểm mạnh**: cân bằng lớp tốt hơn nhiều so với MDS Bone Marrow (lệch tối đa ~2.7 lần, so với 3958 lần) — phù hợp làm dữ liệu train/pretrain phân loại bạch cầu.
- **Giới hạn**: chỉ chứa mẫu từ người khỏe mạnh (không có bệnh lý), nên chỉ dùng để nhận diện loại tế bào nền, không dùng để phát hiện bất thường.

### tabular/nhanes_cbc_2015/
- **Nguồn gốc**: CDC/NCHS — NHANES 2015-2016, khảo sát sức khỏe dân số quốc gia Mỹ. [CBC_I](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2015/DataFiles/CBC_I.htm) + [DEMO_I](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2015/DataFiles/DEMO_I.htm) — public hoàn toàn, tải trực tiếp bằng curl, không cần đăng ký.
- **File chính**: `CBC_I_with_demographics.csv` — **9.165 dòng × 23 cột** — CBC 5-dòng bạch cầu đầy đủ (WBC, LYMp/n, MOp/n, NEp/n, EOp/n, BAp/n cả % và số tuyệt đối), RBC, HGB, HCT, MCV, MCH, MCHC, RDW, PLT, MPV, **đã join sẵn Age + Gender** qua khóa SEQN. File gốc `CBC_I.XPT`/`DEMO_I.XPT` (SAS Transport) giữ nguyên để đối chiếu.
- **Chất lượng**: nguồn chính phủ, độ tin cậy cao nhất trong kho; 1.049/9.165 dòng thiếu phần 5-dòng bạch cầu chi tiết (8.116 dòng đầy đủ hoàn toàn) — không có giá trị âm/vô lý như các bộ Kaggle.
- **Giới hạn**: không có nhãn chẩn đoán bệnh — đây thuần là dữ liệu khảo sát sức khỏe dân số, không phải hồ sơ bệnh án.

## Chưa tải — cần quyết định/thao tác thủ công (đang tạm hoãn)

| Nguồn | Lý do chưa tải | Ghi chú |
|---|---|---|
| MIMIC-IV | Người dùng chủ động loại khỏi phạm vi (chưa qua đào tạo CITI) | Không theo đuổi tiếp trừ khi đổi ý |
| Raabin-WBC | raabindata.com/free-data có khả năng là form yêu cầu | Tải tay nếu cần |
| **Personalized Medication Dataset** (Kaggle `ziya07/personalized-medication-dataset`) | Cần Kaggle, chưa tải | Có Age/Gender/Weight/Height/BMI, Medical history (Chronic conditions/Drug allergies/Genetic disorders), **Symptoms, Diagnosis**, Medication — nguồn tìm được từ đồng đội (`Reference_Data.md`), khớp rất tốt với khoảng trống "thông tin bệnh nhân + triệu chứng + nhãn chẩn đoán". Không có CBC đầy đủ |
| **Laboratory Data** (Kaggle `klingill/laboratory-data`) | Cần Kaggle, chưa tải | ~12.009 dòng: Age/Gender, RBC/WBC/Hemoglobin (CBC rút gọn) + AST/ALT/Cholesterol/Glucose/Lipase/Creatinine/Troponin — không phải các chỉ số sinh hóa thiếu máu chuyên biệt (Ferritin/Iron/TIBC/B12/Folate) đang cần |
| Disease-Symptom Dataset (Kaggle `dhivyeshrk/diseases-and-symptoms-dataset`) | Cần Kaggle, chưa tải | 246.000 dòng, 773 bệnh, 377 triệu chứng one-hot — **dữ liệu tổng hợp/synthetic**, không phải ca bệnh thật. Trùng với nguồn tôi tự tìm được trước đó (cross-confirm) |
| TCIA C-NMC 2019 | Cần công cụ NBIA Data Retriever, không dùng link tải thẳng | Cân nhắc nếu cần mở rộng leukemia image |
| ALL-IDB | Cần gửi email xin quyền theo usage agreement | |
| SEER (Lymphoma/Myeloma) | Cần ký Data Use Agreement | |
| Ferritin, Serum Iron, TIBC, TSAT, Vitamin B12, Folate, LDH, Haptoglobin, PT, INR, D-Dimer | **Không tìm thấy dataset public nào** chứa các chỉ số này kèm nhãn bệnh (đã tìm kiếm kỹ, chỉ có 1 dataset "70.000 bệnh nhân" nhưng là dữ liệu **tổng hợp/synthetic** từ 1 bài báo, không có link tải công khai) | Có thể cần thu thập dữ liệu bệnh viện thật hoặc chấp nhận khoảng trống này |

## Cấu trúc thư mục

```
Data/
├── README.md                      <- file này
├── eda/                           <- script + báo cáo EDA
│   ├── eda_tabular.py
│   ├── eda_images.py
│   ├── report_tabular.txt
│   └── report_images.txt
├── tabular/
│   ├── anemia_cbc_ml_repo/        <- CBC Test dataset (500x21)
│   ├── anemia_ml_basic_repo/      <- Anemia Dataset (1421x6)
│   ├── physionet_sepsis_2019/     <- 40,336 file time-series, dong mau + CBC + Bilirubin + nhan SepsisLabel
│   ├── kaggle_cbc_vizeno/         <- CBC + Age/Gender (417 dong, 77.5% trung lap)
│   ├── kaggle_covid_cbc/          <- CBC subset + Outcome COVID (103 dong)
│   └── rheumatic_dataverse/       <- CRP/ESR + Age/Gender + nhan 7 lop benh tu mien (12,085 dong)
├── images/
│   ├── mds_bone_marrow/           <- 25,067 ảnh, 33 lớp tế bào tủy xương
│   ├── txl_pbc_repo/              <- ảnh detection WBC/RBC/Platelet (YOLO format)
│   └── pbc_barcelona/             <- 17,093 ảnh, 8 lớp tế bào máu khỏe mạnh, can bang tot
└── _manual_needed/                <- placeholder cho các nguồn cần tải tay (xem bảng trên)
```
