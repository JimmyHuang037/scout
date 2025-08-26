"""教师管理模块，处理教师相关的所有操作"""
from flask import jsonify, request, session
from services import TeacherService
from utils.helpers import success_response, error_response, auth_required, role_required
from utils.logger import app_logger


@auth_required
@role_required('admin')
def get_teachers():
    """获取教师列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用教师服务获取教师列表
        teacher_service = TeacherService()
        result = teacher_service.get_all_teachers(page, per_page)
        
        app_logger.info("Admin retrieved teacher list")
        return success_response(result)
        
    except Exception as e:
        app_logger.error(f'Failed to fetch teachers: {str(e)}')
        return error_response(f'Failed to fetch teachers: {str(e)}', 500)


@auth_required
@role_required('admin')
def create_teacher():
    """创建教师"""
    try:
        data = request.get_json()
        # 使用教师服务创建教师
        teacher_service = TeacherService()
        result = teacher_service.create_teacher(data)
        
        if result:
            app_logger.info(f"Admin created teacher {result.get('teacher_id')}")
            return success_response(result, 'Teacher created successfully', 201)
        else:
            app_logger.error("Failed to create teacher")
            return error_response('Failed to create teacher', 400)
            
    except Exception as e:
        app_logger.error(f'Failed to create teacher: {str(e)}')
        return error_response(f'Failed to create teacher: {str(e)}', 500)


@auth_required
@role_required('admin')
def get_teacher(teacher_id):
    """获取单个教师信息"""
    try:
        # 使用教师服务获取教师信息
        teacher_service = TeacherService()
        teacher = teacher_service.get_teacher_by_id(teacher_id)
        
        if teacher:
            return success_response(teacher)
        else:
            return error_response('Teacher not found', 404)
            
    except Exception as e:
        return error_response(f'Failed to fetch teacher: {str(e)}', 500)


@auth_required
@role_required('admin')
def update_teacher(teacher_id):
    """更新教师信息"""
    try:
        data = request.get_json()
        # 使用教师服务更新教师信息
        teacher_service = TeacherService()
        result = teacher_service.update_teacher(teacher_id, data)
        
        if result:
            return success_response(result, 'Teacher updated successfully')
        else:
            return error_response('Failed to update teacher', 400)
            
    except Exception as e:
        return error_response(f'Failed to update teacher: {str(e)}', 500)


@auth_required
@role_required('admin')
def delete_teacher(teacher_id):
    """删除教师"""
    try:
        # 使用教师服务删除教师
        teacher_service = TeacherService()
        result = teacher_service.delete_teacher(teacher_id)
        
        if result:
            return success_response(None, 'Teacher deleted successfully')
        else:
            return error_response('Failed to delete teacher', 400)
            
    except Exception as e:
        return error_response(f'Failed to delete teacher: {str(e)}', 500)