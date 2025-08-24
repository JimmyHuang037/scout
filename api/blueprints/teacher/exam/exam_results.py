from flask import jsonify, request
from api.extensions.database.database import get_db

def get_exam_results():
    """获取考试结果"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # 在实际应用中，这里会从JWT token或session中获取当前教师ID
        # 这里假设教师ID为1
        current_teacher_id = 1
        
        # 获取筛选参数
        exam_type_id = request.args.get('exam_type_id')
        class_id = request.args.get('class_id')
        
        # 构建查询
        query = """
            SELECT er.*
            FROM exam_results er
            JOIN students s ON er.student_name = s.student_name
            JOIN teacher_classes tc ON s.class_name = tc.class_name
            WHERE tc.teacher_id = %s
        """
        
        params = [current_teacher_id]
        
        if exam_type_id:
            query += " AND er.exam_type = %s"
            params.append(exam_type_id)
            
        if class_id:
            query += " AND s.class_id = %s"
            params.append(class_id)
            
        query += " ORDER BY er.total_score DESC"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'data': results
        })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch exam results: {str(e)}'
        }), 500