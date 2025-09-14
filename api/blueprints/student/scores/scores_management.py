"""学生成绩管理模块"""
from flask import Blueprint, request, jsonify, current_app, session
from utils.auth import role_required
from utils.helpers import success_response, error_response
from services.score_service import ScoreService

student_scores_bp = Blueprint('student_scores_bp', __name__)

@student_scores_bp.route('/scores', methods=['GET'])
@role_required('student')
def get_my_scores():
    try:
        # 获取当前学生ID
        student_id = session.get('user_id')
        
        # 获取学生成绩
        scores = ScoreService().get_student_scores(student_id)
        current_app.logger.info(f"Student {student_id} retrieved scores")
        return success_response(scores)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch student scores: {str(e)}')
        return error_response('Failed to fetch scores', 500)