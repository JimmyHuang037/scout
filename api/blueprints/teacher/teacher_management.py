"""教师管理模块，处理教师查看教师信息的操作"""
from flask import jsonify, request, session, current_app
from services import TeacherService
from utils.helpers import success_response, error_response, auth_required, role_required


@auth_required
@role_required('teacher')
def get_teachers():
    """
    获取教师列表（教师可访问）
    
    Returns:
        JSON: 教师列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取教师列表
        teachers_data = TeacherService().get_all_teachers(page, per_page)
        
        current_app.logger.info('Teacher retrieved teacher list')
        return success_response(teachers_data)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve teachers: {str(e)}')
        return error_response("获取教师列表失败", 500)


@auth_required
@role_required('teacher')
def get_teacher(teacher_id):
    """
    获取单个教师信息（教师可访问）
    
    Args:
        teacher_id (str): 教师ID
        
    Returns:
        JSON: 教师信息
    """
    try:
        # 尝试将字符串类型的教师ID转换为整数类型
        try:
            teacher_id_int = int(teacher_id)
        except ValueError:
            return error_response("教师ID格式不正确", 400)
        
        # 获取教师信息
        teacher = TeacherService().get_teacher_by_id(teacher_id_int)
        if not teacher:
            return error_response("教师不存在", 404)
        
        current_app.logger.info(f'Teacher retrieved teacher: {teacher_id_int}')
        return success_response(teacher)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve teacher {teacher_id}: {str(e)}')
        return error_response("获取教师信息失败", 500)