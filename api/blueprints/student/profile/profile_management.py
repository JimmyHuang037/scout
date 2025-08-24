"""学生个人信息管理模块"""
from flask import jsonify, session
from utils.logger import app_logger
from utils.helpers import success_response, error_response, require_auth


def get_my_profile():
    """获取当前学生个人信息"""
    try:
        # 检查认证
        auth_error = require_auth()
        if auth_error:
            return auth_error
            
        # 从session中获取当前学生ID
        current_student_id = session.get('user_id')
        if not current_student_id:
            return error_response('User not authenticated'), 401
        
        # 返回学生ID作为示例（实际应用中应从数据库获取完整信息）
        app_logger.info(f"Student {current_student_id} retrieved their profile")
        return success_response({
            'student_id': current_student_id
        })
        
    except Exception as e:
        app_logger.error(f"Failed to fetch profile: {str(e)}")
        return error_response(f'Failed to fetch profile: {str(e)}'), 500