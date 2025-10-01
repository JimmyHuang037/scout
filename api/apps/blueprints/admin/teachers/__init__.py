from flask import Blueprint

# 创建教师管理蓝图
admin_teachers_bp = Blueprint('admin_teachers', __name__)

# 导入管理函数
from . import teacher_bp

# 注册路由
admin_teachers_bp.add_url_rule('/', methods=['GET'], view_func=teacher_bp.get_teachers)
admin_teachers_bp.add_url_rule('/', methods=['POST'], view_func=teacher_bp.create_teacher)
admin_teachers_bp.add_url_rule('/<int:teacher_id>', methods=['GET'], view_func=teacher_bp.get_teacher)
admin_teachers_bp.add_url_rule('/<int:teacher_id>', methods=['PUT'], view_func=teacher_bp.update_teacher)
admin_teachers_bp.add_url_rule('/<int:teacher_id>', methods=['DELETE'], view_func=teacher_bp.delete_teacher)