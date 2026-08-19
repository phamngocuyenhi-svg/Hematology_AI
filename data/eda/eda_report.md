# EDA Report - Tổng hợp phân tích dữ liệu

**Ngày:** 2026-08-19  
**Mục đích:** Tổng hợp phát hiện từ 4 dataset để hỗ trợ bước Data Cleaning, Data Preparing và Modeling.  
**Nguồn:** `I_CBC.ipynb`, `II_diseases_and_symptoms.ipynb`, `III_laboratory_data.ipynb`, `IV_personalized_medication_dataset.ipynb`  
**Quy trình:** EDA → Data Cleaning → Data Preparing → Modeling

---

## 1. CBC (Complete Blood Count)

### 1.1 Data Profile
| Chỉ tiêu | Giá trị |
|----------|---------|
| Nguồn | `Dataset/Data/CBC.csv` (NHANES-style) |
| Số dòng | 9,165 |
| Số cột | 21 (1 ID + 20 chỉ số sinh huyết) |
| Cấu trúc | 1 cột định danh `SEQN`, 20 cột numeric |
| Nhãn bệnh | Không có |

### 1.2 Phát hiện chính
- **Artifact kỹ thuật:** Giá trị `5.397605346934028e-79` xuất hiện ở **4,284 ô** (~43% dòng), là placeholder hệ thống NHANES. Nếu giữ nguyên sẽ underflow về ~0, gây nhiễu thống kê và mô hình.
  - Cột bị ảnh hưởng: `LBDBANO`, `LBDEONO`, `LBDNENO`, `LBDMONO`, `LBXEOPCT`, `LBXMOPCT`, `LBXNEPCT`, `LBXRBCSI`, `LBXLYPCT` và các cột khác.
- **Missing data:** **1,018 dòng (11.1%)** thiếu hoàn toàn (all NaN) - không có kết quả xét nghiệm. Sau khi xóa, các cột còn lại có tỷ lệ missing thấp (0.38% - 47.7%).
- **Duplicates:** 0 dòng trùng lặp hoàn toàn.
- **Biological outliers:** **96.5% dòng (7,860/8,147)** có ≥1 giá trị ngoài range sinh lý tham khảo. Top outlier: `LBXMOPCT` (46.2%), `LBXNEPCT` (42.3%), `LBXMCHSI` (35.4%).
  - Ví dụ: WBC range 1.40–117.20 (10^3/uL), nằm trong giới hạn sinh lý nhưng cần kiểm tra tính hợp lệ theo từng bệnh.
- **Tương quan:** Các chỉ số cùng nhóm có tương quan cao (HGB-HCT, MCV-MCH, WBC-Neutrophil).

### 1.3 Rủi ro
- Artifact gây nhiễu nếu không xử lý đồng nhất → bias trong imputation.
- Không có target → cần merge với dataset khác để có nhãn bệnh.

### 1.4 Khuyến nghị Cleaning
1. **Artifact:** Thay thế toàn bộ `5.397605346934028e-79` → `NaN`.
2. **Numeric coercion:** `pd.to_numeric(errors='coerce')`.
3. **Missing:** Xóa dòng all-NaN (1,018 dòng). Giữ lại dòng có ≥1 giá trị hợp lệ.
4. **Outlier:** Thêm cột `outlier_flag` đánh dấu, không xóa.
5. **Imputation:** MICE/KNN do tương quan cao giữa các chỉ số CBC.

---

## 2. Diseases_and_Symptoms

### 2.1 Data Profile
| Chỉ tiêu | Giá trị |
|----------|---------|
| Nguồn | `Dataset/Data/diseases_and_symptoms.csv` |
| Số dòng | 246,945 |
| Số cột | 378 (1 target + 377 triệu chứng) |
| Kiểu dữ liệu | Bảng nhị phân (0/1), highly sparse |
| Nhãn bệnh | Có - cột `diseases` (773 lớp) |

### 2.2 Phát hiện chính
- **Missing values:** 0 - không có giá trị thiếu.
- **Duplicates:** **57,298 hàng trùng lặp hoàn toàn (~23.2%)**. Cần xem xét có phải nhiễu hay mẫu hợp lệ trước khi loại bỏ.
- **Giá trị vô lý:** 0 - tất cả triệu chứng nằm trong {0, 1}, không có outlier.
- **Phân bố nhãn:** 773 lớp bệnh, phân bổ khá đồng đều (~1,200 mẫu/lớp ở top), không quá lệch cực đoan nhưng số lớp lớn gây thách thức cho phân loại.
- **Sparsity:** Tỷ lệ 0 chiếm đa số (>95%). Có quasi-constant features (tần suất <1% hoặc >99%).
- **Ma trận tương quan:** Cần kiểm tra các cặp triệu chứng tương quan mạnh (>0.7) để tránh đa cộng tuyến.

