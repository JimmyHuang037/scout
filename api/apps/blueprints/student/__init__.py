from flask import Blueprint

# 学生蓝图模块
student_bp = Blueprint('student', __name__, url_prefix='/api/student')

# 动态导入子蓝图
from .profile import student_profile_bp
from .scores import student_scores_bp
from .exam import student_exam_results_bp

# 注册子蓝图
student_bp.register_blueprint(student_profile_bp)
student_bp.register_blueprint(student_scores_bp)
student_bp.register_blueprint(student_exam_results_bp)