from flask import Blueprint
from .views import get_my_profile

# 学生个人资料管理蓝图
profile_bp = Blueprint('student_profile', __name__)

# 注册路由
profile_bp.add_url_rule('/<string:student_id>/profile', view_func=get_my_profile, methods=['GET'])