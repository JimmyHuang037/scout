from apps.utils.database_service import DatabaseService
from apps.utils.helpers import success_response, error_response
from flask import jsonify, request, session, current_app
"""认证管理模块"""


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
            response = error_response('Missing user_id or password')
            response.status_code = 400
            return response
            
        # 查询数据库验证用户
        db_service = DatabaseService()
        query = """
            SELECT user_id, username, role, password 
            FROM Users 
            WHERE user_id = %s AND password = %s
        """
        result = db_service.execute_query(query, (user_id, password))
        
        if result:
            # 登录成功，设置session
            user = result[0]
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['role'] = user['role']
            
            response = success_response({
                'user_id': user['user_id'],
                'username': user['username'],
                'role': user['role']
            }, 'Login successful')
            return response
        else:
            response = error_response('Invalid credentials')
            response.status_code = 401
            return response
            
    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}")
        response = error_response('Login failed')
        response.status_code = 500
        return response


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
        response = error_response('Logout failed')
        response.status_code = 500
        return response


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
            response = error_response('Not logged in')
            response.status_code = 401
            return response
    except Exception as e:
        current_app.logger.error(f"Error getting current user: {str(e)}")
        response = error_response('Failed to get user info')
        response.status_code = 500
        return response