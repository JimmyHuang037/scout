from .student_management import get_students, create_student, get_student, update_student, delete_student
from flask import Blueprint
"""学生管理蓝图模块"""

student_bp = Blueprint('students', __name__)

# 导入学生管理相关路由

# 注册路由
student_bp.add_url_rule('/students', view_func=get_students, methods=['GET'])
student_bp.add_url_rule('/students', view_func=create_student, methods=['POST'])
student_bp.add_url_rule('/students/<string:student_id>', view_func=get_student, methods=['GET'])
student_bp.add_url_rule('/students/<string:student_id>', view_func=update_student, methods=['PUT'])
student_bp.add_url_rule('/students/<string:student_id>', view_func=delete_student, methods=['DELETE'])