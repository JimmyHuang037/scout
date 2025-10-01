from flask import Blueprint
from .views import login, logout, get_current_user

"""认证蓝图模块"""

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# 注册路由
auth_bp.add_url_rule('/login', view_func=login, methods=['POST'])
auth_bp.add_url_rule('/logout', view_func=logout, methods=['POST'])
auth_bp.add_url_rule('/me', view_func=get_current_user, methods=['GET'])
