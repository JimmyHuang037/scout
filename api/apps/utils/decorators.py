from datetime import datetime
from functools import wraps
import time

from flask import request, current_app, session

from apps.utils.responses import error_response


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return error_response('Authentication required', 401)
        return f(*args, **kwargs)
    return decorated_function


def require_auth():
    if 'user_id' not in session:
        return error_response('Authentication required', 401)
    return None


def require_role(required_role):
    if 'role' not in session:
        return error_response('Role information not found', 401)
    
    if session['role'] != required_role:
        return error_response('Insufficient permissions', 403)
    
    return None


def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_error = require_auth()
            if auth_error:
                return auth_error
            
            role_error = require_role(required_role)
            if role_error:
                return role_error
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def _generate_request_id():
    """Generate a request ID"""
    return f"{int(time.time() * 1000000) % 1000000:06d}"


def _log_exception(e, request_id, func_name):
    """Log the exception"""
    error_msg = f"[{request_id}] {type(e).__name__}: {str(e)}"
    current_app.logger.error(error_msg)
    current_app.logger.exception(f"[{request_id}] Exception in {func_name}")


def _handle_specific_exception(e):
    """Handle specific types of exceptions"""
    if isinstance(e, ValueError):
        return error_response('Invalid input value', 400)
    elif isinstance(e, PermissionError):
        return error_response('Access denied', 403)
    elif isinstance(e, FileNotFoundError):
        return error_response('Resource not found', 404)
    else:
        return error_response('Internal server error', 500)


def handle_exceptions(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            return result
        except Exception as e:
            request_id = getattr(request, 'request_id', None)
            if request_id is None:
                request_id = _generate_request_id()
            
            _log_exception(e, request_id, f.__name__)
            return _handle_specific_exception(e)
    return decorated_function