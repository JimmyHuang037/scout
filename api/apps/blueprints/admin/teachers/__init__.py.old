from flask import Blueprint
from .views import get_teachers, create_teacher, get_teacher, update_teacher, delete_teacher

# 教师管理蓝图
admin_teachers_bp = Blueprint('admin_teachers', __name__, url_prefix='/teachers')

# 注册路由
admin_teachers_bp.add_url_rule('/', methods=['GET'], view_func=get_teachers)
admin_teachers_bp.add_url_rule('/', methods=['POST'], view_func=create_teacher)
admin_teachers_bp.add_url_rule('/<int:teacher_id>', methods=['GET'], view_func=get_teacher)
admin_teachers_bp.add_url_rule('/<int:teacher_id>', methods=['PUT'], view_func=update_teacher)
admin_teachers_bp.add_url_rule('/<int:teacher_id>', methods=['DELETE'], view_func=delete_teacher)