"""科目管理蓝图模块"""
from flask import Blueprint

subject_bp = Blueprint('subjects', __name__)

# 导入科目管理相关路由
from .subject_management import get_subjects, create_subject, get_subject, update_subject, delete_subject

# 注册路由
subject_bp.add_url_rule('/subjects', view_func=get_subjects, methods=['GET'])
subject_bp.add_url_rule('/subjects', view_func=create_subject, methods=['POST'])
subject_bp.add_url_rule('/subjects/<int:subject_id>', view_func=get_subject, methods=['GET'])
subject_bp.add_url_rule('/subjects/<int:subject_id>', view_func=update_subject, methods=['PUT'])
subject_bp.add_url_rule('/subjects/<int:subject_id>', view_func=delete_subject, methods=['DELETE'])