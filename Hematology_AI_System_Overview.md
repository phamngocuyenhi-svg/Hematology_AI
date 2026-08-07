# Hệ thống AI Hỗ trợ Chẩn đoán Sơ bộ Bệnh lý Huyết học

## 1. Kiến trúc hệ thống đề xuất

### Mục tiêu

Xây dựng hệ thống AI hỗ trợ bác sĩ trong việc phân tích dữ liệu huyết học, đánh giá nguy cơ và đưa ra danh sách các bệnh lý có khả năng mắc dựa trên dữ liệu xét nghiệm máu, thông tin lâm sàng và các xét nghiệm liên quan.

Hệ thống **không thay thế bác sĩ**, mà đóng vai trò **Clinical Decision Support System (CDSS)**.


## Kiến trúc tổng thể

```text
                           Hồ sơ bệnh nhân
                                  │
          ┌───────────────────────┼────────────────────────┐
          │                       │                        │
     Thông tin cá nhân        Triệu chứng           Tiền sử bệnh
          │                       │                        │
          └───────────────────────┼────────────────────────┘
                                  │
                           CBC & Xét nghiệm
                                  │
          ┌───────────────────────┼────────────────────────┐
          │                       │                        │
      Sinh hóa máu          Đông máu              Các xét nghiệm khác
                                  │
                                  ▼
                     AI Clinical Decision Engine
                                  │
      ┌──────────────┬──────────────┬──────────────┐
      │              │              │
 CBC Analysis   Disease Prediction  Risk Prediction
      │              │              │
      └──────────────┴──────────────┘
                     │
             Explainable AI (XAI)
                     │
                     ▼
      Báo cáo hỗ trợ chẩn đoán cho bác sĩ
```

## Quy trình hoạt động

1. Nhập dữ liệu bệnh nhân.
2. Kiểm tra tính hợp lệ của dữ liệu.
3. Tiền xử lý dữ liệu.
4. Chuẩn hóa dữ liệu.
5. Đưa dữ liệu vào mô hình AI.
6. AI đánh giá từng nhóm bệnh.
7. Xếp hạng các bệnh có khả năng mắc.
8. Sinh báo cáo hỗ trợ bác sĩ.


# 2. Dữ liệu đầu vào

## 2.1 Thông tin bệnh nhân

| Thuật ngữ | Ý nghĩa | Vai trò |
|-----------|----------|----------|
| Patient ID | Mã bệnh nhân | Định danh dữ liệu |
| Age | Tuổi | Một số bệnh phụ thuộc độ tuổi |
| Gender | Giới tính | Một số bệnh khác nhau theo giới |
| Height | Chiều cao | Tính BMI |
| Weight | Cân nặng | Đánh giá thể trạng |
| BMI | Chỉ số khối cơ thể | Hỗ trợ đánh giá sức khỏe |
| Occupation | Nghề nghiệp | Một số nghề có nguy cơ tiếp xúc hóa chất |
| Smoking | Hút thuốc | Tăng nguy cơ nhiều bệnh máu |
| Alcohol | Uống rượu | Ảnh hưởng tủy xương và gan |
| Family History | Tiền sử gia đình | Đánh giá yếu tố di truyền |
| Medical History | Tiền sử bệnh | Hỗ trợ chẩn đoán |
| Current Medication | Thuốc đang sử dụng | Một số thuốc ảnh hưởng công thức máu |


## 2.2 Triệu chứng lâm sàng

| Triệu chứng | Ý nghĩa | Gợi ý bệnh |
|-------------|----------|------------|
| Fatigue | Mệt mỏi | Thiếu máu |
| Fever | Sốt | Nhiễm trùng, Leukemia |
| Weight Loss | Sụt cân | Ung thư máu |
| Night Sweats | Đổ mồ hôi đêm | Lymphoma |
| Easy Bruising | Dễ bầm tím | Giảm tiểu cầu |
| Bleeding | Chảy máu | Rối loạn đông máu |
| Bone Pain | Đau xương | Leukemia, Myeloma |
| Enlarged Lymph Nodes | Nổi hạch | Lymphoma |
| Shortness of Breath | Khó thở | Thiếu máu |
| Pale Skin | Da xanh xao | Thiếu máu |
| Petechiae | Chấm xuất huyết | Giảm tiểu cầu |


## 2.3 Công thức máu (Complete Blood Count - CBC)

| Chỉ số | Tên đầy đủ | Ý nghĩa | Ứng dụng |
|---------|------------|----------|-----------|
| RBC | Red Blood Cell | Số lượng hồng cầu | Chẩn đoán thiếu máu |
| WBC | White Blood Cell | Số lượng bạch cầu | Nhiễm trùng, Leukemia |
| PLT | Platelet | Tiểu cầu | Đánh giá đông máu |
| Hb | Hemoglobin | Nồng độ Hemoglobin | Thiếu máu |
| HCT | Hematocrit | Tỷ lệ thể tích hồng cầu | Thiếu máu |
| MCV | Mean Corpuscular Volume | Kích thước hồng cầu | Phân loại thiếu máu |
| MCH | Mean Corpuscular Hemoglobin | Lượng Hb trung bình | Đánh giá hồng cầu |
| MCHC | Mean Corpuscular Hemoglobin Concentration | Nồng độ Hb | Thiếu máu |
| RDW | Red Cell Distribution Width | Độ phân bố kích thước hồng cầu | Phân biệt các loại thiếu máu |
| MPV | Mean Platelet Volume | Kích thước tiểu cầu | Bệnh tiểu cầu |
| PDW | Platelet Distribution Width | Độ phân bố tiểu cầu | Rối loạn tiểu cầu |
| PCT | Plateletcrit | Thể tích tiểu cầu | Đánh giá tổng lượng tiểu cầu |
| Neutrophil | Bạch cầu trung tính | Chống vi khuẩn | Nhiễm khuẩn |
| Lymphocyte | Bạch cầu lympho | Miễn dịch | Virus, Leukemia |
| Monocyte | Bạch cầu mono | Viêm mạn tính | Nhiễm trùng |
| Eosinophil | Bạch cầu ái toan | Dị ứng, ký sinh trùng | Dị ứng |
| Basophil | Bạch cầu ái kiềm | Phản ứng miễn dịch | Một số bệnh tăng sinh tủy |
| NRBC | Nucleated RBC | Hồng cầu có nhân | Bệnh lý tủy xương |
| Reticulocyte | Hồng cầu lưới | Hồng cầu non | Đánh giá sinh hồng cầu |


