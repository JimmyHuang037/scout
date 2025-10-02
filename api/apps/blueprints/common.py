from flask import Blueprint, jsonify, request
from apps.utils.decorators import handle_exceptions
from apps.utils.responses import success_response, error_response

"""公共蓝图模块"""
common_bp = Blueprint('common', __name__, url_prefix='/api')


def index():
    """首页路由"""
    return jsonify({
        'message': 'Welcome to School Management API',
        'version': '1.0.0'
    })


def health_check():
    """健康检查路由"""
    return jsonify({
        'status': 'healthy',
        'message': 'API server is running'
    })


@handle_exceptions
def test_error():
    """测试错误处理的路由"""
    # 故意引发一个异常来测试错误处理
    raise Exception("This is a test error for exception handling")


# 注册路由
common_bp.add_url_rule('/', view_func=index, methods=['GET'])
common_bp.add_url_rule('/health', view_func=health_check, methods=['GET'])
common_bp.add_url_rule('/test_error', view_func=test_error, methods=['GET'])