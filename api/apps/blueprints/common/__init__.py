"""公共蓝图模块"""
from flask import Blueprint

common_bp = Blueprint('common', __name__)

# 导入公共路由
from .common_routes import index, health_check

# 注册路由
common_bp.add_url_rule('/', view_func=index, methods=['GET'])
common_bp.add_url_rule('/api/health', view_func=health_check, methods=['GET'])