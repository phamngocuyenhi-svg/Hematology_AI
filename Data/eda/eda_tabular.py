"""
EDA so bo cho 2 bo du lieu dang bang: CBC Test va Anemia Dataset.
Chay: python eda_tabular.py
Output: in ra console + luu report txt vao Data/eda/report_tabular.txt
"""
import pandas as pd
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT = []

def log(msg=""):
    print(msg)
    OUT.append(str(msg))

def section(title):
    log("\n" + "=" * 70)
    log(title)
    log("=" * 70)

def iqr_outliers(series):
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return ((series < lo) | (series > hi)).sum()

# ---------- 1. CBC Test dataset ----------
section("1) CBC TEST DATASET  (tabular/anemia_cbc_ml_repo/cbc information.xlsx)")
cbc_path = BASE / "tabular" / "anemia_cbc_ml_repo" / "cbc information.xlsx"
cbc = pd.read_excel(cbc_path)

log(f"Shape: {cbc.shape}")
log(f"Cot: {list(cbc.columns)}")
na_sum = cbc.isna().sum()
log(f"\nSo gia tri thieu (missing) theo cot:\n{na_sum[na_sum > 0] if na_sum.sum() else 'Khong co missing value'}")
log(f"\nSo dong trung lap: {cbc.duplicated().sum()}")

num_cols = cbc.select_dtypes(include=np.number).columns.drop("ID", errors="ignore")
log("\nThong ke mo ta (describe):")
log(cbc[num_cols].describe().T[["mean", "std", "min", "50%", "max"]].round(2))

log("\nSo luong outlier theo IQR (1.5x) tung cot:")
for c in num_cols:
    n = iqr_outliers(cbc[c])
    if n > 0:
        log(f"  {c:10s}: {n} dong ({n/len(cbc)*100:.1f}%)")

log("\nTuong quan cao (|r| > 0.85) giua cac chi so - canh bao da cong tuyen:")
corr = cbc[num_cols].corr()
seen = set()
for i in corr.columns:
    for j in corr.columns:
        if i != j and abs(corr.loc[i, j]) > 0.85 and (j, i) not in seen:
            log(f"  {i} <-> {j}: r = {corr.loc[i, j]:.3f}")
            seen.add((i, j))

log("\n>> Nhan xet: dataset nay KHONG co san cot nhan benh (target).")
log(">> Can tu sinh nhan (vd Anaemia = 1 neu HGB<11 hoac HCT<36%) hoac dung threshold lam-sang chuan.")

# ---------- 2. Anemia Dataset ----------
section("2) ANEMIA DATASET  (tabular/anemia_ml_basic_repo/anemia data from Kaggle.csv)")
an_path = BASE / "tabular" / "anemia_ml_basic_repo" / "anemia data from Kaggle.csv"
an = pd.read_csv(an_path)

log(f"Shape: {an.shape}")
log(f"Cot: {list(an.columns)}")
na_sum2 = an.isna().sum()
log(f"\nSo gia tri thieu theo cot:\n{na_sum2[na_sum2 > 0] if na_sum2.sum() else 'Khong co missing value'}")
log(f"\nSo dong trung lap: {an.duplicated().sum()}")

log("\nPhan bo Gender (0/1):")
log(an["Gender"].value_counts())

log("\nPhan bo nhan Result (target):")
vc = an["Result"].value_counts()
log(vc)
log(f"Ty le can bang lop (%): {(vc / vc.sum() * 100).round(1).to_dict()}")

log("\nThong ke mo ta cac chi so huyet hoc:")
log(an[["Hemoglobin", "MCH", "MCHC", "MCV"]].describe().T[["mean", "std", "min", "50%", "max"]].round(2))

log("\nHemoglobin trung binh/min/max theo Gender va Result (kiem tra threshold theo gioi):")
log(an.groupby(["Gender", "Result"])["Hemoglobin"].agg(["mean", "min", "max", "count"]).round(2))

log("\n>> Nhan xet: dataset chi co 5 feature huyet hoc (thieu RBC, WBC, PLT, RDW... so voi schema 18 chi so trong overview).")
log(">> Chi du de phan biet 'co/khong thieu mau', KHONG du de phan loai 9 loai thieu mau rieng biet.")

# ---------- Save report ----------
report_path = BASE / "eda" / "report_tabular.txt"
report_path.write_text("\n".join(OUT), encoding="utf-8")
log(f"\n\nDa luu report vao: {report_path}")
