"""教师考试班级管理模块"""
from flask import jsonify, session
from services import ScoreService
from utils.logger import app_logger
from utils.helpers import success_response, error_response, require_auth


def get_exam_classes():
    """获取教师相关的考试班级列表"""
    try:
        # 检查认证
        auth_error = require_auth()
        if auth_error:
            return auth_error
            
        # 从session中获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return error_response('User not authenticated'), 401
        
        # 使用成绩服务获取考试班级列表
        score_service = ScoreService()
        # 这里我们直接使用数据库服务来获取教师相关的班级信息
        from utils import DatabaseService
        db_service = DatabaseService()
        
        try:
            query = """
                SELECT DISTINCT c.class_id, c.class_name
                FROM Classes c
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE tc.teacher_id = %s
                ORDER BY c.class_id
            """
            classes = db_service.execute_query(query, (current_teacher_id,))
            app_logger.info(f"Teacher {current_teacher_id} retrieved exam classes")
            return success_response(classes)
        finally:
            db_service.close()
        
    except Exception as e:
        app_logger.error(f"Failed to fetch exam classes: {str(e)}")
        return error_response(f'Failed to fetch exam classes: {str(e)}'), 500