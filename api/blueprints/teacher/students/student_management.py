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


@teacher_students_bp.route('/students/<string:student_id>', methods=['GET'])
@role_required('teacher')
def get_teacher_student(student_id):
    try:
        # 获取当前教师ID
        teacher_id = session.get('user_id')
        
        # 验证学生是否属于该教师所教班级
        student_service = StudentService()
        students_data = student_service.get_teacher_students(teacher_id, None, 1, 1000)  # 获取所有学生进行验证
        
        # 检查请求的学生是否在教师的学生列表中
        student_found = any(student['student_id'] == student_id for student in students_data.get('students', []))
        
        if not student_found:
            current_app.logger.warning(f"Teacher {teacher_id} attempted to access student {student_id} not in their class")
            return error_response('Student not found or not in your class', 404)
        
        # 获取学生详细信息
        student = student_service.get_student_by_id(student_id)
        if student:
            current_app.logger.info(f"Teacher {teacher_id} retrieved student {student_id}")
            return success_response(student)
        else:
            current_app.logger.warning(f"Student {student_id} not found")
            return error_response('Student not found', 404)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch teacher student: {str(e)}')
        return error_response('Failed to fetch student', 500)


@teacher_students_bp.route('/students/<string:student_id>', methods=['PUT'])
@role_required('teacher')
def update_teacher_student(student_id):
    try:
        # 获取当前教师ID
        teacher_id = session.get('user_id')
        
        # 验证学生是否属于该教师所教班级
        student_service = StudentService()
        students_data = student_service.get_teacher_students(teacher_id, None, 1, 1000)  # 获取所有学生进行验证
        
        # 检查请求的学生是否在教师的学生列表中
        student_found = any(student['student_id'] == student_id for student in students_data.get('students', []))
        
        if not student_found:
            current_app.logger.warning(f"Teacher {teacher_id} attempted to update student {student_id} not in their class")
            return error_response('Student not found or not in your class', 404)
        
        # 获取请求数据
        data = request.get_json()
        student_name = data.get('student_name')
        
        # 更新学生信息
        if student_name:
            result = student_service.update_student_name(student_id, student_name)
            if result:
                current_app.logger.info(f"Teacher {teacher_id} updated student {student_id}")
                return success_response({'message': 'Student updated successfully'})
            else:
                return error_response('Failed to update student', 500)
        else:
            return error_response('No valid fields to update', 400)
    except Exception as e:
        current_app.logger.error(f'Failed to update teacher student: {str(e)}')
        return error_response('Failed to update student', 500)