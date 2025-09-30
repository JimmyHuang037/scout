"""辅助函数模块"""

from flask import jsonify, request, session
import functools
import logging

# 定义角色常量
ADMIN_ROLE = 'admin'
TEACHER_ROLE = 'teacher'
STUDENT_ROLE = 'student'


def success_response(data=None, message='Success'):
    """
    标准成功响应格式
    
    Args:
        data: 响应数据
        message (str): 响应消息
        
    Returns:
        dict: 标准成功响应
    """
    response = {
        'success': True,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response)


def error_response(message='Error', status_code=400):
    """
    标准错误响应格式
    
    Args:
        message (str): 错误消息
        status_code (int): HTTP状态码
        
    Returns:
        tuple: (错误响应, 状态码)
    """
    response = {
        'success': False,
        'error': message
    }
    return jsonify(response), status_code


def auth_required(f):
    """
    装饰器：检查用户是否已认证
    
    Args:
        f (function): 被装饰的函数
        
    Returns:
        function: 装饰后的函数
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # 检查session中是否存在user_id
        if 'user_id' not in session:
            return error_response('Authentication required', 401)
        return f(*args, **kwargs)
    return decorated_function


def role_required(required_role):
    """
    装饰器：检查用户是否具有指定角色
    
    Args:
        required_role (str): 所需的角色
        
    Returns:
        function: 装饰后的函数
    """
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            # 检查session中是否存在role
            if 'role' not in session:
                return error_response('Role information not found', 401)
            
            # 检查角色是否匹配
            if session['role'] != required_role:
                return error_response('Insufficient permissions', 403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_current_user():
    """
    获取当前登录用户信息
    
    Returns:
        dict: 当前用户信息，未登录则返回None
    """
    if 'user_id' in session:
        return {
            'user_id': session['user_id'],
            'username': session.get('username'),
            'role': session.get('role')
        }
    return None


def format_datetime(dt):
    """
    格式化日期时间
    
    Args:
        dt: 日期时间对象
        
    Returns:
        str: 格式化后的日期时间字符串
    """
    if dt:
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    return None


def validate_required_fields(data, required_fields):
    """
    验证必需字段是否存在
    
    Args:
        data (dict): 要验证的数据
        required_fields (list): 必需字段列表
        
    Returns:
        tuple: (是否有效, 错误消息)
    """
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f'Missing required field: {field}'
    return True, None


def setup_logging(app):
    """
    设置应用日志配置
    
    Args:
        app: Flask应用实例
    """
    # 创建文件处理器
    file_handler = logging.FileHandler(app.config['LOG_FILE_PATH'], encoding='utf-8')
    file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    
    # 创建格式化器并将其添加到处理器
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s'
    )
    file_handler.setFormatter(formatter)
    
    # 将处理器添加到应用日志器
    app.logger.addHandler(file_handler)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    
    app.logger.info('Logging setup completed')