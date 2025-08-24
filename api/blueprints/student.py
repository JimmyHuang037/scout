from flask import Blueprint, jsonify, request
from ..database import get_db

student_bp = Blueprint('student', __name__, url_prefix='/api/student')

# 学生专用API端点
@student_bp.route('/profile', methods=['GET'])
def get_profile():
    """获取当前学生个人信息"""
    # 在实际应用中，这里会从JWT token或session中获取当前学生ID
    # 这里返回示例数据
    return jsonify({
        'success': True,
        'data': {
            'student_id': 'S1001',
            'student_name': '示例学生',
            'class_id': 1,
            'class_name': '高三1班'
        }
    })


@student_bp.route('/scores', methods=['GET'])
def get_my_scores():
    """获取当前学生成绩"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # 在实际应用中，这里会从JWT token或session中获取当前学生ID
        # 这里假设学生ID为S1001
        current_student_id = 'S1001'
        
        # 获取筛选参数
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
            WHERE s.student_id = %s
        """
        params = [current_student_id]
        
        # 添加筛选条件
        if subject_id:
            query += " AND s.subject_id = %s"
            params.append(subject_id)
            
        if exam_type_id:
            query += " AND s.exam_type_id = %s"
            params.append(exam_type_id)
            
        query += " ORDER BY s.exam_type_id, s.subject_id"
        
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


@student_bp.route('/exam-results', methods=['GET'])
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