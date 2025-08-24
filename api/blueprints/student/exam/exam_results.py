from flask import Blueprint, jsonify, request
from ...extensions.database.database import get_db

student_exam_results_bp = Blueprint('student_exam_results', __name__, url_prefix='/api/student')

@student_exam_results_bp.route('/exam-results', methods=['GET'])
def get_my_exam_results():
    """获取当前学生考试结果"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # 在实际应用中，这里会从JWT token或session中获取当前学生ID
        # 这里假设学生ID为S1001
        current_student_id = 'S1001'
        
        # 获取筛选参数
        exam_type_id = request.args.get('exam_type_id')
        
        # 构建查询
        query = """
            SELECT er.*
            FROM exam_results er
            JOIN Students s ON er.student_name = s.student_name
            WHERE s.student_id = %s
        """
        params = [current_student_id]
        
        # 添加筛选条件
        if exam_type_id:
            query += " AND er.exam_type = %s"
            params.append(exam_type_id)
            
        query += " ORDER BY er.exam_type"
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500