from flask import Blueprint

# 创建学生管理蓝图
admin_students_bp = Blueprint('admin_students', __name__)

# 导入管理函数
from . import student_management

# 注册路由
admin_students_bp.add_url_rule('/', view_func=student_management.get_students, methods=['GET'])
admin_students_bp.add_url_rule('/', view_func=student_management.create_student, methods=['POST'])
admin_students_bp.add_url_rule('/<string:student_id>', view_func=student_management.get_student, methods=['GET'])
admin_students_bp.add_url_rule('/<string:student_id>', view_func=student_management.update_student, methods=['PUT'])
admin_students_bp.add_url_rule('/<string:student_id>', view_func=student_management.delete_student, methods=['DELETE'])