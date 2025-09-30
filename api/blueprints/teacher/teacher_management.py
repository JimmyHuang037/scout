"""教师管理模块，处理教师相关操作"""
from flask import jsonify, request, current_app
from services.teacher_service import TeacherService
from utils.helpers import success_response, error_response
from utils import database_service


def get_all_teachers():
    """获取所有教师列表"""
    try:
        # 移除了认证检查装饰器，保持系统简单
        teacher_service = TeacherService()
        teachers = teacher_service.get_all_teachers()
        return success_response(teachers)
    except Exception as e:
        current_app.logger.error(f'Error getting teachers: {str(e)}')
        return error_response('Failed to get teachers', 500)


def get_teacher_by_id(teacher_id):
    """根据ID获取教师信息"""
    try:
        # 移除了认证检查装饰器，保持系统简单
        teacher_service = TeacherService()
        teacher = teacher_service.get_teacher_by_id(teacher_id)
        if teacher:
            return success_response(teacher)
        else:
            return error_response('Teacher not found', 404)
    except Exception as e:
        current_app.logger.error(f'Error getting teacher {teacher_id}: {str(e)}')
        return error_response('Failed to get teacher', 500)


def create_teacher():
    """创建新教师"""
    try:
        # 移除了认证检查装饰器，保持系统简单
        data = request.get_json()
        teacher_service = TeacherService()
        result = teacher_service.create_teacher(data)
        return success_response(result, 'Teacher created successfully', 201)
    except Exception as e:
        current_app.logger.error(f'Error creating teacher: {str(e)}')
        return error_response('Failed to create teacher', 500)


def update_teacher(teacher_id):
    """更新教师信息"""
    try:
        # 移除了认证检查装饰器，保持系统简单
        data = request.get_json()
        teacher_service = TeacherService()
        result = teacher_service.update_teacher(teacher_id, data)
        if result:
            return success_response(result, 'Teacher updated successfully')
        else:
            return error_response('Teacher not found', 404)
    except Exception as e:
        current_app.logger.error(f'Error updating teacher {teacher_id}: {str(e)}')
        return error_response('Failed to update teacher', 500)


def delete_teacher(teacher_id):
    """删除教师"""
    try:
        # 移除了认证检查装饰器，保持系统简单
        teacher_service = TeacherService()
        result = teacher_service.delete_teacher(teacher_id)
        if result:
            return success_response(None, 'Teacher deleted successfully')
        else:
            return error_response('Teacher not found', 404)
    except Exception as e:
        current_app.logger.error(f'Error deleting teacher {teacher_id}: {str(e)}')
        return error_response('Failed to delete teacher', 500)