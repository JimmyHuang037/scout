"""管理员蓝图模块，处理管理员相关的所有操作"""
from flask import Blueprint

# 创建管理员蓝图
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# 导入各管理模块
from .students import admin_students_bp
from .teachers import admin_teachers_bp
from .classes import admin_classes_bp
from .subjects import admin_subjects_bp
from .exam_types import admin_exam_types_bp
from .teacher_classes import admin_teacher_classes_bp

# 注册学生管理路由
admin_bp.register_blueprint(admin_students_bp)

# 注册教师管理路由
admin_bp.register_blueprint(admin_teachers_bp)

# 注册班级管理路由
admin_bp.register_blueprint(admin_classes_bp)

# 注册科目管理路由
admin_bp.register_blueprint(admin_subjects_bp)

# 注册考试类型管理路由
admin_bp.register_blueprint(admin_exam_types_bp)

# 注册教师班级关联管理路由
admin_bp.register_blueprint(admin_teacher_classes_bp)