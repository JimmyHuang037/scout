"""教师班级管理模块"""
from flask import Blueprint, request, jsonify, current_app, session
from apps.services import ClassService
from apps.utils.helpers import success_response, error_response

teacher_class_bp = Blueprint('teacher_class_bp', __name__)

@teacher_class_bp.route('/classes', methods=['GET'])
def get_classes():
    try:
        # 暂时使用固定的教师ID进行测试
        teacher_id = "T001"
        
        # 获取教师班级列表
        classes = ClassService().get_classes_by_teacher(teacher_id)
        current_app.logger.info(f"Teacher {teacher_id} retrieved classes")
        return success_response(classes)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch classes: {str(e)}')
        return error_response('Failed to fetch classes', 500)

@teacher_class_bp.route('/classes/<int:class_id>/students', methods=['GET'])
def get_class_students(class_id):
    try:
        # 暂时使用固定的教师ID进行测试
        teacher_id = "T001"
        
        # 获取班级学生列表
        students = ClassService().get_students_by_class(class_id, teacher_id)
        current_app.logger.info(f"Teacher {teacher_id} retrieved students for class {class_id}")
        return success_response(students)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch class students: {str(e)}')
        return error_response('Failed to fetch class students', 500)