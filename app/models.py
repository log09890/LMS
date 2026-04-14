from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Major(db.Model):
    __tablename__ = 'major'
    unique_id = db.Column(db.Integer, primary_key=True)
    major_id = db.Column(db.String(20), unique=True, nullable=False)
    ten_nganh = db.Column(db.String(100), nullable=False)
    hoc_phi_tin_chi = db.Column(db.Float, default=500000)


class MajorClass(db.Model):
    __tablename__ = 'major_class'
    unique_id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.String(50), unique=True)
    ten_lop = db.Column(db.String(100))
    major_id = db.Column(db.Integer, db.ForeignKey('major.unique_id'))

    major_info = db.relationship('Major', backref='classes')


class Student(db.Model):
    __tablename__ = 'student'
    unique_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True)
    ten = db.Column(db.String(100))
    email = db.Column(db.String(100))
    gioi_tinh = db.Column(db.String(10))
    khoa_hoc = db.Column(db.String(10))
    dia_chi = db.Column(db.String(255))
    que_quan = db.Column(db.String(100))
    sdt = db.Column(db.String(15))
    password = db.Column(db.String(100))
    class_id = db.Column(db.Integer, db.ForeignKey('major_class.unique_id'))

    class_info = db.relationship('MajorClass', backref='students')


class Subject(db.Model):
    __tablename__ = 'subject'
    unique_id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.String(20), unique=True)
    ten_mon = db.Column(db.String(100))
    so_tin_chi = db.Column(db.Integer)
    loai_mon = db.Column(db.String(50))


class MajorSubject(db.Model):
    __tablename__ = 'major_subject'
    unique_id = db.Column(db.Integer, primary_key=True)
    major_id = db.Column(db.Integer, db.ForeignKey('major.unique_id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.unique_id'))
    hoc_ky_du_kien = db.Column(db.Integer)

    subject_info = db.relationship('Subject', backref='major_links')
    major_info = db.relationship('Major', backref='subject_links')


class CourseSection(db.Model):
    __tablename__ = 'course_section'
    unique_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.String(50), unique=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.unique_id'))
    giang_vien = db.Column(db.String(100))
    nam_hoc = db.Column(db.Integer)
    hoc_ky = db.Column(db.Integer)

    subject_info = db.relationship('Subject', backref='sections')


class Enrollment(db.Model):
    __tablename__ = 'enrollment'
    unique_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('course_section.unique_id'))
    student_id = db.Column(db.Integer, db.ForeignKey('student.unique_id'))
    diem_chuyen_can = db.Column(db.Float)
    diem_giua_ky = db.Column(db.Float)
    diem_cuoi_ky = db.Column(db.Float)
    diem_he_4 = db.Column(db.Float)
    diem_he_10 = db.Column(db.Float)

    section_info = db.relationship('CourseSection', backref='enrollments')


class TuitionInvoice(db.Model):
    __tablename__ = 'tuition_invoice'
    unique_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.unique_id'))
    hoc_ky = db.Column(db.Integer)
    nam_hoc = db.Column(db.Integer)
    tong_tien = db.Column(db.Float)
    tien_da_nop = db.Column(db.Float)
    han_nop = db.Column(db.String(20))
    trang_thai = db.Column(db.String(50))


class Schedule(db.Model):
    __tablename__ = 'schedule'
    unique_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('course_section.unique_id'))
    thu = db.Column(db.Integer)
    tiet_bat_dau = db.Column(db.Integer)
    phong_hoc = db.Column(db.String(50))
    tiet_ket_thuc = db.Column(db.Integer)