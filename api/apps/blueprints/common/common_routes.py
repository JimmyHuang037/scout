"""公共路由模块"""
from flask import jsonify


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