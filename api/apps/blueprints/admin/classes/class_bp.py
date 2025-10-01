from apps.services import ClassService
from apps.utils.helpers import success_response, error_response
from flask import request, current_app, Blueprint

# 创建班级管理蓝图
admin_classes_bp = Blueprint('admin_classes', __name__, url_prefix='/classes')

"""班级管理模块，处理班级相关的所有操作"""


@admin_classes_bp.route('/', methods=['GET'])
def get_classes():
    """
    获取所有班级列表
    
    Returns:
        JSON: 班级列表
    """
    try:
        # 调用服务获取班级列表
        class_service = ClassService()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        classes_data = class_service.get_all_classes(page, per_page)
        
        # 记录成功日志
        current_app.logger.info(f"成功获取班级列表，第{page}页，每页{per_page}条")
        
        return success_response(classes_data)
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"获取班级列表时发生错误: {str(e)}")
        return error_response("获取班级列表失败", 500)


@admin_classes_bp.route('/', methods=['POST'])
def create_class():
    """
    创建班级
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("请求数据不能为空", 400)
        
        class_name = data.get('class_name')
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
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"创建班级时发生错误: {str(e)}")
        return error_response("创建班级失败", 500)


@admin_classes_bp.route('/<int:class_id>', methods=['GET'])
def get_class(class_id):
    """
    根据ID获取班级信息
    
    Args:
        class_id (int): 班级ID
        
    Returns:
        JSON: 班级信息
    """
    try:
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
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"获取班级信息时发生错误: {str(e)}")
        return error_response("获取班级信息失败", 500)


@admin_classes_bp.route('/<int:class_id>', methods=['PUT'])
def update_class(class_id):
    """
    更新班级信息
    
    Args:
        class_id (int): 班级ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("请求数据不能为空", 400)
        
        class_name = data.get('class_name')
        if not class_name:
            return error_response("班级名称不能为空", 400)
        
        # 准备班级数据字典
        class_data = {
            'class_name': class_name
        }
        
        # 调用服务更新班级
        class_service = ClassService()
        result = class_service.update_class(class_id, class_data)
        
        if not result:
            # 记录警告日志
            current_app.logger.warning(f"班级未找到，ID: {class_id}")
            return error_response("班级不存在", 404)
        
        # 记录成功日志
        current_app.logger.info(f"成功更新班级信息，ID: {class_id}")
        
        return success_response({"message": "班级信息更新成功"})
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"更新班级信息时发生错误: {str(e)}")
        return error_response("更新班级信息失败", 500)


@admin_classes_bp.route('/<int:class_id>', methods=['DELETE'])
def delete_class(class_id):
    """
    删除班级
    
    Args:
        class_id (int): 班级ID
        
    Returns:
        JSON: 删除结果
    """
    try:
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
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"删除班级时发生错误: {str(e)}")
        return error_response("删除班级失败", 500)