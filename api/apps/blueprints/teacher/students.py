from flask import Blueprint, request, current_app
from apps.services.student_service import StudentService
from apps.services import TeacherService
from apps.utils.helpers import success_response, error_response


# 教师学生管理蓝图
teacher_students_bp = Blueprint('teacher_students', __name__, url_prefix='/students')


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


def get_teacher_students(teacher_id):
    try:
        return get_teacher_students_helper(teacher_id)
    except ValueError as e:
        current_app.logger.warning(f'Missing teacher ID: {str(e)}')
        return error_response('Teacher ID is required', 400)


def get_teacher_student(teacher_id, student_id):
    try:
        return get_teacher_student_helper(teacher_id, student_id)
    except ValueError as e:
        current_app.logger.warning(f'Missing teacher ID: {str(e)}')
        return error_response('Teacher ID is required', 400)


def get_teacher_all_classes_students(teacher_id):
    """
    获取教师所有班级的学生列表
    
    Args:
        teacher_id (str): 教师ID
        
    Returns:
        JSON: 教师所有班级的学生列表
    """
    try:
        # 检查是否提供了teacher_id
        if teacher_id is None:
            return error_response('Teacher ID is required', 400)
            
        teacher_service = TeacherService()
        students_data = teacher_service.get_all_classes_students(teacher_id)
        
        return success_response(students_data)
    except Exception as e:
        current_app.logger.error(f"Error getting teacher all classes students: {str(e)}")
        return error_response('Failed to get students', 500)


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


# 注册路由
teacher_students_bp.add_url_rule('/', view_func=get_teacher_students, methods=['GET'], defaults={'teacher_id': None})
teacher_students_bp.add_url_rule('/<string:teacher_id>', view_func=get_teacher_students, methods=['GET'])
teacher_students_bp.add_url_rule('/<string:teacher_id>/<string:student_id>', view_func=get_teacher_student, methods=['GET'])
teacher_students_bp.add_url_rule('/<string:teacher_id>/classes/students', view_func=get_teacher_all_classes_students, methods=['GET'])
teacher_students_bp.add_url_rule('/<string:teacher_id>/all_classes_students', view_func=get_teacher_all_classes_students, methods=['GET'])