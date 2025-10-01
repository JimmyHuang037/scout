from apps.services.score_service import ScoreService
from apps.utils.helpers import success_response, error_response
from flask import Blueprint, request, jsonify, current_app
"""学生成绩管理模块"""

student_scores_bp = Blueprint('student_scores_bp', __name__)

@student_scores_bp.route('/<string:student_id>/scores', methods=['GET'])
def get_my_scores(student_id):
    try:
        # 移除了认证检查装饰器，保持系统简单
        # 从URL路径参数中获取学生ID
        
        # 获取学生成绩
        scores = ScoreService().get_student_scores(student_id)
        current_app.logger.info(f"Student {student_id} retrieved scores")
        return success_response(scores)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch student scores: {str(e)}')
        return error_response('Failed to fetch scores', 500)