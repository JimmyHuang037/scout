"""科目管理模块，处理科目相关的所有操作"""
from flask import jsonify, request, session
from services import SubjectService
from utils.helpers import success_response, error_response, auth_required, role_required
from utils.logger import app_logger


@auth_required
@role_required('admin')
def get_subjects():
    """获取科目列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用科目服务获取科目列表
        subject_service = SubjectService()
        result = subject_service.get_all_subjects(page, per_page)
        
        app_logger.info("Admin retrieved subject list")
        return success_response(result)
        
    except Exception as e:
        app_logger.error(f'Failed to fetch subjects: {str(e)}')
        return error_response(f'Failed to fetch subjects: {str(e)}', 500)


@auth_required
@role_required('admin')
def create_subject():
    """创建科目"""
    try:
        data = request.get_json()
        subject_name = data.get('subject_name')
        
        if not subject_name:
            app_logger.warning("Create subject attempt with missing subject_name")
            return error_response('Missing required field: subject_name', 400)
        
        # 使用科目服务创建科目
        subject_service = SubjectService()
        subject_data = {
            'subject_name': subject_name
        }
        result = subject_service.create_subject(subject_data)  # 修复参数传递问题
        
        if result:
            app_logger.info("Admin created subject")
            return success_response({'message': 'Subject created successfully'}, 'Subject created successfully', 201)
        else:
            app_logger.error("Failed to create subject")
            return error_response('Failed to create subject', 400)
            
    except Exception as e:
        app_logger.error(f'Failed to create subject: {str(e)}')
        return error_response(f'Failed to create subject: {str(e)}', 500)


@auth_required
@role_required('admin')
def get_subject(subject_id):
    """获取单个科目信息"""
    try:
        # 使用科目服务获取科目信息
        subject_service = SubjectService()
        subject = subject_service.get_subject_by_id(subject_id)
        
        if subject:
            return success_response(subject)
        else:
            return error_response('Subject not found', 404)
            
    except Exception as e:
        return error_response(f'Failed to fetch subject: {str(e)}', 500)


@auth_required
@role_required('admin')
def update_subject(subject_id):
    """更新科目信息"""
    try:
        data = request.get_json()
        subject_name = data.get('subject_name')
        
        if not subject_name:
            return error_response('Missing required field: subject_name', 400)
        
        # 使用科目服务更新科目信息
        subject_service = SubjectService()
        result = subject_service.update_subject(subject_id, data)
        
        if result:
            return success_response(result, 'Subject updated successfully')
        else:
            return error_response('Failed to update subject', 400)
            
    except Exception as e:
        return error_response(f'Failed to update subject: {str(e)}', 500)


@auth_required
@role_required('admin')
def delete_subject(subject_id):
    """删除科目"""
    try:
        # 使用科目服务删除科目
        subject_service = SubjectService()
        result = subject_service.delete_subject(subject_id)
        
        if result:
            return success_response(None, 'Subject deleted successfully'), 204
        else:
            return error_response('Failed to delete subject', 400)
            
    except Exception as e:
        return error_response(f'Failed to delete subject: {str(e)}', 500)