"""教师蓝图模块，处理教师相关的所有操作"""
from flask import Blueprint, jsonify, request, current_app, session
from apps.services import TeacherService, ClassService, SubjectService, ExamService, ScoreService
from apps.utils.helpers import success_response, error_response, auth_required, role_required, get_current_user

# 创建教师蓝图
teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')


@teacher_bp.route('/profile', methods=['GET'])
@teacher_bp.route('/<string:teacher_id>/profile', methods=['GET'])
@auth_required
@role_required('teacher')
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
            teacher_id = current_user['user_id']
            
        teacher_service = TeacherService()
        teacher_data = teacher_service.get_teacher_profile(teacher_id)
        
        if not teacher_data:
            return error_response('Teacher not found'), 404
            
        return success_response(teacher_data)
    except Exception as e:
        current_app.logger.error(f"Error getting teacher profile: {str(e)}")
        return error_response('Failed to get teacher profile'), 500


@teacher_bp.route('/classes', methods=['GET'])
@teacher_bp.route('/<string:teacher_id>/classes', methods=['GET'])
@auth_required
@role_required('teacher')
def get_teacher_classes(teacher_id=None):
    """
    获取教师授课班级列表
    
    Args:
        teacher_id (str, optional): 教师ID，如果不提供则获取当前登录教师的班级
        
    Returns:
        JSON: 教师授课班级列表
    """
    try:
        # 如果没有提供teacher_id，则使用当前登录用户
        if teacher_id is None:
            current_user = get_current_user()
            teacher_id = current_user['user_id']
            
        teacher_service = TeacherService()
        classes_data = teacher_service.get_teacher_classes(teacher_id)
        
        return success_response(classes_data)
    except Exception as e:
        current_app.logger.error(f"Error getting teacher classes: {str(e)}")
        return error_response('Failed to get teacher classes'), 500


@teacher_bp.route('/exams', methods=['GET'])
@teacher_bp.route('/<string:teacher_id>/exams', methods=['GET'])
@auth_required
@role_required('teacher')
def get_teacher_exams(teacher_id=None):
    """
    获取教师创建的考试列表
    
    Args:
        teacher_id (str, optional): 教师ID，如果不提供则获取当前登录教师的考试
        
    Returns:
        JSON: 教师创建的考试列表
    """
    try:
        # 如果没有提供teacher_id，则使用当前登录用户
        if teacher_id is None:
            current_user = get_current_user()
            teacher_id = current_user['user_id']
            
        teacher_service = TeacherService()
        exams_data = teacher_service.get_teacher_exams(teacher_id)
        
        return success_response(exams_data)
    except Exception as e:
        current_app.logger.error(f"Error getting teacher exams: {str(e)}")
        return error_response('Failed to get teacher exams'), 500


@teacher_bp.route('/classes/<int:class_id>/subjects/<int:subject_id>/exams', methods=['POST'])
@teacher_bp.route('/<string:teacher_id>/classes/<int:class_id>/subjects/<int:subject_id>/exams', methods=['POST'])
@auth_required
@role_required('teacher')
def create_exam(class_id, subject_id, teacher_id=None):
    """
    为指定班级和科目创建考试
    
    Args:
        teacher_id (str, optional): 教师ID，如果不提供则使用当前登录教师
        class_id (int): 班级ID
        subject_id (int): 科目ID
        
    Returns:
        JSON: 创建的考试信息
    """
    try:
        # 如果没有提供teacher_id，则使用当前登录用户
        if teacher_id is None:
            current_user = get_current_user()
            teacher_id = current_user['user_id']
            
        data = request.get_json()
        if not data:
            return error_response('No data provided'), 400
            
        # 添加教师ID和班级ID到数据中
        data['teacher_id'] = teacher_id
        data['class_id'] = class_id
        data['subject_id'] = subject_id
        
        exam_service = ExamService()
        exam_data = exam_service.create_exam(data)
        
        return success_response(exam_data, 'Exam created successfully'), 201
    except Exception as e:
        current_app.logger.error(f"Error creating exam: {str(e)}")
        return error_response('Failed to create exam'), 500


@teacher_bp.route('/exams/<int:exam_id>/scores', methods=['POST'])
@teacher_bp.route('/<string:teacher_id>/exams/<int:exam_id>/scores', methods=['POST'])
@auth_required
@role_required('teacher')
def enter_exam_scores(exam_id, teacher_id=None):
    """
    录入考试成绩
    
    Args:
        teacher_id (str, optional): 教师ID，如果不提供则使用当前登录教师
        exam_id (int): 考试ID
        
    Returns:
        JSON: 录入结果
    """
    try:
        # 如果没有提供teacher_id，则使用当前登录用户
        if teacher_id is None:
            current_user = get_current_user()
            teacher_id = current_user['user_id']
            
        data = request.get_json()
        if not data:
            return error_response('No data provided'), 400
            
        # 这里虽然接收了teacher_id，但在enter_scores服务中可能不需要直接使用
        # 因为成绩录入主要是基于exam_id和学生分数数据
        score_service = ScoreService()
        result = score_service.enter_scores(exam_id, data)
        
        return success_response(result, 'Scores entered successfully')
    except Exception as e:
        current_app.logger.error(f"Error entering exam scores: {str(e)}")
        return error_response('Failed to enter exam scores'), 500


@teacher_bp.route('/exams/<int:exam_id>/scores', methods=['GET'])
@teacher_bp.route('/<string:teacher_id>/exams/<int:exam_id>/scores', methods=['GET'])
@auth_required
@role_required('teacher')
def get_exam_scores(exam_id, teacher_id=None):
    """
    获取考试成绩
    
    Args:
        teacher_id (str, optional): 教师ID，如果不提供则使用当前登录教师
        exam_id (int): 考试ID
        
    Returns:
        JSON: 考试成绩
    """
    try:
        # 如果没有提供teacher_id，则使用当前登录用户
        if teacher_id is None:
            current_user = get_current_user()
            teacher_id = current_user['user_id']
            
        score_service = ScoreService()
        scores_data = score_service.get_exam_scores(exam_id)
        
        return success_response(scores_data)
    except Exception as e:
        current_app.logger.error(f"Error getting exam scores: {str(e)}")
        return error_response('Failed to get exam scores'), 500


@teacher_bp.route('/exams/<int:exam_id>/analysis', methods=['GET'])
@teacher_bp.route('/<string:teacher_id>/exams/<int:exam_id>/analysis', methods=['GET'])
@auth_required
@role_required('teacher')
def analyze_exam_performance(exam_id, teacher_id=None):
    """
    分析考试表现
    
    Args:
        teacher_id (str, optional): 教师ID，如果不提供则使用当前登录教师
        exam_id (int): 考试ID
        
    Returns:
        JSON: 考试表现分析
    """
    try:
        # 如果没有提供teacher_id，则使用当前登录用户
        if teacher_id is None:
            current_user = get_current_user()
            teacher_id = current_user['user_id']
            
        exam_service = ExamService()
        analysis_data = exam_service.analyze_exam_performance(exam_id)
        
        return success_response(analysis_data)
    except Exception as e:
        current_app.logger.error(f"Error analyzing exam performance: {str(e)}")
        return error_response('Failed to analyze exam performance'), 500