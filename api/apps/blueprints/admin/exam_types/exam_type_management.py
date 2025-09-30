"""考试类型管理模块，处理考试类型相关的所有操作"""
from flask import jsonify, request, session, current_app
from services import ExamTypeService
from utils.helpers import success_response, error_response, auth_required, role_required


@auth_required
@role_required('admin')
def create_exam_type():
    """
    创建考试类型
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 提取必要字段
        name = data.get('exam_type_name') or data.get('name')
        
        # 验证必填字段
        if not name:
            return error_response("缺少必要字段", 400)
        
        # 创建考试类型
        exam_type_service = ExamTypeService()
        exam_type_data = {'exam_type_name': name}
        exam_type = exam_type_service.create_exam_type(exam_type_data)
        
        if not exam_type:
            return error_response("创建考试类型失败", 400)
        
        current_app.logger.info(f'Admin created exam type: {exam_type["exam_type_id"]}')
        return success_response(exam_type, "考试类型创建成功", 201)
    
    except Exception as e:
        current_app.logger.error(f'Failed to create exam type: {str(e)}')
        return error_response("创建考试类型失败", 500)


@auth_required
@role_required('admin')
def get_exam_types():
    """
    获取所有考试类型列表
    
    Returns:
        JSON: 考试类型列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取考试类型列表
        exam_type_service = ExamTypeService()
        exam_types = exam_type_service.get_all_exam_types(page, per_page)
        
        current_app.logger.info('Admin retrieved all exam types')
        return success_response(exam_types)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve exam types: {str(e)}')
        return error_response("获取考试类型列表失败", 500)


@auth_required
@role_required('admin')
def get_exam_type(exam_type_id):
    """
    获取考试类型详情
    
    Args:
        exam_type_id (int): 考试类型ID
        
    Returns:
        JSON: 考试类型详情
    """
    try:
        # 获取考试类型详情
        exam_type_service = ExamTypeService()
        exam_type = exam_type_service.get_exam_type_by_id(exam_type_id)
        if not exam_type:
            return error_response("考试类型不存在", 404)
        
        current_app.logger.info(f'Admin retrieved exam type: {exam_type_id}')
        return success_response(exam_type)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve exam type {exam_type_id}: {str(e)}')
        return error_response("获取考试类型详情失败", 500)


@auth_required
@role_required('admin')
def update_exam_type(exam_type_id):
    """
    更新考试类型
    
    Args:
        exam_type_id (int): 考试类型ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 提取必要字段
        name = data.get('exam_type_name') or data.get('name')
        
        # 验证必填字段
        if not name:
            return error_response("缺少必要字段", 400)
        
        # 更新考试类型
        exam_type_service = ExamTypeService()
        exam_type_data = {'exam_type_name': name}
        result = exam_type_service.update_exam_type(exam_type_id, exam_type_data)
        
        if not result:
            return error_response("考试类型不存在", 404)
        
        current_app.logger.info(f'Admin updated exam type: {exam_type_id}')
        return success_response({"exam_type_id": exam_type_id}, "考试类型更新成功")
    
    except Exception as e:
        current_app.logger.error(f'Failed to update exam type {exam_type_id}: {str(e)}')
        return error_response("更新考试类型失败", 500)


@auth_required
@role_required('admin')
def delete_exam_type(exam_type_id):
    """
    删除考试类型
    
    Args:
        exam_type_id (int): 考试类型ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 删除考试类型
        exam_type_service = ExamTypeService()
        result = exam_type_service.delete_exam_type(exam_type_id)
        if not result:
            return error_response("考试类型不存在", 404)
        
        current_app.logger.info(f'Admin deleted exam type: {exam_type_id}')
        return success_response({"exam_type_id": exam_type_id}, "考试类型删除成功")
    
    except Exception as e:
        current_app.logger.error(f'Failed to delete exam type {exam_type_id}: {str(e)}')
        return error_response("删除考试类型失败", 500)