from flask import Blueprint

"""考试类型管理蓝图模块"""

# 创建考试类型管理蓝图
admin_exam_types_bp = Blueprint('admin_exam_types', __name__)

# 导入管理函数
from . import exam_type_bp

# 注册路由
admin_exam_types_bp.add_url_rule('/', methods=['POST'], view_func=exam_type_bp.create_exam_type)
admin_exam_types_bp.add_url_rule('/', methods=['GET'], view_func=exam_type_bp.get_exam_types)
admin_exam_types_bp.add_url_rule('/<int:exam_type_id>', methods=['GET'], view_func=exam_type_bp.get_exam_type)
admin_exam_types_bp.add_url_rule('/<int:exam_type_id>', methods=['PUT'], view_func=exam_type_bp.update_exam_type)
admin_exam_types_bp.add_url_rule('/<int:exam_type_id>', methods=['DELETE'], view_func=exam_type_bp.delete_exam_type)