from pathlib import Path

readme = r'''<div align="center">
  <img src="https://img.icons8.com/?size=512&id=T256B7gC0I20&format=png" width="100" alt="AI Healthcare Icon" />

  <h1>🩸 HỆ THỐNG AI HỖ TRỢ CHẨN ĐOÁN SƠ BỘ BỆNH LÝ HUYẾT HỌC 🤖</h1>

  <p>
    <b>Hệ thống AI hỗ trợ bác sĩ phân tích dữ liệu huyết học, đánh giá nguy cơ và tham khảo các bệnh lý có khả năng mắc</b>
  </p>

  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Jupyter-F37626.svg?&style=for-the-badge&logo=Jupyter&logoColor=white" alt="Jupyter" />
    <img src="https://img.shields.io/badge/NumPy-777BB4?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy" />
    <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  </p>
</div>

<hr />

## 📖 Giới thiệu (Introduction)

Dự án **Hệ thống AI Hỗ trợ Chẩn đoán Sơ bộ Bệnh lý Huyết học** được xây dựng nhằm hỗ trợ bác sĩ trong quá trình **phân tích dữ liệu huyết học**, **đánh giá nguy cơ** và **tham khảo danh sách các bệnh lý có khả năng mắc** dựa trên nhiều nguồn thông tin liên quan.

Hệ thống hướng đến việc khai thác và kết hợp các dữ liệu như:

- **Dữ liệu xét nghiệm máu** và các chỉ số huyết học.
- **Thông tin lâm sàng** liên quan đến người bệnh.
- **Các xét nghiệm liên quan** được cung cấp trong quá trình đánh giá.

Mục tiêu của dự án là tạo ra một hệ thống có khả năng hỗ trợ quá trình ra quyết định lâm sàng bằng cách cung cấp các thông tin tham khảo từ dữ liệu, từ đó giúp bác sĩ có thêm cơ sở trong quá trình đánh giá người bệnh.

> ⚠️ **Lưu ý quan trọng:** Hệ thống **không thay thế bác sĩ** và không đưa ra chẩn đoán y khoa cuối cùng. Dự án được định hướng như một **Clinical Decision Support System (CDSS)**, đóng vai trò hỗ trợ bác sĩ trong quá trình phân tích và đánh giá, trong khi quyết định chẩn đoán và điều trị cuối cùng thuộc về nhân viên y tế có chuyên môn.

---

## 🎯 Mục tiêu dự án (Project Objectives)

Dự án tập trung vào các mục tiêu chính:

1. **Thu thập và tổ chức dữ liệu** phục vụ bài toán bệnh lý huyết học.
2. **Khám phá dữ liệu (EDA)** để hiểu đặc điểm, phân bố và mối quan hệ giữa các biến.
3. **Làm sạch và chuẩn hóa dữ liệu** nhằm tạo nguồn dữ liệu phù hợp cho các bước phân tích tiếp theo.
4. **Phân tích dữ liệu huyết học** dựa trên các chỉ số xét nghiệm và thông tin liên quan.
5. **Đánh giá nguy cơ** dựa trên dữ liệu đầu vào.
6. **Tham khảo danh sách bệnh lý có khả năng mắc** thay vì đưa ra kết luận chẩn đoán cuối cùng.
7. Từng bước phát triển thành một hệ thống **CDSS** có khả năng hỗ trợ bác sĩ trong thực hành lâm sàng.

---

## 📂 Cấu trúc dự án (Project Structure)

Cấu trúc dự án hiện tại được tổ chức theo hướng tách biệt giữa dữ liệu, dữ liệu đã làm sạch và tài liệu tham khảo:

```text
Hệ thống AI Hỗ trợ Chẩn đoán Sơ bộ Bệnh lý Huyết học/
│
├── 📁 Data/
│   ├── 📁 eda/
│   ├── 📁 tabular/
│   └── 📁 images/
│
├── 📁 Clean/
│
├── 📁 Clean_Data/
│
├── 📁 Tài liệu tham khảo/
│   └── 📄 du_lieu_tham_khao.md
│
├── 📄 *.py
├── 📓 *.ipynb
└── 📄 README.md