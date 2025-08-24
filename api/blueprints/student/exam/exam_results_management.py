"""学生考试结果管理模块"""
from flask import jsonify, request
from api.services import ScoreService


def get_my_exam_results():
    """获取当前学生考试结果"""
    try:
        # 在实际应用中，这里会从JWT token或session中获取当前学生ID
        # 这里假设学生ID为S1001
        current_student_id = 'S1001'
        
        # 获取筛选参数
        exam_type_id = request.args.get('exam_type_id')
        
        # 使用成绩服务获取考试结果
        score_service = ScoreService()
        results = score_service.get_scores(
            student_id=current_student_id,
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