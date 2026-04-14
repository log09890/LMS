from flask import Blueprint, render_template, session, redirect, url_for
from .models import db, Student, MajorSubject, Subject

curriculum_bp = Blueprint('curriculum', __name__, url_prefix='/curriculum')


@curriculum_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    student = Student.query.get(session['user_id'])
    if not student or not student.class_info:
        return "Dữ liệu sinh viên hoặc lớp học chưa hoàn thiện."

    # Lấy Major_ID của sinh viên thông qua lớp học
    major_id = student.class_info.major_id

    # Truy vấn các môn học thuộc ngành này thông qua bảng trung gian MajorSubject
    curriculum_query = db.session.query(MajorSubject, Subject).join(
        Subject, MajorSubject.subject_id == Subject.unique_id
    ).filter(MajorSubject.major_id == major_id).order_by(MajorSubject.hoc_ky_du_kien).all()

    # Nhóm dữ liệu theo kỳ
    curriculum_data = []
    for sem in range(1, 9):
        mon_trong_ky = [s for ms, s in curriculum_query if ms.hoc_ky_du_kien == sem]
        if mon_trong_ky:
            curriculum_data.append({
                'semester': sem,
                'subjects': mon_trong_ky,
                'total_tc': sum(sub.so_tin_chi for sub in mon_trong_ky if sub.so_tin_chi)
            })

    # Tổng tín chỉ yêu cầu cố định
    tong_tin_chi_ctdt = 138

    return render_template('student/curriculum.html',
                           student=student,
                           curriculum_data=curriculum_data,
                           tong_tin_chi_ctdt=tong_tin_chi_ctdt)