"""考试类型管理模块，处理考试类型的增删改查操作"""
from flask import jsonify, request, session
from services.exam_type_service import ExamTypeService
from utils.helpers import success_response, error_response, auth_required, role_required
from utils.logger import app_logger


@auth_required
@role_required('admin')
def get_exam_types():
    """获取考试类型列表"""
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用考试类型服务获取考试类型列表
        exam_type_service = ExamTypeService()
        result = exam_type_service.get_all_exam_types(page, per_page)
        
        return success_response(result)
        
    except Exception as e:
        return error_response(f'Failed to fetch exam types: {str(e)}', 500)


@auth_required
@role_required('admin')
def create_exam_type():
    """创建考试类型"""
    try:
        data = request.get_json()
        exam_type_name = data.get('exam_type_name')
        
        if not exam_type_name:
            return error_response('Missing required field: exam_type_name', 400)
        
        # 使用考试类型服务创建考试类型
        exam_type_service = ExamTypeService()
        exam_type_data = {'exam_type_name': exam_type_name}
        result = exam_type_service.create_exam_type(exam_type_data)
        
        if result:
            app_logger.info("Admin created exam type")
            return success_response({'message': 'Exam type created successfully'}, 'Exam type created successfully', 201)
        else:
            app_logger.error("Failed to create exam type")
            return error_response('Failed to create exam type', 400)
            
    except Exception as e:
        app_logger.error(f'Failed to create exam type: {str(e)}')
        return error_response(f'Failed to create exam type: {str(e)}', 500)


@auth_required
@role_required('admin')
def get_exam_type(exam_type_id):
    """获取考试类型详情"""
    try:
        # 使用考试类型服务获取考试类型信息
        exam_type_service = ExamTypeService()
        exam_type = exam_type_service.get_exam_type_by_id(exam_type_id)
        
        if exam_type:
            return success_response(exam_type)
        else:
            return error_response('Exam type not found', 404)
            
    except Exception as e:
        return error_response(f'Failed to fetch exam type: {str(e)}', 500)


@auth_required
@role_required('admin')
def update_exam_type(exam_type_id):
    """更新考试类型"""
    try:
        data = request.get_json()
        exam_type_name = data.get('exam_type_name')  # 使用正确的字段名
        
        if not exam_type_name:
            return error_response('Missing required field: exam_type_name', 400)
        
        # 使用考试类型服务更新考试类型信息
        exam_type_service = ExamTypeService()
        result = exam_type_service.update_exam_type(exam_type_id, {'exam_type_name': exam_type_name})
        
        if result:
            return success_response(True, 'Exam type updated successfully')  # 修复返回数据结构
        else:
            return error_response('Failed to update exam type', 400)
            
    except Exception as e:
        return error_response(f'Failed to update exam type: {str(e)}', 500)


@auth_required
@role_required('admin')
def delete_exam_type(exam_type_id):
    """删除考试类型"""
    try:
        # 使用考试类型服务删除考试类型
        exam_type_service = ExamTypeService()
        result = exam_type_service.delete_exam_type(exam_type_id)
        
        if result:
            return success_response({'message': 'Exam type deleted successfully'}, 'Exam type deleted successfully', 204)
        else:
            return error_response('Failed to delete exam type', 400)
            
    except Exception as e:
        return error_response(f'Failed to delete exam type: {str(e)}', 500)