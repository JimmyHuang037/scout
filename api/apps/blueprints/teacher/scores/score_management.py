"""成绩管理模块，处理成绩相关的所有操作"""
from flask import Blueprint, request, jsonify, current_app, session
from apps.utils.auth import role_required
from apps.utils.helpers import success_response, error_response
from apps.services import ScoreService

teacher_score_bp = Blueprint('teacher_score_bp', __name__)


@teacher_score_bp.route('/scores', methods=['GET'])
@role_required('teacher')
def get_scores():
    """
    获取成绩列表
    
    Returns:
        JSON: 成绩列表
    """
    try:
        # 获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return error_response("未授权访问", 401)
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 创建成绩服务实例并获取成绩列表
        score_service = ScoreService()
        scores_data = score_service.get_all_scores(page, per_page)
        
        current_app.logger.info(f"Teacher {current_teacher_id} retrieved scores list")
        return success_response(scores_data, "获取成绩列表成功")
    
    except Exception as e:
        current_app.logger.error(f"Failed to retrieve scores: {str(e)}")
        return error_response("获取成绩列表失败", 500)


@teacher_score_bp.route('/scores', methods=['POST'])
@role_required('teacher')
def create_score():
    """
    创建成绩记录
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return error_response("未授权访问", 401)
        
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 创建成绩服务实例并调用create_score方法
        score_service = ScoreService()
        score = score_service.create_score(data)
        
        current_app.logger.info(f"Teacher {current_teacher_id} created score: {score}")
        return success_response({"score_id": score}, "成绩创建成功"), 201
    
    except Exception as e:
        current_app.logger.error(f"Failed to create score: {str(e)}")
        return error_response("创建成绩失败", 500)


@teacher_score_bp.route('/scores/<int:score_id>', methods=['PUT'])
@role_required('teacher')
def update_score(score_id):
    """
    更新成绩记录
    
    Args:
        score_id (int): 成绩ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return error_response("未授权访问", 401)
        
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 创建成绩服务实例并更新成绩
        score_service = ScoreService()
        result = score_service.update_score(score_id, data)
        
        current_app.logger.info(f"Teacher {current_teacher_id} updated score {score_id}")
        return success_response(result, "成绩更新成功")
    
    except Exception as e:
        current_app.logger.error(f"Failed to update score {score_id}: {str(e)}")
        return error_response("成绩更新失败", 500)


@teacher_score_bp.route('/scores/<int:score_id>', methods=['DELETE'])
@role_required('teacher')
def delete_score(score_id):
    """
    删除成绩记录
    
    Args:
        score_id (int): 成绩ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return error_response("未授权访问", 401)
        
        # 创建成绩服务实例并删除成绩
        score_service = ScoreService()
        result = score_service.delete_score(score_id)
        
        current_app.logger.info(f"Teacher {current_teacher_id} deleted score {score_id}")
        return success_response(result, "成绩删除成功")
    
    except Exception as e:
        current_app.logger.error(f"Failed to delete score {score_id}: {str(e)}")
        return error_response("成绩删除失败", 500)


@teacher_score_bp.route('/exams/<int:exam_id>/scores', methods=['GET'])
@role_required('teacher')
def get_exam_scores(exam_id):
    """
    获取考试成绩列表
    
    Args:
        exam_id (int): 考试ID
        
    Returns:
        JSON: 考试成绩列表
    """
    try:
        # 获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return error_response("未授权访问", 401)
        
        # 创建成绩服务实例并获取考试成绩列表
        score_service = ScoreService()
        scores_data = score_service.get_exam_scores(exam_id, current_teacher_id)
        
        current_app.logger.info(f"Teacher {current_teacher_id} retrieved scores for exam {exam_id}")
        return success_response(scores_data, "获取考试成绩列表成功")
    
    except Exception as e:
        current_app.logger.error(f"Failed to retrieve scores for exam {exam_id}: {str(e)}")
        return error_response("获取考试成绩列表失败", 500)