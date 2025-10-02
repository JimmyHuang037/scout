from flask import Blueprint, request, current_app
from apps.services.student_service import StudentService
from apps.utils.decorators import handle_exceptions
from apps.utils.responses import success_response, error_response
from apps.utils.validation import validate_json_input


# 学生管理蓝图
admin_students_bp = Blueprint('admin_students', __name__)


@handle_exceptions
def get_students():
    """
    获取所有学生列表
    
    Returns:
        JSON: 学生列表
    """
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 调用服务获取学生列表
    student_service = StudentService()
    students_data = student_service.get_all_students(page, per_page)
    
    # 记录成功日志
    current_app.logger.info(f"成功获取学生列表，第{page}页，每页{per_page}条")
    
    return success_response(students_data)


@handle_exceptions
def create_student():
    """
    创建学生
    
    Returns:
        JSON: 创建结果
    """
    # 验证请求数据
    data, error = validate_json_input(['student_id', 'student_name', 'class_id'])
    if error:
        return error
    
    student_id = data.get('student_id')
    student_name = data.get('student_name')
    class_id = data.get('class_id')
    password = data.get('password')
    
    # 准备学生数据字典
    student_data = {
        'student_id': student_id,
        'student_name': student_name,
        'class_id': class_id,
        'password': password
    }
    
    # 调用服务创建学生
    student_service = StudentService()
    result = student_service.create_student(student_data)
    
    # 记录成功日志
    current_app.logger.info(f"成功创建学生: {student_name}")
    
    return success_response(result, 201)


@handle_exceptions
def get_student(student_id: str):
    """
    根据ID获取学生信息
    
    Args:
        student_id (str): 学生ID
        
    Returns:
        JSON: 学生信息
    """
    # 调用服务获取学生信息
    student_service = StudentService()
    student_data = student_service.get_student_by_id(student_id)
    
    if not student_data:
        # 记录警告日志
        current_app.logger.warning(f"学生未找到，ID: {student_id}")
        return error_response("学生不存在", 404)
    
    # 记录成功日志
    current_app.logger.info(f"成功获取学生信息，ID: {student_id}")
    
    return success_response(student_data)


@handle_exceptions
def update_student(student_id: str):
    """
    更新学生信息
    
    Args:
        student_id (str): 学生ID
        
    Returns:
        JSON: 更新结果
    """
    # 验证请求数据并获取数据
    data, error = validate_json_input(required_fields=[], allow_empty=True)
    if error:
        return error
    
    # 准备更新数据字典
    update_data = {}
    if 'student_name' in data:
        update_data['student_name'] = data['student_name']
    if 'class_id' in data:
        update_data['class_id'] = data['class_id']
    if 'password' in data:
        update_data['password'] = data['password']
        
    # 如果没有任何更新字段
    if not update_data:
        return error_response("请提供至少一个要更新的字段", 400)
    
    # 调用服务更新学生
    student_service = StudentService()
    result = student_service.update_student(student_id, update_data)
    
    if not result:
        # 记录警告日志
        current_app.logger.warning(f"学生未找到，ID: {student_id}")
        return error_response("学生不存在", 404)
    
    # 记录成功日志
    current_app.logger.info(f"成功更新学生信息，ID: {student_id}")
    
    return success_response({"message": "学生信息更新成功"})


@handle_exceptions
def delete_student(student_id: str):
    """
    删除学生
    
    Args:
        student_id (str): 学生ID
        
    Returns:
        JSON: 删除结果
    """
    # 调用服务删除学生
    student_service = StudentService()
    result = student_service.delete_student(student_id)
    
    if not result:
        # 记录警告日志
        current_app.logger.warning(f"学生未找到，ID: {student_id}")
        return error_response("学生不存在", 404)
    
    # 记录成功日志
    current_app.logger.info(f"成功删除学生，ID: {student_id}")
    
    return success_response({"message": "学生删除成功"})


# 注册路由
admin_students_bp.add_url_rule('/', view_func=get_students, methods=['GET'])
admin_students_bp.add_url_rule('/', view_func=create_student, methods=['POST'])
admin_students_bp.add_url_rule('/<string:student_id>', view_func=get_student, methods=['GET'])
admin_students_bp.add_url_rule('/<string:student_id>', view_func=update_student, methods=['PUT'])
admin_students_bp.add_url_rule('/<string:student_id>', view_func=delete_student, methods=['DELETE'])