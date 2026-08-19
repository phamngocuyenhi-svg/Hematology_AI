# Data Cleaning Report - Tổng hợp phân tích làm sạch dữ liệu

**Ngày:** 2026-08-19  
**Mục đích:** Tổng hợp quy trình và kết quả làm sạch từ 4 dataset để chuẩn bị cho Data Preparing và Modeling.  
**Nguồn:** `I_clean_cbc.ipynb`, `II_clean_diseases_and_symptoms.ipynb`, `III_clean_laboratory_data.ipynb`, `IV_clean_personalized_medication_dataset.ipynb`  
**Quy trình:** EDA → Data Cleaning → Data Preparing → Modeling

---

## 1. CBC (Complete Blood Count)

### 1.1 Data Profile
| Chỉ tiêu | Trước | Sau |
|----------|-------|-----|
| Nguồn | `Dataset/Data/CBC.csv` | `Dataset/Clean_Data/CBC_clean.csv` |
| Số dòng | 9,165 | 8,147 |
| Số cột | 21 | 22 (thêm `outlier_flag`) |
| Cấu trúc | 1 ID + 20 numeric | 1 ID + 20 numeric + 1 flag |
| Nhãn bệnh | Không có | Không có |

### 1.2 Vấn đề phát hiện từ EDA
| # | Vấn đề | Mô tả | Mức độ |
|---|--------|-------|--------|
| 1 | Artifact kỹ thuật | Giá trị `5.397605346934028e-79` xuất hiện ở 4,284 ô (~43% dòng), là placeholder hệ thống NHANES | Cao |
| 2 | Missing values | 1,018 dòng thiếu hoàn toàn (11.1%) - không có kết quả xét nghiệm | Trung bình |
| 3 | Duplicates | 0 dòng trùng lặp hoàn toàn | Thấp |
| 4 | Biological outliers | 96.5% dòng có ≥1 giá trị ngoài range sinh lý tham khảo | Trung bình |
| 5 | Data type | Một số cột bị đọc nhầm kiểu do artifact | Trung bình |
| 6 | No target | Không có cột nhãn bệnh | Cao |

### 1.3 Hành động Cleaning
1. **Artifact handling:** Thay thế toàn bộ `5.397605346934028e-79` bằng `NaN` (4,284 giá trị đã xử lý).
2. **Numeric coercion:** Ép kiểu tất cả cột sang numeric với `errors='coerce'`.
3. **Missing values:** Xóa 1,018 dòng all-NaN (11.1%). Giữ lại dòng có ≥1 giá trị hợp lệ.
4. **Outliers:** Thêm cột `outlier_flag` đánh dấu 7,860 dòng (96.5%) có ≥1 outlier, không xóa giá trị.
5. **Duplicates:** Không có.
6. **Export:** Lưu ra `Clean_Data/CBC_clean.csv`.

### 1.4 Kết quả
- **Output:** 8,147 rows × 22 cols
- **File size:** ~799 KB
- **Artifact remaining:** 0
- **Missing:** Cột `LBDBANO` còn 47.7% missing (đặc thù Basophil count trong NHANES).
- **Outlier flag:** 7,860 dòng (96.5%) có ≥1 outlier được đánh dấu.

---

## 2. Diseases_and_Symptoms

### 2.1 Data Profile
| Chỉ tiêu | Trước | Sau |
|----------|-------|-----|
| Nguồn | `Dataset/Data/diseases_and_symptoms.csv` | `Dataset/Clean_Data/diseases_and_symptoms_clean.csv` |
| Số dòng | 246,945 | 189,647 |
| Số cột | 378 | 378 |
| Kiểu dữ liệu | int64 mặc định | category + bool |
| Nhãn bệnh | Có (`diseases`, 773 lớp) | Có (`diseases`, 773 lớp) |

### 2.2 Vấn đề phát hiện từ EDA
| # | Vấn đề | Mô tả | Mức độ |
|---|--------|-------|--------|
| 1 | Trùng lặp | 57,298 hàng trùng lặp hoàn toàn (~23.2%) | Cao |
| 2 | Kích thước file | ~190MB, 246,945 hàng × 378 cột | Trung bình |
| 3 | Kiểu dữ liệu | CSV đọc mặc định int64 (8 bytes/giá trị) | Trung bình |
| 4 | Missing values | 0 - không có giá trị thiếu | Thấp |
| 5 | Giá trị vô lý | 0 - tất cả triệu chứng nằm trong {0,1} | Thấp |
| 6 | Số lớp bệnh | 773 lớp, phân bổ khá đồng đều (~1,200 mẫu/lớp) | Trung bình |

