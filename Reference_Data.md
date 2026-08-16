# File tổng hợp link dataset đã thu thập

## 1. Personalized Medication Dataset

### Tên dataset
**Personalized Medication Dataset**

### Link dẫn đến dataset
https://www.kaggle.com/datasets/ziya07/personalized-medication-dataset

### Loại hình dataset
- Nguồn: Kaggle
- Dạng: Tabular / Clinical / Medication
- Mục đích: Personalized medication và treatment recommendation

### Các thành phần data
#### Patient demographics
- Age
- Gender
- Weight
- Height
- BMI

#### Medical history
- Chronic conditions
- Drug allergies
- Genetic disorders

#### Clinical information
- Symptoms
- Diagnosis

#### Medication
- Recommended medication
- Dosage
- Duration
- Effectiveness

#### Outcome
- Recovery time
- Adverse reactions

### Ghi chú
Phù hợp cho module Patient Information, Medical History, Symptoms và Medication. Không có bộ CBC đầy đủ.

## 5. Laboratory Data

### Tên dataset
**Laboratory Data**

### Link dẫn đến dataset
https://www.kaggle.com/datasets/klingill/laboratory-data

### Loại hình dataset
- Nguồn: Kaggle
- Dạng: Tabular / Laboratory
- Quy mô được mô tả: khoảng 12.009 patient records
- Mục đích: Laboratory-based AI, risk prediction và feature selection

### Các thành phần data
#### Patient information
- Age
- Gender

#### Hematology / CBC-related
- RBC
- WBC
- Hemoglobin

#### Other laboratory tests
- AST
- ALT
- Cholesterol
- Glucose
- Lipase
- Creatinine
- Troponin
- Các xét nghiệm laboratory khác

### Ghi chú
Có nhiều laboratory features nhưng không phải full CBC và không chuyên biệt cho leukemia.

---

## 6. Disease-Symptom Dataset

### Tên dataset
**Disease-Symptom Dataset**

### Link dẫn đến dataset
https://www.kaggle.com/datasets/dhivyeshrk/diseases-and-symptoms-dataset

### Loại hình dataset
- Nguồn: Kaggle
- Dạng: Tabular / Classification
- Loại dữ liệu: Artificially generated / Synthetic
- Quy mô được mô tả: khoảng 246.000 records
- Diseases: khoảng 773
- Symptoms: khoảng 377

### Các thành phần data
- Disease
- Symptom features
- Các symptom được one-hot encode
- Disease–symptom relationships

### Ghi chú
Phù hợp cho:
- Symptom → Disease classification
- Feature engineering
- Multi-class classification
- Clinical decision-support prototype

Không nên xem đây là dữ liệu bệnh nhân thực vì dataset được artificially generated.

 
## 10. NHANES 2015-2016 Complete Blood Count with 5-Part Differential - Whole Blood (CBC_I) Dataset

### Tên dataset
**NHANES 2015-2016 Complete Blood Count with 5-Part Differential - Whole Blood (CBC_I) Dataset**

### Link dẫn đến dataset
https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2015/DataFiles/CBC_I.htm

### Loại hình dataset
- **Nguồn:** CDC / NCHS - National Health and Nutrition Examination Survey (NHANES)
- **Dạng:** Tabular / Clinical / Whole Blood CBC with 5-Part Differential (File `.XPT` - SAS Transport)
- **Mục đích:** Đánh giá sức khỏe tổng quát, hỗ trợ ước tính tình trạng dinh dưỡng, thiếu hụt vi chất, cũng như sàng lọc các bệnh lý huyết học (thiếu máu, nhiễm trùng, bạch cầu cấp/mạn,...) trên quy mô dân số.

### Các thành phần data
- **SEQN** – Mã định danh đối tượng tham gia khảo sát (Respondent sequence number)
- **LBXWBCSI** – Số lượng bạch cầu (White blood cell count, $10^3 \text{ cells/}\mu\text{L}$)
- **LBXLYPCT** – Tỷ lệ phần trăm bạch cầu Lympho (Lymphocyte percent, %)
- **LBXMOPCT** – Tỷ lệ phần trăm bạch cầu Monocyte (Monocyte percent, %)
- **LBXNEPCT** – Tỷ lệ phần trăm bạch cầu Neutrophil trung tính (Segmented neutrophils percent, %)
- **LBXEOPCT** – Tỷ lệ phần trăm bạch cầu Eosinophil ái kiềm/ái toan (Eosinophils percent, %)
- **LBXBAPCT** – Tỷ lệ phần trăm bạch cầu Basophil ái kiềm (Basophils percent, %)
- **LBDLYMNO** – Số lượng tuyệt đối bạch cầu Lympho (Lymphocyte number, $10^3 \text{ cells/}\mu\text{L}$)
- **LBDMONO** – Số lượng tuyệt đối bạch cầu Monocyte (Monocyte number, $10^3 \text{ cells/}\mu\text{L}$)
- **LBDNENO** – Số lượng tuyệt đối bạch cầu Neutrophil (Segmented neutrophils number, $10^3 \text{ cells/}\mu\text{L}$)
- **LBDEONO** – Số lượng tuyệt đối bạch cầu Eosinophil (Eosinophils number, $10^3 \text{ cells/}\mu\text{L}$)
- **LBDBANO** – Số lượng tuyệt đối bạch cầu Basophil (Basophils number, $10^3 \text{ cells/}\mu\text{L}$)
- **LBXRBCSI** – Số lượng hồng cầu (Red blood cell count, million cells/$\mu\text{L}$)
- **LBXHGB** – Huyết sắc tố (Hemoglobin, g/dL)
- **LBXHCT** – Dung tích hồng cầu / Huyết cầu tố (Hematocrit, %)
- **LBXMCVSI** – Thể tích trung bình hồng cầu (Mean cell volume, fL)
- **LBXMCHSI** – Lượng huyết sắc tố trung bình hồng cầu (Mean cell hemoglobin, pg)
- **LBXMC** – Nồng độ huyết sắc tố trung bình hồng cầu (Mean cell hemoglobin concentration, g/dL)
- **LBXRDW** – Độ phân bố kích thước hồng cầu (Red cell distribution width, %)
- **LBXPLTSI** – Số lượng tiểu cầu (Platelet count, $10^3 \text{ cells/}\mu\text{L}$)
- **LBXMPSI** – Thể tích trung bình tiểu cầu (Mean platelet volume, fL)

### Ghi chú
- Dataset bao phủ đầy đủ các chỉ số CBC chuẩn y khoa bao gồm cả 5 dòng bạch cầu (Lympho, Mono, Neutrophil, Eosinophil, Basophil cả dạng % và số lượng tuyệt đối) cùng các chỉ số hồng cầu, tiểu cầu chuyên sâu (HCT, RDW, MPV).
- Cỡ mẫu khảo sát gồm 9,165 người tham gia từ 1 tuổi trở lên (trong đó có 8,117 mẫu xét nghiệm lâm sàng hoàn chỉnh).
- Để liên kết với các chỉ số nhân khẩu học (như Age, Gender), cần kết hợp file này với Demographics File (DEMO_I) thông qua khóa chung **SEQN**.
