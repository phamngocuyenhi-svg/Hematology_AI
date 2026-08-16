# EDA Report - Tổng hợp phân tích dữ liệu

**Ngày:** 2026-08-16  
**Mục đích:** Tổng hợp phát hiện từ 4 dataset để hỗ trợ bước Data Cleaning, Data Preparing và Modeling.  
**Quy trình:** EDA → Data Cleaning → Data Preparing → Modeling

---

## 1. CBC (Complete Blood Count)

### 1.1 Data Profile
| Chỉ tiêu | Giá trị |
|----------|---------|
| Số dòng | 9,165 |
| Số cột | 21 (1 ID + 20 chỉ số sinh huyết) |
| Cấu trúc | 1 cột định danh `SEQN`, 20 cột numeric |

### 1.2 Phát hiện chính
- **Artifact kỹ thuật:** Giá trị `5.397605346934028e-79` xuất hiện trong **3,961 dòng (43.2%)**. Đây là placeholder hệ thống (phổ biến trong dữ liệu NHANES), không phải giá trị đo lường thực tế.
  - Nếu giữ nguyên và ép kiểu numeric, giá trị sẽ underflow về ~0, gây nhiễu thống kê và mô hình.
  - Cột bị ảnh hưởng: `LBDBANO`, `LBDEONO`, `LBDNENO`, `LBDMONO`, `LBXEOPCT`, `LBXMOPCT`, `LBXNEPCT`, `LBXRBCSI`, `LBXLYPCT` và một số cột khác.
- **Missing data:** ~1,048 dòng thiếu ở hầu hết các cột (11.4%). Một số cột như `LBXMC` có ít missing hơn (1,018).
- **Biological outliers:** Các chỉ số WBC, RBC, HGB, HCT, Platelets có thể chứa outlier sinh học cần review lâm sàng trước khi loại bỏ.
  - Ví dụ: WBC range 1.40–117.20 (đơn vị 10^3/uL), nằm trong giới hạn sinh lý nhưng cần kiểm tra tính hợp lệ theo từng bệnh.

### 1.3 Rủi ro
- Nếu artifact được coi là missing code mà không xử lý đồng nhất, có thể tạo ra bias trong imputation.
- Không có cột target/disease trong dataset này → cần merge với dataset khác (ví dụ Laboratory Data hoặc Personalized Medication) để có label.

### 1.4 Khuyến nghị Cleaning
1. **Artifact handling:** Thay thế toàn bộ `5.397605346934028e-79` bằng `NaN` đồng nhất.
2. **Numeric coercion:** Ép kiểu tất cả cột sang numeric, `errors='coerce'` để bắt giá trị không hợp lệ.
3. **Outlier strategy:** Không xóa vội. Dùng flag/biến nhị phân đánh dấu outlier thay vì loại bỏ.
4. **Imputation:** Cân nhắc MICE hoặc KNN do dữ liệu sinh học có tương quan cao giữa các chỉ số.

---

## 2. Diseases_and_Symptoms

### 2.1 Data Profile
| Chỉ tiêu | Giá trị |
|----------|---------|
| Số dòng | 246,945 |
| Số cột | 378 (1 target + 377 triệu chứng) |
| Kiểu dữ liệu | Bảng nhị phân (0/1), highly sparse |

### 2.2 Phát hiện chính
- **Sparsity:** Ma trận rất thưa. Tỷ lệ 0 chiếm đa số (ước tính >95% tùy phân bố triệu chứng).
- **Class imbalance:** Có nhiều lớp bệnh (ước tính hàng trăm), tỷ lệ max/min rất cao → nguy cơ model thiên về majority class.
- **Quasi-constant features:** Nhiều triệu chứng có tỷ lệ xuất hiện <1% hoặc >99% → không mang thông tin phân biệt.
- **Co-occurrence:** Các triệu chứng cùng nhóm lâm sàng (respiratory, cardiovascular, neurological) có xu hướng xuất hiện đồng thời.
- **Task type:** Hiện tại là single-label classification (mỗi dòng một bệnh), nhưng thực tế bệnh nhân có thể mắc nhiều bệnh đồng thời.

### 2.3 Rủi ro
- **Curse of Dimensionality:** 377 features cho 246k samples, tỷ lệ feature/sample thấp nhưng sparsity cao vẫn gây overfitting với linear models.
- **Sparsity impact:** Gradient-based models (NN, Logistic Regression) khó hội tụ. Tree-based models phù hợp hơn.
- **Label noise:** Nếu dataset được thu thập tự nhiên, có thể có nhiễu nhãn (triệu chứng không đúng với bệnh).

