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
        teacher_class_service = TeacherClassService()
        teacher_class = teacher_class_service.create_teacher_class(teacher_id=teacher_id, class_id=class_id)
        
        current_app.logger.info(f'Admin created teacher-class association: {teacher_id}:{class_id}')
        return success_response({"teacher_class_id": teacher_class}, "教师班级关联创建成功", 201)
    
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
        teacher_class_service = TeacherClassService()
        teacher_classes = teacher_class_service.get_all_teacher_classes(page, per_page)
        
        current_app.logger.info('Admin retrieved all teacher-class associations')
        return success_response(teacher_classes)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve teacher-class associations: {str(e)}')
        return error_response("获取教师班级关联列表失败", 500)


@auth_required
@role_required('admin')
def get_teacher_class(teacher_id=None, teacher_class_id=None):
    """
    根据ID获取教师班级关联信息
    
    Args:
        teacher_id (int): 教师ID
        teacher_class_id (int): 教师班级关联ID
        
    Returns:
        JSON: 教师班级关联信息
    """
    try:
        teacher_class_service = TeacherClassService()
        
        # 如果提供了teacher_id，则根据教师ID获取教师班级关联信息
        if teacher_id is not None:
            teacher_classes = teacher_class_service.get_teacher_class_by_teacher(teacher_id)
            if not teacher_classes:
                return error_response("教师班级关联不存在", 404)
            
            current_app.logger.info(f'Admin retrieved teacher-class associations for teacher: {teacher_id}')
            return success_response(teacher_classes)
        
        # 如果提供了teacher_class_id，则根据教师班级关联ID获取信息
        elif teacher_class_id is not None:
            teacher_class = teacher_class_service.get_teacher_class_by_id(teacher_class_id)
            if not teacher_class:
                return error_response("教师班级关联不存在", 404)
            
            current_app.logger.info(f'Admin retrieved teacher-class association: {teacher_class_id}')
            return success_response(teacher_class)
        
        # 如果都没有提供，则返回错误
        else:
            return error_response("缺少必要参数", 400)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve teacher-class association: {str(e)}')
        return error_response("获取教师班级关联信息失败", 500)


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
        teacher_class_service = TeacherClassService()
        updated_teacher_class = teacher_class_service.update_teacher_class(
            teacher_id=teacher_id,
            class_id=class_id,
            new_teacher_id=new_teacher_id
        )
        
        if not updated_teacher_class:
            return error_response("教师班级关联不存在", 404)
        
        current_app.logger.info(f"Admin updated teacher-class association: {teacher_id}:{class_id} -> {new_teacher_id}:{class_id}")
        return success_response({"teacher_class_id": updated_teacher_class}, "教师班级关联更新成功")
    
    except Exception as e:
        current_app.logger.error(f'Failed to update teacher-class association {teacher_class_id}: {str(e)}')
        return error_response("更新教师班级关联失败", 500)


@auth_required
@role_required('admin')
def delete_teacher_class(teacher_class_id=None, teacher_id=None, class_id=None):
    """
    删除教师班级关联
    
    Args:
        teacher_class_id (int): 教师班级关联ID
        teacher_id (int): 教师ID
        class_id (int): 班级ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 删除教师班级关联
        teacher_class_service = TeacherClassService()
        
        # 如果提供了teacher_id和class_id，则根据教师ID和班级ID删除
        if teacher_id is not None and class_id is not None:
            result = teacher_class_service.delete_teacher_class_by_teacher_and_class(teacher_id, class_id)
            if not result:
                return error_response("教师班级关联不存在", 404)
            
            current_app.logger.info(f'Admin deleted teacher-class association: {teacher_id}:{class_id}')
            return success_response({"teacher_id": teacher_id, "class_id": class_id}, "教师班级关联删除成功")
        
        # 如果提供了teacher_class_id，则根据教师班级关联ID删除
        elif teacher_class_id is not None:
            result = teacher_class_service.delete_teacher_class(teacher_class_id)
            if not result:
                return error_response("教师班级关联不存在", 404)
            
            current_app.logger.info(f'Admin deleted teacher-class association: {teacher_class_id}')
            return success_response({"teacher_class_id": teacher_class_id}, "教师班级关联删除成功")
        
        # 如果都没有提供，则返回错误
        else:
            return error_response("缺少必要参数", 400)
    
    except Exception as e:
        current_app.logger.error(f'Failed to delete teacher-class association: {str(e)}')
        return error_response("删除教师班级关联失败", 500)