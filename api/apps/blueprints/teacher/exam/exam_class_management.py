"""考试班级管理模块，处理考试班级相关操作"""
from flask import jsonify, request, session, current_app
from apps.utils.helpers import success_response, error_response
from apps.utils.auth import require_auth, require_role
from apps.utils.database_service import DatabaseService
from apps.services.score_service import ScoreService


def get_exam_classes(teacher_id):
    """获取指定教师相关的考试班级列表
    
    Args:
        teacher_id: 教师ID
        
    Returns:
        JSON响应，包含班级列表
    """
    try:
        # 直接使用数据库服务来获取教师相关的班级信息
        db_service = DatabaseService()
        
        try:
            query = """
                SELECT DISTINCT c.class_id, c.class_name
                FROM Classes c
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE tc.teacher_id = %s
                ORDER BY c.class_id
            """
            classes = db_service.execute_query(query, (teacher_id,))
            current_app.logger.info(f"Teacher {teacher_id} retrieved exam classes")
            # 确保总是返回成功响应，即使没有数据
            if classes is None:
                classes = []
            return success_response(classes)
        finally:
            db_service.close()
        
    except Exception as e:
        current_app.logger.error(f"Failed to fetch exam classes: {str(e)}")
        # 确保总是返回有效的JSON响应
        return error_response('Failed to fetch exam classes'), 500