### 2.4 Khuyến nghị Cleaning & Preparing
1. **Feature selection:** Loại bỏ quasi-constant features (variance threshold <0.01).
2. **Dimensionality reduction:** Nếu sau lọc vẫn >100 features, áp dụng TruncatedSVD (phù hợp với sparse binary data) hoặc SelectKBest với mutual_info_classif.
3. **Class imbalance:** Dùng class weights, SMOTE, hoặc stratified sampling.
4. **Baseline model:** Random Forest hoặc XGBoost (robust với sparse binary data).
5. **Evaluation:** macro-F1 hoặc weighted-F1 thay vì accuracy.

---

## 3. Laboratory Data

### 3.1 Data Profile
| Chỉ tiêu | Giá trị |
|----------|---------|
| Số dòng | 12,009 |
| Số cột | 14 (1 target + 12 numeric + 1 categorical `Gender`) |
| Target | `Disease` (có trailing space trong raw data) |

### 3.2 Phát hiện chính
- **Scale disparity:** Các chỉ số có biên độ rất khác nhau:
  - Troponin: 0–10 (ng/mL)
  - WBC: 2,000–50,000 (/uL)
  - Glucose: 30–500 (mg/dL)
  - → Cần scaling/standardization trước khi đưa vào model gradient-based.
- **Physiological outliers:** Cần kiểm tra phạm vi hợp lý:
  - Hemoglobin: 7–20 g/dL
  - WBC: 2,000–50,000 /uL
  - Troponin: 0–10 ng/mL (giá trị >0.04 đã là bất thường lâm sàng)
- **Categorical:** Chỉ có `Gender` (Male/Female/Other). Cần encoding (One-Hot hoặc Target Encoding).
- **Missing values:** Một số cột có blank cells, cần xử lý trước khi modeling.

### 3.3 Feature-Disease Relevance
- Mỗi chỉ số có khả năng phân biệt khác nhau giữa các nhóm bệnh.
- Hệ số biến thiên (CV) trên mean của từng bệnh có thể dùng làm proxy cho discriminative power.
- Các chỉ số như Troponin, WBC, Glucose có khả năng cao là strong predictors.

### 3.4 Rủi ro
- **Scale mismatch:** Model có thể bị bias về cột có range lớn (WBC) nếu không scale.
- **Outlier interpretation:** Giá trị vượt phạm vi sinh lý có thể là lỗi nhập liệu hoặc ca bệnh lý đặc biệt → cần distinguish trước khi xử lý.
- **Missing mechanism:** Nếu missing không hoàn toàn ngẫu nhiên (MNAR), imputation đơn giản có thể gây bias.

### 3.5 Khuyến nghị Cleaning & Preparing
1. **Column fix:** Loại bỏ trailing space khỏi `Disease ` → `Disease`.
2. **Scaling:** StandardScaler hoặc RobustScaler (nếu còn outlier sau khi winsorize).
3. **Outlier:** Winsorize ở phân vi 5%/95% hoặc flag thay vì xóa.
4. **Imputation:** KNN/MICE phù hợp với dữ liệu y tế có tương quan.
5. **Encoding:** One-Hot cho `Gender`.

---

## 4. Personalized Medication Dataset

### 4.1 Data Profile
| Chỉ tiêu | Giá trị |
|----------|---------|
| Số dòng | 1,000 |
| Số cột | 17 |
| Target | `Recommended_Medication` |

### 4.2 Phát hiện chính
- **Structural integrity:**
  - Cột BMI cần validate với Height/Weight. Nếu mismatch >1.0 BMI unit → có thể do rounding hoặc nhập liệu thủ công.
  - Cột `Symptoms`, `Drug_Allergies`, `Chronic_Conditions`, `Genetic_Disorders` dạng chuỗi phân tách bằng dấu phẩy → cần tách thành binary indicators.
- **Dosage/Duration:** Chứa cả số và đơn vị (ví dụ: `5 mg`, `30 days`) → cần tách thành 2 cột: giá trị số và đơn vị.
- **"None" semantics:**
  - `Drug_Allergies`, `Genetic_Disorders`, `Dosage`, `Adverse_Reactions` có nhiều giá trị "None".
  - Cần xác định: là thiếu dữ liệu hay thuộc tính thực tế (không có dị ứng/không có tác dụng phụ)?
- **Class imbalance:** Target `Recommended_Medication` có thể lệch → cần kiểm tra phân bố cụ thể.
- **Missing context:** Thiếu thông tin quan trọng như:
  - Tiền sử bệnh lý (comorbidity)
  - Vitals (HR, BP, SpO2, Temp)
  - Thời gian (admission date, duration of illness)
  - Metadata (bệnh viện, bác sĩ, phương pháp điều trị)

