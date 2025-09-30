"""班级管理模块，处理教师查看班级信息的操作"""
from flask import jsonify, request, session, current_app
from services import ClassService
from utils.helpers import success_response, error_response, auth_required, role_required


@auth_required
@role_required('teacher')
def get_classes():
    """
    获取班级列表（教师可访问）
    
    Returns:
        JSON: 班级列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取班级列表
        classes_data = ClassService().get_all_classes(page, per_page)
        
        current_app.logger.info('Teacher retrieved class list')
        return success_response(classes_data)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve classes: {str(e)}')
        return error_response("获取班级列表失败", 500)


@auth_required
@role_required('teacher')
def get_class_students(class_id):
    """
    获取班级学生列表（教师可访问）
    
    Args:
        class_id (int): 班级ID
        
    Returns:
        JSON: 班级学生列表
    """
    try:
        # 获取班级学生列表
        students_data = ClassService().get_class_students(class_id)
        
        current_app.logger.info(f'Teacher retrieved students for class: {class_id}')
        return success_response(students_data)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve students for class {class_id}: {str(e)}')
        return error_response("获取班级学生列表失败", 500)