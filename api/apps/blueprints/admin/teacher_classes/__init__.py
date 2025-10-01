from flask import Blueprint
from .views import get_teacher_classes, create_teacher_class, get_teacher_class, update_teacher_class, delete_teacher_class

# 教师班级关联管理蓝图
admin_teacher_classes_bp = Blueprint('admin_teacher_classes', __name__, url_prefix='/teacher_classes')

# 注册路由
admin_teacher_classes_bp.add_url_rule('/', methods=['GET'], view_func=get_teacher_classes)
admin_teacher_classes_bp.add_url_rule('/', methods=['POST'], view_func=create_teacher_class)
admin_teacher_classes_bp.add_url_rule('/<int:teacher_id>/<int:class_id>', methods=['GET'], view_func=get_teacher_class)
admin_teacher_classes_bp.add_url_rule('/<int:teacher_id>/<int:class_id>', methods=['PUT'], view_func=update_teacher_class)
admin_teacher_classes_bp.add_url_rule('/<int:teacher_id>/<int:class_id>', methods=['DELETE'], view_func=delete_teacher_class)