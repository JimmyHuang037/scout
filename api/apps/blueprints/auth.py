from flask import Blueprint, jsonify, request, session, current_app
from apps.utils.database_service import DatabaseService
from apps.utils.helpers import success_response, error_response


"""认证蓝图模块"""
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


def login():
    """
    用户登录
    
    Returns:
        JSON: 登录结果
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')
        
        if not user_id or not password:
            return error_response('Missing user_id or password', 400)
            
        # 查询数据库验证用户
        db_service = DatabaseService()
        query = """
            SELECT user_id, user_name as username, role, password 
            FROM users 
            WHERE user_id = %s AND password = %s
        """
        result = db_service.execute_query(query, (user_id, password))
        
        if result:
            # 登录成功，设置session
            user = result[0]
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            return success_response({
                'user_id': user['user_id'],
                'username': user['username'],
                'role': user['role']
            }, 'Login successful')
        else:
            return error_response('Invalid credentials', 401)
            
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        return error_response('Login failed', 500)


def logout():
    """
    用户登出
    
    Returns:
        JSON: 登出结果
    """
    try:
        # 清除session
        session.clear()
        return success_response(None, 'Logout successful')
    except Exception as e:
        current_app.logger.error(f"Logout error: {str(e)}")
        return error_response('Logout failed', 500)


def get_current_user():
    """
    获取当前登录用户信息
    
    Returns:
        JSON: 当前用户信息
    """
    try:
        if 'user_id' in session:
            user_info = {
                'user_id': session['user_id'],
                'username': session.get('username'),
                'role': session.get('role')
            }
            return success_response(user_info)
        else:
            return error_response('Not logged in', 401)
    except Exception as e:
        current_app.logger.error(f"Error getting current user: {str(e)}")
        return error_response('Failed to get user info', 500)


# 注册路由
auth_bp.add_url_rule('/login', view_func=login, methods=['POST'])
auth_bp.add_url_rule('/logout', view_func=logout, methods=['POST'])
auth_bp.add_url_rule('/me', view_func=get_current_user, methods=['GET'])