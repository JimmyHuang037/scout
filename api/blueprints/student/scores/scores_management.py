"""学生成绩管理模块"""
from flask import jsonify, request, session
from api.services import ScoreService
from api.utils.logger import app_logger
from api.utils.helpers import success_response, error_response, require_auth


def get_my_scores():
    """获取当前学生成绩"""
    try:
        # 检查认证
        auth_error = require_auth()
        if auth_error:
            return auth_error
        
        # 从session中获取当前学生ID
        current_student_id = session.get('user_id')
        
        # 获取筛选参数
        subject_id = request.args.get('subject_id')
        exam_type_id = request.args.get('exam_type_id')
        
        # 使用成绩服务获取成绩列表
        score_service = ScoreService()
        scores = score_service.get_scores(student_id=current_student_id, subject_id=subject_id, exam_type_id=exam_type_id)
        
        app_logger.info(f"Student {current_student_id} retrieved their scores")
        return success_response(scores)
        
    except Exception as e:
        app_logger.error(f"Failed to fetch scores: {str(e)}")
        return error_response(f'Failed to fetch scores: {str(e)}'), 500