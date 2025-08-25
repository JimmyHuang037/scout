"""认证和权限检查工具模块"""
from flask import session
from utils.helpers import error_response


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