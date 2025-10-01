from flask import Blueprint
from .views import get_teacher_profile

# 教师个人资料管理蓝图
teacher_profile_bp = Blueprint('teacher_profile', __name__)

# 注册路由
teacher_profile_bp.add_url_rule('/<string:teacher_id>/profile', view_func=get_teacher_profile, methods=['GET'])