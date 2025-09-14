from flask import Blueprint, request, current_app, session
from utils.auth import role_required
from utils.helpers import success_response, error_response
from services.score_service import ScoreService

student_exam_results_bp = Blueprint('student_exam_results_bp', __name__)

@student_exam_results_bp.route('/exam/results', methods=['GET'])
@role_required('student')
def get_my_exam_results():
    try:
        # 获取当前学生ID
        student_id = session.get('user_id')
        
        # 获取学生考试结果
        results = ScoreService().get_student_exam_results(student_id)
        current_app.logger.info(f"Student {student_id} retrieved exam results")
        return success_response(results)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch student exam results: {str(e)}')
        return error_response('Failed to fetch exam results', 500)