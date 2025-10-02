from flask import jsonify, request
from apps.utils.decorators import handle_exceptions

from . import views


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