"""认证管理模块，处理用户登录和登出"""
from flask import jsonify, request, session
from utils import database_service
from utils.helpers import success_response, error_response
from utils.logger import app_logger


def login():
    """用户登录"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')
        
        if not user_id or not password:
            app_logger.warning("Login attempt with missing fields")
            return error_response('Missing required fields: user_id, password', 400)
        
        # 查询用户信息
        db_service = database_service.DatabaseService()
        query = """
            SELECT user_id, user_name, password, role 
            FROM users 
            WHERE user_id = %s AND password = %s
        """
        user = db_service.execute_query(query, (user_id, password), fetch_one=True)
        db_service.close()
        
        if user:
            # 存储用户信息到session
            session['user_id'] = user['user_id']
            session['user_name'] = user['user_name']
            session['role'] = user['role']
            
            app_logger.info(f"User {user_id} logged in successfully")
            return success_response({
                'user_id': user['user_id'],
                'user_name': user['user_name'],
                'role': user['role']
            }, 'Login successful')
        else:
            app_logger.warning(f"Failed login attempt for user {user_id}")
            return error_response('Invalid user_id or password', 401)
            
    except Exception as e:
        app_logger.error(f"Login failed: {str(e)}")
        return error_response(f'Login failed: {str(e)}'), 500


def logout():
    """用户登出"""
    try:
        # 清除session中的用户信息
        user_id = session.get('user_id')
        session.clear()
        
        app_logger.info(f"User {user_id} logged out")
        return success_response(message='Logout successful')
        
    except Exception as e:
        app_logger.error(f"Logout failed: {str(e)}")
        return error_response(f'Logout failed: {str(e)}'), 500


def get_current_user():
    """获取当前登录用户信息"""
    try:
        # 从session中获取用户信息
        user_id = session.get('user_id')
        user_name = session.get('user_name')
        role = session.get('role')
        
        if user_id and user_name and role:
            app_logger.debug(f"Retrieved current user info for {user_id}")
            return success_response({
                'user_id': user_id,
                'user_name': user_name,
                'role': role
            })
        else:
            app_logger.warning("Attempt to get current user when not authenticated")
            return error_response('User not authenticated', 401)
            
    except Exception as e:
        app_logger.error(f"Failed to get user info: {str(e)}")
        return error_response(f'Failed to get user info: {str(e)}'), 500