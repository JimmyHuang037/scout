from flask import Blueprint, jsonify, request
from ...extensions.database.database import get_db

student_profile_bp = Blueprint('student_profile', __name__, url_prefix='/api/student')

@student_profile_bp.route('/profile', methods=['GET'])
def get_profile():
    """获取当前学生个人信息"""
    # 在实际应用中，这里会从JWT token或session中获取当前学生ID
    # 这里返回示例数据
    return jsonify({
        'success': True,
        'data': {
            'student_id': 'S1001',
            'student_name': '示例学生',
            'class_id': 1,
            'class_name': '高三1班'
        }
    })