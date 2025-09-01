"""教师管理模块，处理教师相关的所有操作"""
from flask import jsonify, request, session, current_app
from services import TeacherService
from utils.helpers import success_response, error_response, auth_required, role_required


@auth_required
@role_required('admin')
def get_teachers():
    """
    获取教师列表
    
    Returns:
        JSON: 教师列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取教师列表
        teachers_data = TeacherService().get_all_teachers(page, per_page)
        
        current_app.logger.info('Admin retrieved teacher list')
        return success_response(teachers_data)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve teachers: {str(e)}')
        return error_response("获取教师列表失败", 500)


@auth_required
@role_required('admin')
def create_teacher():
    """
    创建教师
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 提取必要字段
        teacher_name = data.get('teacher_name')
        subject_id = data.get('subject_id')
        password = data.get('password')
        
        # 验证必填字段
        if not teacher_name or not subject_id or not password:
            return error_response("缺少必要字段", 400)
        
        # 创建教师
        teacher_service = TeacherService()
        teacher_data = {
            'teacher_name': teacher_name,
            'subject_id': subject_id,
            'password': password
        }
        result = teacher_service.create_teacher(teacher_data)
        
        if not result:
            return error_response("创建教师失败", 400)
        
        # 获取新创建的教师信息
        # 由于create_teacher只返回布尔值，我们需要重新查询获取新创建的教师信息
        # 先获取新创建教师的ID
        query = "SELECT LAST_INSERT_ID() as teacher_id"
        new_teacher_id = teacher_service.db_service.execute_query(query, (), fetch_one=True)['teacher_id']
        
        # 获取新创建的教师信息
        new_teacher = teacher_service.get_teacher_by_id(new_teacher_id)
        
        current_app.logger.info(f'Admin created teacher: {new_teacher_id}')
        return success_response(new_teacher, "教师创建成功", 201)
    
    except Exception as e:
        current_app.logger.error(f'Failed to create teacher: {str(e)}')
        return error_response("创建教师失败", 500)


@auth_required
@role_required('admin')
def get_teacher(teacher_id):
    """
    获取单个教师信息
    
    Args:
        teacher_id (int): 教师ID
        
    Returns:
        JSON: 教师信息
    """
    try:
        # 获取教师信息
        teacher = TeacherService().get_teacher_by_id(teacher_id)
        if not teacher:
            return error_response("教师不存在", 404)
        
        current_app.logger.info(f'Admin retrieved teacher: {teacher_id}')
        return success_response(teacher)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve teacher {teacher_id}: {str(e)}')
        return error_response("获取教师信息失败", 500)


@auth_required
@role_required('admin')
def update_teacher(teacher_id):
    """
    更新教师信息
    
    Args:
        teacher_id (int): 教师ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 更新教师
        result = TeacherService().update_teacher(teacher_id, data)
        
        if not result:
            return error_response("教师不存在", 404)
        
        current_app.logger.info(f'Admin updated teacher: {teacher_id}')
        return success_response({"teacher_id": teacher_id}, "教师更新成功")
    
    except Exception as e:
        current_app.logger.error(f'Failed to update teacher {teacher_id}: {str(e)}')
        return error_response("更新教师失败", 500)


@auth_required
@role_required('admin')
def delete_teacher(teacher_id):
    """
    删除教师
    
    Args:
        teacher_id (int): 教师ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 删除教师
        result = TeacherService().delete_teacher(teacher_id)
        if not result:
            return error_response("教师不存在", 404)
        
        current_app.logger.info(f'Admin deleted teacher: {teacher_id}')
        return success_response({"teacher_id": teacher_id}, "教师删除成功")
    
    except Exception as e:
        current_app.logger.error(f'Failed to delete teacher {teacher_id}: {str(e)}')
        return error_response("删除教师失败", 500)