from .auth_bp import login, logout, get_current_user
from flask import Blueprint
"""认证蓝图模块"""

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# 暂时移除所有认证相关路由，保持系统简单

# 导入认证相关路由

# 注册路由
# auth_bp.add_url_rule('/login', view_func=login, methods=['POST'])
# auth_bp.add_url_rule('/logout', view_func=logout, methods=['POST'])
# auth_bp.add_url_rule('/current_user', view_func=get_current_user, methods=['GET'])