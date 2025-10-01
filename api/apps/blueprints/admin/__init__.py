from .classes.class_management import get_classes, create_class, get_class, update_class, delete_class
from .exam_types.exam_type_management import get_exam_types, create_exam_type, get_exam_type, update_exam_type, delete_exam_type
from .students.student_management import get_students, create_student, get_student, update_student, delete_student
from .subjects.subject_management import get_subjects, create_subject, get_subject, update_subject, delete_subject
from .teacher_classes.teacher_class_management import get_teacher_classes, create_teacher_class, get_teacher_class, update_teacher_class, delete_teacher_class
from .teachers.teacher_management import get_teachers, create_teacher, get_teacher, update_teacher, delete_teacher
from flask import Blueprint
"""管理员蓝图模块，处理管理员相关的所有操作"""
from flask import Blueprint

# 创建管理员蓝图
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# 导入各管理模块
from . import students, teachers, classes, subjects, exam_types, teacher_classes

# 注册学生管理路由
admin_bp.register_blueprint(students.student_bp)

# 注册教师管理路由
admin_bp.register_blueprint(teachers.teacher_bp)

# 注册班级管理路由
admin_bp.register_blueprint(classes.admin_classes_bp)

# 注册科目管理路由
admin_bp.register_blueprint(subjects.admin_subjects_bp)

# 注册考试类型管理路由
admin_bp.register_blueprint(exam_types.admin_exam_types_bp)

# 注册教师班级关联管理路由
admin_bp.register_blueprint(teacher_classes.admin_teacher_classes_bp)