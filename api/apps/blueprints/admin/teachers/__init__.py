from .teacher_management import get_teachers, create_teacher, get_teacher, update_teacher, delete_teacher
from flask import Blueprint
"""教师管理蓝图模块"""

teacher_bp = Blueprint('teachers', __name__)

# 导入教师管理相关路由

# 注册路由
teacher_bp.add_url_rule('/teachers', view_func=get_teachers, methods=['GET'])
teacher_bp.add_url_rule('/teachers', view_func=create_teacher, methods=['POST'])
teacher_bp.add_url_rule('/teachers/<string:teacher_id>', view_func=get_teacher, methods=['GET'])
teacher_bp.add_url_rule('/teachers/<string:teacher_id>', view_func=update_teacher, methods=['PUT'])
teacher_bp.add_url_rule('/teachers/<string:teacher_id>', view_func=delete_teacher, methods=['DELETE'])