### 2.3 Rủi ro
- **Curse of Dimensionality:** 377 features cho 246k samples, sparsity cao vẫn gây overfitting với linear models.
- **Sparsity impact:** Gradient-based models khó hội tụ. Tree-based models phù hợp hơn.
- **Duplicates:** 23.2% trùng lặp có thể gây bias nếu không xử lý.

### 2.4 Khuyến nghị Cleaning & Preparing
1. **Duplicate removal:** Loại bỏ 57,298 hàng trùng lặp.
2. **Memory optimization:** Đọc với `dtype=bool` cho symptoms, `dtype=category` cho diseases.
3. **Feature selection:** Loại bỏ quasi-constant features (variance threshold <0.01).
4. **Dimensionality reduction:** TruncatedSVD hoặc SelectKBest nếu sau lọc vẫn >100 features.
5. **Baseline model:** Random Forest hoặc XGBoost.
6. **Evaluation:** macro-F1 hoặc weighted-F1.

---

## 3. Laboratory Data

### 3.1 Data Profile
| Chỉ tiêu | Giá trị |
|----------|---------|
| Nguồn | `Dataset/Data/laboratory_data.csv` |
| Số dòng | 12,009 |
| Số cột | 14 (1 target + 12 numeric + 1 categorical `Gender`) |
| Target | `Disease` (có trailing space trong raw data, đã strip) |
| Số lớp | 9 |

### 3.2 Phát hiện chính
- **Missing values:** 0 - toàn bộ dữ liệu không có giá trị thiếu.
- **Duplicates:** 0 hàng trùng lặp hoàn toàn.
- **Biological outliers:** Có giá trị nằm ngoài khoảng sinh học (Hemoglobin max 50, RBC max 34, WBC max 27901). Sau cleaning: **2,547 dòng (21.2%)** có ≥1 outlier được đánh dấu.
- **Phân bố nhãn:** Lớp `Anemia` chiếm tỷ trọng cao nhất (2,979 mẫu), các lớp còn lại dao động từ 697 (`Cardiovascular disease`) đến 1,555 (`Heart attack`). Tập dữ liệu có xu hướng lệch nhẹ về lớp đa số.
- **Scale disparity:** Các chỉ số có biên độ rất khác nhau (Troponin 0-10, WBC 500-100000, Glucose 20-500).
- **Categorical:** Chỉ có `Gender` (Male/Female/Other). Cần encoding.

### 3.3 Rủi ro
- **Scale mismatch:** Model có thể bị bias về cột có range lớn (WBC) nếu không scale.
- **Outlier interpretation:** Giá trị vượt phạm vi sinh lý có thể là lỗi nhập liệu hoặc ca bệnh lý đặc biệt.
- **Class imbalance:** Lệch nhẹ về lớp Anemia.

### 3.4 Khuyến nghị Cleaning & Preparing
1. **Column fix:** Đã strip trailing space khỏi tên cột.
2. **Scaling:** StandardScaler hoặc RobustScaler.
3. **Outlier:** Đã thêm cột `outlier_flag` đánh dấu, không xóa.
4. **Imputation:** Không cần (0 missing).
5. **Encoding:** One-Hot cho `Gender`.

---

## 4. Personalized Medication Dataset

### 4.1 Data Profile
| Chỉ tiêu | Giá trị |
|----------|---------|
| Nguồn | `Dataset/Data/personalized_medication_dataset.csv` |
| Số dòng | 1,000 |
| Số cột | 17 |
| Nhãn bệnh | Có - `Diagnosis` (5 lớp) và `Recommended_Medication` (3 lớp) |

### 4.2 Phát hiện chính
- **Missing values:** Có ở 5+ cột: `Chronic_Conditions` (246), `Drug_Allergies` (324), `Genetic_Disorders` (339), `Recommended_Medication` (263), `Dosage` (195), `Duration` (257).
- **Duplicates:** 0 hàng trùng lặp.
- **Giá trị vô lý:** Tất cả đặc trưng số (Age, Weight_kg, Height_cm, BMI, Recovery_Time_Days) đều nằm trong khoảng sinh học hợp lý.
- **Phân bố nhãn:** 
  - `Diagnosis` (5 lớp): Cân bằng tốt (~180-220 mẫu/lớp: Arthritis 218, Inflammation 202, Depression 202, Infection 194, Hypertension 184).
  - `Recommended_Medication` (3 lớp): Amoxicillin 254, Amlodipine 245, Ibuprofen 238.
