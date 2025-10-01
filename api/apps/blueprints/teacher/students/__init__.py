"""学生管理蓝图模块"""
from flask import Blueprint
from .student_bp import get_teacher_students, get_teacher_student

students_bp = Blueprint('students', __name__, url_prefix='/students')

# 注册路由
students_bp.add_url_rule('/', view_func=get_teacher_students, methods=['GET'])
students_bp.add_url_rule('/<string:student_id>', view_func=get_teacher_student, methods=['GET'])