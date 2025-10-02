from flask import Blueprint, request, current_app
from apps.services import ClassService
from apps.utils.helpers import success_response, error_response, validate_json_input
from apps.utils.decorators import handle_exceptions


# 班级管理蓝图
admin_classes_bp = Blueprint('admin_classes', __name__, url_prefix='/classes')


@handle_exceptions
def get_classes():
    """
    获取所有班级列表
    
    Returns:
        JSON: 班级列表
    """
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 调用服务获取班级列表
    class_service = ClassService()
    classes_data = class_service.get_all_classes(page, per_page)
    
    # 记录成功日志
    current_app.logger.info(f"成功获取班级列表，第{page}页，每页{per_page}条")
    
    return success_response(classes_data)


@handle_exceptions
def create_class():
    """
    创建班级
    
    Returns:
        JSON: 创建结果
    """
    # 验证请求数据
    data, error = validate_json_input(['class_name'])
    if error:
        return error
    
    class_name = data.get('class_name')
    
    # 检查必填字段
    if not class_name:
        return error_response("班级名称不能为空", 400)
    
    # 准备班级数据字典
    class_data = {
        'class_name': class_name
    }
    
    # 调用服务创建班级
    class_service = ClassService()
    result = class_service.create_class(class_data)
    
    # 记录成功日志
    current_app.logger.info(f"成功创建班级: {class_name}")
    
    return success_response(result, 201)


@handle_exceptions
def get_class(class_id: int):
    """
    根据ID获取班级信息
    
    Args:
        class_id (int): 班级ID
        
    Returns:
        JSON: 班级信息
    """
    # 调用服务获取班级信息
    class_service = ClassService()
    class_data = class_service.get_class_by_id(class_id)
    
    if not class_data:
        # 记录警告日志
        current_app.logger.warning(f"班级未找到，ID: {class_id}")
        return error_response("班级不存在", 404)
    
    # 记录成功日志
    current_app.logger.info(f"成功获取班级信息，ID: {class_id}")
    
    return success_response(class_data)


@handle_exceptions
def update_class(class_id: int):
    """
    更新班级信息
    
    Args:
        class_id (int): 班级ID
        
    Returns:
        JSON: 更新结果
    """
    # 验证请求数据
    data, error = validate_json_input(required_fields=[], allow_empty=True)
    if error:
        return error
    
    # 准备更新数据字典
    update_data = {}
    if 'class_name' in data:
        update_data['class_name'] = data['class_name']
    
    # 调用服务更新班级
    class_service = ClassService()
    result = class_service.update_class(class_id, update_data)
    
    if not result:
        # 记录警告日志
        current_app.logger.warning(f"班级未找到，ID: {class_id}")
        return error_response("班级不存在", 404)
    
    # 记录成功日志
    current_app.logger.info(f"成功更新班级信息，ID: {class_id}")
    
    return success_response({"message": "班级信息更新成功"})


@handle_exceptions
def delete_class(class_id: int):
    """
    删除班级
    
    Args:
        class_id (int): 班级ID
        
    Returns:
        JSON: 删除结果
    """
    # 调用服务删除班级
    class_service = ClassService()
    result = class_service.delete_class(class_id)
    
    if not result:
        # 记录警告日志
        current_app.logger.warning(f"班级未找到，ID: {class_id}")
        return error_response("班级不存在", 404)
    
    # 记录成功日志
    current_app.logger.info(f"成功删除班级，ID: {class_id}")
    
    return success_response({"message": "班级删除成功"})


# 注册路由
admin_classes_bp.add_url_rule('/', view_func=get_classes, methods=['GET'])
admin_classes_bp.add_url_rule('/', view_func=create_class, methods=['POST'])
admin_classes_bp.add_url_rule('/<int:class_id>', view_func=get_class, methods=['GET'])
admin_classes_bp.add_url_rule('/<int:class_id>', view_func=update_class, methods=['PUT'])
admin_classes_bp.add_url_rule('/<int:class_id>', view_func=delete_class, methods=['DELETE'])