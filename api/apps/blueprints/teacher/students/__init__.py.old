"""教师学生管理蓝图模块"""
from flask import Blueprint
from .views import get_teacher_students, get_teacher_student, get_teacher_all_classes_students

# 教师学生管理蓝图
teacher_students_bp = Blueprint('teacher_students', __name__)

# 注册路由
teacher_students_bp.add_url_rule('/<string:teacher_id>/students', view_func=get_teacher_students, methods=['GET'])
teacher_students_bp.add_url_rule('/<string:teacher_id>/students/<string:student_id>', view_func=get_teacher_student, methods=['GET'])
teacher_students_bp.add_url_rule('/<string:teacher_id>/classes/students', view_func=get_teacher_all_classes_students, methods=['GET'])
teacher_students_bp.add_url_rule('/<string:teacher_id>/all_classes_students', view_func=get_teacher_all_classes_students, methods=['GET'])