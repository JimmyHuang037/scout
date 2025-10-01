"""管理员蓝图模块，处理管理员相关的所有操作"""
from flask import Blueprint

# 创建管理员蓝图
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# 导入各管理模块
from . import students, teachers, classes, subjects, exam_types, teacher_classes

# 注册学生管理路由
admin_bp.register_blueprint(students.admin_students_bp)

# 注册教师管理路由
admin_bp.register_blueprint(teachers.admin_teachers_bp)

# 注册班级管理路由
admin_bp.register_blueprint(classes.admin_classes_bp)

# 注册科目管理路由
admin_bp.register_blueprint(subjects.admin_subjects_bp)

# 注册考试类型管理路由
admin_bp.register_blueprint(exam_types.admin_exam_types_bp)

# 注册教师班级关联管理路由
admin_bp.register_blueprint(teacher_classes.admin_teacher_classes_bp)