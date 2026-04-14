from flask import Blueprint, render_template, session, redirect, url_for
from .models import db, Student, Enrollment, CourseSection, Subject

library_bp = Blueprint('library', __name__, url_prefix='/library')


@library_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    student_id_pk = session['user_id']
    student = Student.query.get(student_id_pk)

    # Lấy danh sách tên các môn học sinh viên đang học trong kỳ này
    # Join qua Enrollment -> CourseSection -> Subject
    current_enrollments = db.session.query(Subject.ten_mon).join(
        CourseSection, Subject.unique_id == CourseSection.subject_id
    ).join(
        Enrollment, CourseSection.unique_id == Enrollment.section_id
    ).filter(Enrollment.student_id == student_id_pk).all()

    # Chuyển thành list string: ['Kinh tế vi mô', 'Toán cao cấp', ...]
    current_subjects = [s[0] for s in current_enrollments]

    return render_template('student/library.html',
                           student=student,
                           current_subjects=current_subjects)