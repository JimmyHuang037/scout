"""考试类型管理蓝图模块"""
from flask import Blueprint

exam_type_bp = Blueprint('exam_types', __name__)

# 导入考试类型管理相关路由
from .exam_type_management import get_exam_types, create_exam_type, get_exam_type, update_exam_type, delete_exam_type

# 注册路由
exam_type_bp.add_url_rule('/exam-types', view_func=create_exam_type, methods=['POST'])
exam_type_bp.add_url_rule('/exam-types', view_func=get_exam_types, methods=['GET'])
exam_type_bp.add_url_rule('/exam-types/<int:exam_type_id>', view_func=get_exam_type, methods=['GET'])
exam_type_bp.add_url_rule('/exam-types/<int:exam_type_id>', view_func=update_exam_type, methods=['PUT'])
exam_type_bp.add_url_rule('/exam-types/<int:exam_type_id>', view_func=delete_exam_type, methods=['DELETE'])