from flask import jsonify, request
from apps.utils.helpers import handle_exceptions


def index():
    """首页"""
    return "Welcome to the API", 200


def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'method': request.method
    }), 200


@handle_exceptions
def test_error():
    """测试错误接口"""
    # 故意引发一个异常来测试错误处理
    raise Exception("This is a test error for exception handling")


"""公共蓝图模块"""

from flask import Blueprint
from .views import index, health_check, test_error

# 创建公共蓝图
common_bp = Blueprint('common', __name__)

# 注册路由
common_bp.add_url_rule('/', view_func=index, methods=['GET'])
common_bp.add_url_rule('/api/health', view_func=health_check, methods=['GET'])
common_bp.add_url_rule('/api/test_error', view_func=test_error, methods=['GET'])
