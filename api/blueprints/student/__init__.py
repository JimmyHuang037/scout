"""学生蓝图模块"""
from flask import Blueprint

student_bp = Blueprint('student', __name__, url_prefix='/api/student')

# 导入并注册成绩相关路由
from .scores.scores_management import get_my_scores
student_bp.add_url_rule('/scores', view_func=get_my_scores, methods=['GET'])

# 导入并注册考试相关路由
from .exam.exam_results_management import get_my_exam_results
student_bp.add_url_rule('/exam/results', view_func=get_my_exam_results, methods=['GET'])