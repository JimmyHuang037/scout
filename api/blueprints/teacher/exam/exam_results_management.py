"""教师考试结果管理模块"""
from flask import jsonify, request
from utils import DatabaseService


def get_exam_results():
    """获取考试结果"""
    try:
        # 在实际应用中，这里会从JWT token或session中获取当前教师ID
        # 这里假设教师ID为1
        current_teacher_id = 1
        
        # 获取筛选参数
        exam_type_id = request.args.get('exam_type_id')
        class_id = request.args.get('class_id')
        
        # 使用数据库服务
        db_service = DatabaseService()
        
        # 构建查询
        query = """
            SELECT er.*
            FROM exam_results er
            JOIN Students s ON er.student_name = s.student_name
            JOIN TeacherClasses tc ON s.class_id = tc.class_id
            WHERE tc.teacher_id = %s
        """
        params = [current_teacher_id]
        
        # 添加筛选条件
        if exam_type_id:
            query += " AND er.exam_type = %s"
            params.append(exam_type_id)
            
        if class_id:
            query += " AND s.class_id = %s"
            params.append(class_id)
            
        query += " ORDER BY er.ranking"
        
        results = db_service.execute_query(query, params)
        db_service.close()
        
        return jsonify({
            'success': True,
            'data': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch exam results: {str(e)}'
        }), 500