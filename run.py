from app import create_app

# Khởi tạo toàn bộ ứng dụng
app = create_app()

if __name__ == '__main__':
    # Chạy Server
    app.run(debug=True, port=5000)