from flask import jsonify, request
from api.extensions.database.database import get_db


@teacher_scores_bp.route('/scores', methods=['GET'])
def get_scores():
    """获取所教班级的成绩"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # 在实际应用中，这里会从JWT token或session中获取当前教师ID
        # 这里假设教师ID为1
        current_teacher_id = 1
        
        # 获取筛选参数
        student_id = request.args.get('student_id')
        subject_id = request.args.get('subject_id')
        exam_type_id = request.args.get('exam_type_id')
        
        # 构建查询
        query = """
            SELECT s.score_id, s.student_id, st.student_name, 
                   s.subject_id, sub.subject_name,
                   s.exam_type_id, et.exam_type_name, s.score
            FROM Scores s
            JOIN Students st ON s.student_id = st.student_id
            JOIN Subjects sub ON s.subject_id = sub.subject_id
            JOIN ExamTypes et ON s.exam_type_id = et.type_id
            JOIN Classes c ON st.class_id = c.class_id
            JOIN TeacherClasses tc ON c.class_id = tc.class_id
            WHERE tc.teacher_id = %s
        """
        
        params = [current_teacher_id]
        
        if student_id:
            query += " AND s.student_id = %s"
            params.append(student_id)
            
        if subject_id:
            query += " AND s.subject_id = %s"
            params.append(subject_id)
            
        if exam_type_id:
            query += " AND s.exam_type_id = %s"
            params.append(exam_type_id)
            
        query += " ORDER BY s.score_id DESC"
        
        cursor.execute(query, params)
        scores = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'data': scores
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500