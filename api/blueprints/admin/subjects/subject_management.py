"""科目管理模块，处理科目相关的所有操作"""
from flask import jsonify, request, session, current_app
from services import SubjectService
from utils.helpers import success_response, error_response, auth_required, role_required


@auth_required
@role_required('admin')
def create_subject():
    """
    创建科目
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 提取必要字段
        subject_name = data.get('subject_name') or data.get('name')
        
        # 验证必填字段
        if not subject_name:
            return error_response("缺少必要字段", 400)
        
        # 创建科目
        subject_service = SubjectService()
        subject_data = {'subject_name': subject_name}
        new_subject_id = subject_service.create_subject(subject_data)
        
        if not new_subject_id:
            return error_response("创建科目失败", 400)
        
        # 获取新创建的科目信息
        new_subject = subject_service.get_subject_by_id(new_subject_id)
        
        current_app.logger.info(f'Admin created subject: {new_subject_id}')
        return success_response(new_subject, "科目创建成功", 201)
    
    except Exception as e:
        current_app.logger.error(f'Failed to create subject: {str(e)}')
        return error_response("创建科目失败", 500)


@auth_required
@role_required('admin')
def get_subjects():
    """
    获取所有科目列表
    
    Returns:
        JSON: 科目列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取科目列表
        subject_service = SubjectService()
        subjects = subject_service.get_all_subjects(page, per_page)
        
        current_app.logger.info('Admin retrieved all subjects')
        return success_response(subjects)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve subjects: {str(e)}')
        return error_response("获取科目列表失败", 500)


@auth_required
@role_required('admin')
def get_subject(subject_id):
    """
    获取科目详情
    
    Args:
        subject_id (int): 科目ID
        
    Returns:
        JSON: 科目详情
    """
    try:
        # 获取科目详情
        subject_service = SubjectService()
        subject = subject_service.get_subject_by_id(subject_id)
        if not subject:
            return error_response("科目不存在", 404)
        
        current_app.logger.info(f'Admin retrieved subject: {subject_id}')
        return success_response(subject)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve subject {subject_id}: {str(e)}')
        return error_response("获取科目详情失败", 500)


@auth_required
@role_required('admin')
def update_subject(subject_id):
    """
    更新科目
    
    Args:
        subject_id (int): 科目ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 提取必要字段
        subject_name = data.get('subject_name') or data.get('name')
        
        # 验证必填字段
        if not subject_name:
            return error_response("缺少必要字段", 400)
        
        # 更新科目
        subject_service = SubjectService()
        subject_data = {'subject_name': subject_name}
        result = subject_service.update_subject(subject_id, subject_data)
        
        if not result:
            return error_response("科目不存在", 404)
        
        current_app.logger.info(f'Admin updated subject: {subject_id}')
        return success_response({"subject_id": subject_id}, "科目更新成功")
    
    except Exception as e:
        current_app.logger.error(f'Failed to update subject {subject_id}: {str(e)}')
        return error_response("更新科目失败", 500)


@auth_required
@role_required('admin')
def delete_subject(subject_id):
    """
    删除科目
    
    Args:
        subject_id (int): 科目ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 删除科目
        subject_service = SubjectService()
        result = subject_service.delete_subject(subject_id)
        if not result:
            return error_response("科目不存在", 404)
        
        current_app.logger.info(f'Admin deleted subject: {subject_id}')
        return success_response({"subject_id": subject_id}, "科目删除成功")
    
    except Exception as e:
        current_app.logger.error(f'Failed to delete subject {subject_id}: {str(e)}')
        return error_response("删除科目失败", 500)