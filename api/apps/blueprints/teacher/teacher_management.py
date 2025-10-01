"""教师蓝图模块，处理教师相关的所有操作"""
from flask import Blueprint, jsonify, request, current_app, session
from apps.services import TeacherService, ClassService
from apps.services.class_service import ClassNotFoundError
from apps.utils.helpers import success_response, error_response, get_current_user

# 创建教师蓝图
teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')


@teacher_bp.route('/profile', methods=['GET'])
@teacher_bp.route('/<string:teacher_id>/profile', methods=['GET'])
def get_teacher_profile(teacher_id=None):
    """
    获取教师个人资料
    
    Args:
        teacher_id (str, optional): 教师ID，如果不提供则获取当前登录教师的资料
        
    Returns:
        JSON: 教师个人资料
    """
    try:
        # 如果没有提供teacher_id，则使用当前登录用户
        if teacher_id is None:
            current_user = get_current_user()
            if not current_user:
                return error_response('Authentication required', 401)
            teacher_id = current_user['user_id']
            
        teacher_service = TeacherService()
        teacher_data = teacher_service.get_teacher_profile(teacher_id)
        
        if not teacher_data:
            return error_response('Teacher not found', 404)
            
        return success_response(teacher_data)
    except Exception as e:
        current_app.logger.error(f"Error getting teacher profile: {str(e)}")
        return error_response('Failed to get teacher profile', 500)


@teacher_bp.route('/classes', methods=['GET'])
@teacher_bp.route('/<string:teacher_id>/classes', methods=['GET'])
def get_teacher_classes(teacher_id=None):
    """
    获取教师授课班级列表
    
    Args:
        teacher_id (str, optional): 教师ID
        
    Returns:
        JSON: 教师授课班级列表
    """
    try:
        # 检查是否提供了teacher_id
        if teacher_id is None:
            return error_response('Teacher ID is required', 400)
            
        teacher_service = TeacherService()
        classes_data = teacher_service.get_teacher_classes(teacher_id)
        
        return success_response(classes_data)
    except Exception as e:
        current_app.logger.error(f"Error getting teacher classes: {str(e)}")
        return error_response('Failed to get teacher classes', 500)


@teacher_bp.route('/classes/students', methods=['GET'])
@teacher_bp.route('/<string:teacher_id>/classes/students', methods=['GET'])
def get_teacher_all_classes_students(teacher_id=None):
    """
    获取教师所有班级的学生列表
    
    Args:
        teacher_id (str, optional): 教师ID
        
    Returns:
        JSON: 教师所有班级的学生列表
    """
    try:
        # 检查是否提供了teacher_id
        if teacher_id is None:
            return error_response('Teacher ID is required', 400)
            
        teacher_service = TeacherService()
        students_data = teacher_service.get_all_classes_students(teacher_id)
        
        return success_response(students_data)
    except Exception as e:
        current_app.logger.error(f"Error getting teacher all classes students: {str(e)}")
        return error_response('Failed to get students', 500)


@teacher_bp.route('/classes/<int:class_id>/students', methods=['GET'])
@teacher_bp.route('/<string:teacher_id>/classes/<int:class_id>/students', methods=['GET'])
def get_class_students(class_id, teacher_id=None):
    """
    获取班级学生列表
    
    Args:
        teacher_id (str, optional): 教师ID，如果不提供则获取当前登录教师
        class_id (int): 班级ID
        
    Returns:
        JSON: 班级学生列表
    """
    try:
        # 如果没有提供teacher_id，则使用当前登录用户
        if teacher_id is None:
            current_user = get_current_user()
            teacher_id = current_user['user_id']
            
        class_service = ClassService()
        students_data = class_service.get_students_by_class(class_id, teacher_id)
        
        return success_response(students_data)
    except ClassNotFoundError as e:
        return error_response(str(e), 404)
    except Exception as e:
        current_app.logger.error(f"Error getting class students: {str(e)}")
        return error_response('Failed to get class students'), 500