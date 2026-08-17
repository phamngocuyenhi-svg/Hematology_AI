# Báo cáo EDA — Hệ thống AI Hỗ trợ Chẩn đoán Sơ bộ Bệnh lý Huyết học

Cập nhật: 2026-08-16
Phạm vi: EDA chi tiết bằng Jupyter Notebook cho toàn bộ 10 dataset trong `D:\AI_08_V1\Data\`. Notebook đặt tại `D:\AI_08_V1\EDA\`, mỗi dataset 1 file, đã chạy thành công 100% (0 lỗi), có biểu đồ trực quan kèm theo.

---

## Mục lục notebook

| # | Notebook | Dataset | Loại |
|---|---|---|---|
| 1 | [01_cbc_test_dataset.ipynb](01_cbc_test_dataset.ipynb) | CBC Test dataset | Bảng |
| 2 | [02_anemia_dataset.ipynb](02_anemia_dataset.ipynb) | Anemia Dataset | Bảng |
| 3 | [03_physionet_sepsis_2019.ipynb](03_physionet_sepsis_2019.ipynb) | PhysioNet Sepsis 2019 | Bảng (time-series) |
| 4 | [04_kaggle_cbc_vizeno.ipynb](04_kaggle_cbc_vizeno.ipynb) | Kaggle CBC (vizeno) | Bảng |
| 5 | [05_kaggle_covid_cbc.ipynb](05_kaggle_covid_cbc.ipynb) | Kaggle COVID-19 CBC | Bảng |
| 6 | [06_rheumatic_dataverse.ipynb](06_rheumatic_dataverse.ipynb) | Rheumatic & Autoimmune Disease Dataset | Bảng |
| 7 | [07_mds_bone_marrow.ipynb](07_mds_bone_marrow.ipynb) | MDS Bone Marrow Cell Dataset | Ảnh |
| 8 | [08_txl_pbc.ipynb](08_txl_pbc.ipynb) | TXL-PBC | Ảnh (detection) |
| 9 | [09_pbc_barcelona.ipynb](09_pbc_barcelona.ipynb) | PBC Barcelona | Ảnh (classification) |
| 10 | [10_nhanes_cbc_2015.ipynb](10_nhanes_cbc_2015.ipynb) | NHANES 2015-2016 CBC_I | Bảng |

---

## Phát hiện quan trọng nhất phát sinh trong lúc làm EDA

Quá trình chạy notebook phát hiện **2 lỗi dữ liệu mà bước kiểm tra thu thập trước đây bỏ sót** (chỉ kiểm tra "không rỗng", chưa kiểm tra nội dung/parse thử) — cả hai đã được xử lý:

1. **5/40.336 file PhysioNet Sepsis** thực chất là trang lỗi HTML (không rỗng nhưng sai nội dung hoàn toàn) → đã xác định, tải lại đúng, xác minh lại toàn bộ 40.336 file hợp lệ 100%.
2. **File rác `.DS_169665.jpg` + thư mục `__MACOSX/`** trong PBC Barcelona (artifact sinh ra khi tạo file zip trên macOS, không phải ảnh thật) → đã xoá.

**Bài học rút ra**: kiểm tra "file không rỗng" là chưa đủ để đảm bảo chất lượng dữ liệu tải về — cần thử parse/đọc nội dung thật (như notebook EDA làm) mới phát hiện được các lỗi dạng này.

---

## Tổng hợp phát hiện theo từng dataset

### 1. CBC Test dataset
- Không missing, không trùng lặp.
- **Lỗi chất lượng nghiêm trọng**: giá trị âm/vô lý (HGB min=-10, MCV min=-79.3, NEUTp max=5317%, HCT max=3715, MPV max=919) — cần lọc theo khoảng sinh học hợp lý trước khi dùng.
- Không có nhãn bệnh. Không phát hiện đa cộng tuyến (|r|>0.85) giữa các chỉ số.

### 2. Anemia Dataset
- **62.4% dòng trùng lặp** (887/1.421) — chỉ còn ~534 dòng thật sự khác nhau.
- Chỉ 5 feature huyết học, đủ phân biệt có/không thiếu máu, không đủ phân loại 9 loại thiếu máu.
- Xu hướng Hemoglobin theo Result hợp lý về lâm sàng → nhãn đáng tin cậy.

### 3. PhysioNet Sepsis 2019
- Time-series đa biến, **tỷ lệ missing rất cao** ở các xét nghiệm không đo mỗi giờ (Fibrinogen, PTT, Bilirubin) — cần forward-fill hoặc chỉ giữ dòng có đo xét nghiệm.
- Nguồn duy nhất trong kho có Fibrinogen/PTT (đông máu).
- Nhãn `SepsisLabel` không phải bệnh huyết học — chỉ dùng bổ sung.

### 4. Kaggle CBC (vizeno)
- **Trùng lặp cực nặng: 77.5%** (323/417) — mức cao nhất kho, chỉ còn ~94 dòng thật.
- Giá trị nằm trong khoảng hợp lý (khác CBC Test dataset #1), có Age/Gender.

### 5. Kaggle COVID-19 CBC
- Không missing, nhãn Outcome cân bằng (Recovered 59.2%/Not Recovered 40.8%).
- Cỡ mẫu rất nhỏ (103 dòng), thiếu nhiều chỉ số CBC cốt lõi, nhãn là outcome COVID không phải bệnh huyết học.

### 6. Rheumatic & Autoimmune Disease Dataset
- **Chất lượng tốt nhất trong nhóm Kaggle/thủ công**: 0 trùng lặp, 12.085 dòng.
- Có CRP/ESR thật + nhãn Disease 7 lớp, lớp nhỏ nhất vẫn có 516 mẫu (mất cân bằng chấp nhận được).
- Là bệnh tự miễn, không phải huyết học — chỉ dùng bù CRP/ESR.

### 7. MDS Bone Marrow Cell Dataset
- **Mất cân bằng cực đoan**: 54 lớp, lệch tới 3.958 lần giữa lớp nhiều nhất và ít nhất; nhiều lớp dưới 10 ảnh.
- Nguồn ảnh duy nhất có nhãn tế bào bất thường thật sự liên quan bệnh huyết học (MDS), gán nhãn bởi tối đa 3 chuyên gia.

### 8. TXL-PBC
- Object detection, 3 lớp: RBC áp đảo 89.7% số box, WBC 7.3%, Platelet 3% — cần class weighting khi train.
- Không phân loại chi tiết dòng bạch cầu; khác bản chất với 2 bộ ảnh classification còn lại.

### 9. PBC Barcelona
- Mất cân bằng nhẹ hơn nhiều (~2.7 lần) so với MDS — phù hợp train/pretrain phân loại bạch cầu.
- Chỉ có mẫu khỏe mạnh — không dùng để phát hiện bất thường.

### 10. NHANES 2015-2016 CBC_I
- **Chất lượng cao nhất toàn kho**: 0 trùng lặp, không giá trị âm/vô lý, tổng % 5 dòng bạch cầu ≈ 100% như kỳ vọng.
- CBC 5-dòng bạch cầu đầy đủ nhất (cả % và số tuyệt đối), Age 1–80 tuổi, Gender cân bằng.
- Không có nhãn chẩn đoán — chỉ dùng làm reference range chất lượng cao theo tuổi/giới.

---

## Kết luận & khuyến nghị bước tiếp theo

**Vấn đề xuyên suốt cần xử lý trước khi train**:
1. **Trùng lặp dữ liệu** là vấn đề phổ biến nhất ở nhóm dataset lấy từ Kaggle (62–77% ở 3/6 bộ bảng) — bắt buộc `drop_duplicates()` trước khi dùng.
2. **Giá trị ngoài khoảng sinh học hợp lý** xuất hiện ở 2 bộ CBC (CBC Test dataset, Kaggle CBC vizeno ít nghiêm trọng hơn) — cần áp dụng range-check thống nhất cho toàn bộ pipeline.
3. **Mất cân bằng lớp cực đoan** ở dữ liệu ảnh (đặc biệt MDS 3.958 lần) — cần chiến lược gộp lớp/augmentation trước khi train classification.
4. **Time-series nhiều missing** ở PhysioNet — cần quy trình resample/impute riêng, không thể coi là bảng tĩnh.

**Chất lượng cao, ưu tiên dùng làm nguồn chính**: NHANES CBC_I (#10) cho CBC, Rheumatic Dataverse (#6) cho CRP/ESR + nhãn đa lớp, PBC Barcelona (#9) cho ảnh phân loại bạch cầu.

**Vẫn hoàn toàn thiếu sau EDA**: Ferritin, Serum Iron, TIBC, Vitamin B12, Folate, LDH, Haptoglobin, PT, INR, D-Dimer, triệu chứng lâm sàng, và nhãn chẩn đoán đúng theo 9 nhóm bệnh huyết học gốc — không dataset nào trong 10 bộ đã EDA đáp ứng được các mục này (xem thêm `Data/Báo cáo thu thập data.md`).
