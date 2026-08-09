# File tổng hợp link dataset đã thu thập
## 1. Complete Blood Count (CBC) Dataset

### Tên dataset
**Complete Blood Count (CBC) Dataset**

### Link dẫn đến dataset
https://www.kaggle.com/datasets/vizeno/complete-blood-count-cbc-dataset

### Loại hình dataset
- Nguồn: Kaggle
- Dạng: Tabular / Clinical / CBC
- Mục đích: Phân tích và xử lý các chỉ số Complete Blood Count (CBC)

### Các thành phần data
- **Age** – tuổi
- **Gender** – giới tính
- **Hemoglobin (Hb)** – huyết sắc tố
- **Platelet Count (PLT)** – số lượng tiểu cầu
- **White Blood Cells (WBC)** – bạch cầu
- **Red Blood Cells (RBC)** – hồng cầu
- **MCV**
- **MCH**
- **MCHC**

### Ghi chú
Dataset phù hợp cho module CBC và patient demographics cơ bản. Không bao phủ đầy đủ HCT, RDW, MPV, PDW, PCT, Neutrophil và Lymphocyte.

---

## 2. COVID-19 Complete Blood Count (CBC) Clinical Database

### Tên dataset
**COVID-19 Complete Blood Count (CBC) Clinical Database**

### Link dẫn đến dataset
https://www.kaggle.com/datasets/tawsifurrahman/covid19-complete-blood-count-clinical-database

### Loại hình dataset
- Nguồn: Kaggle
- Dạng: Clinical tabular / CBC
- Loại dữ liệu: Real clinical data
- Quy mô được mô tả: 103 bệnh nhân
- Bối cảnh: Bệnh nhân COVID-19

### Các thành phần data
- Demographic information
- Complete Blood Count (CBC)
- Các chỉ số huyết học
- Clinical outcome
- Survival / mortality outcome

### Ghi chú
Có thể sử dụng để nghiên cứu clinical AI, outcome prediction và CBC-based prediction. Hạn chế là dataset nhỏ và tập trung vào COVID-19, không phải leukemia.

---

## 3. Personalized Medication Dataset

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

---

## 4. Disease Symptoms and Patient Profile Dataset

### Tên dataset
**Disease Symptoms and Patient Profile Dataset**

### Link dẫn đến dataset
https://www.kaggle.com/datasets/uom190346a/disease-symptoms-and-patient-profile-dataset

### Loại hình dataset
- Nguồn: Kaggle
- Dạng: Tabular / Symptoms / Patient Profile
- Mục đích: Disease prediction và symptom classification

### Các thành phần data
#### Patient information
- Age
- Gender

#### Symptoms
- Fever
- Cough
- Fatigue
- Difficulty breathing
- Các triệu chứng khác

#### Health indicators
- Blood pressure
- Cholesterol

#### Target
- Disease

### Ghi chú
Phù hợp cho module Clinical Symptoms và Patient Profile. Không có CBC đầy đủ, medical history và medication.

---

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

---

## 7. Healthcare Symptoms–Disease Classification Dataset

### Tên dataset
**Healthcare Symptoms–Disease Classification Dataset**

### Link dẫn đến dataset
https://www.kaggle.com/datasets/kundanbedmutha/healthcare-symptomsdisease-classification-dataset

### Loại hình dataset
- Nguồn: Kaggle
- Dạng: Synthetic tabular
- Loại dữ liệu: Synthetic
- Quy mô được mô tả: 25.000 records
- Số bệnh: 30 diseases

### Các thành phần data
- Demographic attributes
- Symptom list
- Diagnosis
- Disease labels
- Symptom patterns

### Ghi chú
Phù hợp cho:
- Multi-class disease classification
- Symptom pattern analysis
- NLP trên symptom text
- Medical decision-support prototype

Đây là synthetic data nên phù hợp hơn cho prototype và thử nghiệm phương pháp.

---

## 8. Medical Conditions – 50,000+ Records

### Tên dataset
**Medical Conditions – 50,000+ records**

### Link dẫn đến dataset
https://www.kaggle.com/datasets/abdelrahmangamal236/medical-conditions50000

### Loại hình dataset
- Nguồn: Kaggle
- Dạng: Tabular / Medical NLP
- Quy mô: hơn 50.000 records
- Mục đích: Medical NLP, symptom-to-disease và medication recommendation prototype

### Các thành phần data
- ID
- Symptoms / Question
- Disease
- Recommended Medicines
- Clinical advice / information liên quan

### Ghi chú
Phù hợp cho:
- Symptom → Disease
- Medical NLP
- Medication recommendation prototype

Không có CBC và patient demographics đầy đủ.

---

## 9. Leukemia Cancer Risk Prediction Dataset

### Tên dataset
**Leukemia Cancer Risk Prediction Dataset**

### Link dẫn đến dataset
https://www.kaggle.com/datasets/ankushpanday1/leukemia-cancer-risk-prediction-dataset

### Loại hình dataset
- Nguồn: Kaggle
- Dạng: Tabular / Risk Prediction
- Loại dữ liệu: Simulated / Synthetic
- Quy mô được mô tả: khoảng 143.194 records
- Phạm vi: 22 quốc gia

### Các thành phần data
- Demographic factors
- Socioeconomic factors
- Leukemia risk-related features
- Leukemia risk / target
- Các biến phục vụ classification
- Các yếu tố phục vụ bias và fairness analysis
- Imbalanced classification features

### Ghi chú
Phù hợp cho:
- Leukemia risk prediction
- Classification
- Fairness analysis
- Imbalanced learning

Dataset được mô tả là simulated data, không phải hồ sơ bệnh nhân leukemia thực và không có full CBC theo schema của project.
