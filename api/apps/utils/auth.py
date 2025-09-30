"""认证和权限检查工具模块"""
from functools import wraps
from flask import session
from apps.utils.helpers import error_response


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