"""学生蓝图模块"""
from flask import Blueprint

student_bp = Blueprint('student', __name__, url_prefix='/api/student')

# 导入个人资料相关路由
from .profile.profile_management import get_profile

# 导入成绩相关路由
from .scores.scores_management import get_my_scores

# 导入考试相关路由
from .exam.exam_results_management import get_my_exam_results

# 注册个人资料路由
student_bp.add_url_rule('/profile', view_func=get_profile, methods=['GET'])

# 注册成绩相关路由
student_bp.add_url_rule('/scores', view_func=get_my_scores, methods=['GET'])

# 注册考试相关路由
student_bp.add_url_rule('/exam/results', view_func=get_my_exam_results, methods=['GET'])