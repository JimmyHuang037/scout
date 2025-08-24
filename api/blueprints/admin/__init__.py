"""管理员蓝图模块"""
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# 导入学生管理相关路由
from .students.student_management import get_students, create_student, get_student, update_student, delete_student

# 导入教师管理相关路由
from .teachers.teacher_management import get_teachers, create_teacher, get_teacher, update_teacher, delete_teacher

# 注册学生管理路由
admin_bp.add_url_rule('/students', view_func=get_students, methods=['GET'])
admin_bp.add_url_rule('/students', view_func=create_student, methods=['POST'])
admin_bp.add_url_rule('/students/<string:student_id>', view_func=get_student, methods=['GET'])
admin_bp.add_url_rule('/students/<string:student_id>', view_func=update_student, methods=['PUT'])
admin_bp.add_url_rule('/students/<string:student_id>', view_func=delete_student, methods=['DELETE'])

# 注册教师管理路由
admin_bp.add_url_rule('/teachers', view_func=get_teachers, methods=['GET'])
admin_bp.add_url_rule('/teachers', view_func=create_teacher, methods=['POST'])
admin_bp.add_url_rule('/teachers/<int:teacher_id>', view_func=get_teacher, methods=['GET'])
admin_bp.add_url_rule('/teachers/<int:teacher_id>', view_func=update_teacher, methods=['PUT'])
admin_bp.add_url_rule('/teachers/<int:teacher_id>', view_func=delete_teacher, methods=['DELETE'])