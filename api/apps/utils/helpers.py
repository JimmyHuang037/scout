from datetime import datetime
from flask import jsonify, session, request
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


def validate_json_input(required_fields=None, allow_empty=False):
    """
    验证JSON输入数据
    
    Args:
        required_fields (list): 必需的字段列表
        allow_empty (bool): 是否允许空数据
        
    Returns:
        tuple: (data, error_response) 如果验证成功，error_response为None；如果验证失败，data为None
    """
    # 获取请求数据
    data = request.get_json()
    if not data:
        if allow_empty:
            return {}, None
        return None, error_response("请求数据不能为空", 400)
    
    # 检查必需字段
    if required_fields:
        for field in required_fields:
            if field not in data or not data[field]:
                return None, error_response(f"缺少必需字段: {field}", 400)
    
    return data, None
