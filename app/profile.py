from flask import Blueprint, render_template, session, redirect, url_for
from .models import Student

# Khai báo blueprint với prefix /profile
profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    student_id_pk = session['user_id']
    # Kéo toàn bộ thông tin sinh viên từ database để đổ vào giao diện Hồ sơ
    student = Student.query.get(student_id_pk)

    return render_template('student/profile.html', student=student)