"""认证蓝图模块"""
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# 导入认证相关路由
from .auth_management import login, logout, get_current_user

# 注册认证相关路由
auth_bp.add_url_rule('/login', view_func=login, methods=['POST'])
auth_bp.add_url_rule('/logout', view_func=logout, methods=['POST'])
auth_bp.add_url_rule('/user', view_func=get_current_user, methods=['GET'])