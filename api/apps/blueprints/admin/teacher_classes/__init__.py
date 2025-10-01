from .teacher_class_management import get_teacher_classes, create_teacher_class, get_teacher_class, update_teacher_class, delete_teacher_class
from flask import Blueprint
"""教师班级关联管理蓝图模块"""

teacher_class_bp = Blueprint('teacher_classes', __name__)

# 导入教师班级关联管理相关路由

# 注册路由
teacher_class_bp.add_url_rule('/teacher-classes', view_func=get_teacher_classes, methods=['GET'])
teacher_class_bp.add_url_rule('/teacher-classes', view_func=create_teacher_class, methods=['POST'])
teacher_class_bp.add_url_rule('/teacher-classes/<int:teacher_class_id>', view_func=get_teacher_class, methods=['GET'])
teacher_class_bp.add_url_rule('/teacher-classes/<int:teacher_class_id>', view_func=update_teacher_class, methods=['PUT'])
teacher_class_bp.add_url_rule('/teacher-classes/<int:teacher_class_id>', view_func=delete_teacher_class, methods=['DELETE'])