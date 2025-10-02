from datetime import datetime
from functools import wraps
import time
from flask import request, current_app, session

from .responses import error_response


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


def require_auth():
    """
    检查用户是否已认证
    
    Returns:
        None or error_response: 如果已认证返回None，否则返回错误响应
    """
    # 检查session中是否存在user_id
    if 'user_id' not in session:
        return error_response('Authentication required', 401)
    return None


def require_role(required_role):
    """
    检查用户是否具有指定角色
    
    Args:
        required_role (str): 所需的角色
        
    Returns:
        None or error_response: 如果具有所需角色返回None，否则返回错误响应
    """
    # 检查session中是否存在role
    if 'role' not in session:
        return error_response('Role information not found', 401)
    
    # 检查角色是否匹配
    if session['role'] != required_role:
        return error_response('Insufficient permissions', 403)
    
    return None


def role_required(required_role):
    """
    装饰器：检查用户是否具有指定角色
    
    Args:
        required_role (str): 所需的角色
        
    Returns:
        function: 装饰器函数
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 检查用户认证
            auth_error = require_auth()
            if auth_error:
                return auth_error
            
            # 检查角色权限
            role_error = require_role(required_role)
            if role_error:
                return role_error
            
            # 如果认证和角色检查都通过，则执行原函数
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
            # 获取请求ID（如果存在）
            request_id = getattr(request, 'request_id', None)
            if request_id is None:
                # 生成新的请求ID
                request_id = f"{int(time.time() * 1000000) % 1000000:06d}"
            
            # 记录详细的异常信息
            error_msg = f"[{request_id}] {type(e).__name__}: {str(e)}"
            current_app.logger.error(error_msg)
            
            # 记录堆栈跟踪信息
            current_app.logger.exception(f"[{request_id}] Exception in {f.__name__}")
            
            # 根据异常类型返回不同的错误信息
            if isinstance(e, ValueError):
                return error_response('Invalid input value', 400)
            elif isinstance(e, PermissionError):
                return error_response('Access denied', 403)
            elif isinstance(e, FileNotFoundError):
                return error_response('Resource not found', 404)
            else:
                # 默认错误响应
                return error_response('Internal server error', 500)
    return decorated_function