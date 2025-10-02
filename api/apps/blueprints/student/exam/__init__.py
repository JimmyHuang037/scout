from flask import Blueprint
from .views import get_my_exam_results

# 学生考试结果管理蓝图
student_exam_results_bp = Blueprint('student_exam_results', __name__)

# 注册路由
student_exam_results_bp.add_url_rule('/<string:student_id>/exam_results', view_func=get_my_exam_results, methods=['GET'])