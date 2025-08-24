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

        # 查询参数
        exam_type_id = request.args.get('exam_type_id')
        class_id = request.args.get('class_id')

        # 构建查询
        query = """
            SELECT ec.class_id, ec.class_name, ec.exam_type_id, ec.exam_type_name,
                   ec.a_count, ec.b_count, ec.c_count, ec.d_count, ec.total_count
            FROM exam_class ec
            JOIN TeacherClasses tc ON ec.class_id = tc.class_id
            WHERE tc.teacher_id = %s
        """
        params = [current_teacher_id]

        # 添加筛选条件
        if exam_type_id:
            query += " AND ec.exam_type_id = %s"
            params.append(exam_type_id)

        if class_id:
            query += " AND ec.class_id = %s"
            params.append(class_id)

        query += " ORDER BY ec.class_id, ec.exam_type_id"

        # 执行查询
        exam_classes = db_service.execute_query(query, params)

        return jsonify({
            'success': True,
            'data': exam_classes
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch exam classes: {str(e)}'
        }), 500
    finally:
        if db_service:
            db_service.close()