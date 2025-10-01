from apps.services.score_service import ScoreService
from apps.utils.helpers import success_response, error_response
from flask import current_app

def get_my_exam_results(student_id):
    """获取指定学生的考试结果"""
    try:
        # 获取学生考试结果
        exam_results = ScoreService().get_student_exam_results(student_id)
        current_app.logger.info(f"Student {student_id} retrieved exam results")
        return success_response(exam_results)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch exam results: {str(e)}')
        return error_response('Failed to fetch exam results', 500)