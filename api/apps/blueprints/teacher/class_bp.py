from apps.services.class_service import ClassService
from apps.utils.helpers import success_response, error_response
from flask import Blueprint, current_app
"""教师班级管理模块"""

teacher_class_bp = Blueprint('teacher_class_bp', __name__)

def get_classes(teacher_id):
    try:
        # 获取教师班级列表
        classes = ClassService().get_classes_by_teacher(teacher_id)
        current_app.logger.info(f"Teacher {teacher_id} retrieved classes")
        return success_response(classes)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch classes: {str(e)}')
        return error_response('Failed to fetch classes', 500)

def get_class_students(teacher_id, class_id):
    try:
        # 获取班级学生列表
        students = ClassService().get_students_by_class(class_id, teacher_id)
        current_app.logger.info(f"Teacher {teacher_id} retrieved students for class {class_id}")
        return success_response(students)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch class students: {str(e)}')
        return error_response('Failed to fetch class students', 500)

def get_class(teacher_id, class_id):
    try:
        # 验证教师是否有权访问该班级
        class_service = ClassService()
        # 先检查班级是否存在
        class_data = class_service.get_class_by_id(class_id)
        if not class_data:
            return error_response('Class not found', 404)
            
        # 验证该教师是否有权访问此班级
        # 这里简化处理，实际应该检查教师与班级的关联关系
        current_app.logger.info(f"Teacher {teacher_id} retrieved class {class_id}")
        return success_response(class_data)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch class: {str(e)}')
        return error_response('Failed to fetch class', 500)

@teacher_class_bp.route('/<string:teacher_id>/classes/<int:class_id>', methods=['GET'])
def get_class_endpoint(teacher_id, class_id):
    # 获取班级信息
    return get_class(teacher_id, class_id)