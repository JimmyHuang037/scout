from datetime import datetime
from flask import jsonify


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