# File tổng hợp link dataset cho Hệ thống AI Hỗ trợ Chẩn đoán Sơ bộ Bệnh lý Huyết học

## I. Clinical_CBC_Data

### Tổng quan
- **Số lượng:** 4 bộ dataset
- **Dạng dữ liệu:** Tabular / Clinical / Laboratory / Synthetic
- **Tổng quy mô:** ~269,119 dòng, đa dạng kích thước cột (từ 14 đến 378 cột)
- **Nguồn:** CDC/NCHS (NHANES), Kaggle

## 1. CBC (Complete Blood Count) - NHANES 2015-2016 CBC_I

### Nguồn thu thập
**Link:** https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2015/DataFiles/CBC_I.htm

### Nội dung data
- **Quy mô:** 9,165 dòng × 21 cột (1 ID + 20 chỉ số sinh huyết)
- **Định dạng:** `.XPT` (SAS Transport)
- **Mô tả:** Dữ liệu CBC đầy đủ với 5 phân biệt bạch cầu (Lympho, Mono, Neutrophil, Eosinophil, Basophil cả dạng % và số lượng tuyệt đối), cùng các chỉ số hồng cầu (HCT, RDW) và tiểu cầu (MPV).

### Phân tích data
- Cấu trúc: 1 cột định danh `SEQN`, 20 cột numeric thuần túy
- Bao phủ đầy đủ các chỉ số CBC chuẩn y khoa, bao gồm cả 5 dòng bạch cầu
- Thiếu cột target/disease → cần merge với dataset khác để có nhãn chẩn đoán
- Có thể liên kết với Demographics File (DEMO_I) qua khóa chung `SEQN`

### EDA
- **Artifact kỹ thuật:** Giá trị `5.397605346934028e-79` xuất hiện trong 3,961 dòng (43.2%), là placeholder hệ thống NHANES
  - Nếu giữ nguyên và ép kiểu numeric sẽ underflow về ~0, gây nhiễu thống kê
  - Cột bị ảnh hưởng: `LBDBANO`, `LBDEONO`, `LBDNENO`, `LBDMONO`, `LBXEOPCT`, `LBXMOPCT`, `LBXNEPCT`, `LBXRBCSI`, `LBXLYPCT`
- **Missing data:** ~1,048 dòng thiếu ở hầu hết các cột (11.4%)
- **Biological outliers:** WBC range 1.40–117.20 (10^3/uL), nằm trong giới hạn sinh lý nhưng cần kiểm tra tính hợp lệ lâm sàng
- **Khuyến nghị:** Thay artifact bằng `NaN` đồng nhất, dùng MICE/KNN imputation, flag outlier thay vì xóa

---

## 2. Diseases and Symptoms Dataset

### Nguồn thu thập
**Link:** https://www.kaggle.com/datasets/dhivyeshrk/diseases-and-symptoms-dataset

### Nội dung data
- **Quy mô:** 246,945 dòng × 378 cột (1 target + 377 triệu chứng)
- **Định dạng:** Tabular / Binary (0/1)
- **Mô tả:** Bảng nhị phân one-hot encode mối quan hệ bệnh–triệu chứng, gồm ~773 bệnh và ~377 triệu chứng.

### Phân tích data
- Dữ liệu artificially generated / synthetic
- Mỗi dòng tương ứng một bệnh (single-label), các triệu chứng được one-hot encode
- Ma trận rất thưa (sparsity >95%)
- Phù hợp cho symptom → disease classification, multi-class classification, clinical decision-support prototype
- Không phải dữ liệu bệnh nhân thực

### EDA
- **Sparsity:** Tỷ lệ 0 chiếm đa số (>95%), highly sparse
- **Class imbalance:** Nhiều lớp bệnh (~773), tỷ lệ max/min rất cao → nguy cơ model thiên về majority class
- **Quasi-constant features:** Nhiều triệu chứng có tỷ lệ xuất hiện <1% hoặc >99% → không phân biệt
- **Co-occurrence:** Triệu chứng cùng nhóm lâm sàng (respiratory, cardiovascular, neurological) có xu hướng xuất hiện đồng thời
- **Task type:** Hiện tại single-label, nhưng thực tế bệnh nhân có thể mắc nhiều bệnh đồng thời
- **Khuyến nghị:** Loại bỏ quasi-constant features, dùng TruncatedSVD nếu còn >100 features, baseline với XGBoost/RF, đánh giá bằng macro-F1/weighted-F1

