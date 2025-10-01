from .profile.profile_bp import student_profile_bp
from .scores.scores_bp import student_scores_bp
from .exam.exam_results_bp import student_exam_results_bp
from flask import Blueprint
"""学生蓝图模块"""

student_bp = Blueprint('student', __name__, url_prefix='/api/student')

# 注册学生个人资料管理路由
student_bp.register_blueprint(student_profile_bp)

# 注册学生成绩管理路由
student_bp.register_blueprint(student_scores_bp)

# 注册学生考试结果管理路由
student_bp.register_blueprint(student_exam_results_bp)