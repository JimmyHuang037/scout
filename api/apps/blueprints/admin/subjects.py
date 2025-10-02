from flask import Blueprint, request, current_app
from apps.services.subject_service import SubjectService
from apps.utils.decorators import handle_exceptions
from apps.utils.responses import success_response, error_response
from apps.utils.validation import validate_json_input


# 科目管理蓝图模块
admin_subjects_bp = Blueprint('admin_subjects', __name__, url_prefix='/subjects')


@handle_exceptions
def get_subjects():
    """
    获取所有科目列表
    
    Returns:
        JSON: 科目列表
    """
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 调用服务获取科目列表
    subject_service = SubjectService()
    subjects_data = subject_service.get_all_subjects(page, per_page)
    
    # 记录成功日志
    current_app.logger.info(f"成功获取科目列表，第{page}页，每页{per_page}条")
    
    return success_response(subjects_data)


@handle_exceptions
def create_subject():
    """
    创建科目
    
    Returns:
        JSON: 创建结果
    """
    # 验证请求数据
    data, error = validate_json_input(['subject_name'])
    if error:
        return error
    
    subject_name = data.get('subject_name')
    
    # 检查必填字段
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
    
    return success_response(result, 201)


@handle_exceptions
def get_subject(subject_id: int):
    """
    根据ID获取科目信息
    
    Args:
        subject_id (int): 科目ID
        
    Returns:
        JSON: 科目信息
    """
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


@handle_exceptions
def update_subject(subject_id: int):
    """
    更新科目信息
    
    Args:
        subject_id (int): 科目ID
        
    Returns:
        JSON: 更新结果
    """
    # 验证请求数据
    data, error = validate_json_input(required_fields=[], allow_empty=True)
    if error:
        return error
    
    # 准备更新数据字典
    update_data = {}
    if 'subject_name' in data:
        update_data['subject_name'] = data['subject_name']
    
    # 调用服务更新科目
    subject_service = SubjectService()
    result = subject_service.update_subject(subject_id, update_data)
    
    if not result:
        # 记录警告日志
        current_app.logger.warning(f"科目未找到，ID: {subject_id}")
        return error_response("科目不存在", 404)
    
    # 记录成功日志
    current_app.logger.info(f"成功更新科目信息，ID: {subject_id}")
    
    return success_response({"message": "科目信息更新成功"})


@handle_exceptions
def delete_subject(subject_id: int):
    """
    删除科目
    
    Args:
        subject_id (int): 科目ID
        
    Returns:
        JSON: 删除结果
    """
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


# 注册路由
admin_subjects_bp.add_url_rule('/', view_func=get_subjects, methods=['GET'])
admin_subjects_bp.add_url_rule('/', view_func=create_subject, methods=['POST'])
admin_subjects_bp.add_url_rule('/<int:subject_id>', view_func=get_subject, methods=['GET'])
admin_subjects_bp.add_url_rule('/<int:subject_id>', view_func=update_subject, methods=['PUT'])
admin_subjects_bp.add_url_rule('/<int:subject_id>', view_func=delete_subject, methods=['DELETE'])