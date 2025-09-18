"""认证管理模块，处理用户登录和登出"""
from flask import jsonify, request, session, current_app
from utils import database_service
from utils.helpers import success_response, error_response
import time


def login():
    """用户登录"""
    try:
        start_time = time.time()
        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')
        
        if not user_id or not password:
            current_app.logger.warning("Login attempt with missing fields")
            return error_response('Missing required fields: user_id, password', 400)
        
        # 查询用户信息
        db_service = database_service.DatabaseService()
        query = """
            SELECT user_id, user_name, password, role 
            FROM users 
            WHERE user_id = %s AND password = %s
        """
        current_app.logger.info(f"Attempting login with user_id: {user_id}")
        query_start = time.time()
        user = db_service.execute_query(query, (user_id, password), fetch_one=True)
        query_end = time.time()
        db_service.close()
        
        current_app.logger.info(f"Database query took {query_end - query_start:.2f} seconds")
        
        if user:
            # 登录成功，设置session
            session['user_id'] = user['user_id']
            session['user_name'] = user['user_name']
            session['role'] = user['role']
            
            end_time = time.time()
            current_app.logger.info(f"User {user['user_id']} logged in successfully. Total time: {end_time - start_time:.2f} seconds")
            return success_response({
                'user_id': user['user_id'],
                'user_name': user['user_name'],
                'role': user['role']
            })
        else:
            end_time = time.time()
            current_app.logger.warning(f"Login failed for user_id: {user_id}. Total time: {end_time - start_time:.2f} seconds")
            return error_response('Invalid credentials', 401)
    except Exception as e:
        current_app.logger.error(f'Login error: {str(e)}')
        return error_response('Internal server error', 500)


def logout():
    """用户登出"""
    try:
        # 清除session
        session.clear()
        current_app.logger.info("User logged out successfully")
        return success_response({'message': 'Logged out successfully'})
    except Exception as e:
        current_app.logger.error(f'Logout error: {str(e)}')
        return error_response('Internal server error', 500)


def get_current_user():
    """获取当前登录用户信息"""
    try:
        # 检查session中的用户信息
        user_id = session.get('user_id')
        user_name = session.get('user_name')
        role = session.get('role')
        
        if user_id and user_name and role:
            current_app.logger.info(f"Retrieved current user: {user_id}")
            return success_response({
                'user_id': user_id,
                'user_name': user_name,
                'role': role
            })
        else:
            current_app.logger.info("No user currently logged in")
            return error_response('Not authenticated', 401)
    except Exception as e:
        current_app.logger.error(f'Get current user error: {str(e)}')
        return error_response('Internal server error', 500)