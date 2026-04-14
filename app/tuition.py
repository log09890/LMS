from flask import Blueprint, render_template, session, redirect, url_for
from .models import Student, TuitionInvoice, Enrollment

tuition_bp = Blueprint('tuition', __name__, url_prefix='/tuition')


@tuition_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # Lấy ID từ session
    user_pk = session['user_id']
    student = Student.query.get(user_pk)

    if not student:
        return redirect(url_for('auth.logout'))

    # Sửa lỗi: Sử dụng student_id (viết thường) để lọc hóa đơn
    # Lưu ý: student.unique_id là khóa chính của bảng Student
    invoices = TuitionInvoice.query.filter_by(student_id=student.unique_id).all()

    # Xác định đơn giá tín chỉ an toàn
    don_gia_tin_chi = 500000
    if student.class_info and student.class_info.major_info:
        don_gia_tin_chi = getattr(student.class_info.major_info, 'hoc_phi_tin_chi', 500000) or 500000

    # Kéo danh sách môn học để tính tiền chi tiết
    enrollments = Enrollment.query.filter_by(student_id=student.unique_id).all()

    tuition_details = []
    tong_tien_chi_tiet = 0

    for e in enrollments:
        if e.section_info and e.section_info.subject_info:
            subject = e.section_info.subject_info
            thanh_tien = subject.so_tin_chi * don_gia_tin_chi
            tong_tien_chi_tiet += thanh_tien

            tuition_details.append({
                'ma_mon': getattr(subject, 'subject_id', subject.unique_id),
                'ten_mon': subject.ten_mon,
                'so_tc': subject.so_tin_chi,
                'don_gia': don_gia_tin_chi,
                'thanh_tien': thanh_tien
            })

    return render_template('student/tuition.html',
                           student=student,
                           invoices=invoices,
                           tuition_details=tuition_details,
                           tong_tien_chi_tiet=tong_tien_chi_tiet)