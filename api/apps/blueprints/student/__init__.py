from flask import Blueprint

# 学生蓝图模块
student_bp = Blueprint('student', __name__, url_prefix='/api/student')

# 动态导入子蓝图
from .profile import profile_bp
from .scores import scores_bp
from .exam import exam_results_bp

# 注册子蓝图
student_bp.register_blueprint(profile_bp)
student_bp.register_blueprint(scores_bp)
student_bp.register_blueprint(exam_results_bp)