from flask import Blueprint

"""考试类型管理蓝图模块"""

# 创建考试类型管理蓝图
admin_exam_types_bp = Blueprint('admin_exam_types', __name__, url_prefix='/api/admin/exam-types')

# 导入管理函数
from . import exam_type_management

# 注册路由
admin_exam_types_bp.add_url_rule('/', methods=['POST'], view_func=exam_type_management.create_exam_type)
admin_exam_types_bp.add_url_rule('/', methods=['GET'], view_func=exam_type_management.get_exam_types)
admin_exam_types_bp.add_url_rule('/<int:exam_type_id>', methods=['GET'], view_func=exam_type_management.get_exam_type)
admin_exam_types_bp.add_url_rule('/<int:exam_type_id>', methods=['PUT'], view_func=exam_type_management.update_exam_type)
admin_exam_types_bp.add_url_rule('/<int:exam_type_id>', methods=['DELETE'], view_func=exam_type_management.delete_exam_type)