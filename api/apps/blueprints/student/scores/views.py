from apps.services.score_service import ScoreService
from apps.utils.helpers import success_response, error_response
from flask import Blueprint, request, current_app

"""学生成绩管理模块"""
scores_bp = Blueprint('scores_bp', __name__)

def get_my_scores(student_id):
    """获取指定学生的成绩"""
    try:
        # 获取学生成绩
        scores = ScoreService().get_student_scores(student_id)
        current_app.logger.info(f"Student {student_id} retrieved scores")
        return success_response(scores)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch scores: {str(e)}')
        return error_response('Failed to fetch scores', 500)

# 创建学生成绩管理蓝图
student_scores_bp = Blueprint('student_scores', __name__)

# 注册路由
student_scores_bp.add_url_rule('/<string:student_id>/scores', view_func=get_my_scores, methods=['GET'])

"""学生成绩管理模块"""
scores_bp = Blueprint('scores_bp', __name__)

@scores_bp.route('/<string:student_id>/scores', methods=['GET'])
def get_my_scores(student_id):
    """获取指定学生的成绩"""
    try:
        # 获取学生成绩
        scores = ScoreService().get_student_scores(student_id)
        current_app.logger.info(f"Student {student_id} retrieved scores")
        return success_response(scores)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch student scores: {str(e)}')
        return error_response('Failed to fetch scores', 500)