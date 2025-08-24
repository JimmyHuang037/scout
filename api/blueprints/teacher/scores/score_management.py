"""成绩管理模块，处理成绩相关的所有操作"""
from flask import jsonify, request, session
from api.services import ScoreService


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
        
        # 使用成绩服务创建成绩
        score_service = ScoreService()
        # 从session中获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return jsonify({
                'success': False,
                'error': 'User not authenticated'
            }), 401
            
        score_data = {
            'student_id': student_id,
            'subject_id': subject_id,
            'exam_type_id': exam_type_id,
            'score': score
        }
        result = score_service.create_score(score_data, current_teacher_id)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Score created/updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create/update score'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create/update score: {str(e)}'
        }), 500


def update_score(score_id):
    """更新成绩"""
    try:
        data = request.get_json()
        score = data.get('score')
        
        if score is None:
            return jsonify({
                'success': False,
                'error': 'Missing required field: score'
            }), 400
        
        # 验证分数范围
        if not (0 <= score <= 100):
            return jsonify({
                'success': False,
                'error': 'Score must be between 0 and 100'
            }), 400
        
        # 使用成绩服务更新成绩
        score_service = ScoreService()
        # 从session中获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return jsonify({
                'success': False,
                'error': 'User not authenticated'
            }), 401
            
        score_data = {'score': score}
        result = score_service.update_score(score_id, score_data, current_teacher_id)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Score updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update score'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update score: {str(e)}'
        }), 500