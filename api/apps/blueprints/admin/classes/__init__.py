from flask import Blueprint
from .views import get_classes, create_class, get_class, update_class, delete_class

# 班级管理蓝图
admin_classes_bp = Blueprint('admin_classes', __name__)

# 注册路由
admin_classes_bp.add_url_rule('/', methods=['GET'], view_func=get_classes)
admin_classes_bp.add_url_rule('/', methods=['POST'], view_func=create_class)
admin_classes_bp.add_url_rule('/<int:class_id>', methods=['GET'], view_func=get_class)
admin_classes_bp.add_url_rule('/<int:class_id>', methods=['PUT'], view_func=update_class)
admin_classes_bp.add_url_rule('/<int:class_id>', methods=['DELETE'], view_func=delete_class)