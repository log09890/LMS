from flask import Blueprint, render_template, session, redirect, url_for
from .models import Student, Enrollment

grades_bp = Blueprint('grades', __name__, url_prefix='/grades')


@grades_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # Lấy ID từ session (đã lưu lúc login)
    user_pk = session['user_id']
    student = Student.query.get(user_pk)

    if not student:
        return redirect(url_for('auth.logout'))

    # Sửa lỗi: Sử dụng student_id (viết thường) để lọc
    enrollments = Enrollment.query.filter_by(student_id=student.unique_id).all()

    tong_tc = 0
    tong_diem = 0
    for e in enrollments:
        # Kiểm tra e.section_info tồn tại để tránh lỗi NoneType
        if e.section_info and e.section_info.subject_info and e.diem_he_10 is not None:
            tc = e.section_info.subject_info.so_tin_chi
            tong_tc += tc
            tong_diem += (e.diem_he_10 * tc)

    gpa = round(tong_diem / tong_tc, 2) if tong_tc > 0 else 0

    return render_template('student/grades.html',
                           student=student,
                           enrollments=enrollments,
                           gpa=gpa,
                           tong_tin_chi=tong_tc)