"""学生管理模块，处理学生相关的所有操作"""
from flask import jsonify, request, session, current_app
# 修复导入问题，使用相对导入
import sys
import os
# 将api目录添加到Python路径中
api_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

from services import StudentService
from utils.helpers import success_response, error_response, auth_required, role_required


@auth_required
@role_required('admin')
def get_students():
    """
    获取所有学生列表
    
    Returns:
        JSON: 学生列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取学生列表
        students_data = StudentService().get_all_students(page, per_page)
        
        current_app.logger.info('Admin retrieved all students')
        return success_response(students_data)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve students: {str(e)}')
        return error_response("获取学生列表失败", 500)


@auth_required
@role_required('admin')
def create_student():
    """
    创建学生
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 提取必要字段
        student_id = data.get('student_id')
        student_name = data.get('student_name')
        class_id = data.get('class_id')
        password = data.get('password')
        
        # 验证必填字段
        if not student_id or not student_name or not class_id or not password:
            return error_response("缺少必要字段", 400)
        
        # 创建学生
        student_data = {
            'student_id': student_id,
            'student_name': student_name,
            'class_id': class_id,
            'password': password
        }
        new_student = StudentService().create_student(student_data)
        
        if not new_student:
            return error_response("创建学生失败", 400)
        
        current_app.logger.info(f'Admin created student: {student_id}')
        return success_response({"student_id": student_id}, "学生创建成功", 201)
    
    except Exception as e:
        current_app.logger.error(f'Failed to create student: {str(e)}')
        return error_response("创建学生失败", 500)


@auth_required
@role_required('admin')
def get_student(student_id):
    """
    获取单个学生信息
    
    Args:
        student_id (int): 学生ID
        
    Returns:
        JSON: 学生信息
    """
    try:
        # 获取学生信息
        student = StudentService().get_student_by_id(student_id)
        if not student:
            return error_response("学生不存在", 404)
        
        current_app.logger.info(f'Admin retrieved student: {student_id}')
        return success_response(student)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve student {student_id}: {str(e)}')
        return error_response("获取学生信息失败", 500)


@auth_required
@role_required('admin')
def update_student(student_id):
    """
    更新学生信息
    
    Args:
        student_id (int): 学生ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 更新学生
        result = StudentService().update_student(student_id, data)
        
        if not result:
            return error_response("学生不存在", 404)
        
        current_app.logger.info(f'Admin updated student: {student_id}')
        return success_response({"student_id": student_id}, "学生更新成功")
    
    except Exception as e:
        current_app.logger.error(f'Failed to update student {student_id}: {str(e)}')
        return error_response("更新学生失败", 500)


@auth_required
@role_required('admin')
def delete_student(student_id):
    """
    删除学生
    
    Args:
        student_id (int): 学生ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 删除学生
        result = StudentService().delete_student(student_id)
        if not result:
            return error_response("学生不存在", 404)
        
        current_app.logger.info(f'Admin deleted student: {student_id}')
        return success_response({"student_id": student_id}, "学生删除成功")
    
    except Exception as e:
        current_app.logger.error(f'Failed to delete student {student_id}: {str(e)}')
        return error_response("删除学生失败", 500)