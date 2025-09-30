from flask import Blueprint, request, jsonify, current_app
from utils.helpers import success_response, error_response
from services.student_service import StudentService

student_profile_bp = Blueprint('student_profile_bp', __name__)

@student_profile_bp.route('/profile', methods=['GET'])
def get_my_profile():
    try:
        # 移除了认证检查装饰器，保持系统简单
        # 暂时使用固定的学生ID进行测试
        student_id = "20230001"
        
        # 获取学生个人信息
        student_service = StudentService()
        profile = student_service.get_student_profile(student_id)
        current_app.logger.info(f"Student {student_id} retrieved profile")
        return success_response(profile)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch student profile: {str(e)}')
        return error_response('Failed to fetch profile', 500)