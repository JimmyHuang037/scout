from flask import Blueprint

teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')
from flask import jsonify, request
from ...extensions.database import get_db

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
        
        db = get_db()
        cursor = db.cursor()
        
        # 检查成绩是否存在且属于教师所教班级
        current_teacher_id = 1  # 示例教师ID
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM Scores sc
            JOIN Students s ON sc.student_id = s.student_id
            JOIN TeacherClasses tc ON s.class_id = tc.class_id
            WHERE sc.score_id = %s AND tc.teacher_id = %s
        """, (score_id, current_teacher_id))
        
        if cursor.fetchone()['count'] == 0:
            return jsonify({
                'success': False,
                'error': 'Score not found or not in your class'
            }), 404
        
        # 更新成绩
        cursor.execute("""
            UPDATE Scores 
            SET score = %s 
            WHERE score_id = %s
        """, (score, score_id))
        
        db.commit()
        
        return jsonify({
            'success': True,
            'message': 'Score updated successfully'
        })
    ```
    
    创建新文件__init__.py：
    ```python
    <<<<<<< SEARCH
    from flask import Blueprint
    from .score_update import update_score
    
    teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')
    
    teacher_bp.route('/scores/<int:score_id>', methods=['PUT'])(update_score)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500