"""学生个人资料管理模块"""
from flask import jsonify, request
from api.services import StudentService


def get_profile():
    """获取当前学生个人资料"""
    try:
        # 在实际应用中，这里会从JWT token或session中获取当前学生ID
        # 这里假设学生ID为1
        current_student_id = "1"
        
        # 使用学生服务获取学生详情
        student_service = StudentService()
        student = student_service.get_student_by_id(current_student_id)
        
        if student:
            return jsonify({
                'success': True,
                'data': student
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch profile: {str(e)}'
        }), 500