### 2.3 Hành động Cleaning
1. **Memory optimization:** Đọc CSV với `dtype=category` cho `diseases` và `dtype=bool` cho symptoms, giảm memory từ ~500MB xuống ~90MB.
2. **Duplicate removal:** Loại bỏ 57,298 hàng trùng lặp hoàn toàn bằng `drop_duplicates()`.
3. **Data validation:** Xác nhận không có missing values, không có giá trị ngoài {0,1}.
4. **Label preservation:** Giữ nguyên cột `diseases` dạng category để preserve 773 lớp.
5. **Export:** Lưu ra `Clean_Data/diseases_and_symptoms_clean.csv`.

### 2.4 Kết quả
- **Output:** 189,647 rows × 378 cols
- **File size:** ~38 MB
- **Duplicates removed:** 57,298 (23.2%)
- **Memory (in-RAM):** ~90MB (giảm từ ~500MB)
- **Missing:** 0
- **Invalid values:** 0

---

## 3. Laboratory Data

### 3.1 Data Profile
| Chỉ tiêu | Trước | Sau |
|----------|-------|-----|
| Nguồn | `Dataset/Data/laboratory_data.csv` | `Dataset/Clean_Data/laboratory_data_clean.csv` |
| Số dòng | 12,009 | 12,009 |
| Số cột | 14 | 15 (thêm `outlier_flag`) |
| Kiểu dữ liệu | mixed | mixed + int flag |
| Nhãn bệnh | Có (`Disease`, 9 lớp) | Có (`Disease`, 9 lớp) |

### 3.2 Vấn đề phát hiện từ EDA
| # | Vấn đề | Mô tả | Mức độ |
|---|--------|-------|--------|
| 1 | Missing values | 0 - toàn bộ dữ liệu không có giá trị thiếu | Thấp |
| 2 | Duplicates | 0 hàng trùng lặp hoàn toàn | Thấp |
| 3 | Biological outliers | Một số giá trị nằm ngoài khoảng sinh học (Hemoglobin max 50, RBC max 34, WBC max 27901) | Trung bình |
| 4 | Imbalanced labels | Lớp Anemia chiếm tỷ trọng cao (2,979), Cardiovascular disease thấp (697) | Trung bình |
| 5 | Scale disparity | Các chỉ số có biên độ rất khác nhau (Troponin 0-10, WBC 500-100000) | Trung bình |
| 6 | Categorical | Chỉ có `Gender` (Male/Female/Other) | Thấp |

### 3.3 Hành động Cleaning
1. **Strip columns:** Xóa khoảng trắng thừa ở tên cột (ví dụ: `Disease ` → `Disease`).
2. **Missing values:** Không có, giữ nguyên.
3. **Duplicates:** Không có, giữ nguyên.
4. **Outliers:** Thêm cột `outlier_flag` đánh dấu 2,547 dòng (21.2%) có ≥1 giá trị ngoài range sinh học tham khảo.
5. **Export:** Lưu ra `Clean_Data/laboratory_data_clean.csv`.

### 3.4 Kết quả
- **Output:** 12,009 rows × 15 cols
- **File size:** ~1.8 MB
- **Missing:** 0
- **Duplicates:** 0
- **Outlier flag:** 2,547 dòng (21.2%) có ≥1 outlier
- **Target:** Cột `Disease` giữ nguyên (9 lớp)

---

## 4. Personalized Medication Dataset

### 4.1 Data Profile
| Chỉ tiêu | Trước | Sau |
|----------|-------|-----|
| Nguồn | `Dataset/Data/personalized_medication_dataset.csv` | `Dataset/Clean_Data/personalized_medication_dataset_clean.csv` |
| Số dòng | 1,000 | 1,000 |
| Số cột | 17 | 17 |
| Kiểu dữ liệu | mixed | mixed |
| Nhãn bệnh | Có (`Diagnosis`, 5 lớp + `Recommended_Medication`, 3 lớp) | Có (giữ nguyên) |

