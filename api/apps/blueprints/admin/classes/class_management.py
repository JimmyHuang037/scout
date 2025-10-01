from apps.services import ClassService
from apps.utils.helpers import success_response, error_response
from flask import request, current_app
"""班级管理模块，处理班级相关的所有操作"""


def get_classes():
    """
    获取所有班级列表
    
    Returns:
        JSON: 班级列表
    """
    try:
        # 调用服务获取班级列表
        class_service = ClassService()
        classes_data = class_service.get_all_classes()
        
        current_app.logger.info("Admin retrieved class list")
        return success_response(classes_data)
    except Exception as e:
        current_app.logger.error(f"Error getting classes: {str(e)}")
        return error_response('Failed to get classes', 500)


def create_class():
    """
    创建新班级
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            current_app.logger.warning("Create class attempt with missing required fields")
            return error_response('No data provided', 400)
            
        # 调用服务创建班级
        class_service = ClassService()
        result = class_service.create_class(data)
        
        if result:
            current_app.logger.info(f"Admin created class {result.get('class_id')}")
            return success_response(result, 'Class created successfully'), 201
        else:
            current_app.logger.error("Failed to create class")
            return error_response('Failed to create class', 400)
    except Exception as e:
        current_app.logger.error(f"Error creating class: {str(e)}")
        return error_response('Failed to create class', 500)


def get_class(class_id):
    """
    获取指定班级信息
    
    Args:
        class_id (int): 班级ID
        
    Returns:
        JSON: 班级信息
    """
    try:
        # 调用服务获取班级信息
        class_service = ClassService()
        class_data = class_service.get_class_by_id(class_id)
        
        if not class_data:
            current_app.logger.warning(f"Class {class_id} not found")
            return error_response('Class not found', 404)
            
        current_app.logger.info(f"Admin retrieved class {class_id}")
        return success_response(class_data)
    except Exception as e:
        current_app.logger.error(f"Error getting class {class_id}: {str(e)}")
        return error_response('Failed to get class', 500)


def update_class(class_id):
    """
    更新班级信息
    
    Args:
        class_id (int): 班级ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            current_app.logger.warning("Update class attempt with missing required fields")
            return error_response('No data provided', 400)
            
        # 调用服务更新班级信息
        class_service = ClassService()
        result = class_service.update_class(class_id, data)
        
        if not result:
            current_app.logger.warning(f"Class {class_id} not found for update")
            return error_response('Class not found', 404)
            
        current_app.logger.info(f"Admin updated class {class_id}")
        return success_response(result, 'Class updated successfully')
    except Exception as e:
        current_app.logger.error(f"Error updating class {class_id}: {str(e)}")
        return error_response('Failed to update class', 500)


def delete_class(class_id):
    """
    删除班级
    
    Args:
        class_id (int): 班级ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 调用服务删除班级
        class_service = ClassService()
        result = class_service.delete_class(class_id)
        
        if not result:
            current_app.logger.warning(f"Class {class_id} not found for deletion")
            return error_response('Class not found', 404)
            
        current_app.logger.info(f"Admin deleted class {class_id}")
        return success_response(None, 'Class deleted successfully')
    except Exception as e:
        current_app.logger.error(f"Error deleting class {class_id}: {str(e)}")
        return error_response('Failed to delete class', 500)