"""教师学生管理模块，处理教师查看学生信息相关操作"""
from flask import Blueprint, request, jsonify, current_app
from apps.utils.helpers import success_response, error_response
from apps.services.student_service import StudentService

teacher_student_bp = Blueprint('teacher_student_bp', __name__)

def _get_teacher_id():
    """从请求中获取教师ID"""
    # 尝试从JWT token中获取教师ID
    if hasattr(request, 'user') and request.user:
        return request.user.get('id')
    
    # 或者从请求头中获取
    teacher_id = request.headers.get('X-Teacher-ID')
    if teacher_id:
        return teacher_id
    
    # 如果没有提供教师ID，返回错误
    raise ValueError("Teacher ID is required")

@teacher_student_bp.route('/students', methods=['GET'])
def get_teacher_students(teacher_id):
    try:
        return get_teacher_students_helper(teacher_id)
    except ValueError as e:
        current_app.logger.warning(f'Missing teacher ID: {str(e)}')
        return error_response('Teacher ID is required', 400)

@teacher_student_bp.route('/students/<string:student_id>', methods=['GET'])
def get_teacher_student(teacher_id, student_id):
    try:
        return get_teacher_student_helper(teacher_id, student_id)
    except ValueError as e:
        current_app.logger.warning(f'Missing teacher ID: {str(e)}')
        return error_response('Teacher ID is required', 400)

def get_teacher_students_helper(teacher_id):
    """Helper function to get teacher's students"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取教师学生列表
        students_data = StudentService().get_teacher_students(teacher_id, None, page, per_page)
        current_app.logger.info(f"Teacher {teacher_id} retrieved students")
        return success_response(students_data)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch students: {str(e)}')
        return error_response('Failed to fetch students', 500)

def get_teacher_student_helper(teacher_id, student_id):
    """Helper function to get teacher's student details"""
    try:
        # 获取学生详情
        student_data = StudentService().get_student_by_id(student_id)
        if not student_data:
            return error_response('Student not found', 404)
            
        current_app.logger.info(f"Teacher {teacher_id} retrieved student {student_id}")
        return success_response(student_data)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch student: {str(e)}')
        return error_response('Failed to fetch student', 500)