from functools import wraps
from flask import request, current_app, session

from .helpers import error_response


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


def handle_exceptions(f):
    """
    全局异常处理装饰器，统一处理视图函数中的异常
    
    Args:
        f: 被装饰的函数
        
    Returns:
        function: 装饰后的函数
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            return result
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            current_app.logger.error(error_msg)
            return error_response('Internal server error', 500)
    return decorated_function