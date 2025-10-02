from flask import Blueprint, request, current_app, session
from apps.utils.decorators import handle_exceptions
from apps.utils.responses import success_response, error_response
from apps.services.user_service import UserService


"""认证蓝图模块"""
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@handle_exceptions
def login():
    """
    用户登录
    
    Returns:
        JSON: 登录结果
    """
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')
    
    if not user_id or not password:
        return error_response('缺少用户ID或密码', 400)
        
    # 使用UserService验证用户
    user_service = UserService()
    user = user_service.authenticate_user(user_id, password)
    
    if user:
        # 登录成功，设置session
        session['user_id'] = user['user_id']
        session['username'] = user['username']
        session['role'] = user['role']
        
        return success_response({
            'user_id': user['user_id'],
            'username': user['username'],
            'role': user['role']
        }, 'Login successful')
    else:
        return error_response('无效的凭证', 401)


@handle_exceptions
def logout():
    """
    用户登出
    
    Returns:
        JSON: 登出结果
    """
    # 清除session
    session.clear()
    return success_response(None, '登出成功')


@handle_exceptions
def get_current_user():
    """
    获取当前登录用户信息
    
    Returns:
        JSON: 当前用户信息
    """
    if 'user_id' in session:
        user_info = {
            'user_id': session['user_id'],
            'username': session.get('username'),
            'role': session.get('role')
        }
        return success_response(user_info)
    else:
        return error_response('未登录', 401)


# 注册路由
auth_bp.add_url_rule('/login', view_func=login, methods=['POST'])
auth_bp.add_url_rule('/logout', view_func=logout, methods=['POST'])
auth_bp.add_url_rule('/me', view_func=get_current_user, methods=['GET'])
