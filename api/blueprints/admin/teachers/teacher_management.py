"""教师管理模块，处理教师相关的所有操作"""
from flask import jsonify, request, session, current_app
from services import TeacherService
from utils.helpers import success_response, error_response, auth_required, role_required


@auth_required
@role_required('admin')
def create_teacher():
    """
    创建教师账户
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 提取必要字段
        name = data.get('name')
        email = data.get('email')
        subject_id = data.get('subject_id')
        
        # 验证必填字段
        if not all([name, email, subject_id]):
            return error_response("缺少必要字段", 400)
        
        # 创建教师
        teacher = TeacherService.create_teacher(name=name, email=email, subject_id=subject_id)
        
        current_app.logger.info(f'Admin created teacher: {teacher.id}')
        return success_response("教师创建成功", {"teacher_id": teacher.id})
    
    except Exception as e:
        current_app.logger.error(f'Failed to create teacher: {str(e)}')
        return error_response("创建教师失败", 500)


@auth_required
@role_required('admin')
def get_teacher(teacher_id):
    """
    获取教师详情
    
    Args:
        teacher_id (int): 教师ID
        
    Returns:
        JSON: 教师详情
    """
    try:
        # 获取教师详情
        teacher = TeacherService.get_teacher_by_id(teacher_id)
        if not teacher:
            return error_response("教师不存在", 404)
        
        current_app.logger.info(f'Admin retrieved teacher: {teacher_id}')
        return success_response("获取教师详情成功", teacher)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve teacher {teacher_id}: {str(e)}')
        return error_response("获取教师详情失败", 500)


@auth_required
@role_required('admin')
def get_teachers():
    """
    获取所有教师列表
    
    Returns:
        JSON: 教师列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取教师列表
        teachers_data = TeacherService.get_all_teachers(page, per_page)
        
        current_app.logger.info('Admin retrieved all teachers')
        return success_response("获取教师列表成功", teachers_data)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve teachers: {str(e)}')
        return error_response("获取教师列表失败", 500)


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
        updated_teacher = TeacherService.update_teacher(
            teacher_id=teacher_id,
            name=data.get('name'),
            email=data.get('email'),
            subject_id=data.get('subject_id')
        )
        
        if not updated_teacher:
            return error_response("教师不存在", 404)
        
        current_app.logger.info(f'Admin updated teacher: {teacher_id}')
        return success_response("教师更新成功", {"teacher_id": updated_teacher.id})
    
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
        result = TeacherService.delete_teacher(teacher_id)
        if not result:
            return error_response("教师不存在", 404)
        
        current_app.logger.info(f'Admin deleted teacher: {teacher_id}')
        return success_response("教师删除成功", {"teacher_id": teacher_id})
    
    except Exception as e:
        current_app.logger.error(f'Failed to delete teacher {teacher_id}: {str(e)}')
        return error_response("删除教师失败", 500)