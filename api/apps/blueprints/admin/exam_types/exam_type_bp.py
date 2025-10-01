"""考试类型管理模块，处理考试类型相关的所有操作"""
from flask import request, current_app, Blueprint
from apps.services import ExamTypeService
from apps.utils.helpers import success_response, error_response

# 创建考试类型管理蓝图
admin_exam_types_bp = Blueprint('admin_exam_types', __name__, url_prefix='/exam_types')


@admin_exam_types_bp.route('/', methods=['POST'])
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
            return error_response("请求数据不能为空", 400)
        
        exam_type_name = data.get('exam_type_name')
        if not exam_type_name:
            return error_response("考试类型名称不能为空", 400)
        
        # 准备考试类型数据字典
        exam_type_data = {
            'exam_type_name': exam_type_name
        }
        
        # 调用服务创建考试类型
        exam_type_service = ExamTypeService()
        result = exam_type_service.create_exam_type(exam_type_data)
        
        # 记录成功日志
        current_app.logger.info(f"成功创建考试类型: {exam_type_name}")
        
        return success_response({"exam_type_id": result}, 201)
        
    except ValueError as e:
        # 处理考试类型名称已存在的情况
        current_app.logger.warning(f"创建考试类型时发生错误: {str(e)}")
        return error_response(str(e), 400)
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"创建考试类型时发生错误: {str(e)}")
        return error_response("创建考试类型失败", 500)


@admin_exam_types_bp.route('/', methods=['GET'])
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
        
        # 调用服务获取考试类型列表
        exam_type_service = ExamTypeService()
        exam_types_data = exam_type_service.get_all_exam_types(page, per_page)
        
        # 记录成功日志
        current_app.logger.info(f"成功获取考试类型列表，第{page}页，每页{per_page}条")
        
        return success_response(exam_types_data)
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"获取考试类型列表时发生错误: {str(e)}")
        return error_response("获取考试类型列表失败", 500)


@admin_exam_types_bp.route('/<int:exam_type_id>', methods=['GET'])
def get_exam_type(exam_type_id):
    """
    根据ID获取考试类型信息
    
    Args:
        exam_type_id (int): 考试类型ID
        
    Returns:
        JSON: 考试类型信息
    """
    try:
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
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"获取考试类型信息时发生错误: {str(e)}")
        return error_response("获取考试类型信息失败", 500)


@admin_exam_types_bp.route('/<int:exam_type_id>', methods=['PUT'])
def update_exam_type(exam_type_id):
    """
    更新考试类型信息
    
    Args:
        exam_type_id (int): 考试类型ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("请求数据不能为空", 400)
        
        exam_type_name = data.get('exam_type_name')
        if not exam_type_name:
            return error_response("考试类型名称不能为空", 400)
        
        # 准备考试类型数据字典
        exam_type_data = {
            'exam_type_name': exam_type_name
        }
        
        # 调用服务更新考试类型
        exam_type_service = ExamTypeService()
        result = exam_type_service.update_exam_type(exam_type_id, exam_type_data)
        
        if not result:
            # 记录警告日志
            current_app.logger.warning(f"考试类型未找到，ID: {exam_type_id}")
            return error_response("考试类型不存在", 404)
        
        # 记录成功日志
        current_app.logger.info(f"成功更新考试类型信息，ID: {exam_type_id}")
        
        return success_response({"message": "考试类型信息更新成功"})
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"更新考试类型信息时发生错误: {str(e)}")
        return error_response("更新考试类型信息失败", 500)


@admin_exam_types_bp.route('/<int:exam_type_id>', methods=['DELETE'])
def delete_exam_type(exam_type_id):
    """
    删除考试类型
    
    Args:
        exam_type_id (int): 考试类型ID
        
    Returns:
        JSON: 删除结果
    """
    try:
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
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"删除考试类型时发生错误: {str(e)}")
        return error_response("删除考试类型失败", 500)