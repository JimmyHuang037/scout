from flask import jsonify, request


def index():
    """首页"""
    return "Welcome to the API", 200


def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'method': request.method
    }), 200
from flask import Blueprint
from .views import index, health_check

"""公共蓝图模块"""

common_bp = Blueprint('common', __name__)

# 注册路由
common_bp.add_url_rule('/', view_func=index, methods=['GET'])
common_bp.add_url_rule('/api/health', view_func=health_check, methods=['GET'])