---

## 3. Laboratory Data

### Nguồn thu thập
**Link:** https://www.kaggle.com/datasets/klingill/laboratory-data

### Nội dung data
- **Quy mô:** 12,009 dòng × 14 cột (1 target + 12 numeric + 1 categorical `Gender`)
- **Định dạng:** Tabular / Laboratory
- **Mô tả:** Dữ liệu xét nghiệm laboratory phục vụ AI-based risk prediction và feature selection, bao gồm CBC-related (RBC, WBC, Hemoglobin) và các xét nghiệm khác (AST, ALT, Cholesterol, Glucose, Lipase, Creatinine, Troponin).

### Phân tích data
- Có nhiều laboratory features nhưng không phải full CBC và không chuyên biệt cho leukemia
- Target: `Disease` (có trailing space trong raw data)
- Categorical: chỉ có `Gender` (Male/Female/Other)
- Thiếu cột target chi tiết cho chẩn đoán huyết học chuyên sâu

### EDA
- **Scale disparity:** Các chỉ số có biên độ rất khác nhau (Troponin 0–10, WBC 2,000–50,000, Glucose 30–500) → cần scaling
- **Physiological outliers:** 
  - Hemoglobin: 7–20 g/dL
  - WBC: 2,000–50,000 /uL
  - Troponin: 0–10 ng/mL (>0.04 đã bất thường lâm sàng)
- **Missing values:** Một số cột có blank cells
- **Khuyến nghị:** Fix trailing space cột `Disease`, dùng StandardScaler/RobustScaler, winsorize outlier, KNN/MICE imputation, One-Hot cho `Gender`

---

## 4. Personalized Medication Dataset

### Nguồn thu thập
**Link:** https://www.kaggle.com/datasets/ziya07/personalized-medication-dataset

### Nội dung data
- **Quy mô:** 1,000 dòng × 17 cột
- **Định dạng:** Tabular / Clinical / Medication
- **Mô tả:** Dữ liệu về medication recommendation bao gồm demographics (Age, Gender, Weight, Height, BMI), medical history (chronic conditions, drug allergies, genetic disorders), symptoms, diagnosis, recommended medication, dosage, duration, effectiveness, recovery time và adverse reactions.

### Phân tích data
- Phù hợp cho module Patient Information, Medical History, Symptoms và Medication
- Không có bộ CBC đầy đủ
- Cột BMI cần validate với Height/Weight
- Các cột `Symptoms`, `Drug_Allergies`, `Chronic_Conditions`, `Genetic_Disorders` dạng chuỗi phân tách bằng dấu phẩy → cần tách thành binary indicators
- Thiếu thông tin quan trọng: tiền sử bệnh lý, vitals (HR, BP, SpO2, Temp), thời gian, metadata

## II. Hematology_Biochemical_Coagulation

## 1. CBC Test dataset

**Nguồn thu thập**: Kaggle `abdelrhmankaram/complete-blood-count-cbc-test`, lấy lại qua repo GitHub `Pfuglo1/anemia-detection-cbc-ml` (repo tái sử dụng dataset gốc, đã có sẵn notebook phân tích).

**Nội dung data**: File `cbc information.xlsx` — 500 dòng × 21 cột: `ID, WBC, LYMp, MIDp, NEUTp, LYMn, MIDn, NEUTn, RBC, HGB, HCT, MCV, MCH, MCHC, RDWSD, RDWCV, PLT, MPV, PDW, PCT, PLCR`. Đầy đủ bộ chỉ số CBC chuẩn (tỷ lệ % và số tuyệt đối của bạch cầu, các chỉ số hồng cầu, tiểu cầu).

