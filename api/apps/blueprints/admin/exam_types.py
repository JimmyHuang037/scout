from flask import Blueprint, request, current_app
from apps.services.exam_type_service import ExamTypeService
from apps.utils.decorators import handle_exceptions
from apps.utils.responses import success_response, error_response
from apps.utils.validation import validate_json_input


# 考试类型管理蓝图
admin_exam_types_bp = Blueprint('admin_exam_types', __name__)


@handle_exceptions
def get_exam_types():
    """
    获取所有考试类型列表
    
    Returns:
        JSON: 考试类型列表
    """
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 调用服务获取考试类型列表
    exam_type_service = ExamTypeService()
    exam_types_data = exam_type_service.get_all_exam_types(page, per_page)
    
    # 记录成功日志
    current_app.logger.info(f"成功获取考试类型列表，第{page}页，每页{per_page}条")
    
    return success_response(exam_types_data)


@handle_exceptions
def create_exam_type():
    """
    创建考试类型
    
    Returns:
        JSON: 创建结果
    """
    # 验证请求数据
    data, error = validate_json_input(['exam_type_name'])
    if error:
        return error
    
    exam_type_name = data.get('exam_type_name')
    
    # 准备考试类型数据字典
    exam_type_data = {
        'exam_type_name': exam_type_name
    }
    
    # 调用服务创建考试类型
    exam_type_service = ExamTypeService()
    result = exam_type_service.create_exam_type(exam_type_data)
    
    # 记录成功日志
    current_app.logger.info(f"成功创建考试类型: {exam_type_name}")
    
    return success_response(result, 201)


@handle_exceptions
def get_exam_type(exam_type_id: int):
    """
    根据ID获取考试类型信息
    
    Args:
        exam_type_id (int): 考试类型ID
        
    Returns:
        JSON: 考试类型信息
    """
    # 调用服务获取考试类型信息
    exam_type_service = ExamTypeService()
    exam_type_data = exam_type_service.get_exam_type_by_id(exam_type_id)
    
    if not exam_type_data:
        # 记录警告日志
        current_app.logger.warning(f"考试类型未找到，ID: {exam_type_id}")
        return error_response("考试类型不存在", 404)
    
    # 记录成功日志
    current_app.logger.info(f"成功获取考试类型信息，ID: {exam_type_id}")
    
    return success_response(exam_type_data)


@handle_exceptions
def update_exam_type(exam_type_id: int):
    """
    更新考试类型信息
    
    Args:
        exam_type_id (int): 考试类型ID
        
    Returns:
        JSON: 更新结果
    """
    # 验证请求数据
    data, error = validate_json_input(required_fields=[], allow_empty=True)
    if error:
        return error
    
    # 准备更新数据字典
    update_data = {}
    if 'exam_type_name' in data:
        update_data['exam_type_name'] = data['exam_type_name']
    
    # 调用服务更新考试类型
    exam_type_service = ExamTypeService()
    result = exam_type_service.update_exam_type(exam_type_id, update_data)
    
    if not result:
        # 记录警告日志
        current_app.logger.warning(f"考试类型未找到，ID: {exam_type_id}")
        return error_response("考试类型不存在", 404)
    
    # 记录成功日志
    current_app.logger.info(f"成功更新考试类型信息，ID: {exam_type_id}")
    
    return success_response({"message": "考试类型信息更新成功"})


@handle_exceptions
def delete_exam_type(exam_type_id: int):
    """
    删除考试类型
    
    Args:
        exam_type_id (int): 考试类型ID
        
    Returns:
        JSON: 删除结果
    """
    # 调用服务删除考试类型
    exam_type_service = ExamTypeService()
    result = exam_type_service.delete_exam_type(exam_type_id)
    
    if not result:
        # 记录警告日志
        current_app.logger.warning(f"考试类型未找到，ID: {exam_type_id}")
        return error_response("考试类型不存在", 404)
    
    # 记录成功日志
    current_app.logger.info(f"成功删除考试类型，ID: {exam_type_id}")
    
    return success_response({"message": "考试类型删除成功"})


# 注册路由
admin_exam_types_bp.add_url_rule('/', view_func=get_exam_types, methods=['GET'])
admin_exam_types_bp.add_url_rule('/', view_func=create_exam_type, methods=['POST'])
admin_exam_types_bp.add_url_rule('/<int:exam_type_id>', view_func=get_exam_type, methods=['GET'])
admin_exam_types_bp.add_url_rule('/<int:exam_type_id>', view_func=update_exam_type, methods=['PUT'])
admin_exam_types_bp.add_url_rule('/<int:exam_type_id>', view_func=delete_exam_type, methods=['DELETE'])