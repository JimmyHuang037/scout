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
        name = data.get('name')
        
        # 验证必填字段
        if not name:
            return error_response("缺少必要字段", 400)
        
        # 创建科目
        subject = SubjectService.create_subject(name=name)
        
        current_app.logger.info(f'Admin created subject: {subject.id}')
        return success_response("科目创建成功", {"subject_id": subject.id})
    
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
        # 获取科目列表
        subjects = SubjectService.get_all_subjects()
        
        current_app.logger.info('Admin retrieved all subjects')
        return success_response("获取科目列表成功", subjects)
    
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
        subject = SubjectService.get_subject_by_id(subject_id)
        if not subject:
            return error_response("科目不存在", 404)
        
        current_app.logger.info(f'Admin retrieved subject: {subject_id}')
        return success_response("获取科目详情成功", subject)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve subject {subject_id}: {str(e)}')
        return error_response("获取科目详情失败", 500)


@auth_required
@role_required('admin')
def update_subject(subject_id):
    """
    更新科目信息
    
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
        name = data.get('name')
        
        # 验证必填字段
        if not name:
            return error_response("缺少必要字段", 400)
        
        # 更新科目
        updated_subject = SubjectService.update_subject(subject_id=subject_id, name=name)
        if not updated_subject:
            return error_response("科目不存在", 404)
        
        current_app.logger.info(f'Admin updated subject: {subject_id}')
        return success_response("科目更新成功", {"subject_id": updated_subject.id})
    
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
        result = SubjectService.delete_subject(subject_id)
        if not result:
            return error_response("科目不存在", 404)
        
        current_app.logger.info(f'Admin deleted subject: {subject_id}')
        return success_response("科目删除成功", {"subject_id": subject_id})
    
    except Exception as e:
        current_app.logger.error(f'Failed to delete subject {subject_id}: {str(e)}')
        return error_response("删除科目失败", 500)