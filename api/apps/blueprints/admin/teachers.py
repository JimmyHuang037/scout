from flask import Blueprint, request, current_app
from apps.services.teacher_service import TeacherService
from apps.utils.decorators import handle_exceptions
from apps.utils.responses import success_response, error_response
from apps.utils.validation import validate_json_input

admin_teachers_bp = Blueprint('admin_teachers', __name__)

@handle_exceptions
def get_teachers():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    teacher_service = TeacherService()
    teachers_data = teacher_service.get_all_teachers(page, per_page)
    current_app.logger.info(f"成功获取教师列表，第{page}页，每页{per_page}条")
    return success_response(teachers_data)

@handle_exceptions
def create_teacher():
    data, error = validate_json_input(['teacher_name', 'subject_id'])
    if error:
        return error
    teacher_name = data.get('teacher_name')
    subject_id = data.get('subject_id')
    password = data.get('password')
    if not teacher_name or not subject_id:
        return error_response("教师姓名和科目ID不能为空", 400)
    teacher_data = {
        'teacher_name': teacher_name,
        'subject_id': subject_id,
        'password': password
    }
    teacher_service = TeacherService()
    result = teacher_service.create_teacher(teacher_data)
    current_app.logger.info(f"成功创建教师: {teacher_name}")
    return success_response(result, 201)

@handle_exceptions
def get_teacher(teacher_id):
    teacher_service = TeacherService()
    teacher_data = teacher_service.get_teacher_by_id(teacher_id)
    if not teacher_data:
        current_app.logger.warning(f"教师未找到，ID: {teacher_id}")
        return error_response("教师不存在", 404)
    current_app.logger.info(f"成功获取教师信息，ID: {teacher_id}")
    return success_response(teacher_data)

@handle_exceptions
def update_teacher(teacher_id):
    data, error = validate_json_input(required_fields=[], allow_empty=True)
    if error:
        return error
    update_data = {}
    if 'teacher_name' in data:
        update_data['teacher_name'] = data['teacher_name']
    if 'subject_id' in data:
        update_data['subject_id'] = data['subject_id']
    if 'password' in data:
        update_data['password'] = data['password']
    teacher_service = TeacherService()
    result = teacher_service.update_teacher(teacher_id, update_data)
    if not result:
        current_app.logger.warning(f"教师未找到，ID: {teacher_id}")
        return error_response("教师不存在", 404)
    current_app.logger.info(f"成功更新教师信息，ID: {teacher_id}")
    return success_response({"message": "教师信息更新成功"})

@handle_exceptions
def delete_teacher(teacher_id):
    teacher_service = TeacherService()
    result = teacher_service.delete_teacher(teacher_id)
    if not result:
        current_app.logger.warning(f"教师未找到，ID: {teacher_id}")
        return error_response("教师不存在", 404)
    current_app.logger.info(f"成功删除教师，ID: {teacher_id}")
    return success_response({"message": "教师删除成功"})

admin_teachers_bp.add_url_rule('/', view_func=get_teachers, methods=['GET'])
admin_teachers_bp.add_url_rule('/', view_func=create_teacher, methods=['POST'])
admin_teachers_bp.add_url_rule('/<teacher_id>', view_func=get_teacher, methods=['GET'])
admin_teachers_bp.add_url_rule('/<teacher_id>', view_func=update_teacher, methods=['PUT'])
admin_teachers_bp.add_url_rule('/<teacher_id>', view_func=delete_teacher, methods=['DELETE'])