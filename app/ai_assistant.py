import google.generativeai as genai
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import markdown
import logging
import requests
from .models import db, Student, ChatSession, ChatMessage, Major, MajorClass, Enrollment, TuitionInvoice
from datetime import datetime

logger = logging.getLogger(__name__)
ai_assistant_bp = Blueprint('ai_assistant', __name__, url_prefix='/ai-assistant')

# API CONFIG
GEMINI_KEY = "AIzaSyAkkqyF2TYwIW52mci73kIo_cnhyK2RWdQ"
OLLAMA_URL = "http://localhost:11434/api/generate"


@ai_assistant_bp.route('/')
@ai_assistant_bp.route('/s/<int:session_id>')
def index(session_id=None):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    uid = session['user_id']
    student = Student.query.get(uid)
    all_sessions = ChatSession.query.filter_by(student_id=uid).order_by(ChatSession.created_at.desc()).all()

    current_messages = []
    active_session = None
    if session_id:
        active_session = ChatSession.query.filter_by(id=session_id, student_id=uid).first()
        if active_session:
            current_messages = ChatMessage.query.filter_by(session_id=session_id).order_by(
                ChatMessage.timestamp.asc()).all()

    return render_template('student/ai_assistant.html',
                           student=student, all_sessions=all_sessions,
                           current_messages=current_messages, active_session=active_session)


@ai_assistant_bp.route('/delete/<int:session_id>', methods=['POST'])
def delete_session(session_id):
    uid = session.get('user_id')
    sess = ChatSession.query.filter_by(id=session_id, student_id=uid).first()
    if sess:
        try:
            db.session.delete(sess)
            db.session.commit()
            return jsonify({'status': 'success'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 500
    return jsonify({'status': 'not_found'}), 404


def generate_chat_title(first_msg):
    prompt = f"Tóm tắt câu hỏi sau thành một tiêu đề cực ngắn (2-4 từ) để lưu vào lịch sử: '{first_msg}'. Trả về kết quả trực tiếp."
    try:
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        if response.text: return response.text.strip()[:40]
    except:
        pass
    return first_msg[:25] + "..."


def get_ai_response(msg, pref, student, history):
    # 1. Thu thập dữ liệu ngữ cảnh của sinh viên
    major_name = student.class_info.major_info.ten_nganh if student.class_info else "Chưa rõ"
    class_name = student.class_info.ten_lop if student.class_info else "Chưa rõ"

    # Lấy thông tin học phí gần nhất
    tuition = TuitionInvoice.query.filter_by(student_id=student.unique_id).order_by(
        TuitionInvoice.nam_hoc.desc()).first()
    tuition_info = f"Học phí kỳ gần nhất: {tuition.tong_tien} VNĐ, Trạng thái: {tuition.trang_thai}" if tuition else "Chưa có dữ liệu học phí."

    # Xây dựng chuỗi lịch sử hội thoại (Context)
    chat_context = ""
    for h in history[-6:]:  # Lấy 6 tin nhắn gần nhất để AI nhớ ngữ cảnh
        role_name = "Em" if h.role == 'user' else "Cô"
        chat_context += f"{role_name}: {h.content}\n"

    # 2. Xây dựng System Prompt cực kỳ chi tiết
    sys_prompt = f"""Bạn là CÔ GIÁO NEU AI tại Đại học Kinh tế Quốc dân.
[THÔNG TIN SINH VIÊN ĐANG HỎI]:
- Tên: {student.ten}
- Mã SV: {student.student_id}
- Ngành học: {major_name}
- Lớp: {class_name}
- Khóa: {student.khoa_hoc}
- {tuition_info}

[PHONG CÁCH CỦA BẠN]:
1. Luôn xưng 'Cô', gọi sinh viên là 'em' hoặc '{student.ten}'.
2. Thái độ: Ân cần, hiền hậu, hay khích lệ em học tập tốt.
3. Nếu em hỏi về thông tin cá nhân (điểm, ngành...), hãy dựa vào dữ liệu trên để trả lời chính xác.
4. Trình bày bằng Markdown đẹp mắt.

[LỊCH SỬ TRÒ CHUYỆN TRƯỚC ĐÓ]:
{chat_context}
"""

    full_query = f"{sys_prompt}\n\nCÂU HỎI HIỆN TẠI CỦA EM: {msg}"

    if pref == 'gemini':
        try:
            genai.configure(api_key=GEMINI_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(full_query)
            if response.text: return markdown.markdown(response.text)
        except:
            pref = 'local'

    if pref == 'local':
        try:
            res = requests.post(OLLAMA_URL, json={"model": "llama3", "prompt": full_query, "stream": False}, timeout=20)
            if res.status_code == 200: return markdown.markdown(res.json().get('response', ''))
        except:
            pass
    return f"<p>Chào {student.ten}, Cô đang gặp chút lỗi kết nối. Em đợi Cô một lát nhé!</p>"


@ai_assistant_bp.route('/chat', methods=['POST'])
def chat():
    uid = session.get('user_id')
    student = Student.query.get(uid)
    data = request.json
    msg_text = data.get('message', '').strip()
    raw_id = data.get('session_id')
    pref = data.get('model_preference', 'gemini')

    sess_id = None
    if raw_id is not None and str(raw_id).lower() not in ['null', 'none']:
        sess_id = int(raw_id)

    new_title = None
    if sess_id is None:
        new_title = generate_chat_title(msg_text)
        new_sess = ChatSession(student_id=uid, title=new_title)
        db.session.add(new_sess)
        db.session.commit()
        sess_id = new_sess.id

    # Lấy lịch sử hội thoại trước khi tạo tin nhắn mới
    history = ChatMessage.query.filter_by(session_id=sess_id).order_by(ChatMessage.timestamp.asc()).all()

    # Lưu tin nhắn user
    db.session.add(ChatMessage(session_id=sess_id, role='user', content=msg_text))

    # Gọi AI với đầy đủ ngữ cảnh
    reply = get_ai_response(msg_text, pref, student, history)

    # Lưu tin nhắn AI
    db.session.add(ChatMessage(session_id=sess_id, role='ai', content=reply))
    db.session.commit()

    return jsonify({'reply': reply, 'session_id': sess_id, 'new_title': new_title})