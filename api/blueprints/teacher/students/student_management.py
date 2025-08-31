"""教师学生管理模块，处理教师查看学生信息相关操作"""
from flask import Blueprint, request, jsonify, current_app
from utils.auth import role_required
from utils.helpers import success_response, error_response
from services.student_service import StudentService

teacher_students_bp = Blueprint('teacher_students_bp', __name__)

@teacher_students_bp.route('/students', methods=['GET'])
@role_required('teacher')
def get_teacher_students():
    try:
        # 获取当前教师ID
        teacher_id = request.user['user_id']
        
        # 获取查询参数
        class_id = request.args.get('class_id')
        
        # 获取教师的学生列表
        students = StudentService.get_teacher_students(teacher_id, class_id)
        current_app.logger.info(f"Teacher {teacher_id} retrieved student list")
        return success_response(students)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch teacher students: {str(e)}')
        return error_response('Failed to fetch students', 500)
