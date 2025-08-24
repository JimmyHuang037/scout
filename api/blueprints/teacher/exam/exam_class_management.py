"""教师考试班级管理模块"""
from flask import jsonify, request, session
from api.services import DatabaseService


def get_exam_classes():
    """获取考试班级列表"""
    db_service = None
    try:
        db_service = DatabaseService()
        
        # 从session中获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return jsonify({
                'success': False,
                'error': 'User not authenticated'
            }), 401
        
        # 查询教师所教的班级
        query = """
            SELECT c.class_id, c.class_name
            FROM Classes c
            JOIN TeacherClasses tc ON c.class_id = tc.class_id
            WHERE tc.teacher_id = %s
            ORDER BY c.class_id
        """
        classes = db_service.execute_query(query, (current_teacher_id,))
        
        return jsonify({
            'success': True,
            'data': classes
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch exam classes: {str(e)}'
        }), 500
    finally:
        if db_service:
            db_service.close()