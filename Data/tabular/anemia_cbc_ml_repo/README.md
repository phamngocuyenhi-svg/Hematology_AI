<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=Anemia%20Detection%20via%20CBC&fontSize=42&fontColor=fff&animation=twinkling&fontAlignY=38&desc=Machine%20Learning%20on%20Complete%20Blood%20Count%20Parameters&descAlignY=56&descSize=16" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.4+-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-189FB5?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.readthedocs.io/)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge)](LICENSE)

<br/>

> **A clinical-grade machine learning pipeline to detect anemia from routine CBC blood test parameters — with Yeo-Johnson power transformation, IQR-based outlier removal, statistical significance testing, and an XGBoost model achieving perfect recall.**

<br/>

[🔍 Explore the Notebook](#-project-structure) · [📊 See Results](#-model-performance) · [🚀 Run Locally](#-getting-started) · [🧪 Predict on a Patient](#-predict-on-a-new-patient)

<br/>
</div>

---

## 🩸 Problem Statement

Anemia affects over **1.6 billion people** worldwide and is frequently missed in routine screenings. This project builds a binary classification pipeline on real Complete Blood Count (CBC) data to automatically flag anemic patients — with a laser focus on **maximizing Recall**, because a missed diagnosis (False Negative) is a clinical risk.

**Anemia is defined as:**
```
Anaemia = 1  if  HGB < 11.0 g/dL  OR  HCT < 36.0%
Anaemia = 0  otherwise
```

---

## 📁 Project Structure

```
anemia-detection-cbc-ml/
│
├── 📓 Project_7_Anemia_Detection.ipynb     # Full pipeline — all 9 parts
├── 📊 data/
│   ├── cbc_raw.xlsx                         # Original Kaggle dataset
│   └── dataset.json                         # Cleaned dataset (output)
├── 🤖 models/
│   ├── anaemia_model.pkl                    # Final saved XGBoost model
│   └── scaler.pkl                           # Fitted StandardScaler
└── 📄 README.md
```

---

## 🗂️ Dataset

| Property | Detail |
|---|---|
| **Source** | [Kaggle – Complete Blood Count CBC Test](https://www.kaggle.com/datasets/ahmedelsayedtaha/complete-blood-count-cbc-test/data) |
| **Raw shape** | 500 rows × 21 columns |
| **After cleaning** | 361 rows × 21 columns (139 outlier rows removed) |
| **Features** | 20 CBC parameters |
| **Target** | `Target` — binary (1 = Anemic, 0 = Not Anemic) |
| **Missing values** | ✅ None — dataset is fully complete |
| **Duplicates** | ✅ None |

### CBC Feature Reference

| Feature | Full Name | Role |
|---|---|---|
| `HGB` | Hemoglobin | 🔴 Primary anemia indicator |
| `HCT` | Hematocrit | 🔴 Primary anemia indicator |
| `RBC` | Red Blood Cell Count | 🟠 Highly significant |
| `MCV` | Mean Corpuscular Volume | 🟠 Highly significant |
| `MCH` | Mean Corpuscular Hemoglobin | 🟠 Highly significant |
| `MCHC` | Mean Corpuscular Hemoglobin Concentration | 🟠 Highly significant |
| `RDWSD` / `RDWCV` | Red Cell Distribution Width | 🟡 Significant |
| `WBC`, `PLT`, `MPV`, etc. | White cells & platelet indices | ⚪ Not significant |

---

## 🔬 Full Pipeline

```
Raw CBC Data (500 × 21)
        │
        ▼
Part 1: EDA ──────────── shape, dtypes, zero missing values, describe()
        │
        ▼
Part 2: Target Creation ─ Anaemia = f(HGB < 11 OR HCT < 36)
        │                  271 non-anemic (54.2%) | 229 anemic (45.8%)
        ▼
Part 3: Deep EDA ─────── histograms + KDE, skewness, kurtosis,
        │                  boxplots by class, t-tests, correlation heatmap
        ▼
Part 4: Preprocessing ── Yeo-Johnson power transform (handles skew better than log1p),
        │                  IQR outlier removal → 361 clean rows,
        │                  train-test split (80/20, stratified), StandardScaler
        ▼
Part 5: Model Training ── 5 classifiers trained & evaluated
        │
        ▼
Part 6: ROC Curves ─────── AUC comparison across top models
        │
        ▼
Part 7: Feature Selection ─ XGBoost importances → top 5 features selected
        │                    Reduced model retrained → same perfect metrics
        ▼
Part 8: Persistence ────── model + scaler saved as .pkl / dataset as .json
        │
        ▼
Part 9: Inference ──────── load → predict on new patient sample
```

---

## 📊 Class Distribution

After creating the target label from clinical thresholds:

| Class | Count | Percentage |
|---|---|---|
| 0 — Not Anemic | 271 | 54.2% |
| 1 — Anemic | 229 | 45.8% |

> The dataset is **nearly balanced** — no SMOTE or class-weight adjustment was required.
> After outlier removal, the training split shifts to **64% / 36%** in the cleaned dataset.

---

## 🧪 Statistical Analysis

### T-Test Results (feature vs. anemia target)

| Feature | P-Value | Significant? |
|---|---|---|
| Hemoglobin | 7.14e-71 | ✅ Yes |
| Hematocrit | 1.42e-76 | ✅ Yes |
| Red Blood Cell Count | 1.70e-41 | ✅ Yes |
| Mean Corpuscular Hemoglobin | 2.27e-27 | ✅ Yes |
| MCHC | 1.86e-23 | ✅ Yes |
| Mean Corpuscular Volume | 1.30e-17 | ✅ Yes |
| RDW Coefficient of Variation | 3.63e-06 | ✅ Yes |
| RDW Standard Deviation | 0.0037 | ✅ Yes |
| WBC, Lymphocytes, Platelets, etc. | > 0.05 | ❌ No |

### Point-Biserial Correlation (top features vs. target)

| Feature | Correlation |
|---|---|
| Hematocrit | **-0.785** |
| Hemoglobin | **-0.766** |
| Red Blood Cell Count | **-0.631** |
| Mean Corpuscular Hemoglobin | **-0.529** |
| MCHC | **-0.493** |
| Mean Corpuscular Volume | **-0.429** |
| RDW Coefficient of Variation | **+0.241** |

> Negative correlations confirm lower values → higher anemia probability, which aligns with clinical knowledge.

---

## 🤖 Model Performance

All 5 models trained on **288 samples**, tested on **73 samples** (stratified 80/20 split, StandardScaler applied).

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| Logistic Regression | 0.9726 | 0.9615 | 0.9615 | 0.9615 | 0.9403 | 0.9992 |
| Decision Tree | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| Random Forest | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| KNN | 0.8767 | 0.8400 | 0.8077 | 0.8235 | 0.7292 | 0.9431 |
| **XGBoost** ⭐ | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.0000** | **1.0000** |

> **XGBoost** was selected as the final model — perfect metrics with **zero False Negatives** on the test set.

---

## 🏆 Feature Importance (XGBoost)

XGBoost assigned nearly all predictive weight to just 5 features:

| Rank | Feature | Importance |
|---|---|---|
| 1 | Hemoglobin | **55.97%** |
| 2 | Hematocrit | **41.13%** |
| 3 | MCHC | 2.23% |
| 4 | Mean Corpuscular Volume | 0.47% |
| 5 | Mean Corpuscular Hemoglobin | 0.20% |
| All others | WBC, PLT, RDW, etc. | 0.00% |

### Reduced Model (Top 5 Features Only)

A simplified model retrained on only these 5 features achieves **identical performance**:

| Metric | Full Model (20 features) | Reduced Model (5 features) |
|---|---|---|
| Accuracy | 1.0000 | 1.0000 |
| Recall | 1.0000 | 1.0000 |
| ROC-AUC | 1.0000 | 1.0000 |

> ✅ **Same performance with 75% fewer features** — the reduced model is simpler, faster, and more interpretable for clinical deployment.

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/anemia-detection-cbc-ml.git
cd anemia-detection-cbc-ml
```

### 2. Install dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn xgboost scipy joblib jupyter
```

### 3. Get the dataset

Download from [Kaggle](https://www.kaggle.com/datasets/ahmedelsayedtaha/complete-blood-count-cbc-test/data) and place in `data/`.

### 4. Run the notebook

```bash
jupyter notebook Project_7_Anemia_Detection.ipynb
```

---

## 🧪 Predict on a New Patient

```python
import joblib
import pandas as pd

model = joblib.load('models/anaemia_model.pkl')
scaler = joblib.load('models/scaler.pkl')

# Top 5 features used by the final reduced model
sample = pd.DataFrame({
    'Hemoglobin': [10.5],
    'Hematocrit': [34.0],
    'Mean_Corpuscular_Hemoglobin_Concentration': [33.0],
    'Mean_Corpuscular_Volume': [88.0],
    'Mean_Corpuscular_Hemoglobin': [28.0]
})

sample_scaled = scaler.transform(sample)
pred_class = model.predict(sample_scaled)[0]
pred_proba = model.predict_proba(sample_scaled)[0][1]

print(f"Predicted anemia status: {pred_class} ({'Anemic' if pred_class else 'Not Anemic'})")
print(f"Probability of anemia  : {pred_proba:.2f}")
```

---

## 📌 Key Findings & Insights

- **Zero missing values and duplicates** in the original dataset — no imputation required
- **Yeo-Johnson power transformation** outperformed log1p for reducing feature skewness across all CBC parameters
- **139 outlier rows removed** via IQR method (500 → 361 rows), preserving data integrity
- **8 out of 20 features** are statistically significant predictors of anemia (t-test p < 0.05); WBC, platelet indices, and percentage-based WBC features are not
- **HGB and HCT dominate prediction** — XGBoost assigns 97.1% of total feature importance to these two
- **Reduced 5-feature model** matches the full 20-feature model exactly — confirming that most CBC parameters are noise for this task
- **Logistic Regression** also performs remarkably well (97.26% accuracy), validating the near-linear separability of the classes

---

## 🧠 Skills Demonstrated

| Area | Details |
|---|---|
| **Data Engineering** | Feature renaming, target derivation from clinical rules, IQR outlier removal |
| **Statistical Analysis** | Independent t-tests, Pearson/Spearman/Point-Biserial correlations |
| **Feature Engineering** | Yeo-Johnson power transform, StandardScaler, skewness/kurtosis analysis |
| **ML Modeling** | 5 classifiers trained and rigorously compared with full metrics |
| **Model Evaluation** | Accuracy, Precision, Recall, F1, MCC, ROC-AUC, PR-AUC, confusion matrix |
| **Feature Selection** | XGBoost importance ranking, reduced model validation |
| **ML Ops** | joblib model persistence, inference pipeline, clean train/test separation |
| **Domain Awareness** | Clinical CBC interpretation, anemia thresholds, minimizing False Negatives |

---

## 📚 References

- Dataset: [Kaggle – Complete Blood Count CBC Test](https://www.kaggle.com/datasets/ahmedelsayedtaha/complete-blood-count-cbc-test/data)
- WHO Anemia Guidelines: [who.int/health-topics/anaemia](https://www.who.int/health-topics/anaemia)
- Scikit-learn Documentation: [scikit-learn.org](https://scikit-learn.org)
- XGBoost Documentation: [xgboost.readthedocs.io](https://xgboost.readthedocs.io)

---

## 📄 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

**Made with ❤️ and a lot of blood tests**

⭐ Star this repo if you found it useful!

</div>
