from flask import Blueprint, request, current_app
from apps.services.class_service import ClassService
from apps.utils.decorators import handle_exceptions
from apps.utils.responses import success_response, error_response
from apps.utils.validation import validate_json_input

admin_classes_bp = Blueprint('admin_classes', __name__)

@handle_exceptions
def get_classes():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    class_service = ClassService()
    classes_data = class_service.get_all_classes(page, per_page)
    current_app.logger.info(f"成功获取班级列表，第{page}页，每页{per_page}条")
    return success_response(classes_data)

@handle_exceptions
def create_class():
    data, error = validate_json_input(['class_name'])
    if error:
        return error
    class_name = data.get('class_name')
    if not class_name:
        return error_response("班级名称不能为空", 400)
    class_data = {'class_name': class_name}
    class_service = ClassService()
    result = class_service.create_class(class_data)
    current_app.logger.info(f"成功创建班级: {class_name}")
    return success_response(result, 201)

@handle_exceptions
def get_class(class_id: int):
    class_service = ClassService()
    class_data = class_service.get_class_by_id(class_id)
    if not class_data:
        current_app.logger.warning(f"班级未找到，ID: {class_id}")
        return error_response("班级不存在", 404)
    current_app.logger.info(f"成功获取班级信息，ID: {class_id}")
    return success_response(class_data)

@handle_exceptions
def update_class(class_id: int):
    data, error = validate_json_input(required_fields=[], allow_empty=True)
    if error:
        return error
    update_data = {}
    if 'class_name' in data:
        update_data['class_name'] = data['class_name']
    class_service = ClassService()
    result = class_service.update_class(class_id, update_data)
    if not result:
        current_app.logger.warning(f"班级未找到，ID: {class_id}")
        return error_response("班级不存在", 404)
    current_app.logger.info(f"成功更新班级信息，ID: {class_id}")
    return success_response({"message": "班级信息更新成功"})

@handle_exceptions
def delete_class(class_id: int):
    class_service = ClassService()
    result = class_service.delete_class(class_id)
    if not result:
        current_app.logger.warning(f"班级未找到，ID: {class_id}")
        return error_response("班级不存在", 404)
    current_app.logger.info(f"成功删除班级，ID: {class_id}")
    return success_response({"message": "班级删除成功"})

admin_classes_bp.add_url_rule('/', view_func=get_classes, methods=['GET'])
admin_classes_bp.add_url_rule('/', view_func=create_class, methods=['POST'])
admin_classes_bp.add_url_rule('/<int:class_id>', view_func=get_class, methods=['GET'])
admin_classes_bp.add_url_rule('/<int:class_id>', view_func=update_class, methods=['PUT'])
admin_classes_bp.add_url_rule('/<int:class_id>', view_func=delete_class, methods=['DELETE'])