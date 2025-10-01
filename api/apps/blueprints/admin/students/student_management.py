from apps.services import StudentService
from apps.utils.helpers import success_response, error_response
from flask import request, current_app, Blueprint

# 创建学生管理蓝图
admin_students_bp = Blueprint('admin_students', __name__, url_prefix='/students')

"""学生管理模块，处理学生相关的所有操作"""


@admin_students_bp.route('/', methods=['GET'])
def get_students():
    """
    获取所有学生列表
    
    Returns:
        JSON: 学生列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取学生列表
        students_data = StudentService().get_all_students(page, per_page)
        
        current_app.logger.info('Admin retrieved all students')
        return success_response(students_data)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve students: {str(e)}')
        return error_response("获取学生列表失败", 500)


@admin_students_bp.route('/', methods=['POST'])
def create_student():
    """
    创建学生
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 调用服务创建学生
        student_service = StudentService()
        result = student_service.create_student(data)
        
        if not result:
            return error_response("创建学生失败", 400)
            
        student_id = data.get('student_id')
        current_app.logger.info(f'Admin created student: {student_id}')
        return success_response(result, "学生创建成功"), 201
    
    except Exception as e:
        current_app.logger.error(f'Failed to create student: {str(e)}')
        return error_response("创建学生失败", 500)


@admin_students_bp.route('/<string:student_id>', methods=['GET'])
def get_student(student_id):
    """
    获取单个学生信息
    
    Args:
        student_id (int): 学生ID
        
    Returns:
        JSON: 学生信息
    """
    try:
        # 获取学生信息
        student = StudentService().get_student_by_id(student_id)
        if not student:
            return error_response("学生不存在", 404)
        
        current_app.logger.info(f'Admin retrieved student: {student_id}')
        return success_response(student)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve student {student_id}: {str(e)}')
        return error_response("获取学生信息失败", 500)


@admin_students_bp.route('/<string:student_id>', methods=['PUT'])
def update_student(student_id):
    """
    更新学生信息
    
    Args:
        student_id (int): 学生ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 更新学生
        result = StudentService().update_student(student_id, data)
        
        if not result:
            return error_response("学生不存在", 404)
        
        current_app.logger.info(f'Admin updated student: {student_id}')
        return success_response({"student_id": student_id}, "学生更新成功")
    
    except Exception as e:
        current_app.logger.error(f'Failed to update student {student_id}: {str(e)}')
        return error_response("更新学生失败", 500)


@admin_students_bp.route('/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """
    删除学生
    
    Args:
        student_id (int): 学生ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 删除学生
        result = StudentService().delete_student(student_id)
        if not result:
            return error_response("学生不存在", 404)
        
        current_app.logger.info(f'Admin deleted student: {student_id}')
        return success_response({"student_id": student_id}, "学生删除成功")
    
    except Exception as e:
        current_app.logger.error(f'Failed to delete student {student_id}: {str(e)}')
        return error_response("删除学生失败", 500)