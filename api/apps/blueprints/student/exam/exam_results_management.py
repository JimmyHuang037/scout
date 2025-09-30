from flask import Blueprint, request, current_app
from apps.utils.helpers import success_response, error_response
from apps.services.score_service import ScoreService

student_exam_results_bp = Blueprint('student_exam_results_bp', __name__)

@student_exam_results_bp.route('/exam/results', methods=['GET'])
def get_my_exam_results():
    try:
        # 移除了认证检查装饰器，保持系统简单
        # 暂时使用固定的学生ID进行测试
        student_id = "20230001"
        
        # 获取学生考试结果
        results = ScoreService().get_student_exam_results(student_id)
        current_app.logger.info(f"Student {student_id} retrieved exam results")
        return success_response(results)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch student exam results: {str(e)}')
        return error_response('Failed to fetch exam results', 500)