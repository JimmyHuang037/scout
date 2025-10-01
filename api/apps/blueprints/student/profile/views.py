from apps.services.student_service import StudentService
from apps.utils.helpers import success_response, error_response
from flask import Blueprint, request, current_app

# 创建学生个人资料管理蓝图
student_profile_bp = Blueprint('student_profile', __name__)

def get_my_profile(student_id):
    try:
        # 获取学生个人资料
        student_service = StudentService()
        profile_data = student_service.get_student_profile(student_id)
        
        if not profile_data:
            return error_response('Student profile not found', 404)
            
        current_app.logger.info(f"Student {student_id} profile retrieved")
        return success_response(profile_data)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch student profile: {str(e)}')
        return error_response('Failed to fetch student profile', 500)