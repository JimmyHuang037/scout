"""用户认证管理模块"""
from flask import jsonify, request, session
from api.services import DatabaseService


def login():
    """用户登录"""
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        password = data.get('password')
        
        if not user_id or not password:
            return jsonify({
                'success': False,
                'error': 'Missing user_id or password'
            }), 400
        
        # 验证用户凭据
        db_service = DatabaseService()
        try:
            # 查询用户信息
            query = """
                SELECT user_id, user_name, password, role 
                FROM users 
                WHERE user_id = %s AND password = %s
            """
            user = db_service.execute_query(query, (user_id, password), fetch_one=True)
            
            if user:
                # 登录成功，将用户信息存储在session中
                session['user_id'] = user['user_id']
                session['user_name'] = user['user_name']
                session['role'] = user['role']
                
                return jsonify({
                    'success': True,
                    'message': 'Login successful',
                    'data': {
                        'user_id': user['user_id'],
                        'user_name': user['user_name'],
                        'role': user['role']
                    }
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Invalid user_id or password'
                }), 401
        finally:
            db_service.close()
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Login failed: {str(e)}'
        }), 500


def logout():
    """用户登出"""
    try:
        # 清除session中的用户信息
        session.pop('user_id', None)
        session.pop('user_name', None)
        session.pop('role', None)
        
        return jsonify({
            'success': True,
            'message': 'Logout successful'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Logout failed: {str(e)}'
        }), 500


def get_current_user():
    """获取当前登录用户信息"""
    try:
        # 检查用户是否已登录
        user_id = session.get('user_id')
        user_name = session.get('user_name')
        role = session.get('role')
        
        if user_id and user_name and role:
            return jsonify({
                'success': True,
                'data': {
                    'user_id': user_id,
                    'user_name': user_name,
                    'role': role
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': 'User not authenticated'
            }), 401
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get user info: {str(e)}'
        }), 500