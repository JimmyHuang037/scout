from apps.services import TeacherService
from apps.utils.helpers import success_response, error_response
from flask import request, current_app, Blueprint

# 创建教师管理蓝图
admin_teachers_bp = Blueprint('admin_teachers', __name__, url_prefix='/teachers')

"""教师管理模块，处理教师相关的所有操作"""


@admin_teachers_bp.route('/', methods=['GET'])
def get_teachers():
    """
    获取所有教师列表
    
    Returns:
        JSON: 教师列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 调用服务获取教师列表
        teacher_service = TeacherService()
        teachers_data = teacher_service.get_all_teachers(page, per_page)
        
        current_app.logger.info('Admin retrieved all teachers')
        return success_response(teachers_data)
    except Exception as e:
        current_app.logger.error(f"Error getting teachers: {str(e)}")
        return error_response('Failed to get teachers', 500)


@admin_teachers_bp.route('/', methods=['POST'])
def create_teacher():
    """
    创建新教师
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response('No data provided', 400)
            
        # 验证必要字段
        if not data.get('teacher_id') or not data.get('teacher_name'):
            return error_response('Missing required fields: teacher_id and teacher_name', 400)
            
        # 调用服务创建教师
        teacher_service = TeacherService()
        result = teacher_service.create_teacher(data)
        
        current_app.logger.info(f"Teacher {data.get('teacher_id')} created successfully")
        return success_response(result, 'Teacher created successfully'), 201
    except Exception as e:
        current_app.logger.error(f"Error creating teacher: {str(e)}")
        return error_response('Failed to create teacher', 500)


@admin_teachers_bp.route('/<string:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    """
    获取单个教师信息
    
    Args:
        teacher_id (str): 教师ID
        
    Returns:
        JSON: 教师信息
    """
    try:
        # 调用服务获取教师信息
        teacher_service = TeacherService()
        teacher = teacher_service.get_teacher_by_id(teacher_id)
        
        if not teacher:
            return error_response('Teacher not found', 404)
            
        current_app.logger.info(f'Admin retrieved teacher: {teacher_id}')
        return success_response(teacher)
    except Exception as e:
        current_app.logger.error(f"Error getting teacher {teacher_id}: {str(e)}")
        return error_response('Failed to get teacher', 500)


@admin_teachers_bp.route('/<string:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    """
    更新教师信息
    
    Args:
        teacher_id (str): 教师ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response('No data provided', 400)
            
        # 调用服务更新教师信息
        teacher_service = TeacherService()
        result = teacher_service.update_teacher(teacher_id, data)
        
        if not result:
            return error_response('Teacher not found', 404)
            
        current_app.logger.info(f'Admin updated teacher: {teacher_id}')
        return success_response({"teacher_id": teacher_id}, "Teacher updated successfully")
    except Exception as e:
        current_app.logger.error(f"Error updating teacher {teacher_id}: {str(e)}")
        return error_response('Failed to update teacher', 500)


@admin_teachers_bp.route('/<string:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    """
    删除教师
    
    Args:
        teacher_id (str): 教师ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 调用服务删除教师
        teacher_service = TeacherService()
        result = teacher_service.delete_teacher(teacher_id)
        
        if not result:
            return error_response('Teacher not found', 404)
            
        current_app.logger.info(f'Admin deleted teacher: {teacher_id}')
        return success_response({"teacher_id": teacher_id}, "Teacher deleted successfully")
    except Exception as e:
        current_app.logger.error(f"Error deleting teacher {teacher_id}: {str(e)}")
        return error_response('Failed to delete teacher', 500)