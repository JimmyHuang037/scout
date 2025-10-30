from flask import Blueprint, request, current_app
from apps.services.subject_service import SubjectService
from apps.utils.decorators import handle_exceptions
from apps.utils.responses import success_response, error_response
from apps.utils.validation import validate_json_input

admin_subjects_bp = Blueprint('admin_subjects', __name__)

@handle_exceptions
def get_subjects():
    subject_service = SubjectService()
    subjects_data = subject_service.get_all_subjects()
    current_app.logger.info("成功获取科目列表")
    return success_response({'subjects': subjects_data})

@handle_exceptions
def create_subject():
    data, error = validate_json_input(['subject_name'])
    if error:
        return error
    subject_name = data.get('subject_name')
    if not subject_name:
        return error_response("科目名称不能为空", 400)
    subject_data = {'subject_name': subject_name}
    subject_service = SubjectService()
    result = subject_service.create_subject(subject_data)
    current_app.logger.info(f"成功创建科目: {subject_name}")
    return success_response(result, 201)

@handle_exceptions
def get_subject(subject_id):
    subject_service = SubjectService()
    subject_data = subject_service.get_subject_by_id(subject_id)
    if not subject_data:
        current_app.logger.warning(f"科目未找到，ID: {subject_id}")
        return error_response("科目不存在", 404)
    current_app.logger.info(f"成功获取科目信息，ID: {subject_id}")
    return success_response(subject_data)

@handle_exceptions
def update_subject(subject_id):
    data, error = validate_json_input(['subject_name'])
    if error:
        return error
    subject_name = data.get('subject_name')
    if not subject_name:
        return error_response("科目名称不能为空", 400)
    subject_service = SubjectService()
    result = subject_service.update_subject(subject_id, {'subject_name': subject_name})
    if not result:
        current_app.logger.warning(f"科目未找到，ID: {subject_id}")
        return error_response("科目不存在", 404)
    current_app.logger.info(f"成功更新科目信息，ID: {subject_id}")
    return success_response({"message": "科目信息更新成功"})

@handle_exceptions
def delete_subject(subject_id):
    subject_service = SubjectService()
    result = subject_service.delete_subject(subject_id)
    if not result:
        current_app.logger.warning(f"科目未找到，ID: {subject_id}")
        return error_response("科目不存在", 404)
    current_app.logger.info(f"成功删除科目，ID: {subject_id}")
    return success_response({"message": "科目删除成功"})

admin_subjects_bp.add_url_rule('/', view_func=get_subjects, methods=['GET'])
admin_subjects_bp.add_url_rule('/', view_func=create_subject, methods=['POST'])
admin_subjects_bp.add_url_rule('/<subject_id>', view_func=get_subject, methods=['GET'])
admin_subjects_bp.add_url_rule('/<subject_id>', view_func=update_subject, methods=['PUT'])
admin_subjects_bp.add_url_rule('/<subject_id>', view_func=delete_subject, methods=['DELETE'])