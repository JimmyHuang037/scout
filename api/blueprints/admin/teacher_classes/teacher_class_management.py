"""教师班级关联管理模块，处理教师班级关联相关的所有操作"""
from flask import jsonify, request, session
from services import TeacherClassService
from utils.helpers import success_response, error_response, require_auth, require_role
from utils.logger import app_logger


def get_teacher_classes():
    """获取教师班级关联列表"""
    try:
        # 检查认证和权限
        auth_error = require_auth()
        if auth_error:
            return auth_error
            
        role_error = require_role('admin')
        if role_error:
            return role_error
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用教师班级服务获取教师班级关联列表
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.get_all_teacher_classes(page, per_page)
        
        app_logger.info("Admin retrieved teacher-class associations")
        return success_response(result)
        
    except Exception as e:
        app_logger.error(f'Failed to fetch teacher-class associations: {str(e)}')
        return error_response(f'Failed to fetch teacher-class associations: {str(e)}', 500)


def create_teacher_class():
    """创建教师班级关联"""
    try:
        # 检查认证和权限
        auth_error = require_auth()
        if auth_error:
            return auth_error
            
        role_error = require_role('admin')
        if role_error:
            return role_error
        
        data = request.get_json()
        teacher_id = data.get('teacher_id')
        class_id = data.get('class_id')
        
        if not all([teacher_id, class_id]):
            app_logger.warning("Create teacher-class association attempt with missing fields")
            return error_response('Missing required fields: teacher_id, class_id', 400)
        
        # 使用教师班级服务创建教师班级关联
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.create_teacher_class(teacher_id, class_id)
        
        if result:
            app_logger.info(f"Admin created teacher-class association: teacher_id={teacher_id}, class_id={class_id}")
            return success_response(result, 'Teacher-class association created successfully', 201)
        else:
            app_logger.error("Failed to create teacher-class association")
            return error_response('Failed to create teacher-class association', 400)
            
    except Exception as e:
        app_logger.error(f'Failed to create teacher-class association: {str(e)}')
        return error_response(f'Failed to create teacher-class association: {str(e)}', 500)


def get_teacher_class_by_teacher(teacher_id):
    """根据教师ID获取教师班级关联信息"""
    try:
        # 检查认证和权限
        auth_error = require_auth()
        if auth_error:
            return auth_error
            
        role_error = require_role('admin')
        if role_error:
            return role_error
        
        # 使用教师班级服务根据教师ID获取教师班级关联信息
        teacher_class_service = TeacherClassService()
        teacher_classes = teacher_class_service.get_teacher_classes_by_teacher(teacher_id)
        
        if teacher_classes is not None:
            return success_response(teacher_classes)
        else:
            return error_response('Teacher classes not found', 404)
            
    except Exception as e:
        return error_response(f'Failed to fetch teacher classes: {str(e)}', 500)


def delete_teacher_class(teacher_id, class_id):
    """删除教师班级关联"""
    try:
        # 使用教师班级服务删除教师班级关联
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.delete_teacher_class(teacher_id, class_id)
        
        if result:
            # 修复返回值格式，避免返回嵌套元组
            return success_response(None, 'Teacher class deleted successfully', 204)
        else:
            return error_response('Failed to delete teacher class', 400)
            
    except Exception as e:
        return error_response(f'Failed to delete teacher class: {str(e)}', 500)