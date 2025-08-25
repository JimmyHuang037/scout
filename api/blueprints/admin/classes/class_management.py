"""班级管理模块，处理班级相关的所有操作"""
from flask import jsonify, request, session
from services import ClassService
from utils.helpers import success_response, error_response, require_auth, require_role
from utils.logger import app_logger


def get_classes():
    """获取班级列表"""
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
        
        # 使用班级服务获取班级列表
        class_service = ClassService()
        result = class_service.get_all_classes(page, per_page)
        
        app_logger.info("Admin retrieved class list")
        return success_response(result)
        
    except Exception as e:
        app_logger.error(f'Failed to fetch classes: {str(e)}')
        return error_response(f'Failed to fetch classes: {str(e)}', 500)


def create_class():
    """创建班级"""
    try:
        # 检查认证和权限
        auth_error = require_auth()
        if auth_error:
            return auth_error
            
        role_error = require_role('admin')
        if role_error:
            return role_error
        
        data = request.get_json()
        class_name = data.get('class_name')
        grade = data.get('grade')
        
        if not all([class_name, grade]):
            app_logger.warning("Create class attempt with missing required fields")
            return error_response('Missing required fields: class_name, grade', 400)
        
        # 使用班级服务创建班级
        class_service = ClassService()
        result = class_service.create_class(data)
        
        if result:
            app_logger.info(f"Admin created class {result.get('class_id')}")
            return success_response(result, 'Class created successfully', 201)
        else:
            app_logger.error("Failed to create class")
            return error_response('Failed to create class', 400)
            
    except Exception as e:
        app_logger.error(f'Failed to create class: {str(e)}')
        return error_response(f'Failed to create class: {str(e)}', 500)


def get_class(class_id):
    """获取单个班级信息"""
    try:
        # 检查认证和权限
        auth_error = require_auth()
        if auth_error:
            return auth_error
            
        role_error = require_role('admin')
        if role_error:
            return role_error
        
        # 使用班级服务获取班级信息
        class_service = ClassService()
        class_info = class_service.get_class_by_id(class_id)
        
        if class_info:
            app_logger.info(f"Admin retrieved class details for {class_id}")
            return success_response(class_info)
        else:
            app_logger.warning(f"Class not found: {class_id}")
            return error_response('Class not found', 404)
            
    except Exception as e:
        app_logger.error(f'Failed to fetch class: {str(e)}')
        return error_response(f'Failed to fetch class: {str(e)}', 500)


def update_class(class_id):
    """更新班级信息"""
    try:
        # 检查认证和权限
        auth_error = require_auth()
        if auth_error:
            return auth_error
            
        role_error = require_role('admin')
        if role_error:
            return role_error
        
        data = request.get_json()
        class_name = data.get('class_name')
        grade = data.get('grade')
        
        if not all([class_name, grade]):
            app_logger.warning(f"Update class attempt with missing required fields for {class_id}")
            return error_response('Missing required fields: class_name, grade', 400)
        
        # 使用班级服务更新班级信息
        class_service = ClassService()
        result = class_service.update_class(class_id, data)
        
        if result:
            app_logger.info(f"Admin updated class {class_id}")
            return success_response(result, 'Class updated successfully')
        else:
            app_logger.error(f"Failed to update class {class_id}")
            return error_response('Failed to update class', 400)
            
    except Exception as e:
        app_logger.error(f'Failed to update class: {str(e)}')
        return error_response(f'Failed to update class: {str(e)}', 500)


def delete_class(class_id):
    """删除班级"""
    try:
        # 使用班级服务删除班级
        class_service = ClassService()
        result = class_service.delete_class(class_id)
        
        if result:
            return success_response(None, 'Class deleted successfully'), 204
        else:
            return error_response('Failed to delete class', 400)
            
    except Exception as e:
        return error_response(f'Failed to delete class: {str(e)}', 500)