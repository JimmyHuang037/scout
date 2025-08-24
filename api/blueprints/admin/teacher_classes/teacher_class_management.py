"""教师班级关联管理模块，处理教师班级关联相关的所有操作"""
from flask import jsonify, request
from services import TeacherClassService
from utils.helpers import success_response, error_response


def get_teacher_classes():
    """获取教师班级关联列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用教师班级关联服务获取列表
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.get_all_teacher_classes(page, per_page)
        
        return success_response(result)
        
    except Exception as e:
        return error_response(f'Failed to fetch teacher classes: {str(e)}'), 500


def create_teacher_class():
    """创建教师班级关联"""
    try:
        data = request.get_json()
        teacher_id = data.get('teacher_id')
        class_id = data.get('class_id')
        
        if not all([teacher_id, class_id]):
            return error_response('Missing required fields: teacher_id, class_id'), 400
        
        # 使用教师班级关联服务创建关联
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.create_teacher_class(data)
        
        if result:
            return success_response(message='Teacher class association created successfully'), 201
        else:
            return error_response('Failed to create teacher class association'), 400
            
    except Exception as e:
        return error_response(f'Failed to create teacher class association: {str(e)}'), 500


def get_teacher_class_by_teacher(teacher_id):
    """根据教师ID获取教师班级关联信息"""
    try:
        # 使用教师班级关联服务获取信息
        teacher_class_service = TeacherClassService()
        teacher_classes = teacher_class_service.get_teacher_class_by_teacher(teacher_id)
        
        return success_response(teacher_classes)
            
    except Exception as e:
        return error_response(f'Failed to fetch teacher classes: {str(e)}'), 500


def delete_teacher_class(teacher_id, class_id):
    """删除教师班级关联"""
    try:
        # 使用教师班级关联服务删除关联
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.delete_teacher_class(teacher_id, class_id)
        
        if result:
            return success_response(message='Teacher class association deleted successfully')
        else:
            return error_response('Failed to delete teacher class association'), 400
            
    except Exception as e:
        return error_response(f'Failed to delete teacher class association: {str(e)}'), 500
