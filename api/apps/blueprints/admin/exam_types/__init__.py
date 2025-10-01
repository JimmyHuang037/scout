from flask import Blueprint
from .views import create_exam_type, get_exam_types, get_exam_type, update_exam_type, delete_exam_type

# 考试类型管理蓝图
admin_exam_types_bp = Blueprint('admin_exam_types', __name__, url_prefix='/exam_types')

# 注册路由
admin_exam_types_bp.add_url_rule('/', methods=['POST'], view_func=create_exam_type)
admin_exam_types_bp.add_url_rule('/', methods=['GET'], view_func=get_exam_types)
admin_exam_types_bp.add_url_rule('/<int:exam_type_id>', methods=['GET'], view_func=get_exam_type)
admin_exam_types_bp.add_url_rule('/<int:exam_type_id>', methods=['PUT'], view_func=update_exam_type)
admin_exam_types_bp.add_url_rule('/<int:exam_type_id>', methods=['DELETE'], view_func=delete_exam_type)