from flask import session


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