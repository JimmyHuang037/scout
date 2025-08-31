from flask import Blueprint, request, jsonify, current_app
from utils.auth import role_required
from utils.helpers import success_response, error_response
from services.student_service import StudentService

student_profile_bp = Blueprint('student_profile_bp', __name__)

@student_profile_bp.route('/profile', methods=['GET'])
@role_required('student')
def get_my_profile():
    try:
        # 获取当前学生ID
        student_id = request.user['user_id']
        
        # 获取学生个人信息
        profile = StudentService.get_student_profile(student_id)
        current_app.logger.info(f"Student {student_id} retrieved profile")
        return success_response(profile)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch student profile: {str(e)}')
        return error_response('Failed to fetch profile', 500)