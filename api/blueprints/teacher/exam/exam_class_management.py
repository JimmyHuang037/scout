"""考试班级管理模块，处理考试班级相关操作"""
from flask import Blueprint, request, jsonify, current_app
from utils.auth import role_required
from utils.helpers import success_response, error_response
from services.exam_service import ExamService

teacher_exam_classes_bp = Blueprint('teacher_exam_classes_bp', __name__)

@teacher_exam_classes_bp.route('/exam/classes', methods=['GET'])
@role_required('teacher')
def get_teacher_classes():
    try:
        # 获取当前教师ID
        teacher_id = request.user['user_id']
        
        # 获取教师的班级列表
        classes = ExamService.get_teacher_classes(teacher_id)
        current_app.logger.info(f"Teacher {teacher_id} retrieved class list")
        return success_response(classes)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch teacher classes: {str(e)}')
        return error_response('Failed to fetch classes', 500)
