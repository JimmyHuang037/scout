"""学生管理模块，处理学生相关的所有操作"""
from flask import jsonify, request, session
from services import StudentService
from utils.helpers import success_response, error_response, auth_required, role_required
from utils.logger import app_logger


@auth_required
@role_required('admin')
def get_students():
    """获取学生列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用学生服务获取学生列表
        student_service = StudentService()
        result = student_service.get_all_students(page, per_page)
        
        app_logger.info("Admin retrieved student list")
        return success_response(result)
        
    except Exception as e:
        app_logger.error(f'Failed to fetch students: {str(e)}')
        return error_response(f'Failed to fetch students: {str(e)}', 500)


@auth_required
@role_required('admin')
def create_student():
    """创建学生"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        student_name = data.get('student_name')
        class_id = data.get('class_id')
        password = data.get('password')
        
        if not all([student_id, student_name, class_id, password]):
            app_logger.warning("Create student attempt with missing fields")
            return error_response('Missing required fields: student_id, student_name, class_id, password', 400)
        
        # 使用学生服务创建学生
        student_service = StudentService()
        result = student_service.create_student(data)
        
        if result:
            app_logger.info(f"Admin created student {student_id}")
            # 修复返回数据格式，确保返回创建的学生信息
            student_service = StudentService()
            student_info = student_service.get_student_by_id(student_id)
            return success_response(student_info, 'Student created successfully', 201)
        else:
            app_logger.error("Failed to create student")
            return error_response('Failed to create student', 400)
            
    except Exception as e:
        app_logger.error(f'Failed to create student: {str(e)}')
        return error_response(f'Failed to create student: {str(e)}', 500)


@auth_required
@role_required('admin')
def get_student(student_id):
    """获取单个学生信息"""
    try:
        # 使用学生服务获取学生信息
        student_service = StudentService()
        student = student_service.get_student_by_id(student_id)
        
        if student:
            return success_response(student)
        else:
            return error_response('Student not found', 404)
            
    except Exception as e:
        return error_response(f'Failed to fetch student: {str(e)}', 500)


@auth_required
@role_required('admin')
def update_student(student_id):
    """更新学生信息"""
    try:
        data = request.get_json()
        student_name = data.get('student_name')
        class_id = data.get('class_id')
        password = data.get('password')
        
        if not all([student_name, class_id, password]):
            return error_response('Missing required fields: student_name, class_id, password', 400)
        
        # 使用学生服务更新学生信息
        student_service = StudentService()
        result = student_service.update_student(student_id, data)
        
        if result:
            return success_response(result, 'Student updated successfully')
        else:
            return error_response('Failed to update student', 400)
            
    except Exception as e:
        return error_response(f'Failed to update student: {str(e)}', 500)


@auth_required
@role_required('admin')
def delete_student(student_id):
    """删除学生"""
    try:
        # 使用学生服务删除学生
        student_service = StudentService()
        result = student_service.delete_student(student_id)
        
        if result:
            # 修复返回值问题，确保返回正确的响应格式
            return success_response({'message': 'Student deleted successfully'}, 200)
        else:
            return error_response('Failed to delete student', 400)
            
    except Exception as e:
        return error_response(f'Failed to delete student: {str(e)}', 500)