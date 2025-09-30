"""教师学生管理模块，处理教师查看学生信息相关操作"""
from flask import Blueprint, request, jsonify, current_app
from apps.utils.auth import role_required
from apps.utils.helpers import success_response, error_response
from apps.services.student_service import StudentService

teacher_student_bp = Blueprint('teacher_student_bp', __name__)

@teacher_student_bp.route('/students', methods=['GET'])
def get_teacher_students():
    try:
        # 暂时使用固定的教师ID进行测试
        teacher_id = "T001"
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取教师学生列表
        students_data = StudentService().get_students_by_teacher(teacher_id, page, per_page)
        current_app.logger.info(f"Teacher {teacher_id} retrieved students")
        return success_response(students_data)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch students: {str(e)}')
        return error_response('Failed to fetch students', 500)

@teacher_student_bp.route('/students/<int:student_id>', methods=['GET'])
def get_teacher_student(student_id):
    try:
        # 暂时使用固定的教师ID进行测试
        teacher_id = "T001"
        
        # 获取学生详情
        student_data = StudentService().get_student_by_id(student_id, teacher_id)
        if not student_data:
            return error_response('Student not found'), 404
            
        current_app.logger.info(f"Teacher {teacher_id} retrieved student {student_id}")
        return success_response(student_data)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch student: {str(e)}')
        return error_response('Failed to fetch student', 500)

@teacher_student_bp.route('/students/<int:student_id>', methods=['PUT'])
def update_teacher_student(student_id):
    try:
        # 暂时使用固定的教师ID进行测试
        teacher_id = "T001"
        
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response('No data provided'), 400
            
        # 更新学生信息
        student_data = StudentService().update_student(student_id, data, teacher_id)
        if not student_data:
            return error_response('Student not found or access denied'), 404
            
        current_app.logger.info(f"Teacher {teacher_id} updated student {student_id}")
        return success_response(student_data, 'Student updated successfully')
    except Exception as e:
        current_app.logger.error(f'Failed to update student: {str(e)}')
        return error_response('Failed to update student', 500)