**Review data có gì**:
- Không có giá trị thiếu (missing = 0), không có dòng trùng lặp.
- **Không có cột nhãn bệnh** — cần tự sinh nhãn (VD ngưỡng lâm sàng HGB/HCT) hoặc dùng làm dữ liệu unsupervised/phân cụm.
- **Phát hiện lỗi chất lượng nghiêm trọng**: nhiều giá trị vượt ngoài khoảng sinh học hợp lý — `HGB` min = **-10** (âm), `MCV` min = **-79.3** (âm), `NEUTp` (đáng lẽ 0–100%) có max = **5317**, `HCT` max = **3715**, `MPV` max = **919**. Đây gần như chắc chắn là lỗi nhập liệu/sai đơn vị trong dataset gốc, không phải outlier lâm sàng thật — bắt buộc phải lọc theo range hợp lý trước khi dùng.

**EDA sơ bộ** (script: `eda/eda_tabular.py`, output: `eda/report_tabular.txt`):
- Không tìm thấy tương quan nào giữa các chỉ số vượt |r| > 0.85 — đa cộng tuyến không phải vấn đề chính.
- Số lượng outlier theo IQR (1.5×) dao động 1.6%–8.2% tuỳ cột, cao nhất ở `MIDn` (8.2%) và `RDWSD` (7.2%).

---

## 2. Anemia Dataset

**Nguồn thu thập**: Kaggle `biswaranjanrao/anemia-dataset`, lấy lại qua repo GitHub `maladeep/anemia-detection-with-machine-learning`.

**Nội dung data**: File `anemia data from Kaggle.csv` — 1.421 dòng × 6 cột: `Gender, Hemoglobin, MCH, MCHC, MCV, Result`. `Result` là nhãn nhị phân (có/không thiếu máu).

**Review data có gì**:
- Không có giá trị thiếu.
- **Trùng lặp nặng: 887/1.421 dòng bị trùng lặp hoàn toàn (62.4%)** — sau khi loại trùng chỉ còn khoảng 534 dòng thật sự khác nhau.
- Chỉ có 5 feature huyết học (thiếu RBC, WBC, PLT, RDW... so với schema 18 chỉ số CBC trong tài liệu gốc dự án) — chỉ đủ phân biệt "có/không thiếu máu", không đủ phân loại 9 loại thiếu máu riêng biệt.
- Repo đi kèm đã có sẵn model huấn luyện (`random_forest_model.pkl`) và 2 notebook minh hoạ.

**EDA sơ bộ**:
- Phân bố `Gender`: 1 = 740, 0 = 681 (tương đối cân bằng).
- Phân bố nhãn `Result` (trên dữ liệu còn trùng lặp, cần tính lại sau khi loại trùng): 0 = 801 (56.4%), 1 = 620 (43.6%).
- Hemoglobin trung bình theo nhóm Gender × Result cho thấy nhóm Result=1 (thiếu máu) có Hb thấp hơn rõ rệt ở cả 2 giới — xu hướng hợp lý về mặt lâm sàng.

---

## 3. PhysioNet Sepsis 2019

