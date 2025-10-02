from flask import Blueprint, request, current_app
from apps.services import TeacherClassService
from apps.utils.helpers import success_response, error_response, validate_json_input
from apps.utils.decorators import handle_exceptions


# 教师班级关联管理蓝图
admin_teacher_classes_bp = Blueprint('admin_teacher_classes', __name__, url_prefix='/teacher_classes')


@handle_exceptions
def get_teacher_classes():
    """
    获取所有教师班级关联列表
    
    Returns:
        JSON: 教师班级关联列表
    """
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 调用服务获取教师班级关联列表
    teacher_class_service = TeacherClassService()
    teacher_classes_data = teacher_class_service.get_all_teacher_classes(page, per_page)
    
    # 记录成功日志
    current_app.logger.info(f"成功获取教师班级关联列表，第{page}页，每页{per_page}条")
    
    return success_response(teacher_classes_data)


@handle_exceptions
def create_teacher_class():
    """
    创建教师班级关联
    
    Returns:
        JSON: 创建结果
    """
    # 验证请求数据
    data, error = validate_json_input(['teacher_id', 'class_id'])
    if error:
        return error
    
    teacher_id = data.get('teacher_id')
    class_id = data.get('class_id')
    
    # 调用服务创建教师班级关联
    teacher_class_service = TeacherClassService()
    result = teacher_class_service.create_teacher_class(teacher_id, class_id)
    
    # 记录成功日志
    current_app.logger.info(f"成功创建教师班级关联: 教师{teacher_id}-班级{class_id}")
    return success_response({"message": "教师班级关联创建成功"}, 201)


@handle_exceptions
def get_teacher_class(teacher_id: int, class_id: int):
    """
    根据教师ID和班级ID获取教师班级关联信息
    
    Args:
        teacher_id (int): 教师ID
        class_id (int): 班级ID
        
    Returns:
        JSON: 教师班级关联信息
    """
    # 调用服务获取教师班级关联信息
    teacher_class_service = TeacherClassService()
    teacher_class_data = teacher_class_service.get_teacher_class(teacher_id, class_id)
    
    if not teacher_class_data:
        # 记录警告日志
        current_app.logger.warning(f"教师班级关联未找到，教师ID: {teacher_id}，班级ID: {class_id}")
        return error_response("教师班级关联不存在", 404)
    
    # 记录成功日志
    current_app.logger.info(f"成功获取教师班级关联信息，教师ID: {teacher_id}，班级ID: {class_id}")
    
    return success_response(teacher_class_data)


@handle_exceptions
def update_teacher_class(teacher_id: int, class_id: int):
    """
    更新教师班级关联信息
    
    Args:
        teacher_id (int): 教师ID
        class_id (int): 班级ID
        
    Returns:
        JSON: 更新结果
    """
    # 验证请求数据
    data, error = validate_json_input(required_fields=[], allow_empty=True)
    if error:
        return error
    
    new_teacher_id = data.get('new_teacher_id')
    
    # 调用服务更新教师班级关联
    teacher_class_service = TeacherClassService()
    result = teacher_class_service.update_teacher_class(teacher_id, class_id, new_teacher_id)
    
    if not result:
        # 记录警告日志
        current_app.logger.warning(f"教师班级关联未找到，教师ID: {teacher_id}，班级ID: {class_id}")
        return error_response("教师班级关联不存在", 404)
    
    # 记录成功日志
    current_app.logger.info(f"成功更新教师班级关联信息，教师ID: {teacher_id}，班级ID: {class_id}")
    
    return success_response({"message": "教师班级关联信息更新成功"})


@handle_exceptions
def delete_teacher_class(teacher_id: int, class_id: int):
    """
    删除教师班级关联
    
    Args:
        teacher_id (int): 教师ID
        class_id (int): 班级ID
        
    Returns:
        JSON: 删除结果
    """
    # 调用服务删除教师班级关联
    teacher_class_service = TeacherClassService()
    result = teacher_class_service.delete_teacher_class(teacher_id, class_id)
    
    if not result:
        # 记录警告日志
        current_app.logger.warning(f"教师班级关联未找到，教师ID: {teacher_id}，班级ID: {class_id}")
        return error_response("教师班级关联不存在", 404)
    
    # 记录成功日志
    current_app.logger.info(f"成功删除教师班级关联，教师ID: {teacher_id}，班级ID: {class_id}")
    
    return success_response({"message": "教师班级关联删除成功"})


# 注册路由
admin_teacher_classes_bp.add_url_rule('/', view_func=get_teacher_classes, methods=['GET'])
admin_teacher_classes_bp.add_url_rule('/', view_func=create_teacher_class, methods=['POST'])
admin_teacher_classes_bp.add_url_rule('/<int:teacher_id>/<int:class_id>', view_func=get_teacher_class, methods=['GET'])
admin_teacher_classes_bp.add_url_rule('/<int:teacher_id>/<int:class_id>', view_func=update_teacher_class, methods=['PUT'])
admin_teacher_classes_bp.add_url_rule('/<int:teacher_id>/<int:class_id>', view_func=delete_teacher_class, methods=['DELETE'])