from .class_management import get_classes, create_class, get_class, update_class, delete_class
from flask import Blueprint
"""班级管理蓝图模块"""

class_bp = Blueprint('classes', __name__)

# 导入班级管理相关路由

# 注册路由
class_bp.add_url_rule('/classes', view_func=get_classes, methods=['GET'])
class_bp.add_url_rule('/classes', view_func=create_class, methods=['POST'])
class_bp.add_url_rule('/classes/<int:class_id>', view_func=get_class, methods=['GET'])
class_bp.add_url_rule('/classes/<int:class_id>', view_func=update_class, methods=['PUT'])
class_bp.add_url_rule('/classes/<int:class_id>', view_func=delete_class, methods=['DELETE'])