**Nguồn thu thập**: PhysioNet/Computing in Cardiology Challenge 2019 — [physionet.org/content/challenge-2019/1.0.0](https://physionet.org/content/challenge-2019/1.0.0/), giấy phép CC BY 4.0, **không cần credential** (khác MIMIC-IV). Tự động tải bằng `curl --parallel` (40.336 request riêng lẻ, không có sẵn file zip gộp).

**Nội dung data**: 40.336 file `.psv` (20.336 ở `training_setA/`, 20.000 ở `training_setB/`), mỗi file là 1 bệnh nhân, các dòng là chuỗi thời gian đo theo giờ (`ICULOS`). Cột liên quan tới dự án: `HR, O2Sat, Temp, SBP, MAP, DBP, Resp` (sinh hiệu), `Bilirubin_total, Bilirubin_direct, AST, Alkalinephos` (sinh hóa gan), `Hct, Hgb, WBC, Platelets` (CBC rút gọn), **`PTT, Fibrinogen`** (đông máu), `Age, Gender` (thông tin bệnh nhân), **`SepsisLabel`** (nhãn nhị phân theo từng giờ).

**Review data có gì**:
- Đây là nguồn **duy nhất** trong toàn bộ kho bù được một phần chỉ số **đông máu** (Fibrinogen chắc chắn khớp; PTT có khả năng tương đương aPTT nhưng cần xác minh vì PTT và aPTT về mặt xét nghiệm không hoàn toàn là một).
- Có nhãn outcome thật (`SepsisLabel`) nhưng là **nhiễm trùng huyết**, không phải bệnh lý huyết học trong 9 nhóm bệnh mục tiêu của dự án.
- Kiểm tra ban đầu (không rỗng) cho thấy 100% file tải thành công, nhưng **EDA bằng notebook sau đó phát hiện 5/40.336 file thực chất là trang lỗi HTML** (không rỗng nhưng sai nội dung, lọt qua bước kiểm tra ban đầu) — đã xác định và tải lại đúng cả 5 file, xác minh lại toàn bộ 40.336 file hợp lệ 100%. Bài học: kiểm tra "không rỗng" là chưa đủ, cần kiểm tra nội dung/parse thử.

**EDA sơ bộ** (xem `EDA/03_physionet_sepsis_2019.ipynb` — lấy mẫu ngẫu nhiên 2.000/40.336 bệnh nhân để phân tích nhanh):
- Dữ liệu dạng time-series đa biến, **tỷ lệ missing rất cao** ở các chỉ số xét nghiệm không đo mỗi giờ (Fibrinogen, PTT, Bilirubin) — cần chiến lược xử lý riêng (forward-fill, hoặc chỉ giữ dòng có đo xét nghiệm) trước khi coi là dữ liệu bảng tĩnh.
- Kích thước: 336MB.

---

## 4. Kaggle CBC (vizeno)

**Nguồn thu thập**: Kaggle `vizeno/complete-blood-count-cbc-dataset` — người dùng tự tải tay qua trình duyệt (Kaggle yêu cầu đăng nhập, không tự động hoá được).

**Nội dung data**: File `blood_count_dataset.csv` — 417 dòng × 9 cột: `Age, Gender, Hemoglobin, Platelet_Count, White_Blood_Cells, Red_Blood_Cells, MCV, MCH, MCHC`.

**Review data có gì**:
- Không có giá trị thiếu.
- **Trùng lặp cực nặng: 323/417 dòng bị trùng lặp hoàn toàn (77.5%)** — chỉ còn ~94 dòng thật sự khác nhau, đây là mức trùng lặp cao nhất trong toàn bộ kho dữ liệu.
- **Không có cột nhãn bệnh.**
- Có `Age` và `Gender` — bù được một phần nhỏ cho nhóm "thông tin bệnh nhân" đang thiếu.

**EDA sơ bộ**:
- `describe()` cho thấy phân phối các chỉ số nằm trong khoảng sinh học hợp lý (không có giá trị âm/vô lý như bộ CBC Test dataset) — chất lượng giá trị tốt hơn, nhưng số lượng dòng thật sự dùng được lại rất ít do trùng lặp.

---

## 5. Kaggle COVID-19 CBC

**Nguồn thu thập**: Kaggle `tawsifurrahman/covid19-complete-blood-count-clinical-database` — người dùng tự tải tay.

**Nội dung data**: File `COVID-19_CBC_Data.csv` — 103 dòng × 14 cột: `Admission_DATE, Discharge_DATE or date of Death, Outcome, Patient Age, Gender, Sample Collection Date, What kind of Treatment provided, Ventilated (Y/N), Red blood cell distribution width, Monocytes(%), White blood cell count, Platelet Count, Lymphocyte Count, Neutrophils Count`.

**Review data có gì**:
- Không có giá trị thiếu — hiếm gặp so với các bộ khác trong kho.
- Có nhãn **Outcome** thật (Recovered / Not Recovered) — nhưng là outcome điều trị COVID-19, không phải chẩn đoán bệnh huyết học.
- Thiếu nhiều chỉ số CBC cốt lõi so với 2 bộ CBC kia (không có RBC, Hgb, HCT, MCV, MCH, MCHC).
- Cỡ mẫu rất nhỏ (103 dòng) — chỉ phù hợp làm proof-of-concept, không đủ để train model đáng tin cậy.

**EDA sơ bộ**:
- Phân bố nhãn: Recovered 61 (59.2%), Not Recovered 42 (40.8%) — tương đối cân bằng.

---

## 6. Rheumatic & Autoimmune Disease Dataset

**Nguồn thu thập**: Harvard Dataverse, DOI `10.7910/DVN/VM4OR3` — người dùng tự tải tay (khi thử tự động hoá, bị chặn bởi AWS WAF bot-challenge `x-amzn-waf-action: challenge`, không vượt qua được bằng curl).

**Nội dung data**: File `Rheumatic and Autoimmune Disease Dataset.xlsx` — **12.085 dòng × 15 cột**: `Age, Gender, ESR, CRP, RF, Anti-CCP, HLA-B27, ANA, Anti-Ro, Anti-La, Anti-dsDNA, Anti-Sm, C3, C4, Disease`.

**Review data có gì**:
- **Chất lượng tốt nhất trong toàn bộ kho dữ liệu đã thu thập**: 0 dòng trùng lặp, cỡ mẫu lớn (12.085 dòng).
- Có `ESR` và `CRP` thật — 2 chỉ số sinh hóa duy nhất trong kho có dữ liệu thực tế (trước đó hoàn toàn không có nguồn nào).
- Có nhãn `Disease` thật với 7 lớp: Rheumatoid Arthritis, Ankylosing Spondylitis, Sjögren's Syndrome, Psoriatic Arthritis, Normal, Systemic Lupus Erythematosus, Reactive Arthritis.
- **Giới hạn quan trọng**: đây là bệnh **tự miễn/thấp khớp**, không thuộc 9 nhóm bệnh huyết học mục tiêu của dự án — chỉ dùng được để bù chỉ số CRP/ESR làm dữ liệu tham chiếu/huấn luyện phụ (transfer learning, hoặc mở rộng phạm vi hệ thống), không dùng làm nhãn chính cho bài toán chẩn đoán huyết học.
- Có missing value ở các cột huyết thanh học (ESR thiếu 9%, CRP thiếu 20%, các marker khác thiếu 15–43%) — hợp lý vì không phải bệnh nhân nào cũng làm đủ panel xét nghiệm.

**EDA sơ bộ**:
- Phân bố nhãn Disease: Rheumatoid Arthritis 2.848, Ankylosing Spondylitis 2.127, Sjögren's Syndrome 1.852, Psoriatic Arthritis 1.783, Normal 1.604, Systemic Lupus Erythematosus 1.355, Reactive Arthritis 516 — lớp nhỏ nhất vẫn có 516 mẫu, mức mất cân bằng chấp nhận được (khác hẳn tình trạng lệch cực đoan ở các bộ ảnh).
- Thống kê CRP: mean 13.33, std 10.39, min 0.10, max 30.00 (n=9.668 sau loại missing).
- Thống kê ESR: mean 24.21, std 14.37, min 0.00, max 49.00 (n=10.997 sau loại missing).

---

## 7. MDS Bone Marrow Cell Dataset

**Nguồn thu thập**: figshare, DOI `10.6084/m9.figshare.28737170.v1` — bài báo "A large dataset of bone marrow cells in myelodysplastic syndrome for classification systems" (Scientific Data, 2025). Tải tự động bằng curl (link tải trực tiếp qua figshare API).

**Nội dung data**: `dataset_BM_cell_MDS.zip` (giữ nguyên gốc) + đã giải nén — **25.067 ảnh JPEG**, 54 thư mục lớp con (33 loại tế bào × 2 thư mục `main/`+`add/`), gồm cả tế bào bình thường và bất thường đặc trưng của MDS (Blast NOC, Myeloblast, Dysplastic erythroblast, Micromegakaryocyte, Segmented neutrophil...).

**Review data có gì**:
- Đây là nguồn ảnh **duy nhất** trong kho có gán nhãn tế bào bất thường thật sự liên quan đến bệnh lý huyết học (Hội chứng loạn sản tủy).
- Gán nhãn bởi tối đa 3 chuyên gia độc lập — độ tin cậy nhãn cao.

**EDA sơ bộ** (script: `eda/eda_images.py`, output: `eda/report_images.txt`):
- **Mất cân bằng cực đoan**: lớp nhiều nhất `Mature lymphocyte` = 3.958 ảnh (15.83%), lớp ít nhất `Dysplastic megakaryocyte` = **chỉ 1 ảnh** — tỷ lệ lệch **3.958 lần**.
- Nhiều lớp có dưới 10 ảnh (VD `Segmented basophil` add = 2, `Proerythroblast` add = 3, `Mitosis` add = 7) — không đủ để train riêng, bắt buộc phải gộp nhóm hoặc dùng few-shot/augmentation mạnh.

---

## 8. TXL-PBC

**Nguồn thu thập**: GitHub `lugan113/TXL-PBC_Dataset` — dữ liệu gộp/tái gán nhãn từ 4 nguồn công khai (BCCD, BCDD, PBC Barcelona, Raabin-WBC). Tải tự động bằng `git clone`.

**Nội dung data**: `TXL-PBC/images/{train,val,test}` + `TXL-PBC/labels/{train,val,test}` — 1.260 ảnh với 18.143 bounding box annotation dạng **YOLO detection**, chỉ 3 lớp: `WBC (0), RBC (1), Platelet (2)`.

**Review data có gì**:
- Đây là bài toán **object detection** (định vị + đếm tế bào trong ảnh), khác hẳn bản chất với 2 bộ ảnh kia (classification từng ảnh 1 tế bào) — không thể gộp trực tiếp làm cùng 1 pipeline huấn luyện.
- Chỉ phân biệt 3 loại tế bào lớn (không phân loại tiếp neutrophil/eosinophil/lymphocyte...) — muốn phân loại chi tiết hơn phải dùng nguồn khác (VD Raabin, PBC Barcelona).
- Đi kèm sẵn script gốc: `dataset_splits.py`, `baseline_model.py`, `dataset_statistical_analysis.py`.

**EDA sơ bộ**:
- Số ảnh theo split: train 882, val 252, test 126.
- Số bounding box theo lớp (tập train): WBC 908 (7.3%), **RBC 11.220 (89.7%)**, Platelet 382 (3.0%) — RBC áp đảo hoàn toàn (đúng thực tế sinh học), cần class weighting/loss balancing khi huấn luyện detection.

---

## 9. PBC Barcelona

**Nguồn thu thập**: Mendeley Data (Acevedo et al., Hospital Clinic Barcelona), liên kết DOI `snkd93bnjr` — người dùng tự tải tay (khi thử tự động qua Mendeley public API, gặp lỗi 404/chặn JS, không tải được).

**Nội dung data**: `PBC_dataset_normal_DIB/` — **17.093 ảnh JPG** (360×363px, chụp bằng máy CellaVision DM96), 8 thư mục lớp: `basophil, eosinophil, erythroblast, ig (immature granulocytes), lymphocyte, monocyte, neutrophil, platelet`.

**Review data có gì**:
- Toàn bộ mẫu lấy từ người **khỏe mạnh** (không nhiễm trùng, không bệnh huyết học/ung thư, không dùng thuốc tại thời điểm lấy máu) — chỉ dùng để nhận diện loại tế bào nền, **không dùng để phát hiện bất thường/bệnh lý**.
- Gán nhãn bởi bác sĩ giải phẫu bệnh chuyên khoa.

**EDA sơ bộ**:
- Số ảnh theo lớp: neutrophil 3.330, eosinophil 3.117, ig 2.895, platelet 2.348, erythroblast 1.551, monocyte 1.420, basophil 1.218, lymphocyte 1.214.
- Mức mất cân bằng: lệch tối đa ~**2.7 lần** (3.330/1.214) — **cân bằng tốt hơn đáng kể** so với MDS Bone Marrow (3.958 lần), phù hợp làm dữ liệu train/pretrain cho bài toán phân loại bạch cầu.

---
