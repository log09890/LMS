from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from .models import Student, Enrollment
import requests
import json

ai_assistant_bp = Blueprint('ai_assistant', __name__, url_prefix='/ai-assistant')


@ai_assistant_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    student = Student.query.get(session['user_id'])

    # Tính toán ngữ cảnh GPA và Tín chỉ
    enrollments = Enrollment.query.filter_by(student_id=student.unique_id).all()
    tong_tc = 0
    tong_diem = 0
    for e in enrollments:
        if e.diem_he_10 is not None:
            tc = e.section_info.subject_info.so_tin_chi
            tong_tc += tc
            tong_diem += (e.diem_he_10 * tc)
    gpa = round(tong_diem / tong_tc, 2) if tong_tc > 0 else 0

    context = {
        "ten": student.ten,
        "nganh": student.class_info.major_info.ten_nganh if student.class_info else "N/A",
        "gpa_4": round(gpa / 10 * 4, 2),
        "tin_chi": tong_tc
    }

    return render_template('student/ai_assistant.html', student=student, context=context)


@ai_assistant_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')
    context_data = data.get('context')

    # Cấu hình System Prompt cho AI Local
    system_prompt = f"""Bạn là trợ lý ảo NEU AI. 
    Thông tin sinh viên: {context_data['ten']}, Ngành: {context_data['nganh']}, GPA: {context_data['gpa_4']}, Tín chỉ: {context_data['tin_chi']}/138.
    Hãy tư vấn học tập ngắn gọn, chuyên nghiệp bằng tiếng Việt."""

    # Gọi tới Ollama API (Mặc định chạy ở port 11434)
    # Bạn cần chạy lệnh 'ollama run llama3' trước đó
    try:
        response = requests.post('http://localhost:11434/api/generate',
                                 json={
                                     "model": "llama3",
                                     "prompt": f"{system_prompt}\n\nNgười dùng hỏi: {user_message}\nTrợ lý trả lời:",
                                     "stream": False
                                 }, timeout=30)

        result = response.json()
        return jsonify({"reply": result.get('response', 'AI không phản hồi.')})
    except Exception as e:
        return jsonify({
                           "reply": f"Lỗi: Không thể kết nối tới Ollama. Hãy đảm bảo bạn đã chạy 'ollama serve'. Detail: {str(e)}"}), 500