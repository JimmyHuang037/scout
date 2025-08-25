"""班级管理模块，处理班级相关的所有操作"""
from flask import jsonify, request
from services import ClassService
from utils.helpers import success_response, error_response


def get_classes():
    """获取班级列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用班级服务获取班级列表
        class_service = ClassService()
        result = class_service.get_all_classes(page, per_page)
        
        return success_response(result)
        
    except Exception as e:
        return error_response(f'Failed to fetch classes: {str(e)}', 500)


def create_class():
    """创建班级"""
    try:
        data = request.get_json()
        class_name = data.get('class_name')
        grade = data.get('grade')
        
        if not all([class_name, grade]):
            return error_response('Missing required fields: class_name, grade', 400)
        
        # 使用班级服务创建班级
        class_service = ClassService()
        result = class_service.create_class(data)
        
        if result:
            return success_response(result, 'Class created successfully', 201)
        else:
            return error_response('Failed to create class', 400)
            
    except Exception as e:
        return error_response(f'Failed to create class: {str(e)}', 500)


def get_class(class_id):
    """获取单个班级信息"""
    try:
        # 使用班级服务获取班级信息
        class_service = ClassService()
        class_info = class_service.get_class_by_id(class_id)
        
        if class_info:
            return success_response(class_info)
        else:
            return error_response('Class not found', 404)
            
    except Exception as e:
        return error_response(f'Failed to fetch class: {str(e)}', 500)


def update_class(class_id):
    """更新班级信息"""
    try:
        data = request.get_json()
        class_name = data.get('class_name')
        grade = data.get('grade')
        
        if not all([class_name, grade]):
            return error_response('Missing required fields: class_name, grade', 400)
        
        # 使用班级服务更新班级信息
        class_service = ClassService()
        result = class_service.update_class(class_id, data)
        
        if result:
            return success_response(result, 'Class updated successfully')
        else:
            return error_response('Failed to update class', 400)
            
    except Exception as e:
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