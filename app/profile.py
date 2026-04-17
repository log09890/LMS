from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from .models import db, Student

# Khai báo blueprint với prefix /profile
profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    student_id_pk = session['user_id']
    # Kéo thông tin sinh viên từ database
    student = Student.query.get(student_id_pk)

    if not student:
        flash("Không tìm thấy thông tin sinh viên.", "danger")
        return redirect(url_for('auth.logout'))

    return render_template('student/profile.html', student=student)


@profile_bp.route('/update', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    student = Student.query.get(session['user_id'])
    if student:
        try:
            # Nhận dữ liệu từ form (thuộc tính 'name' trong html)
            student.ten = request.form.get('ten')
            student.email = request.form.get('email')
            student.gioi_tinh = request.form.get('gioi_tinh')
            student.que_quan = request.form.get('que_quan')
            student.dia_chi = request.form.get('dia_chi')
            student.sdt = request.form.get('sdt')

            db.session.commit()
            flash('Cập nhật hồ sơ thành công!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Lỗi hệ thống: {str(e)}', 'danger')

    return redirect(url_for('profile.index'))


@profile_bp.route('/delete', methods=['POST'])
def delete_profile():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    student = Student.query.get(session['user_id'])
    if student:
        try:
            db.session.delete(student)
            db.session.commit()
            session.clear()  # Xóa session để đẩy ra trang đăng nhập
            flash('Hồ sơ đã được xóa vĩnh viễn.', 'info')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('Không thể thực hiện xóa hồ sơ lúc này.', 'danger')

    return redirect(url_for('profile.index'))