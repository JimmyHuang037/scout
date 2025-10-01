from flask import Blueprint

# 创建班级管理蓝图
admin_classes_bp = Blueprint('admin_classes', __name__)

# 导入管理函数
from . import class_bp

# 注册路由
admin_classes_bp.add_url_rule('/', methods=['GET'], view_func=class_bp.get_classes)
admin_classes_bp.add_url_rule('/', methods=['POST'], view_func=class_bp.create_class)
admin_classes_bp.add_url_rule('/<int:class_id>', methods=['GET'], view_func=class_bp.get_class)
admin_classes_bp.add_url_rule('/<int:class_id>', methods=['PUT'], view_func=class_bp.update_class)
admin_classes_bp.add_url_rule('/<int:class_id>', methods=['DELETE'], view_func=class_bp.delete_class)