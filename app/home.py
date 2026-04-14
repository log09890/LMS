from flask import Blueprint, render_template, session, redirect, url_for
from .models import db, Student, Enrollment, CourseSection, Subject, Schedule, TuitionInvoice

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # Dùng tên cột viết thường unique_id
    student = Student.query.get(session['user_id'])

    if not student:
        session.clear()
        return redirect(url_for('auth.login'))

    # Query TKB với các cột viết thường
    schedules = db.session.query(Schedule, CourseSection, Subject).join(
        CourseSection, Schedule.section_id == CourseSection.unique_id
    ).join(
        Subject, CourseSection.subject_id == Subject.unique_id
    ).join(
        Enrollment, CourseSection.unique_id == Enrollment.section_id
    ).filter(Enrollment.student_id == student.unique_id).all()

    # Tính điểm
    enrollments = Enrollment.query.filter_by(student_id=student.unique_id).all()
    tong_tc = 0
    tong_diem = 0
    for e in enrollments:
        if e.section_info and e.section_info.subject_info and e.diem_he_10 is not None:
            tc = e.section_info.subject_info.so_tin_chi
            tong_tc += tc
            tong_diem += (e.diem_he_10 * tc)

    gpa = round(tong_diem / tong_tc, 2) if tong_tc > 0 else 0
    tuition = TuitionInvoice.query.filter_by(student_id=student.unique_id).first()

    return render_template('student/home.html',
                           student=student, schedules=schedules,
                           gpa=gpa, gpa_he4=round(gpa / 10 * 4, 2),
                           tong_tin_chi=tong_tc, tuition=tuition)