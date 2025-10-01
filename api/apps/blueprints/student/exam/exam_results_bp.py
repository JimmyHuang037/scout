from flask import request
from apps.services.score_service import ScoreService
from apps.utils.helpers import success_response, error_response

def get_my_exam_results(student_id):
    """
    获取指定学生的考试成绩
    """
    try:
        scores = ScoreService.get_student_scores(student_id)
        return success_response(data=scores)
    except Exception as e:
        return error_response(message=str(e))
from flask import Blueprint
from .views import get_my_exam_results

# 创建学生考试结果管理蓝图
student_exam_results_bp = Blueprint('student_exam_results', __name__)

# 注册路由
student_exam_results_bp.add_url_rule('/<string:student_id>/exam_results', view_func=get_my_exam_results, methods=['GET'])
