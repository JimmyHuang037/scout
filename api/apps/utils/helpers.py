from datetime import datetime
from flask import jsonify, session
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




