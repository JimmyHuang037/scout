from flask import Blueprint, jsonify, request
from utils import DatabaseService

teacher_score_create_bp = Blueprint('teacher_score_create', __name__, url_prefix='/api/teacher')


@teacher_score_create_bp.route('/scores', methods=['POST'])
def create_score():
    """录入成绩"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        subject_id = data.get('subject_id')
        exam_type_id = data.get('exam_type_id')
        score = data.get('score')
        
        if not all([student_id, subject_id, exam_type_id, score is not None]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: student_id, subject_id, exam_type_id, score'
            }), 400
        
        # 验证分数范围
        if not (0 <= score <= 100):
            return jsonify({
                'success': False,
                'error': 'Score must be between 0 and 100'
            }), 400
        
        db_service = DatabaseService()
        
        # 检查学生是否在教师所教班级中
        current_teacher_id = 1  # 示例教师ID
        check_query = """
            SELECT COUNT(*) as count
            FROM Students s
            JOIN TeacherClasses tc ON s.class_id = tc.class_id
            WHERE s.student_id = %s AND tc.teacher_id = %s
        """
        check_result = db_service.execute_query(check_query, (student_id, current_teacher_id), fetch_one=True)
        
        if check_result['count'] == 0:
            db_service.close()
            return jsonify({
                'success': False,
                'error': 'Student not in your class'
            }), 403
        
        # 检查成绩是否已存在
        exist_query = """
            SELECT score_id FROM Scores 
            WHERE student_id = %s AND subject_id = %s AND exam_type_id = %s
        """
        exist_result = db_service.execute_query(exist_query, (student_id, subject_id, exam_type_id), fetch_one=True)
        
        if exist_result:
            # 更新已存在的成绩
            update_query = """
                UPDATE Scores 
                SET score = %s 
                WHERE score_id = %s
            """
            db_service.execute_update(update_query, (score, exist_result['score_id']))
            message = 'Score updated successfully'
        else:
            # 插入新成绩
            insert_query = """
                INSERT INTO Scores (student_id, subject_id, exam_type_id, score)
                VALUES (%s, %s, %s, %s)
            """
            db_service.execute_update(insert_query, (student_id, subject_id, exam_type_id, score))
            message = 'Score created successfully'
        
        db_service.close()
        
        return jsonify({
            'success': True,
            'message': message
        }), 201
    except Exception as e:
        # 确保数据库连接被关闭
        try:
            db_service.close()
        except:
            pass
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500