### 4.2 Vấn đề phát hiện từ EDA
| # | Vấn đề | Mô tả | Mức độ |
|---|--------|-------|--------|
| 1 | Missing values | 6 cột có giá trị thiếu: Chronic_Conditions (246), Drug_Allergies (324), Genetic_Disorders (339), Recommended_Medication (263), Dosage (195), Duration (257) | Trung bình |
| 2 | Duplicates | 0 hàng trùng lặp | Thấp |
| 3 | Biological outliers | Không có giá trị vô lý ngoài khoảng sinh học | Thấp |
| 4 | Structural issues | Cột `Dosage`, `Duration` dạng chuỗi; cột `Symptoms`, `Drug_Allergies` dạng multi-value | Trung bình |
| 5 | None semantics | Nhiều giá trị "None" trong các cột text | Trung bình |
| 6 | Data leakage | `Treatment_Effectiveness`, `Adverse_Reactions` có thể gây leakage | Trung bình |

### 4.3 Hành động Cleaning
1. **Strip columns:** Xóa khoảng trắng thừa ở tên cột.
2. **Strip text values:** Xóa khoảng trắng thừa ở các cột text.
3. **Missing values:** Impute 6 cột categorical/text với giá trị `"Unknown"` (tổng 1,564 missing values).
4. **Duplicates:** Không có, giữ nguyên.
5. **Outliers:** Không có, giữ nguyên.
6. **Export:** Lưu ra `Clean_Data/personalized_medication_dataset_clean.csv`.

### 4.4 Kết quả
- **Output:** 1,000 rows × 17 cols
- **File size:** ~170 KB
- **Missing:** 0 (đã impute hết)
- **Duplicates:** 0
- **Target:** Cột `Diagnosis` (5 lớp) giữ nguyên

---

## 5. Tổng kết

### 5.1 Bảng so sánh tổng thể
| Chỉ tiêu | CBC | Diseases_and_Symptoms | Laboratory Data | Personalized Medication |
|----------|-----|----------------------|-----------------|------------------------|
| Input rows | 9,165 | 246,945 | 12,009 | 1,000 |
| Output rows | 8,147 | 189,647 | 12,009 | 1,000 |
| Output cols | 22 | 378 | 15 | 17 |
| Artifact/Technical noise | High (4,284 values) | Low | Low | Low |
| Missing handled | 1,018 rows (11.1%) | 0 | 0 | 1,564 values (6 cols) |
| Duplicates removed | 0 | 57,298 (23.2%) | 0 | 0 |
| Outliers flagged | 7,860 rows (96.5%) | N/A | 2,547 rows (21.2%) | 0 |
| Target preserved | No | Yes (773 classes) | Yes (9 classes) | Yes (5 classes) |
| Memory optimization | No | Yes (~500MB → ~90MB) | No | No |

### 5.2 Files đã tạo
| Dataset | Input | Output |
|---------|-------|--------|
| CBC | `Dataset/Data/CBC.csv` | `Dataset/Clean_Data/CBC_clean.csv` |
| Diseases_and_Symptoms | `Dataset/Data/diseases_and_symptoms.csv` | `Dataset/Clean_Data/diseases_and_symptoms_clean.csv` |
| Laboratory Data | `Dataset/Data/laboratory_data.csv` | `Dataset/Clean_Data/laboratory_data_clean.csv` |
| Personalized Medication | `Dataset/Data/personalized_medication_dataset.csv` | `Dataset/Clean_Data/personalized_medication_dataset_clean.csv` |

### 5.3 Khuyến nghị bước tiếp theo
1. **Data Preparing:** Thực hiện imputation (MICE/KNN), encoding (One-Hot/Target), scaling (StandardScaler/RobustScaler).
2. **Feature engineering:** Tách cột hỗn hợp (Dosage/Duration), multi-hot encoding cho symptoms.
3. **Train/Val/Test split:** Stratified split, có thể nhóm theo bệnh.
4. **Baseline modeling:** 
   - CBC: Cần merge target trước.
   - Diseases_and_Symptoms: XGBoost/RF sau feature selection.
   - Laboratory Data: XGBoost/RF/Neural Network.
   - Personalized Medication: Cần thêm data hoặc augmentation.
5. **Evaluation:** macro-F1 / weighted-F1 / ROC-AUC tùy imbalance level.

---

**Lưu ý:** Tất cả quyết định cleaning đã được thực hiện theo nguyên tắc tối thiểu thay đổi, giữ nguyên cấu trúc dữ liệu gốc, và không xóa outlier mà chỉ đánh dấu để review lâm sàng.
