from flask import Blueprint
from .views import get_students, create_student, get_student, update_student, delete_student

# 学生管理蓝图
admin_students_bp = Blueprint('admin_students', __name__)

# 注册路由
admin_students_bp.add_url_rule('/', view_func=get_students, methods=['GET'])
admin_students_bp.add_url_rule('/', view_func=create_student, methods=['POST'])
admin_students_bp.add_url_rule('/<string:student_id>', view_func=get_student, methods=['GET'])
admin_students_bp.add_url_rule('/<string:student_id>', view_func=update_student, methods=['PUT'])
admin_students_bp.add_url_rule('/<string:student_id>', view_func=delete_student, methods=['DELETE'])