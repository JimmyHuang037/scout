from apps.services import TeacherClassService
from apps.utils.helpers import success_response, error_response
from flask import request, current_app, Blueprint

# 创建教师班级关联管理蓝图
admin_teacher_classes_bp = Blueprint('admin_teacher_classes', __name__, url_prefix='/teacher_classes')

"""教师班级关联管理模块，处理教师和班级关联相关的所有操作"""


@admin_teacher_classes_bp.route('/', methods=['POST'])
def create_teacher_class():
    """
    创建教师班级关联
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("请求数据不能为空", 400)
        
        teacher_id = data.get('teacher_id')
        class_id = data.get('class_id')
        
        # 检查必填字段
        if not teacher_id or not class_id:
            return error_response("教师ID和班级ID不能为空", 400)
        
        # 调用服务创建教师班级关联
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.create_teacher_class(teacher_id, class_id)
        
        # 记录成功日志
        current_app.logger.info(f"成功创建教师班级关联: 教师{teacher_id}-班级{class_id}")
        
        return success_response(result, 201)
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"创建教师班级关联时发生错误: {str(e)}")
        return error_response("创建教师班级关联失败", 500)


@admin_teacher_classes_bp.route('/', methods=['GET'])
def get_teacher_classes():
    """
    获取所有教师班级关联列表
    
    Returns:
        JSON: 教师班级关联列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 调用服务获取教师班级关联列表
        teacher_class_service = TeacherClassService()
        teacher_classes_data = teacher_class_service.get_all_teacher_classes(page, per_page)
        
        # 记录成功日志
        current_app.logger.info(f"成功获取教师班级关联列表，第{page}页，每页{per_page}条")
        
        return success_response(teacher_classes_data)
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"获取教师班级关联列表时发生错误: {str(e)}")
        return error_response("获取教师班级关联列表失败", 500)


@admin_teacher_classes_bp.route('/<int:teacher_id>/<int:class_id>', methods=['GET'])
def get_teacher_class(teacher_id, class_id):
    """
    根据教师ID和班级ID获取教师班级关联信息
    
    Args:
        teacher_id (int): 教师ID
        class_id (int): 班级ID
        
    Returns:
        JSON: 教师班级关联信息
    """
    try:
        # 调用服务获取教师班级关联信息
        teacher_class_service = TeacherClassService()
        teacher_class_data = teacher_class_service.get_teacher_class_by_id(teacher_id, class_id)
        
        if not teacher_class_data:
            # 记录警告日志
            current_app.logger.warning(f"教师班级关联未找到，教师ID: {teacher_id}, 班级ID: {class_id}")
            return error_response("教师班级关联不存在", 404)
        
        # 记录成功日志
        current_app.logger.info(f"成功获取教师班级关联信息，教师ID: {teacher_id}, 班级ID: {class_id}")
        
        return success_response(teacher_class_data)
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"获取教师班级关联信息时发生错误: {str(e)}")
        return error_response("获取教师班级关联信息失败", 500)


@admin_teacher_classes_bp.route('/<int:teacher_id>/<int:class_id>', methods=['PUT'])
def update_teacher_class(teacher_id, class_id):
    """
    更新教师班级关联信息
    
    Args:
        teacher_id (int): 教师ID
        class_id (int): 班级ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("请求数据不能为空", 400)
        
        new_teacher_id = data.get('teacher_id')
        new_class_id = data.get('class_id')
        
        # 检查必填字段
        if not new_teacher_id:
            return error_response("教师ID不能为空", 400)
        
        # 如果提供了新的class_id，则需要确保它与原class_id相同（因为服务层不支持修改class_id）
        if new_class_id and new_class_id != class_id:
            return error_response("不支持修改班级ID", 400)
        
        # 调用服务更新教师班级关联
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.update_teacher_class(teacher_id, class_id, new_teacher_id)
        
        if not result:
            # 记录警告日志
            current_app.logger.warning(f"教师班级关联未找到，教师ID: {teacher_id}, 班级ID: {class_id}")
            return error_response("教师班级关联不存在", 404)
        
        # 记录成功日志
        current_app.logger.info(f"成功更新教师班级关联信息，原教师ID: {teacher_id}, 原班级ID: {class_id}")
        
        return success_response({"message": "教师班级关联更新成功"})
        
    except ValueError as e:
        # 处理教师不存在的情况
        current_app.logger.warning(f"更新教师班级关联时发生错误: {str(e)}")
        return error_response(str(e), 400)
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"更新教师班级关联信息时发生错误: {str(e)}")
        return error_response("更新教师班级关联信息失败", 500)


@admin_teacher_classes_bp.route('/<int:teacher_id>/<int:class_id>', methods=['DELETE'])
def delete_teacher_class(teacher_id, class_id):
    """
    删除教师班级关联
    
    Args:
        teacher_id (int): 教师ID
        class_id (int): 班级ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 调用服务删除教师班级关联
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.delete_teacher_class(teacher_id, class_id)
        
        if not result:
            # 记录警告日志
            current_app.logger.warning(f"教师班级关联未找到，教师ID: {teacher_id}, 班级ID: {class_id}")
            return error_response("教师班级关联不存在", 404)
        
        # 记录成功日志
        current_app.logger.info(f"成功删除教师班级关联，教师ID: {teacher_id}, 班级ID: {class_id}")
        
        return success_response({"message": "教师班级关联删除成功"})
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"删除教师班级关联时发生错误: {str(e)}")
        return error_response("删除教师班级关联失败", 500)