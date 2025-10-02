from apps.services.student_service import StudentService
from apps.utils.decorators import handle_exceptions
from apps.utils.helpers import success_response, error_response
from flask import current_app

@handle_exceptions
def get_my_profile(student_id):
    # 获取学生个人资料
    student_service = StudentService()
    profile_data = student_service.get_student_profile(student_id)
    
    if not profile_data:
        return error_response('Student profile not found', 404)
        
    current_app.logger.info(f"Student {student_id} profile retrieved")
    return success_response(profile_data)