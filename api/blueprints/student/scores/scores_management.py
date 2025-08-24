"""学生成绩管理模块"""
from flask import jsonify, request, session
from api.services import ScoreService


def get_my_scores():
    """获取当前学生成绩"""
    try:
        # 从session中获取当前学生ID
        current_student_id = session.get('user_id')
        if not current_student_id:
            return jsonify({
                'success': False,
                'error': 'User not authenticated'
            }), 401
        
        # 获取筛选参数
        subject_id = request.args.get('subject_id')
        exam_type_id = request.args.get('exam_type_id')
        
        # 使用成绩服务获取成绩列表
        score_service = ScoreService()
        scores = score_service.get_scores(
            student_id=current_student_id,
            subject_id=subject_id,
            exam_type_id=exam_type_id
        )
        
        return jsonify({
            'success': True,
            'data': scores
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch scores: {str(e)}'
        }), 500