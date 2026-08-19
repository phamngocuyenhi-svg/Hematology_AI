# Báo cáo làm sạch dữ liệu (Clean Data) — Hệ thống AI Hỗ trợ Chẩn đoán Sơ bộ Bệnh lý Huyết học

Cập nhật: 2026-08-16
Phạm vi: làm sạch toàn bộ 10 dataset dựa trên phát hiện từ `EDA/Báo cáo EDA.md`. Notebook đặt tại `D:\AI_08_V1\Clean\`, output tại `D:\AI_08_V1\Clean_Data\`. Dữ liệu gốc trong `Data/` giữ nguyên không đổi.

**Nguyên tắc áp dụng**: không impute giá trị lỗi/thiếu (loại bỏ hoặc giữ NaU rõ ràng), không gộp nhãn khác ý nghĩa giữa các nguồn, ghi log đầy đủ số dòng trước/sau mỗi bước.

---

## Kết quả từng dataset

| # | Notebook | Vấn đề | Xử lý | Trước → Sau |
|---|---|---|---|---|
| 1 | [01_clean_cbc_test_dataset.ipynb](01_clean_cbc_test_dataset.ipynb) | Giá trị âm/vô lý | Loại dòng vi phạm khoảng sinh học hợp lý (20 cột) | 500 → **461 dòng** (92.2%) |
| 2 | [02_clean_anemia_dataset.ipynb](02_clean_anemia_dataset.ipynb) | 62.4% trùng lặp | `drop_duplicates()` | 1.421 → **534 dòng** (37.6%) |
| 3 | [03_clean_physionet_sepsis.ipynb](03_clean_physionet_sepsis.ipynb) | Time-series, missing cao | Aggregate 1 dòng/bệnh nhân (giá trị gần nhất) | 40.336 file → **40.336 dòng bảng tĩnh** |
| 4 | [04_clean_kaggle_cbc_vizeno.ipynb](04_clean_kaggle_cbc_vizeno.ipynb) | 77.5% trùng lặp | `drop_duplicates()` | 417 → **94 dòng** (22.5%) |
| 5 | [05_clean_kaggle_covid_cbc.ipynb](05_clean_kaggle_covid_cbc.ipynb) | Tên cột chưa chuẩn | Chuẩn hóa tên cột (snake_case) | 103 → **103 dòng** (không đổi) |
| 6 | [06_clean_rheumatic_dataverse.ipynb](06_clean_rheumatic_dataverse.ipynb) | Missing 9–43% cột huyết thanh học | Giữ NaN, thêm 12 cột `_missing` flag | 12.085 → **12.085 dòng** (không đổi, +12 cột) |
| 7 | [07_clean_mds_bone_marrow.ipynb](07_clean_mds_bone_marrow.ipynb) | 54 lớp, lệch 3.958 lần | Gộp main/add cùng loại tế bào + gộp lớp <20 ảnh vào `Rare_Other` | 54 lớp → **28 lớp**, lệch còn **187 lần** |
| 8 | *(không cần notebook)* | RBC chiếm 89.7% box | Không xử lý ở bước clean — để dành class weighting lúc train model | Không đổi |
| 9 | [09_clean_pbc_barcelona.ipynb](09_clean_pbc_barcelona.ipynb) | Nghi ngờ còn file hỏng | Quét toàn vẹn bằng `PIL.Image.verify()` | 17.093 → **17.092 ảnh hợp lệ**, 0 lỗi phát hiện thêm |
| 10 | [10_clean_nhanes_cbc.ipynb](10_clean_nhanes_cbc.ipynb) | 11.4% thiếu 5-dòng bạch cầu | Xuất 2 bản: đầy đủ + chỉ ca hoàn chỉnh | 9.165 dòng → **2 file** (9.165 và 8.116 dòng) |

---

## File output trong `Clean_Data/`

```
Clean_Data/
├── schema_mapping.csv                      <- bảng ánh xạ tên cột giữa các nguồn về 1 schema chuẩn
└── tabular/
    ├── cbc_test_dataset_clean.csv          (461 dòng)
    ├── anemia_dataset_clean.csv            (534 dòng)
    ├── physionet_sepsis_clean.csv          (40.336 dòng, 1 dòng/bệnh nhân)
    ├── kaggle_cbc_vizeno_clean.csv         (94 dòng)
    ├── kaggle_covid_cbc_clean.csv          (103 dòng)
    ├── rheumatic_dataverse_clean.csv       (12.085 dòng)
    ├── mds_bone_marrow_manifest.csv        (25.009 dòng — ánh xạ ảnh, không copy ảnh)
    ├── pbc_barcelona_manifest.csv          (17.092 dòng — ánh xạ ảnh)
    ├── nhanes_cbc_full.csv                 (9.165 dòng)
    └── nhanes_cbc_complete_only.csv        (8.116 dòng)
