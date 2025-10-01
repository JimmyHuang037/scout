from flask import Blueprint

# 创建学生管理蓝图
admin_students_bp = Blueprint('admin_students', __name__)

# 导入管理函数
from . import student_management

# 注册路由
admin_students_bp.add_url_rule('/', methods=['GET'], view_func=student_management.get_students)
admin_students_bp.add_url_rule('/', methods=['POST'], view_func=student_management.create_student)
admin_students_bp.add_url_rule('/<string:student_id>', methods=['GET'], view_func=student_management.get_student)
admin_students_bp.add_url_rule('/<string:student_id>', methods=['PUT'], view_func=student_management.update_student)
admin_students_bp.add_url_rule('/<string:student_id>', methods=['DELETE'], view_func=student_management.delete_student)