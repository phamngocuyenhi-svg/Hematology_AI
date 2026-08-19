# Báo cáo thu thập data — Hệ thống AI Hỗ trợ Chẩn đoán Sơ bộ Bệnh lý Huyết học

Cập nhật: 2026-08-16 (v2)
Phạm vi: toàn bộ dataset đã thu thập trong `D:\AI_08_V1\Data\` tính đến thời điểm báo cáo — 10 bộ dữ liệu (7 dạng bảng, 3 dạng ảnh), tổng dung lượng ~1.4GB. Ngoài ra có 3 nguồn đã xác định được (từ `Reference_Data.md` của đồng đội) nhưng chưa tải — xem mục "Nguồn đã biết, chưa thu thập" ở cuối file.

---

## Mục lục

| # | Tên dataset | Loại | Vị trí |
|---|---|---|---|
| 1 | CBC Test dataset | Bảng | `tabular/anemia_cbc_ml_repo/` |
| 2 | Anemia Dataset | Bảng | `tabular/anemia_ml_basic_repo/` |
| 3 | PhysioNet Sepsis 2019 | Bảng (time-series) | `tabular/physionet_sepsis_2019/` |
| 4 | Kaggle CBC (vizeno) | Bảng | `tabular/kaggle_cbc_vizeno/` |
| 5 | Kaggle COVID-19 CBC | Bảng | `tabular/kaggle_covid_cbc/` |
| 6 | Rheumatic & Autoimmune Disease Dataset | Bảng | `tabular/rheumatic_dataverse/` |
| 7 | MDS Bone Marrow Cell Dataset | Ảnh | `images/mds_bone_marrow/` |
| 8 | TXL-PBC | Ảnh (detection) | `images/txl_pbc_repo/` |
| 9 | PBC Barcelona | Ảnh (classification) | `images/pbc_barcelona/` |
| 10 | NHANES 2015-2016 CBC_I | Bảng | `tabular/nhanes_cbc_2015/` |

---

## 1. CBC Test dataset

**Nguồn thu thập**: Kaggle `abdelrhmankaram/complete-blood-count-cbc-test`, lấy lại qua repo GitHub `Pfuglo1/anemia-detection-cbc-ml` (repo tái sử dụng dataset gốc, đã có sẵn notebook phân tích).

**Nội dung data**: File `cbc information.xlsx` — 500 dòng × 21 cột: `ID, WBC, LYMp, MIDp, NEUTp, LYMn, MIDn, NEUTn, RBC, HGB, HCT, MCV, MCH, MCHC, RDWSD, RDWCV, PLT, MPV, PDW, PCT, PLCR`. Đầy đủ bộ chỉ số CBC chuẩn (tỷ lệ % và số tuyệt đối của bạch cầu, các chỉ số hồng cầu, tiểu cầu).

**Review data có gì**:
- Không có giá trị thiếu (missing = 0), không có dòng trùng lặp.
- **Không có cột nhãn bệnh** — cần tự sinh nhãn (VD ngưỡng lâm sàng HGB/HCT) hoặc dùng làm dữ liệu unsupervised/phân cụm.
- **Phát hiện lỗi chất lượng nghiêm trọng**: nhiều giá trị vượt ngoài khoảng sinh học hợp lý — `HGB` min = **-10** (âm), `MCV` min = **-79.3** (âm), `NEUTp` (đáng lẽ 0–100%) có max = **5317**, `HCT` max = **3715**, `MPV` max = **919**. Đây gần như chắc chắn là lỗi nhập liệu/sai đơn vị trong dataset gốc, không phải outlier lâm sàng thật — bắt buộc phải lọc theo range hợp lý trước khi dùng.

**EDA sơ bộ** (script: `eda/eda_tabular.py`, output: `eda/report_tabular.txt`):
- Không tìm thấy tương quan nào giữa các chỉ số vượt |r| > 0.85 — đa cộng tuyến không phải vấn đề chính.
- Số lượng outlier theo IQR (1.5×) dao động 1.6%–8.2% tuỳ cột, cao nhất ở `MIDn` (8.2%) và `RDWSD` (7.2%).

---

## 2. Anemia Dataset

**Nguồn thu thập**: Kaggle `biswaranjanrao/anemia-dataset`, lấy lại qua repo GitHub `maladeep/anemia-detection-with-machine-learning`.

**Nội dung data**: File `anemia data from Kaggle.csv` — 1.421 dòng × 6 cột: `Gender, Hemoglobin, MCH, MCHC, MCV, Result`. `Result` là nhãn nhị phân (có/không thiếu máu).

**Review data có gì**:
- Không có giá trị thiếu.
- **Trùng lặp nặng: 887/1.421 dòng bị trùng lặp hoàn toàn (62.4%)** — sau khi loại trùng chỉ còn khoảng 534 dòng thật sự khác nhau.
- Chỉ có 5 feature huyết học (thiếu RBC, WBC, PLT, RDW... so với schema 18 chỉ số CBC trong tài liệu gốc dự án) — chỉ đủ phân biệt "có/không thiếu máu", không đủ phân loại 9 loại thiếu máu riêng biệt.
- Repo đi kèm đã có sẵn model huấn luyện (`random_forest_model.pkl`) và 2 notebook minh hoạ.

**EDA sơ bộ**:
- Phân bố `Gender`: 1 = 740, 0 = 681 (tương đối cân bằng).
- Phân bố nhãn `Result` (trên dữ liệu còn trùng lặp, cần tính lại sau khi loại trùng): 0 = 801 (56.4%), 1 = 620 (43.6%).
- Hemoglobin trung bình theo nhóm Gender × Result cho thấy nhóm Result=1 (thiếu máu) có Hb thấp hơn rõ rệt ở cả 2 giới — xu hướng hợp lý về mặt lâm sàng.

---

## 3. PhysioNet Sepsis 2019

**Nguồn thu thập**: PhysioNet/Computing in Cardiology Challenge 2019 — [physionet.org/content/challenge-2019/1.0.0](https://physionet.org/content/challenge-2019/1.0.0/), giấy phép CC BY 4.0, **không cần credential** (khác MIMIC-IV). Tự động tải bằng `curl --parallel` (40.336 request riêng lẻ, không có sẵn file zip gộp).

**Nội dung data**: 40.336 file `.psv` (20.336 ở `training_setA/`, 20.000 ở `training_setB/`), mỗi file là 1 bệnh nhân, các dòng là chuỗi thời gian đo theo giờ (`ICULOS`). Cột liên quan tới dự án: `HR, O2Sat, Temp, SBP, MAP, DBP, Resp` (sinh hiệu), `Bilirubin_total, Bilirubin_direct, AST, Alkalinephos` (sinh hóa gan), `Hct, Hgb, WBC, Platelets` (CBC rút gọn), **`PTT, Fibrinogen`** (đông máu), `Age, Gender` (thông tin bệnh nhân), **`SepsisLabel`** (nhãn nhị phân theo từng giờ).

**Review data có gì**:
- Đây là nguồn **duy nhất** trong toàn bộ kho bù được một phần chỉ số **đông máu** (Fibrinogen chắc chắn khớp; PTT có khả năng tương đương aPTT nhưng cần xác minh vì PTT và aPTT về mặt xét nghiệm không hoàn toàn là một).
- Có nhãn outcome thật (`SepsisLabel`) nhưng là **nhiễm trùng huyết**, không phải bệnh lý huyết học trong 9 nhóm bệnh mục tiêu của dự án.
- Kiểm tra ban đầu (không rỗng) cho thấy 100% file tải thành công, nhưng **EDA bằng notebook sau đó phát hiện 5/40.336 file thực chất là trang lỗi HTML** (không rỗng nhưng sai nội dung, lọt qua bước kiểm tra ban đầu) — đã xác định và tải lại đúng cả 5 file, xác minh lại toàn bộ 40.336 file hợp lệ 100%. Bài học: kiểm tra "không rỗng" là chưa đủ, cần kiểm tra nội dung/parse thử.

**EDA sơ bộ** (xem `EDA/03_physionet_sepsis_2019.ipynb` — lấy mẫu ngẫu nhiên 2.000/40.336 bệnh nhân để phân tích nhanh):
- Dữ liệu dạng time-series đa biến, **tỷ lệ missing rất cao** ở các chỉ số xét nghiệm không đo mỗi giờ (Fibrinogen, PTT, Bilirubin) — cần chiến lược xử lý riêng (forward-fill, hoặc chỉ giữ dòng có đo xét nghiệm) trước khi coi là dữ liệu bảng tĩnh.
- Kích thước: 336MB.

---

## 4. Kaggle CBC (vizeno)

**Nguồn thu thập**: Kaggle `vizeno/complete-blood-count-cbc-dataset` — người dùng tự tải tay qua trình duyệt (Kaggle yêu cầu đăng nhập, không tự động hoá được).

**Nội dung data**: File `blood_count_dataset.csv` — 417 dòng × 9 cột: `Age, Gender, Hemoglobin, Platelet_Count, White_Blood_Cells, Red_Blood_Cells, MCV, MCH, MCHC`.

**Review data có gì**:
- Không có giá trị thiếu.
- **Trùng lặp cực nặng: 323/417 dòng bị trùng lặp hoàn toàn (77.5%)** — chỉ còn ~94 dòng thật sự khác nhau, đây là mức trùng lặp cao nhất trong toàn bộ kho dữ liệu.
- **Không có cột nhãn bệnh.**
- Có `Age` và `Gender` — bù được một phần nhỏ cho nhóm "thông tin bệnh nhân" đang thiếu.

**EDA sơ bộ**:
- `describe()` cho thấy phân phối các chỉ số nằm trong khoảng sinh học hợp lý (không có giá trị âm/vô lý như bộ CBC Test dataset) — chất lượng giá trị tốt hơn, nhưng số lượng dòng thật sự dùng được lại rất ít do trùng lặp.

---

## 5. Kaggle COVID-19 CBC

**Nguồn thu thập**: Kaggle `tawsifurrahman/covid19-complete-blood-count-clinical-database` — người dùng tự tải tay.

**Nội dung data**: File `COVID-19_CBC_Data.csv` — 103 dòng × 14 cột: `Admission_DATE, Discharge_DATE or date of Death, Outcome, Patient Age, Gender, Sample Collection Date, What kind of Treatment provided, Ventilated (Y/N), Red blood cell distribution width, Monocytes(%), White blood cell count, Platelet Count, Lymphocyte Count, Neutrophils Count`.

**Review data có gì**:
- Không có giá trị thiếu — hiếm gặp so với các bộ khác trong kho.
- Có nhãn **Outcome** thật (Recovered / Not Recovered) — nhưng là outcome điều trị COVID-19, không phải chẩn đoán bệnh huyết học.
- Thiếu nhiều chỉ số CBC cốt lõi so với 2 bộ CBC kia (không có RBC, Hgb, HCT, MCV, MCH, MCHC).
- Cỡ mẫu rất nhỏ (103 dòng) — chỉ phù hợp làm proof-of-concept, không đủ để train model đáng tin cậy.

**EDA sơ bộ**:
- Phân bố nhãn: Recovered 61 (59.2%), Not Recovered 42 (40.8%) — tương đối cân bằng.

---

## 6. Rheumatic & Autoimmune Disease Dataset

**Nguồn thu thập**: Harvard Dataverse, DOI `10.7910/DVN/VM4OR3` — người dùng tự tải tay (khi thử tự động hoá, bị chặn bởi AWS WAF bot-challenge `x-amzn-waf-action: challenge`, không vượt qua được bằng curl).

**Nội dung data**: File `Rheumatic and Autoimmune Disease Dataset.xlsx` — **12.085 dòng × 15 cột**: `Age, Gender, ESR, CRP, RF, Anti-CCP, HLA-B27, ANA, Anti-Ro, Anti-La, Anti-dsDNA, Anti-Sm, C3, C4, Disease`.

**Review data có gì**:
- **Chất lượng tốt nhất trong toàn bộ kho dữ liệu đã thu thập**: 0 dòng trùng lặp, cỡ mẫu lớn (12.085 dòng).
- Có `ESR` và `CRP` thật — 2 chỉ số sinh hóa duy nhất trong kho có dữ liệu thực tế (trước đó hoàn toàn không có nguồn nào).
- Có nhãn `Disease` thật với 7 lớp: Rheumatoid Arthritis, Ankylosing Spondylitis, Sjögren's Syndrome, Psoriatic Arthritis, Normal, Systemic Lupus Erythematosus, Reactive Arthritis.
- **Giới hạn quan trọng**: đây là bệnh **tự miễn/thấp khớp**, không thuộc 9 nhóm bệnh huyết học mục tiêu của dự án — chỉ dùng được để bù chỉ số CRP/ESR làm dữ liệu tham chiếu/huấn luyện phụ (transfer learning, hoặc mở rộng phạm vi hệ thống), không dùng làm nhãn chính cho bài toán chẩn đoán huyết học.
- Có missing value ở các cột huyết thanh học (ESR thiếu 9%, CRP thiếu 20%, các marker khác thiếu 15–43%) — hợp lý vì không phải bệnh nhân nào cũng làm đủ panel xét nghiệm.

**EDA sơ bộ**:
- Phân bố nhãn Disease: Rheumatoid Arthritis 2.848, Ankylosing Spondylitis 2.127, Sjögren's Syndrome 1.852, Psoriatic Arthritis 1.783, Normal 1.604, Systemic Lupus Erythematosus 1.355, Reactive Arthritis 516 — lớp nhỏ nhất vẫn có 516 mẫu, mức mất cân bằng chấp nhận được (khác hẳn tình trạng lệch cực đoan ở các bộ ảnh).
- Thống kê CRP: mean 13.33, std 10.39, min 0.10, max 30.00 (n=9.668 sau loại missing).
- Thống kê ESR: mean 24.21, std 14.37, min 0.00, max 49.00 (n=10.997 sau loại missing).

---

## 7. MDS Bone Marrow Cell Dataset

**Nguồn thu thập**: figshare, DOI `10.6084/m9.figshare.28737170.v1` — bài báo "A large dataset of bone marrow cells in myelodysplastic syndrome for classification systems" (Scientific Data, 2025). Tải tự động bằng curl (link tải trực tiếp qua figshare API).

**Nội dung data**: `dataset_BM_cell_MDS.zip` (giữ nguyên gốc) + đã giải nén — **25.067 ảnh JPEG**, 54 thư mục lớp con (33 loại tế bào × 2 thư mục `main/`+`add/`), gồm cả tế bào bình thường và bất thường đặc trưng của MDS (Blast NOC, Myeloblast, Dysplastic erythroblast, Micromegakaryocyte, Segmented neutrophil...).

**Review data có gì**:
- Đây là nguồn ảnh **duy nhất** trong kho có gán nhãn tế bào bất thường thật sự liên quan đến bệnh lý huyết học (Hội chứng loạn sản tủy).
- Gán nhãn bởi tối đa 3 chuyên gia độc lập — độ tin cậy nhãn cao.

**EDA sơ bộ** (script: `eda/eda_images.py`, output: `eda/report_images.txt`):
- **Mất cân bằng cực đoan**: lớp nhiều nhất `Mature lymphocyte` = 3.958 ảnh (15.83%), lớp ít nhất `Dysplastic megakaryocyte` = **chỉ 1 ảnh** — tỷ lệ lệch **3.958 lần**.
- Nhiều lớp có dưới 10 ảnh (VD `Segmented basophil` add = 2, `Proerythroblast` add = 3, `Mitosis` add = 7) — không đủ để train riêng, bắt buộc phải gộp nhóm hoặc dùng few-shot/augmentation mạnh.

---

## 8. TXL-PBC

**Nguồn thu thập**: GitHub `lugan113/TXL-PBC_Dataset` — dữ liệu gộp/tái gán nhãn từ 4 nguồn công khai (BCCD, BCDD, PBC Barcelona, Raabin-WBC). Tải tự động bằng `git clone`.

**Nội dung data**: `TXL-PBC/images/{train,val,test}` + `TXL-PBC/labels/{train,val,test}` — 1.260 ảnh với 18.143 bounding box annotation dạng **YOLO detection**, chỉ 3 lớp: `WBC (0), RBC (1), Platelet (2)`.

**Review data có gì**:
- Đây là bài toán **object detection** (định vị + đếm tế bào trong ảnh), khác hẳn bản chất với 2 bộ ảnh kia (classification từng ảnh 1 tế bào) — không thể gộp trực tiếp làm cùng 1 pipeline huấn luyện.
- Chỉ phân biệt 3 loại tế bào lớn (không phân loại tiếp neutrophil/eosinophil/lymphocyte...) — muốn phân loại chi tiết hơn phải dùng nguồn khác (VD Raabin, PBC Barcelona).
- Đi kèm sẵn script gốc: `dataset_splits.py`, `baseline_model.py`, `dataset_statistical_analysis.py`.

**EDA sơ bộ**:
- Số ảnh theo split: train 882, val 252, test 126.
- Số bounding box theo lớp (tập train): WBC 908 (7.3%), **RBC 11.220 (89.7%)**, Platelet 382 (3.0%) — RBC áp đảo hoàn toàn (đúng thực tế sinh học), cần class weighting/loss balancing khi huấn luyện detection.

---

## 9. PBC Barcelona

**Nguồn thu thập**: Mendeley Data (Acevedo et al., Hospital Clinic Barcelona), liên kết DOI `snkd93bnjr` — người dùng tự tải tay (khi thử tự động qua Mendeley public API, gặp lỗi 404/chặn JS, không tải được).

**Nội dung data**: `PBC_dataset_normal_DIB/` — **17.093 ảnh JPG** (360×363px, chụp bằng máy CellaVision DM96), 8 thư mục lớp: `basophil, eosinophil, erythroblast, ig (immature granulocytes), lymphocyte, monocyte, neutrophil, platelet`.

**Review data có gì**:
- Toàn bộ mẫu lấy từ người **khỏe mạnh** (không nhiễm trùng, không bệnh huyết học/ung thư, không dùng thuốc tại thời điểm lấy máu) — chỉ dùng để nhận diện loại tế bào nền, **không dùng để phát hiện bất thường/bệnh lý**.
- Gán nhãn bởi bác sĩ giải phẫu bệnh chuyên khoa.

**EDA sơ bộ**:
- Số ảnh theo lớp: neutrophil 3.330, eosinophil 3.117, ig 2.895, platelet 2.348, erythroblast 1.551, monocyte 1.420, basophil 1.218, lymphocyte 1.214.
- Mức mất cân bằng: lệch tối đa ~**2.7 lần** (3.330/1.214) — **cân bằng tốt hơn đáng kể** so với MDS Bone Marrow (3.958 lần), phù hợp làm dữ liệu train/pretrain cho bài toán phân loại bạch cầu.

---

## 10. NHANES 2015-2016 CBC_I

**Nguồn thu thập**: CDC/NCHS — National Health and Nutrition Examination Survey (NHANES) 2015-2016, khảo sát sức khỏe dân số quốc gia Mỹ. File [CBC_I](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2015/DataFiles/CBC_I.htm) + [DEMO_I](https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2015/DataFiles/DEMO_I.htm) — nguồn tìm được từ đồng đội (`Reference_Data.md`), tải tự động bằng curl (public hoàn toàn, không cần đăng ký/credential, khác hẳn phần lớn nguồn Kaggle/Dataverse gặp phải trước đó).

**Nội dung data**: File gốc `CBC_I.XPT` + `DEMO_I.XPT` (định dạng SAS Transport) — đã parse bằng `pandas.read_sas` và join qua khóa `SEQN`, xuất ra `CBC_I_with_demographics.csv` — **9.165 dòng × 23 cột**: `SEQN, LBXWBCSI (WBC), LBXLYPCT/LBDLYMNO (Lymphocyte %/số tuyệt đối), LBXMOPCT/LBDMONO (Monocyte), LBXNEPCT/LBDNENO (Neutrophil), LBXEOPCT/LBDEONO (Eosinophil), LBXBAPCT/LBDBANO (Basophil), LBXRBCSI (RBC), LBXHGB (Hemoglobin), LBXHCT (Hematocrit), LBXMCVSI (MCV), LBXMCHSI (MCH), LBXMC (MCHC), LBXRDW (RDW), LBXPLTSI (Platelet), LBXMPSI (MPV), Age, Gender`.

**Review data có gì**:
- **Chất lượng cao nhất trong toàn bộ kho** xét về độ tin cậy nguồn: dữ liệu khảo sát chính phủ, có phương pháp luận công khai, không phát hiện giá trị âm/vô lý nào (khác hẳn bộ CBC Test dataset #1 và Kaggle CBC vizeno #4).
- Bao phủ đầy đủ **CBC 5-dòng bạch cầu** (cả % và số tuyệt đối cho Lymphocyte, Monocyte, Neutrophil, Eosinophil, Basophil) + các chỉ số hồng cầu/tiểu cầu chuyên sâu (HCT, RDW, MPV) — đầy đủ hơn cả bộ CBC Test dataset #1 vốn thiếu dạng số tuyệt đối riêng biệt cho từng dòng bạch cầu.
- Đã join sẵn `Age` (1–80 tuổi, bao phủ cả trẻ em) và `Gender` qua khóa `SEQN` với file Demographics.
- **Giới hạn quan trọng**: đây là dữ liệu khảo sát sức khỏe dân số, **không có nhãn chẩn đoán bệnh** — không dùng trực tiếp cho bài toán phân loại bệnh, chỉ dùng làm nguồn "phân phối bình thường" chất lượng cao (baseline references theo tuổi/giới) hoặc để tăng cường/pretrain.

**EDA sơ bộ**:
- 1.049/9.165 dòng thiếu phần 5-dòng bạch cầu chi tiết (còn 8.116 dòng đầy đủ hoàn toàn — khớp với mô tả gốc "8.117 mẫu hoàn chỉnh").
- Age: mean 33.19, std 24.31, min 1, max 80 — phân phối trải rộng toàn bộ lứa tuổi.
- Gender: 4.668 nữ (mã 2) / 4.497 nam (mã 1) — cân bằng tốt.

---

## Nguồn đã biết, chưa thu thập

Từ `Reference_Data.md` của đồng đội — 3 nguồn còn lại đều nằm trên Kaggle, cần tài khoản/API token để tải (khác NHANES ở trên):

| Dataset | Link | Giá trị dự kiến | Trạng thái |
|---|---|---|---|
| **Personalized Medication Dataset** | [kaggle.com/ziya07/personalized-medication-dataset](https://www.kaggle.com/datasets/ziya07/personalized-medication-dataset) | Có Age/Gender/Weight/Height/BMI, Medical history (Chronic conditions/Drug allergies/Genetic disorders), **Symptoms, Diagnosis**, Medication, Outcome — nguồn tiềm năng nhất để bù nhóm "thông tin bệnh nhân + triệu chứng + nhãn chẩn đoán" đang trống hoàn toàn. Không có CBC đầy đủ | Chưa tải — chờ quyết định về Kaggle |
| **Laboratory Data** | [kaggle.com/klingill/laboratory-data](https://www.kaggle.com/datasets/klingill/laboratory-data) | ~12.009 dòng: Age/Gender, RBC/WBC/Hemoglobin + AST/ALT/Cholesterol/Glucose/Lipase/Creatinine/Troponin — không phải các chỉ số thiếu máu chuyên biệt (Ferritin/Iron/TIBC/B12/Folate) đang thiếu | Chưa tải — chờ quyết định về Kaggle |
| **Disease-Symptom Dataset** | [kaggle.com/dhivyeshrk/diseases-and-symptoms-dataset](https://www.kaggle.com/datasets/dhivyeshrk/diseases-and-symptoms-dataset) | 246.000 dòng, 773 bệnh, 377 triệu chứng one-hot — **dữ liệu tổng hợp/synthetic**, không phải ca bệnh thật. Trùng với nguồn tôi tự tìm được độc lập trước đó (cross-confirm) | Chưa tải — chờ quyết định về Kaggle |

Ghi chú: `Reference_Data.md` chỉ liệt kê mục 1, 5, 6, 10 — có khả năng còn mục 2, 3, 4, 7, 8, 9 chưa được chia sẻ, cần xin thêm để đối chiếu đầy đủ.

---

## Tổng kết đối chiếu với yêu cầu dự án gốc

| Nhóm chỉ số cần (theo `Hematology_AI_System_Overview.md`) | Mức độ đáp ứng | Nguồn |
|---|---|---|
| CBC (RBC, WBC, PLT, Hb, HCT, MCV, MCH, MCHC, RDW, MPV, PDW, PCT, Neutrophil, Lymphocyte) | ✅ Đầy đủ, có 2 nguồn chất lượng cao | Bộ #1 (CBC Test dataset), Bộ #10 (NHANES — chất lượng tốt hơn, quy mô 9.165 người) |
| CRP, ESR | ✅ Có thật | Bộ #6 (Rheumatic Dataverse) — nhưng gắn với bệnh tự miễn, không phải huyết học |
| Bilirubin | ✅ Có thật | Bộ #3 (PhysioNet Sepsis) |
| Fibrinogen | ✅ Có thật | Bộ #3 (PhysioNet Sepsis) |
| PTT (~aPTT, cần xác minh) | 🟡 Có, chưa chắc tương đương | Bộ #3 (PhysioNet Sepsis) |
| Tuổi, Giới tính | ✅ Có thật | Bộ #3, #4, #6, #10 |
| Chiều cao, cân nặng, tiền sử bệnh, dị ứng thuốc | 🟡 Có nguồn, chưa tải | Personalized Medication Dataset (Kaggle, xem mục "Nguồn đã biết, chưa thu thập") |
| Triệu chứng lâm sàng, Nhãn chẩn đoán (Diagnosis) | 🟡 Có nguồn tiềm năng, chưa tải, chưa xác minh có phải bệnh huyết học | Personalized Medication Dataset (Kaggle) |
| Ferritin, Serum Iron, TIBC, Vitamin B12, Folate, LDH, Haptoglobin | ❌ Không có nguồn public nào | — |
| PT, INR, D-Dimer | ❌ Không có nguồn public nào | — |
| Nhãn chẩn đoán đúng theo 9 nhóm bệnh huyết học gốc | ❌ Chưa có bộ nào đạt được | Các nhãn hiện có (SepsisLabel, Result, Outcome, Disease) đều thuộc bệnh lý khác hoặc quá đơn giản (nhị phân) |

**Kết luận**: mảng CBC đã hoàn thiện rất tốt (2 nguồn độc lập, chất lượng cao); mảng đông máu và sinh hóa chỉ đạt một phần nhỏ; mảng thông tin bệnh nhân/triệu chứng vừa xuất hiện nguồn tiềm năng (Personalized Medication Dataset) nhưng chưa tải/xác minh; nhãn chẩn đoán huyết học chuyên biệt vẫn hoàn toàn trống — cần thu thập dữ liệu thật hoặc thu hẹp phạm vi hệ thống ở giai đoạn đầu.