## 2.4 Sinh hóa máu

| Xét nghiệm | Ý nghĩa | Ứng dụng |
|-------------|----------|-----------|
| Ferritin | Dự trữ sắt | Thiếu máu thiếu sắt |
| Serum Iron | Sắt huyết thanh | Đánh giá chuyển hóa sắt |
| TIBC | Total Iron Binding Capacity | Khả năng gắn sắt | Thiếu máu |
| Transferrin Saturation | Độ bão hòa Transferrin | Thiếu sắt |
| Vitamin B12 | Vitamin B12 | Thiếu máu hồng cầu khổng lồ |
| Folate | Acid folic | Thiếu máu Megaloblastic |
| LDH | Lactate Dehydrogenase | Tan máu |
| Bilirubin | Bilirubin | Thiếu máu tan máu |
| Haptoglobin | Haptoglobin | Đánh giá tan máu |
| CRP | C-Reactive Protein | Viêm |
| ESR | Erythrocyte Sedimentation Rate | Tốc độ lắng máu | Viêm, tự miễn |


## 2.5 Xét nghiệm đông máu

| Xét nghiệm | Ý nghĩa | Ứng dụng |
|-------------|----------|-----------|
| PT | Prothrombin Time | Đường đông máu ngoại sinh | Đánh giá đông máu |
| INR | International Normalized Ratio | Chuẩn hóa PT | Theo dõi Warfarin |
| aPTT | Activated Partial Thromboplastin Time | Đường đông máu nội sinh | Hemophilia |
| Fibrinogen | Protein đông máu | DIC |
| D-Dimer | Sản phẩm thoái hóa fibrin | Huyết khối |
| Thrombin Time | Thời gian Thrombin | Đánh giá Fibrinogen |
| Anti-Xa | Hoạt tính kháng Xa | Theo dõi Heparin |


# 3. Các nhóm bệnh hệ thống hỗ trợ

## 3.1 Thiếu máu (Anemia)

- Iron Deficiency Anemia
- Thalassemia
- Megaloblastic Anemia
- Hemolytic Anemia
- Aplastic Anemia
- Anemia of Chronic Disease
- Sickle Cell Disease


## 3.2 Bệnh bạch cầu (Leukemia)

- Acute Lymphoblastic Leukemia (ALL)
- Acute Myeloid Leukemia (AML)
- Chronic Lymphocytic Leukemia (CLL)
- Chronic Myeloid Leukemia (CML)


## 3.3 Rối loạn bạch cầu

- Leukocytosis
- Leukopenia
- Neutropenia
- Neutrophilia
- Lymphocytosis
- Lymphopenia
- Monocytosis
- Eosinophilia
- Basophilia

## 3.4 Bệnh lý tiểu cầu

- Thrombocytopenia
- Immune Thrombocytopenia (ITP)
- Thrombocytosis
- Essential Thrombocythemia


## 3.5 Rối loạn đông máu

- Disseminated Intravascular Coagulation (DIC)
- Hemophilia A
- Hemophilia B
- Von Willebrand Disease
- Deep Vein Thrombosis (DVT)
- Pulmonary Embolism (PE)


## 3.6 Bệnh tăng sinh tủy

- Polycythemia Vera
- Primary Myelofibrosis
- Essential Thrombocythemia
- Chronic Neutrophilic Leukemia


## 3.7 Hội chứng loạn sản tủy

- Myelodysplastic Syndrome (MDS)

## 3.8 U lympho và bệnh tương bào

- Hodgkin Lymphoma
- Non-Hodgkin Lymphoma
- Multiple Myeloma
- Monoclonal Gammopathy (MGUS)


## 3.9 Các bệnh huyết học khác

- Pancytopenia
- Polycythemia
- Febrile Neutropenia
- Hemophagocytic Lymphohistiocytosis (HLH)
- Paroxysmal Nocturnal Hemoglobinuria (PNH)

---

# Ghi chú

- Hệ thống chỉ có vai trò **hỗ trợ quyết định lâm sàng**, không thay thế bác sĩ.
- Kết quả AI nên trả về **Top-N bệnh có khả năng cao nhất** kèm theo xác suất dự đoán và giải thích dựa trên các chỉ số đầu vào.
- Trong tương lai có thể mở rộng bằng cách tích hợp thêm dữ liệu ảnh tiêu bản máu, Flow Cytometry, xét nghiệm di truyền và dữ liệu giải trình tự gen để nâng cao độ chính xác.