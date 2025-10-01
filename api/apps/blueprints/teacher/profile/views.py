from flask import Blueprint, current_app
from apps.services import TeacherService
from apps.utils.helpers import success_response, error_response

# 创建教师个人资料管理蓝图
teacher_profile_bp = Blueprint('teacher_profile', __name__)


def get_teacher_profile(teacher_id):
    """获取指定教师的个人资料"""
    try:
        teacher_service = TeacherService()
        profile_data = teacher_service.get_teacher_profile(teacher_id)

        if not profile_data:
            return error_response('Teacher profile not found', 404)

        current_app.logger.info(f"Teacher {teacher_id} profile retrieved")
        return success_response(profile_data)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch teacher profile: {str(e)}')
        return error_response('Failed to fetch teacher profile', 500)