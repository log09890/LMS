from flask import Blueprint, render_template, session, redirect, url_for
from .models import db, Student, MajorSubject, Subject, Enrollment

curriculum_bp = Blueprint('curriculum', __name__, url_prefix='/curriculum')


@curriculum_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    student = Student.query.get(session['user_id'])
    if not student or not student.class_info:
        return "Dữ liệu sinh viên hoặc lớp học chưa hoàn thiện."

    major_id = student.class_info.major_id

    # 1. Quét bảng Điểm (Enrollment) để lấy trạng thái thật của sinh viên
    enrollments = Enrollment.query.filter_by(student_id=student.unique_id).all()
    status_map = {}
    for e in enrollments:
        if e.section_info:
            sub_id = e.section_info.subject_id
            # Nếu đã có điểm hệ 10 thì coi như đã hoàn thành (Tích lũy)
            if e.diem_he_10 is not None:
                status_map[sub_id] = 'completed'
            else:
                status_map[sub_id] = 'learning'  # Có đăng ký nhưng chưa có điểm -> Đang học

    # 2. Lấy khung chương trình của ngành
    curriculum_query = db.session.query(MajorSubject, Subject).join(
        Subject, MajorSubject.subject_id == Subject.unique_id
    ).filter(MajorSubject.major_id == major_id).order_by(MajorSubject.hoc_ky_du_kien).all()

    # 3. Gom nhóm dữ liệu theo từng kỳ
    curriculum_data = []
    tong_tin_chi_ctdt = 0

    for sem in range(1, 9):
        mon_trong_ky = []
        tc_ky = 0
        for ms, s in curriculum_query:
            if ms.hoc_ky_du_kien == sem:
                stt_code = status_map.get(s.unique_id, 'waiting')  # Mặc định là Chưa học
                block = 'general' if sem <= 3 else 'major'

                mon_trong_ky.append({
                    'ma_hp': s.subject_id,
                    'ten_mon': s.ten_mon,
                    'so_tc': s.so_tin_chi,
                    'ly_thuyet': s.so_tin_chi * 15 if s.so_tin_chi else 0,
                    'thuc_hanh': 0,
                    'status': stt_code,
                    'block': block
                })
                tc_ky += (s.so_tin_chi or 0)

        if mon_trong_ky:
            curriculum_data.append({
                'semester': sem,
                'subjects': mon_trong_ky,
                'total_tc': tc_ky
            })
            tong_tin_chi_ctdt += tc_ky

    return render_template('student/curriculum.html',
                           student=student,
                           curriculum_data=curriculum_data,
                           tong_tin_chi_ctdt=tong_tin_chi_ctdt)