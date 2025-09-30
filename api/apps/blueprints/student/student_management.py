"""学生蓝图模块，处理学生相关的所有操作"""
from flask import Blueprint, jsonify, request, current_app, session
from apps.services import StudentService
from apps.utils.helpers import success_response, error_response, auth_required, role_required, get_current_user

# 创建学生蓝图
student_bp = Blueprint('student', __name__, url_prefix='/api/student')


@student_bp.route('/profile', methods=['GET'])
@auth_required
@role_required('student')
def get_student_profile():
    """
    获取当前学生个人资料
    
    Returns:
        JSON: 学生个人资料
    """
    try:
        current_user = get_current_user()
        student_id = current_user['user_id']
        
        student_service = StudentService()
        student_data = student_service.get_student_profile(student_id)
        
        if not student_data:
            return error_response('Student not found'), 404
            
        return success_response(student_data)
    except Exception as e:
        current_app.logger.error(f"Error getting student profile: {str(e)}")
        return error_response('Failed to get student profile'), 500


@student_bp.route('/scores', methods=['GET'])
@auth_required
@role_required('student')
def get_student_scores():
    """
    获取当前学生成绩列表
    
    Returns:
        JSON: 学生成绩列表
    """
    try:
        current_user = get_current_user()
        student_id = current_user['user_id']
        
        student_service = StudentService()
        scores_data = student_service.get_student_scores(student_id)
        
        return success_response(scores_data)
    except Exception as e:
        current_app.logger.error(f"Error getting student scores: {str(e)}")
        return error_response('Failed to get student scores'), 500


@student_bp.route('/exams', methods=['GET'])
@auth_required
@role_required('student')
def get_student_exams():
    """
    获取当前学生参加的考试列表
    
    Returns:
        JSON: 学生考试列表
    """
    try:
        current_user = get_current_user()
        student_id = current_user['user_id']
        
        student_service = StudentService()
        exams_data = student_service.get_student_exams(student_id)
        
        return success_response(exams_data)
    except Exception as e:
        current_app.logger.error(f"Error getting student exams: {str(e)}")
        return error_response('Failed to get student exams'), 500


@student_bp.route('/exams/<int:exam_id>/scores', methods=['GET'])
@auth_required
@role_required('student')
def get_student_exam_scores(exam_id):
    """
    获取当前学生某次考试的成绩详情
    
    Args:
        exam_id (int): 考试ID
        
    Returns:
        JSON: 考试成绩详情
    """
    try:
        current_user = get_current_user()
        student_id = current_user['user_id']
        
        student_service = StudentService()
        scores_data = student_service.get_student_exam_score(student_id, exam_id)
        
        return success_response(scores_data)
    except Exception as e:
        current_app.logger.error(f"Error getting student exam scores: {str(e)}")
        return error_response('Failed to get student exam scores'), 500