from flask import Blueprint, render_template, request, redirect, url_for, session
from .models import Student

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        student = Student.query.filter_by(student_id=username).first()

        if student and student.password == password:
            session['user_id'] = student.unique_id
            session['student_id'] = student.student_id
            session['user_name'] = student.ten
            # Sửa lỗi ở dòng này: Chuyển hướng về trang chủ đúng (home.index)
            return redirect(url_for('home.index'))
        else:
            error = "Tên đăng nhập hoặc mật khẩu không chính xác!"

    return render_template('auth/login.html', error=error)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))