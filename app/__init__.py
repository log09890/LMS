from flask import Flask
import os


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'neu_student_portal_secret'

    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'DBwebSv.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .models import db
    db.init_app(app)

    # Import Blueprint
    from .auth import auth_bp
    from .home import home_bp
    from .profile import profile_bp
    from .grades import grades_bp
    from .tuition import tuition_bp
    from .curriculum import curriculum_bp
    from .scholarships import scholarships_bp
    from .ai_assistant import ai_assistant_bp
    from .library import library_bp  # <-- THÊM DÒNG NÀY

    # Đăng ký Blueprint
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(grades_bp)
    app.register_blueprint(tuition_bp)
    app.register_blueprint(curriculum_bp)
    app.register_blueprint(scholarships_bp)
    app.register_blueprint(ai_assistant_bp)
    app.register_blueprint(library_bp)  # <-- THÊM DÒNG NÀY

    return app