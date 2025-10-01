from apps.services.student_service import StudentService
from apps.utils.helpers import success_response, error_response
from flask import Blueprint, request, jsonify, current_app
student_profile_bp = Blueprint('student_profile_bp', __name__)

@student_profile_bp.route('/<string:student_id>/profile', methods=['GET'])
def get_my_profile(student_id):
    try:
        # 移除了认证检查装饰器，保持系统简单
        # 从URL路径参数中获取学生ID
        
        # 获取学生个人信息
        student_service = StudentService()
        profile = student_service.get_student_profile(student_id)
        if profile is None:
            return error_response('Student profile not found', 404)
        current_app.logger.info(f"Student {student_id} retrieved profile")
        return success_response(profile)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch student profile: {str(e)}')
        return error_response('Failed to fetch profile', 500)