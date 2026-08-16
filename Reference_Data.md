# File tổng hợp link dataset cho Hệ thống AI Hỗ trợ Chẩn đoán Sơ bộ Bệnh lý Huyết học

## Phạm vi các dataset đã thu thập

### Tổng quan
- **Số lượng:** 4 bộ dataset
- **Dạng dữ liệu:** Tabular / Clinical / Laboratory / Synthetic
- **Tổng quy mô:** ~269,119 dòng, đa dạng kích thước cột (từ 14 đến 378 cột)
- **Nguồn:** CDC/NCHS (NHANES), Kaggle

---

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

### EDA
- **Structural integrity:** 
  - BMI cần validate với Height/Weight, nếu mismatch >1.0 BMI unit → rounding hoặc nhập liệu thủ công
  - Cột multi-value cần tách thành binary indicators
- **Dosage/Duration:** Chứa cả số và đơn vị (`5 mg`, `30 days`) → cần tách thành giá trị số và đơn vị
- **"None" semantics:** `Drug_Allergies`, `Genetic_Disorders`, `Dosage`, `Adverse_Reactions` có nhiều "None" → cần xác định là missing hay thực tế
- **Class imbalance:** Target `Recommended_Medication` có thể lệch
- **Data leakage risk:** `Treatment_Effectiveness`, `Adverse_Reactions` là thông tin sau điều trị, có thể gây leakage nếu dùng làm feature
- **Small sample size:** 1,000 dòng cho multi-class classification → dễ overfitting
- **Khuyến nghị:** Kiểm tra BMI mismatch, tách multi-value columns, giữ "None" như category riêng, cân nhắc drop leakage columns, dùng StandardScaler
