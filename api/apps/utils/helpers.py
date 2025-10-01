from datetime import datetime
from functools import wraps
import os
from flask import jsonify, request, current_app, session
"""助手函数模块，包含各种通用工具函数"""



def success_response(data=None, message="Success"):
    """
    生成成功的JSON响应
    
    Args:
        data: 响应数据
        message: 响应消息
        
    Returns:
        JSON: 成功响应
    """
    response = {
        'success': True,
        'message': message,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(response)


def error_response(message="Error", status_code=400):
    """
    生成错误的JSON响应
    
    Args:
        message: 错误消息
        status_code: HTTP状态码
        
    Returns:
        JSON: 错误响应
    """
    response = {
        'success': False,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(response), status_code


def auth_required(f):
    """
    认证装饰器，检查用户是否已登录
    
    Args:
        f: 被装饰的函数
        
    Returns:
        function: 装饰后的函数
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return error_response('Authentication required', 401)
        return f(*args, **kwargs)
    return decorated_function


def role_required(required_role):
    """
    角色权限装饰器，检查用户是否具有指定角色
    
    Args:
        required_role (str): 需要的角色
        
    Returns:
        function: 装饰器函数
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_role' not in session or session['user_role'] != required_role:
                return error_response('Access denied', 403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_current_user():
    """
    获取当前登录用户信息
    
    Returns:
        dict: 当前用户信息
    """
    return {
        'user_id': session.get('user_id'),
        'username': session.get('username'),
        'role': session.get('user_role')
    }




def configure_logging(app):
    """
    配置应用日志（使用Flask内置日志系统）
    
    Args:
        app: Flask应用实例
    """
    # 使用Flask内置的日志配置
    if not app.config.get('TESTING', False):
        # 确保日志目录存在
        logs_dir = app.config.get('LOGS_DIR')
        if logs_dir and not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
            
        # 配置日志格式和级别
        app.logger.setLevel(app.config['LOG_LEVEL'])
        
        # 注意：实际的日志文件处理器应该在app.py中配置，
        # 这里只保留应用特定的日志配置逻辑