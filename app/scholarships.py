from flask import Blueprint, render_template, session, redirect, url_for
from .models import Student

scholarships_bp = Blueprint('scholarships', __name__, url_prefix='/scholarships')


@scholarships_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    student_id_pk = session['user_id']
    student = Student.query.get(student_id_pk)

    # Dữ liệu chuẩn mô phỏng các chính sách (Có thể chuyển vào DB sau này nếu muốn)
    policies = {
        'mien_giam': [
            {'doi_tuong': 'Con của người có công với cách mạng, con thương binh, liệt sĩ',
             'muc_ho_tro': 'Miễn 100% học phí', 'dieu_kien': 'Có giấy xác nhận của Sở LĐ-TB&XH'},
            {'doi_tuong': 'Sinh viên khuyết tật, tàn tật có khó khăn về kinh tế', 'muc_ho_tro': 'Miễn 100% học phí',
             'dieu_kien': 'Có giấy xác nhận khuyết tật và sổ hộ nghèo/cận nghèo'},
            {'doi_tuong': 'Sinh viên là người dân tộc thiểu số ở vùng KTXH đặc biệt khó khăn',
             'muc_ho_tro': 'Miễn 100% học phí', 'dieu_kien': 'Sổ hộ khẩu thường trú tại vùng ĐBKK'},
            {'doi_tuong': 'Sinh viên là người dân tộc thiểu số (không ở vùng ĐBKK)', 'muc_ho_tro': 'Giảm 70% học phí',
             'dieu_kien': 'Giấy khai sinh và Sổ hộ khẩu'},
            {'doi_tuong': 'Sinh viên là con cán bộ, công nhân, viên chức bị tai nạn lao động',
             'muc_ho_tro': 'Giảm 50% học phí', 'dieu_kien': 'Sổ hưởng trợ cấp hàng tháng của bố/mẹ'}
        ],
        'tro_cap': [
            {'doi_tuong': 'Sinh viên mồ côi cả cha lẫn mẹ, không nơi nương tựa', 'muc_ho_tro': '140.000đ / tháng',
             'dieu_kien': 'Giấy báo tử của cha mẹ, xác nhận của địa phương'},
            {'doi_tuong': 'Sinh viên là người dân tộc thiểu số thuộc hộ nghèo/cận nghèo',
             'muc_ho_tro': '140.000đ / tháng', 'dieu_kien': 'Giấy chứng nhận hộ nghèo/cận nghèo hợp lệ'},
            {'doi_tuong': 'Sinh viên thuộc hộ nghèo vượt khó học tập', 'muc_ho_tro': '100.000đ / tháng',
             'dieu_kien': 'Giấy chứng nhận hộ nghèo, điểm TBC >= 2.0'}
        ],
        'hoc_bong': [
            {'doi_tuong': 'Sinh viên đạt danh hiệu Xuất sắc', 'muc_ho_tro': '120% định mức học phí',
             'dieu_kien': 'Điểm TBC học tập >= 3.6 và Điểm rèn luyện >= 90'},
            {'doi_tuong': 'Sinh viên đạt danh hiệu Giỏi', 'muc_ho_tro': '100% định mức học phí',
             'dieu_kien': 'Điểm TBC học tập >= 3.2 và Điểm rèn luyện >= 80'},
            {'doi_tuong': 'Sinh viên đạt danh hiệu Khá', 'muc_ho_tro': '80% định mức học phí',
             'dieu_kien': 'Điểm TBC học tập >= 2.5 và Điểm rèn luyện >= 70'}
        ]
    }

    return render_template('student/scholarships.html',
                           student=student,
                           policies=policies)