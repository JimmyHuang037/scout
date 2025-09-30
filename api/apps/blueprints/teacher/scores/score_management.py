"""成绩管理模块，处理成绩相关的所有操作"""
from flask import Blueprint, request, jsonify, current_app, session
from apps.utils.helpers import success_response, error_response
from apps.services import ScoreService

teacher_score_bp = Blueprint('teacher_score_bp', __name__)


def get_scores(teacher_id):
    """
    获取成绩列表
    
    Args:
        teacher_id (string): 教师ID
        
    Returns:
        JSON: 成绩列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 创建成绩服务实例并获取成绩列表
        score_service = ScoreService()
        scores_data = score_service.get_teacher_scores(teacher_id, page, per_page)
        
        current_app.logger.info(f"Teacher {teacher_id} retrieved scores list")
        return success_response(scores_data)
    
    except Exception as e:
        current_app.logger.error(f"Failed to retrieve scores: {str(e)}")
        return error_response("获取成绩列表失败")


def create_score(teacher_id):
    """
    创建成绩记录
    
    Args:
        teacher_id (string): 教师ID
        
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 创建成绩服务实例并调用create_score方法
        score_service = ScoreService()
        score = score_service.create_score(data)
        
        current_app.logger.info(f"Teacher {teacher_id} created score: {score}")
        return success_response({"score_id": score}), 201
    
    except Exception as e:
        current_app.logger.error(f"Failed to create score: {str(e)}")
        return error_response("创建成绩失败", 500)


def update_score(teacher_id, score_id):
    """
    更新成绩记录
    
    Args:
        teacher_id (string): 教师ID
        score_id (int): 成绩ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 创建成绩服务实例并更新成绩
        score_service = ScoreService()
        result = score_service.update_score(score_id, data)
        
        current_app.logger.info(f"Teacher {teacher_id} updated score {score_id}")
        return success_response(result)
    
    except Exception as e:
        current_app.logger.error(f"Failed to update score {score_id}: {str(e)}")
        return error_response("成绩更新失败", 500)


def delete_score(teacher_id, score_id):
    """
    删除成绩记录
    
    Args:
        teacher_id (string): 教师ID
        score_id (int): 成绩ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 创建成绩服务实例并删除成绩
        score_service = ScoreService()
        result = score_service.delete_score(score_id)
        
        current_app.logger.info(f"Teacher {teacher_id} deleted score {score_id}")
        return success_response(result)
    
    except Exception as e:
        current_app.logger.error(f"Failed to delete score {score_id}: {str(e)}")
        return error_response("成绩删除失败", 500)