### 4.3 Rủi ro
- **Data leakage:** Nếu dùng `Treatment_Effectiveness` hoặc `Adverse_Reactions` làm feature cho model dự đoán medication, có thể gây leakage (thông tin từ sau điều trị).
- **Small sample size:** Chỉ 1,000 dòng cho multi-class classification → dễ overfitting.
- **None handling:** Nếu "None" được xử lý như missing và impute, có thể làm sai lệch distribution.

### 4.4 Khuyến nghị Cleaning & Preparing
1. **Structural:** Kiểm tra BMI mismatch; nếu >5% thì cần review lại công thức hoặc nhập liệu.
2. **Feature extraction:**
   - Tách `Dosage` → `Dosage_Value` (float) + `Dosage_Unit` (category).
   - Tách `Duration` → `Duration_Days` (int) + `Duration_Unit` (category).
   - Tách `Symptoms` thành top N binary columns (multi-hot encoding).
3. **None strategy:** Giữ "None" như một category riêng nếu nó mang thông tin lâm sàng (không có dị ứng ≠ dị ứng nhẹ).
4. **Drop leakage columns:** Cân nhắc loại bỏ `Treatment_Effectiveness`, `Adverse_Reactions` khỏi training features nếu model chỉ dự đoán medication.
5. **Scaling:** StandardScaler cho numeric features.
6. **Target encoding:** LabelEncoder hoặc One-Hot cho `Recommended_Medication` tùy model.

---

## 5. Tổng kết & Khuyến nghị bước tiếp theo

### 5.1 Cross-cutting Issues
| Vấn đề | CBC | Diseases_and_Symptoms | Laboratory Data | Personalized Medication |
|--------|-----|----------------------|-----------------|------------------------|
| Artifact/Technical noise | High | Low | Low | Low |
| Missing data | Medium | Low | Medium | Medium |
| Outliers | Medium | Low | High | Low |
| Class imbalance | N/A | High | Medium | Medium |
| Sparsity | Low | High | Low | Medium |
| Scale mismatch | Medium | N/A | High | Medium |

### 5.2 Priority Actions
1. **Artifact sanitization (CBC):** Thay artifact `5.397605346934028e-79` bằng `NaN`. Đây là bước quan trọng nhất để tránh nhiễu thống kê.
2. **Column integrity (Laboratory + Personalized):** Fix trailing spaces, tách cột hỗn hợp (Dosage/Duration), đảm bảo BMI khớp Height/Weight.
3. **Feature extraction (Personalized + Diseases_and_Symptoms):**
   - Tách multi-value columns thành binary indicators.
   - Loại bỏ quasi-constant features.
4. **Outlier strategy:** Dùng clinical plausibility bounds thay vì xóa dòng. Flag extreme values để model biết đây là ca đặc biệt.
5. **Encoding & Scaling:**
   - Categorical: One-Hot hoặc Target Encoding.
   - Numeric: StandardScaler/RobustScaler.
6. **Imputation:** Ưu tiên KNN/MICE cho dữ liệu y tế có tương quan. Tránh mean/median đơn giản nếu missing không ngẫu nhiên.

### 5.3 Modeling Readiness
- **Diseases_and_Symptoms:** Sẵn sàng cho baseline sau khi loại bỏ quasi-constant + feature selection. Dùng XGBoost/RF.
- **Laboratory Data:** Sẵn sàng sau khi scaling + imputation. Phù hợp cho XGBoost, RF, hoặc Neural Network nếu có thêm data.
- **Personalized Medication:** Cần thêm data hoặc augmentation trước khi training do sample size nhỏ (1,000). Cân nhắc transfer learning từ dataset khác.
- **CBC:** Cần merge với target từ dataset khác trước khi có thể training.

### 5.4 Next Steps
1. Hoàn thành `Dataset_cleaning.ipynb` theo checklist từng dataset.
2. Tạo `Dataset_preparing.ipynb` cho imputation, encoding, scaling.
3. Định nghĩa train/val/test split strategy (stratified, có thể nhóm theo bệnh).
4. Baseline modeling với các model phù hợp từng dataset.
5. Đánh giá bằng metrics phù hợp: macro-F1 / weighted-F1 / ROC-AUC tùy imbalance level.

---

**Lưu ý:** Tất cả phân tích trên chỉ mang tính khám phá. Mọi quyết định cleaning cần có xác nhận từ domain expert (bác sĩ/lâm sàng) trước khi áp dụng, đặc biệt với outlier handling và artifact replacement.
