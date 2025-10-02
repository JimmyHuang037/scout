from flask import Blueprint

# 教师蓝图模块
teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')

# 导入各管理模块
from .profile import teacher_profile_bp
from .classes import teacher_classes_bp
from .students import teacher_students_bp
from .scores import teacher_scores_bp

# 注册教师个人资料管理路由
teacher_bp.register_blueprint(teacher_profile_bp)

# 注册教师班级管理路由
teacher_bp.register_blueprint(teacher_classes_bp)

# 注册教师学生管理路由
teacher_bp.register_blueprint(teacher_students_bp)

# 注册教师成绩管理路由
teacher_bp.register_blueprint(teacher_scores_bp)