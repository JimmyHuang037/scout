"""教师考试结果管理模块"""
from flask import jsonify, request
from api.services import ScoreService


def get_exam_results():
    """获取考试结果"""
    try:
        # 在实际应用中，这里会从JWT token或session中获取当前教师ID
        # 这里假设教师ID为1
        current_teacher_id = 1
        
        # 获取筛选参数
        exam_type_id = request.args.get('exam_type_id')
        class_id = request.args.get('class_id')
        
        # 使用成绩服务获取考试结果
        # TODO: 实现根据班级筛选的功能
        score_service = ScoreService()
        results = score_service.get_scores(
            teacher_id=current_teacher_id,
            exam_type_id=exam_type_id
        )
        
        return jsonify({
            'success': True,
            'data': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch exam results: {str(e)}'
        }), 500