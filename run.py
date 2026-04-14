import os
from app import create_app

# Khởi tạo app từ folder 'app'
app = create_app()

if __name__ == '__main__':
    # Chỉ dùng khi chạy máy cá nhân
    port = int(os.environ.get("PORT", 500))
    app.run(host='0.0.0.0', port=port)
