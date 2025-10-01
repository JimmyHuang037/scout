from flask import Blueprint
from .views import get_classes, get_class_endpoint, get_class_students

# 教师班级管理蓝图
teacher_classes_bp = Blueprint('teacher_classes', __name__)

# 注册路由
teacher_classes_bp.add_url_rule('/<string:teacher_id>/classes', view_func=get_classes, methods=['GET'])
teacher_classes_bp.add_url_rule('/<string:teacher_id>/classes/<int:class_id>', view_func=get_class_endpoint, methods=['GET'])
teacher_classes_bp.add_url_rule('/<string:teacher_id>/classes/<int:class_id>/students', view_func=get_class_students, methods=['GET'])