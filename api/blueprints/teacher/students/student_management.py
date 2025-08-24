"""教师视角学生管理模块"""
from flask import jsonify, request
from api.services import StudentService


def get_my_students():
    """获取当前教师所教班级的学生信息"""
    try:
        # 分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 在实际应用中，这里会从JWT token或session中获取当前教师ID
        # 这里假设教师ID为1
        current_teacher_id = 1
        
        # 使用学生服务获取学生列表
        student_service = StudentService()
        # TODO: 实现根据教师ID过滤学生列表的功能
        result = student_service.get_all_students(page, per_page)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch students: {str(e)}'
        }), 500