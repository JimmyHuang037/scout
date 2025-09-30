"""学生蓝图模块"""
from flask import Blueprint

student_bp = Blueprint('student', __name__, url_prefix='/api/student')

# 导入学生考试结果相关路由
from .exam.exam_results_management import get_my_exam_results
from .profile.profile_management import get_my_profile
from .scores.scores_management import get_my_scores

# 注册路由
student_bp.add_url_rule('/exam/results', view_func=get_my_exam_results, methods=['GET'])
student_bp.add_url_rule('/profile', view_func=get_my_profile, methods=['GET'])
student_bp.add_url_rule('/scores', view_func=get_my_scores, methods=['GET'])