```

**Về 2 bộ ảnh**: không copy lại file ảnh vật lý (tránh nhân đôi 500MB+ dung lượng) — thay vào đó tạo **manifest CSV** ánh xạ `image_path -> lớp gốc -> lớp đã làm sạch`, dùng manifest này để load ảnh theo lớp mới khi huấn luyện. TXL-PBC không cần bước clean vì mất cân bằng của nó phản ánh đúng thực tế sinh học (RBC nhiều hơn WBC/tiểu cầu), không phải lỗi dữ liệu.

**`schema_mapping.csv`**: bảng đối chiếu 22 chỉ số (CBC + CRP/ESR + đông máu + nhãn) qua tên cột thực tế ở từng dataset — dùng để tra cứu khi cần gộp/so sánh chỉ số giữa các nguồn, **không dùng để gộp nhãn bệnh** (cột `disease_label` ghi rõ ý nghĩa khác nhau giữa các nguồn, không gộp chung).

---

## Phát hiện quan trọng phát sinh khi làm sạch

**PhysioNet Sepsis — vẫn rất thưa dữ liệu đông máu dù đã lấy giá trị gần nhất**: sau khi aggregate về 1 dòng/bệnh nhân, tỷ lệ thiếu vẫn cao đáng kể ở đúng các chỉ số đông máu cần nhất:

| Chỉ số | % thiếu (sau aggregate) |
|---|---|
| Bilirubin_direct | 94.9% |
| Fibrinogen | 88.8% |
| Alkalinephos | 64.9% |
| Bilirubin_total | 64.7% |
| AST | 64.4% |
| PTT | 49.8% |

→ Có nghĩa là **chỉ khoảng 11% bệnh nhân từng được đo Fibrinogen** trong suốt lượt nằm viện, dù dataset có 40.336 bệnh nhân. Đây là điểm cần lưu ý nghiêm túc: nguồn "duy nhất" bù chỉ số đông máu trong kho thực ra chỉ cung cấp dữ liệu Fibrinogen đáng tin cậy cho **~4.400 bệnh nhân**, không phải toàn bộ 40.336 như con số tổng gợi ý.

---

## Còn lại chưa xử lý / không cần xử lý

- **Bộ Disease-Symptom, Personalized Medication, Laboratory Data** (Kaggle, từ `Reference_Data.md`): chưa tải nên chưa có gì để clean.
- **TXL-PBC**: cố ý không xử lý (xem bảng trên).
- **Đơn vị đo giữa các nguồn CBC**: `schema_mapping.csv` mới dừng ở mức ánh xạ tên cột — **chưa verify từng cặp nguồn có cùng đơn vị hay không** (VD Platelet Count ở Kaggle CBC vizeno vs CBC Test dataset). Cần làm ở bước tích hợp/gộp dữ liệu tiếp theo, không thuộc phạm vi làm sạch từng dataset riêng lẻ này.

## Bước tiếp theo đề xuất

1. Verify đơn vị đo chéo giữa các nguồn CBC bằng cách so sánh phân phối giá trị theo `schema_mapping.csv`.
2. Với PhysioNet: cân nhắc lọc riêng tập con "có đo Fibrinogen/PTT" (~4.400–20.000 bệnh nhân tuỳ chỉ số) làm tập chuyên biệt cho phần đông máu, thay vì dùng chung 40.336 dòng đầy NaN.
3. Bắt đầu thiết kế feature engineering / bài toán mô hình cụ thể trên các file trong `Clean_Data/` — đã đủ sạch để dùng bước tiếp theo.
