"""通用工具函数模块"""
from flask import jsonify, session


def success_response(data=None, message="Success", status_code=200):
    """
    创建成功的JSON响应
    
    Args:
        data: 响应数据
        message: 响应消息
        status_code: HTTP状态码
        
    Returns:
        tuple: (JSON响应, HTTP状态码)
    """
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code


def error_response(message="Error", status_code=400):
    """
    创建错误的JSON响应
    
    Args:
        message: 错误消息
        status_code: HTTP状态码
        
    Returns:
        tuple: (JSON响应, HTTP状态码)
    """
    return jsonify({
        'success': False,
        'error': message
    }), status_code


def get_current_user():
    """
    获取当前登录用户信息
    
    Returns:
        dict: 用户信息，如果未登录则返回None
    """
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    role = session.get('role')
    
    if user_id and user_name and role:
        return {
            'user_id': user_id,
            'user_name': user_name,
            'role': role
        }
    return None


def require_auth():
    """
    检查用户是否已认证
    
    Returns:
        tuple or None: 如果未认证返回错误响应，否则返回None
    """
    if not get_current_user():
        return error_response('User not authenticated', 401)
    return None


def require_role(required_role):
    """
    检查用户是否有指定角色
    
    Args:
        required_role (str): 需要的角色
        
    Returns:
        tuple or None: 如果权限不足返回错误响应，否则返回None
    """
    user = get_current_user()
    if not user:
        return error_response('User not authenticated', 401)
    
    if user['role'] != required_role:
        return error_response('Insufficient permissions', 403)
    
    return None