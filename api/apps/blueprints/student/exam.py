from flask import Blueprint, current_app
from apps.services.score_service import ScoreService
from apps.utils.helpers import success_response, error_response


# 学生考试结果管理蓝图
student_exam_results_bp = Blueprint('student_exam_results', __name__, url_prefix='/exam_results')


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


# 注册路由
student_exam_results_bp.add_url_rule('/<string:student_id>', view_func=get_my_exam_results, methods=['GET'])