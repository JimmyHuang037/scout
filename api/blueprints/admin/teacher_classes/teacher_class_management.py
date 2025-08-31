"""教师班级关联管理模块，处理教师和班级关联相关的所有操作"""
from flask import jsonify, request, session, current_app
from services import TeacherClassService
from utils.helpers import success_response, error_response, auth_required, role_required


@auth_required
@role_required('admin')
def create_teacher_class():
    """
    创建教师班级关联
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 提取必要字段
        teacher_id = data.get('teacher_id')
        class_id = data.get('class_id')
        
        # 验证必填字段
        if not all([teacher_id, class_id]):
            return error_response("缺少必要字段", 400)
        
        # 创建教师班级关联
        teacher_class = TeacherClassService.create_teacher_class(teacher_id=teacher_id, class_id=class_id)
        
        current_app.logger.info(f'Admin created teacher-class association: {teacher_id}:{class_id}')
        return success_response("教师班级关联创建成功", {"teacher_class_id": teacher_class.id})
    
    except Exception as e:
        current_app.logger.error(f'Failed to create teacher-class association: {str(e)}')
        return error_response("创建教师班级关联失败", 500)


@auth_required
@role_required('admin')
def get_teacher_classes():
    """
    获取所有教师班级关联列表
    
    Returns:
        JSON: 教师班级关联列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取教师班级关联列表
        teacher_classes_data = TeacherClassService.get_all_teacher_classes(page, per_page)
        
        current_app.logger.info('Admin retrieved all teacher-class associations')
        return success_response("获取教师班级关联列表成功", teacher_classes_data)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve teacher-class associations: {str(e)}')
        return error_response("获取教师班级关联列表失败", 500)


@auth_required
@role_required('admin')
def get_teacher_class(teacher_class_id):
    """
    获取教师班级关联详情
    
    Args:
        teacher_class_id (int): 教师班级关联ID
        
    Returns:
        JSON: 教师班级关联详情
    """
    try:
        # 获取教师班级关联详情
        teacher_class = TeacherClassService.get_teacher_class_by_id(teacher_class_id)
        if not teacher_class:
            return error_response("教师班级关联不存在", 404)
        
        current_app.logger.info(f'Admin retrieved teacher-class association: {teacher_class_id}')
        return success_response("获取教师班级关联详情成功", teacher_class)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve teacher-class association {teacher_class_id}: {str(e)}')
        return error_response("获取教师班级关联详情失败", 500)


@auth_required
@role_required('admin')
def update_teacher_class(teacher_class_id):
    """
    更新教师班级关联信息
    
    Args:
        teacher_class_id (int): 教师班级关联ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 提取必要字段
        teacher_id = data.get('teacher_id')
        class_id = data.get('class_id')
        new_teacher_id = data.get('new_teacher_id')
        
        # 验证必填字段
        if not all([teacher_id, class_id]):
            current_app.logger.warning("Update teacher-class association attempt with missing fields")
            return error_response("缺少必要字段", 400)
        
        # 更新教师班级关联
        updated_teacher_class = TeacherClassService.update_teacher_class(
            teacher_class_id=teacher_class_id,
            teacher_id=teacher_id,
            class_id=class_id,
            new_teacher_id=new_teacher_id
        )
        
        if not updated_teacher_class:
            return error_response("教师班级关联不存在", 404)
        
        current_app.logger.info(f"Admin updated teacher-class association: {teacher_id}:{class_id} -> {new_teacher_id}:{class_id}")
        return success_response("教师班级关联更新成功", {"teacher_class_id": updated_teacher_class.id})
    
    except Exception as e:
        current_app.logger.error(f'Failed to update teacher-class association {teacher_class_id}: {str(e)}')
        return error_response("更新教师班级关联失败", 500)


@auth_required
@role_required('admin')
def delete_teacher_class(teacher_class_id):
    """
    删除教师班级关联
    
    Args:
        teacher_class_id (int): 教师班级关联ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 删除教师班级关联
        result = TeacherClassService.delete_teacher_class(teacher_class_id)
        if not result:
            return error_response("教师班级关联不存在", 404)
        
        current_app.logger.info(f'Admin deleted teacher-class association: {teacher_class_id}')
        return success_response("教师班级关联删除成功", {"teacher_class_id": teacher_class_id})
    
    except Exception as e:
        current_app.logger.error(f'Failed to delete teacher-class association {teacher_class_id}: {str(e)}')
        return error_response("删除教师班级关联失败", 500)