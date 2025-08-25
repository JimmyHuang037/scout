from flask import Blueprint, jsonify, request
from utils import DatabaseService

teacher_score_update_bp = Blueprint('teacher_score_update', __name__, url_prefix='/api/teacher')


@teacher_score_update_bp.route('/scores/<int:score_id>', methods=['PUT'])
def update_score(score_id):
    """更新成绩"""
    try:
        data = request.get_json()
        score = data.get('score')
        
        if score is None:
            return jsonify({
                'success': False,
                'error': 'Score is required'
            }), 400
        
        # 验证分数范围
        if not (0 <= score <= 100):
            return jsonify({
                'success': False,
                'error': 'Score must be between 0 and 100'
            }), 400
        
        db_service = DatabaseService()
        
        # 检查成绩是否存在且属于教师所教班级
        current_teacher_id = 1  # 示例教师ID
        check_query = """
            SELECT COUNT(*) as count
            FROM Scores sc
            JOIN Students s ON sc.student_id = s.student_id
            JOIN TeacherClasses tc ON s.class_id = tc.class_id
            WHERE sc.score_id = %s AND tc.teacher_id = %s
        """
        check_result = db_service.execute_query(check_query, (score_id, current_teacher_id), fetch_one=True)
        
        if check_result['count'] == 0:
            db_service.close()
            return jsonify({
                'success': False,
                'error': 'Score not found or not in your class'
            }), 404
        
        # 更新成绩
        update_query = """
            UPDATE Scores 
            SET score = %s 
            WHERE score_id = %s
        """
        db_service.execute_update(update_query, (score, score_id))
        db_service.close()
        
        return jsonify({
            'success': True,
            'message': 'Score updated successfully'
        })
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