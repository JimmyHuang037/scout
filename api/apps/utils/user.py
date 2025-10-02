from flask import session


def get_current_user():
    return {
        'user_id': session.get('user_id'),
        'username': session.get('username'),
        'role': session.get('user_role')
    }