- **Structural issues:**
  - Cột `Dosage`, `Duration` dạng chuỗi (ví dụ: `5 mg`, `30 days`) → cần tách thành số + đơn vị.
  - Cột `Symptoms`, `Drug_Allergies`, `Chronic_Conditions`, `Genetic_Disorders` dạng chuỗi phân tách bằng dấu phẩy → cần tách thành binary indicators.
  - Nhiều giá trị "None" trong các cột text → cần xác định là missing hay category thực tế.

### 4.3 Rủi ro
- **Data leakage:** `Treatment_Effectiveness`, `Adverse_Reactions` có thể gây leakage nếu dùng làm feature.
- **Small sample size:** Chỉ 1,000 dòng → dễ overfitting.
- **None handling:** Nếu "None" được xử lý như missing và impute, có thể làm sai lệch distribution.

### 4.4 Khuyến nghị Cleaning & Preparing
1. **Structural:** Strip whitespace từ tên cột và giá trị text.
2. **Missing values:** Impute categorical/text với `"Unknown"`.
3. **Feature extraction:**
   - Tách `Dosage` → `Dosage_Value` + `Dosage_Unit`.
   - Tách `Duration` → `Duration_Days` + `Duration_Unit`.
   - Tách `Symptoms` thành binary indicators (multi-hot).
4. **None strategy:** Giữ "None" như category riêng nếu mang thông tin lâm sàng.
5. **Drop leakage columns:** Cân nhắc loại bỏ `Treatment_Effectiveness`, `Adverse_Reactions` khỏi training features.
6. **Scaling:** StandardScaler cho numeric features.

---

## 5. Tổng kết & Khuyến nghị bước tiếp theo

### 5.1 Cross-cutting Issues
| Vấn đề | CBC | Diseases_and_Symptoms | Laboratory Data | Personalized Medication |
|--------|-----|----------------------|-----------------|------------------------|
| Artifact/Technical noise | High (4,284 values) | Low | Low | Low |
| Missing data | Medium (11.1% rows) | Low (0) | Low (0) | Medium (5+ cols) |
| Outliers | High (96.5% rows) | Low | Medium (21.2% rows) | Low |
| Duplicates | Low (0) | High (23.2%) | Low (0) | Low (0) |
| Class imbalance | N/A | High (773 classes) | Medium (9 classes, Anemia dominant) | Low (5-3 classes, balanced) |
| Sparsity | Low | High | Low | Medium |
| Scale mismatch | Medium | N/A | High | Medium |

### 5.2 Priority Actions
1. **Artifact sanitization (CBC):** Thay artifact `5.397605346934028e-79` bằng `NaN`. Đây là bước quan trọng nhất để tránh nhiễu thống kê.
2. **Duplicate removal (Diseases_and_Symptoms):** Loại bỏ 57,298 hàng trùng lặp.
3. **Column integrity (Laboratory + Personalized):** Fix trailing spaces, tách cột hỗn hợp (Dosage/Duration).
4. **Outlier strategy:** Dùng clinical plausibility bounds thay vì xóa dòng. Flag extreme values.
5. **Encoding & Scaling:**
   - Categorical: One-Hot hoặc Target Encoding.
   - Numeric: StandardScaler/RobustScaler.
6. **Imputation:** Ưu tiên KNN/MICE cho dữ liệu y tế có tương quan.

### 5.3 Modeling Readiness
- **Diseases_and_Symptoms:** Sẵn sàng cho baseline sau khi loại bỏ duplicates + quasi-constant + feature selection. Dùng XGBoost/RF.
- **Laboratory Data:** Sẵn sàng sau khi scaling + outlier flagging. Phù hợp cho XGBoost, RF, hoặc Neural Network.
- **Personalized Medication:** Cần thêm data hoặc augmentation trước khi training do sample size nhỏ (1,000). Cân nhắc transfer learning.
- **CBC:** Cần merge với target từ dataset khác trước khi có thể training.

### 5.4 Next Steps
1. Hoàn thành `Dataset_cleaning.ipynb` theo checklist từng dataset.
2. Tạo `Dataset_preparing.ipynb` cho imputation, encoding, scaling.
3. Định nghĩa train/val/test split strategy (stratified, có thể nhóm theo bệnh).
4. Baseline modeling với các model phù hợp từng dataset.
5. Đánh giá bằng metrics phù hợp: macro-F1 / weighted-F1 / ROC-AUC tùy imbalance level.

---

**Lưu ý:** Tất cả phân tích trên chỉ mang tính khám phá. Mọi quyết định cleaning cần có xác nhận từ domain expert (bác sĩ/lâm sàng) trước khi áp dụng, đặc biệt với outlier handling và artifact replacement.
