"""考试类型管理模块，处理考试类型相关的所有操作"""
from flask import jsonify, request
from services import ExamTypeService
from utils.helpers import success_response, error_response


def get_exam_types():
    """获取考试类型列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用考试类型服务获取考试类型列表
        exam_type_service = ExamTypeService()
        result = exam_type_service.get_all_exam_types(page, per_page)
        
        return success_response(result)
        
    except Exception as e:
        return error_response(f'Failed to fetch exam types: {str(e)}', 500)


def create_exam_type():
    """创建考试类型"""
    try:
        data = request.get_json()
        type_name = data.get('type_name')
        description = data.get('description')
        
        if not type_name:
            return error_response('Missing required field: type_name', 400)
        
        # 使用考试类型服务创建考试类型
        exam_type_service = ExamTypeService()
        result = exam_type_service.create_exam_type(data)
        
        if result:
            return success_response(result, 'Exam type created successfully', 201)
        else:
            return error_response('Failed to create exam type', 400)
            
    except Exception as e:
        return error_response(f'Failed to create exam type: {str(e)}', 500)


def get_exam_type(type_id):
    """获取单个考试类型信息"""
    try:
        # 使用考试类型服务获取考试类型信息
        exam_type_service = ExamTypeService()
        exam_type = exam_type_service.get_exam_type_by_id(type_id)
        
        if exam_type:
            return success_response(exam_type)
        else:
            return error_response('Exam type not found', 404)
            
    except Exception as e:
        return error_response(f'Failed to fetch exam type: {str(e)}', 500)


def update_exam_type(type_id):
    """更新考试类型信息"""
    try:
        data = request.get_json()
        type_name = data.get('type_name')
        description = data.get('description')
        
        if not type_name:
            return error_response('Missing required field: type_name', 400)
        
        # 使用考试类型服务更新考试类型信息
        exam_type_service = ExamTypeService()
        result = exam_type_service.update_exam_type(type_id, data)
        
        if result:
            return success_response(result, 'Exam type updated successfully')
        else:
            return error_response('Failed to update exam type', 400)
            
    except Exception as e:
        return error_response(f'Failed to update exam type: {str(e)}', 500)


def delete_exam_type(type_id):
    """删除考试类型"""
    try:
        # 使用考试类型服务删除考试类型
        exam_type_service = ExamTypeService()
        result = exam_type_service.delete_exam_type(type_id)
        
        if result:
            return success_response(None, 'Exam type deleted successfully'), 204
        else:
            return error_response('Failed to delete exam type', 400)
            
    except Exception as e:
        return error_response(f'Failed to delete exam type: {str(e)}', 500)