"""科目管理模块，处理科目相关的所有操作"""
from flask import request, current_app, Blueprint
from apps.services import SubjectService
from apps.utils.helpers import success_response, error_response

# 创建科目管理蓝图
admin_subjects_bp = Blueprint('admin_subjects', __name__, url_prefix='/subjects')


@admin_subjects_bp.route('/', methods=['POST'])
def create_subject():
    """
    创建科目
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("请求数据不能为空", 400)
        
        subject_name = data.get('subject_name')
        if not subject_name:
            return error_response("科目名称不能为空", 400)
        
        # 准备科目数据字典
        subject_data = {
            'subject_name': subject_name
        }
        
        # 调用服务创建科目
        subject_service = SubjectService()
        result = subject_service.create_subject(subject_data)
        
        # 记录成功日志
        current_app.logger.info(f"成功创建科目: {subject_name}")
        
        return success_response({"subject_id": result}, 201)
        
    except ValueError as e:
        # 处理科目名称已存在的情况
        current_app.logger.warning(f"创建科目时发生错误: {str(e)}")
        return error_response(str(e), 400)
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"创建科目时发生错误: {str(e)}")
        return error_response("创建科目失败", 500)


@admin_subjects_bp.route('/', methods=['GET'])
def get_subjects():
    """
    获取所有科目列表
    
    Returns:
        JSON: 科目列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 调用服务获取科目列表
        subject_service = SubjectService()
        subjects_data = subject_service.get_all_subjects(page, per_page)
        
        # 记录成功日志
        current_app.logger.info(f"成功获取科目列表，第{page}页，每页{per_page}条")
        
        return success_response(subjects_data)
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"获取科目列表时发生错误: {str(e)}")
        return error_response("获取科目列表失败", 500)


@admin_subjects_bp.route('/<int:subject_id>', methods=['GET'])
def get_subject(subject_id):
    """
    根据ID获取科目信息
    
    Args:
        subject_id (int): 科目ID
        
    Returns:
        JSON: 科目信息
    """
    try:
        # 调用服务获取科目信息
        subject_service = SubjectService()
        subject_data = subject_service.get_subject_by_id(subject_id)
        
        if not subject_data:
            # 记录警告日志
            current_app.logger.warning(f"科目未找到，ID: {subject_id}")
            return error_response("科目不存在", 404)
        
        # 记录成功日志
        current_app.logger.info(f"成功获取科目信息，ID: {subject_id}")
        
        return success_response(subject_data)
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"获取科目信息时发生错误: {str(e)}")
        return error_response("获取科目信息失败", 500)


@admin_subjects_bp.route('/<int:subject_id>', methods=['PUT'])
def update_subject(subject_id):
    """
    更新科目信息
    
    Args:
        subject_id (int): 科目ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("请求数据不能为空", 400)
        
        subject_name = data.get('subject_name')
        if not subject_name:
            return error_response("科目名称不能为空", 400)
        
        # 准备科目数据字典
        subject_data = {
            'subject_name': subject_name
        }
        
        # 调用服务更新科目
        subject_service = SubjectService()
        result = subject_service.update_subject(subject_id, subject_data)
        
        if not result:
            # 记录警告日志
            current_app.logger.warning(f"科目未找到，ID: {subject_id}")
            return error_response("科目不存在", 404)
        
        # 记录成功日志
        current_app.logger.info(f"成功更新科目信息，ID: {subject_id}")
        
        return success_response({"message": "科目信息更新成功"})
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"更新科目信息时发生错误: {str(e)}")
        return error_response("更新科目信息失败", 500)


@admin_subjects_bp.route('/<int:subject_id>', methods=['DELETE'])
def delete_subject(subject_id):
    """
    删除科目
    
    Args:
        subject_id (int): 科目ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 调用服务删除科目
        subject_service = SubjectService()
        result = subject_service.delete_subject(subject_id)
        
        if not result:
            # 记录警告日志
            current_app.logger.warning(f"科目未找到，ID: {subject_id}")
            return error_response("科目不存在", 404)
        
        # 记录成功日志
        current_app.logger.info(f"成功删除科目，ID: {subject_id}")
        
        return success_response({"message": "科目删除成功"})
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"删除科目时发生错误: {str(e)}")
        return error_response("删除科目失败", 500)