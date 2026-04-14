NEU Student Portal - Cổng Thông Tin Sinh Viên 

Dự án xây dựng hệ thống quản lý và tra cứu thông tin sinh viên dành cho sinh viên Đại học Kinh tế Quốc dân (NEU). Hệ thống được tích hợp các công nghệ hiện đại như Trợ lý ảo AI và Thư viện số thông minh.

 Tính năng nổi bật

1. Dashboard 

Hiển thị thông tin cá nhân dưới dạng thẻ sinh viên số.

Thống kê nhanh KPI học tập: GPA tích lũy, Số tín chỉ, Tình trạng học phí.

Thời khóa biểu tuần trực quan và danh sách thông báo mới nhất.

2. Thư viện số 

Giao diện tra cứu sách được thiết kế theo phong cách cổng truyện hiện đại.

Tính năng cá nhân hóa: Tự động đề xuất giáo trình và tài liệu dựa trên các môn học sinh viên đang đăng ký trong kỳ.

Thông tin chi tiết: Pop-up hiển thị mô tả, chủ đề và bìa sách tối giản (Minimalist Cover) cho các đầu sách thiếu ảnh.

Tích hợp dữ liệu từ Open Library API.

3. Trợ lý ảo NEU AI

Hỗ trợ giải đáp quy chế, tư vấn lộ trình học tập và tính toán điểm mục tiêu.

Chế độ linh hoạt: Hỗ trợ cả Gemini API (Cloud) và Ollama (Local AI - Llama3/Mistral).

4. Quản lý Đào tạo & Tài chính

Bảng điểm: Theo dõi kết quả học tập chi tiết qua từng kỳ.

Chương trình đào tạo: Tra cứu lộ trình các môn học dự kiến theo ngành.

Học phí: Quản lý hóa đơn, chi tiết học phần và tích hợp thanh toán E-bills.

 Công nghệ sử dụng

Backend: Python (Flask)

Database: SQLAlchemy (SQLite) - Thiết kế chuẩn theo ERD quan hệ.

Frontend: Jinja2, Bootstrap 5, FontAwesome, JavaScript (ES6+).

AI Integration: Google Gemini API / Ollama Service.

Deployment: Render, Gunicorn.

 Cấu trúc dự án

├── app/
│   ├── templates/          # Giao diện HTML (Jinja2)
│   ├── static/             # CSS, JS, Hình ảnh
│   ├── models.py           # Định nghĩa cấu trúc Database (ERD)
│   ├── auth.py             # Xử lý đăng nhập/đăng ký
│   ├── home.py             # Logic Dashboard chính
│   ├── ai_assistant.py     # Module Trợ lý AI
│   └── library.py          # Module Thư viện số
├── DBwebSv.db              # File cơ sở dữ liệu SQLite
├── run.py                  # File khởi chạy ứng dụng
├── requirements.txt        # Danh sách thư viện cần thiết
└── Procfile                # Cấu hình triển khai Render


Hướng dẫn cài đặt

Clone dự án:

git clone [https://github.com/yourusername/neu-student-portal.git](https://github.com/yourusername/neu-student-portal.git)
cd neu-student-portal


Cài đặt môi trường ảo & Thư viện:

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt


Cấu hình AI (Tùy chọn):

Để dùng AI Local: Cài đặt Ollama và chạy ollama run llama3.

Để dùng Cloud: Đăng ký API Key tại Google AI Studio.

Chạy ứng dụng:

python run.py


Truy cập: https://lms-ua01.onrender.com

Triển khai (Deployment)

Dự án được tối ưu hóa để triển khai trên Render hoặc PythonAnywhere.

Build Command: pip install -r requirements.txt

Start Command: gunicorn run:app

Bản quyền

© 2026 Dự án thuộc về Sinh viên Đại học Kinh tế Quốc dân.
