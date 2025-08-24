"""教师考试表现管理模块"""
from flask import jsonify, request, session
from api.services.teacher import ScoreService  # 更新后的导入路径


def get_performance():
    """获取考试表现统计"""
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
        
        # 使用成绩服务获取考试表现数据
        score_service = ScoreService()
        performance = score_service.get_teacher_performance(
            teacher_id=current_teacher_id,
            exam_type_id=exam_type_id,
            class_id=class_id
        )
        
        return jsonify({
            'success': True,
            'data': performance
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch performance data: {str(e)}'
        }), 500