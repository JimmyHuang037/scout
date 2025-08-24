"""教师考试结果管理模块"""
from flask import jsonify, request, session
from api.services import ScoreService


def get_exam_results():
    """获取考试结果"""
    try:
        # 从session中获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return jsonify({
                'success': False,
                'error': 'User not authenticated'
            }), 401
        
        # 获取筛选参数
        exam_type_id = request.args.get('exam_type_id')
        class_id = request.args.get('class_id')
        
        # 使用成绩服务获取考试结果
        score_service = ScoreService()
        exam_results = score_service.get_exam_results(
            teacher_id=current_teacher_id,
            exam_type_id=exam_type_id,
            class_id=class_id
        )
        
        return jsonify({
            'success': True,
            'data': exam_results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch exam results: {str(e)}'
        }), 500