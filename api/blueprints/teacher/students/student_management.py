"""教师学生管理模块，处理教师查看学生信息相关操作"""
from flask import Blueprint, request, jsonify, current_app, session
from utils.auth import role_required
from utils.helpers import success_response, error_response
from services.student_service import StudentService

teacher_students_bp = Blueprint('teacher_students_bp', __name__)

@teacher_students_bp.route('/students', methods=['GET'])
@role_required('teacher')
def get_teacher_students():
    try:
        # 获取当前教师ID
        teacher_id = session.get('user_id')
        
        # 获取查询参数
        class_id = request.args.get('class_id')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取教师的学生列表
        student_service = StudentService()
        students_data = student_service.get_teacher_students(teacher_id, class_id, page, per_page)
        current_app.logger.info(f"Teacher {teacher_id} retrieved student list")
        return success_response(students_data)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch teacher students: {str(e)}')
        return error_response('Failed to fetch students', 500)