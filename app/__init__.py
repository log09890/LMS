from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Khởi tạo đối tượng db bên ngoài để tránh lỗi vòng lặp (circular import)
from .models import db


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'neu_student_portal_2026_secret'

    # Lấy đường dẫn thư mục gốc của dự án (thư mục chứa run.py)
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # 1. Cấu hình Database CHÍNH
    main_db_path = os.path.join(basedir, 'DBwebSv.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{main_db_path}'

    # 2. Cấu hình Database CHAT (Bind key: chat_db)
    chat_db_path = os.path.join(basedir, 'ChatData.db')
    app.config['SQLALCHEMY_BINDS'] = {
        'chat_db': f'sqlite:///{chat_db_path}'
    }

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Khởi tạo db với app
    db.init_app(app)

    with app.app_context():
        # Import các Blueprints
        from .auth import auth_bp
        from .home import home_bp
        from .profile import profile_bp
        from .grades import grades_bp
        from .tuition import tuition_bp
        from .curriculum import curriculum_bp
        from .scholarships import scholarships_bp
        from .ai_assistant import ai_assistant_bp
        from .library import library_bp

        # Đăng ký Blueprints
        app.register_blueprint(auth_bp)
        app.register_blueprint(home_bp)
        app.register_blueprint(profile_bp)
        app.register_blueprint(grades_bp)
        app.register_blueprint(tuition_bp)
        app.register_blueprint(curriculum_bp)
        app.register_blueprint(scholarships_bp)
        app.register_blueprint(ai_assistant_bp)
        app.register_blueprint(library_bp)

        # TỰ ĐỘNG TẠO CÁC BẢNG NẾU CHƯA CÓ
        try:
            db.create_all()  # Tạo bảng cho DB chính
            db.create_all(bind_key='chat_db')  # Tạo bảng cho DB Chat
            print("--- Database đã được khởi tạo thành công ---")
        except Exception as e:
            print(f"--- Lỗi khởi tạo Database: {e} ---")

    return app