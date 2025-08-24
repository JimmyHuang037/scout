from flask import Blueprint, jsonify, request
from ...extensions.database.database import get_db

teacher_exam_class_bp = Blueprint('teacher_exam_class', __name__, url_prefix='/api/teacher')

@teacher_exam_class_bp.route('/exam-class', methods=['GET'])
def get_exam_class():
    """获取班级成绩等级分布"""
    try:
        current_teacher_id = 1  # 从JWT token或session中获取的教师ID
        
        # 获取筛选参数
        exam_type_id = request.args.get('exam_type_id')
        class_id = request.args.get('class_id')
        
        results = get_exam_class_data(current_teacher_id, exam_type_id, class_id)
        
        return jsonify({
            'success': True,
            'data': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500