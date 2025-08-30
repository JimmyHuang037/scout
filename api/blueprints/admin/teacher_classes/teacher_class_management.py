"""教师班级关联管理模块，处理教师班级关联相关的所有操作"""
from flask import jsonify, request, session
from services import TeacherClassService
from utils.helpers import success_response, error_response, auth_required, role_required
from utils.logger import app_logger


@auth_required
@role_required('admin')
def get_teacher_classes():
    """获取教师班级关联列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用教师班级服务获取教师班级关联列表
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.get_all_teacher_classes(page, per_page)
        
        app_logger.info("Admin retrieved teacher-class associations")
        return success_response(result)
        
    except Exception as e:
        app_logger.error(f'Failed to fetch teacher-class associations: {str(e)}')
        return error_response(f'Failed to fetch teacher-class associations: {str(e)}', 500)


@auth_required
@role_required('admin')
def create_teacher_class():
    """创建教师班级关联"""
    try:
        data = request.get_json()
        teacher_id = data.get('teacher_id')
        class_id = data.get('class_id')
        
        if not all([teacher_id, class_id]):
            app_logger.warning("Create teacher-class association attempt with missing fields")
            return error_response('Missing required fields: teacher_id, class_id', 400)
        
        # 使用教师班级服务创建教师班级关联
        teacher_class_service = TeacherClassService()
        # 修复参数传递问题，将参数封装成字典
        teacher_class_data = {
            'teacher_id': teacher_id,
            'class_id': class_id
        }
        result = teacher_class_service.create_teacher_class(teacher_class_data)
        
        if result:
            app_logger.info(f"Admin created teacher-class association: teacher_id={teacher_id}, class_id={class_id}")
            return success_response({'message': 'Teacher-class association created successfully'}, 'Teacher-class association created successfully', 201)
        else:
            app_logger.error("Failed to create teacher-class association")
            return error_response('Failed to create teacher-class association', 400)
            
    except Exception as e:
        app_logger.error(f'Failed to create teacher-class association: {str(e)}')
        return error_response(f'Failed to create teacher-class association: {str(e)}', 500)


@auth_required
@role_required('admin')
def get_teacher_class(teacher_id):
    """获取特定教师的班级关联"""
    try:
        # 使用教师班级服务获取教师班级关联详情
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.get_teacher_class_by_teacher(teacher_id)
        
        app_logger.info(f"Admin retrieved teacher-class associations for teacher_id={teacher_id}")
        return success_response(result)
        
    except Exception as e:
        app_logger.error(f'Failed to fetch teacher classes: {str(e)}')
        return error_response(f'Failed to fetch teacher classes: {str(e)}', 500)


@auth_required
@role_required('admin')
def update_teacher_class(teacher_id):
    """更新教师班级关联"""
    try:
        data = request.get_json()
        new_teacher_id = data.get('teacher_id')
        class_id = data.get('class_id')
        
        if not all([new_teacher_id, class_id]):
            app_logger.warning("Update teacher-class association attempt with missing fields")
            return error_response('Missing required fields: teacher_id, class_id', 400)
        
        # 使用教师班级服务更新教师班级关联
        teacher_class_service = TeacherClassService()
        # 先删除旧的关联
        delete_result = teacher_class_service.delete_teacher_class(teacher_id, class_id)
        
        if delete_result:
            # 创建新的关联
            teacher_class_data = {
                'teacher_id': new_teacher_id,
                'class_id': class_id
            }
            create_result = teacher_class_service.create_teacher_class(teacher_class_data)
            
            if create_result:
                app_logger.info(f"Admin updated teacher-class association: {teacher_id}:{class_id} -> {new_teacher_id}:{class_id}")
                return success_response(create_result, 'Teacher-class association updated successfully')
            else:
                # 如果创建新关联失败，尝试恢复旧关联
                teacher_class_service.create_teacher_class({
                    'teacher_id': teacher_id,
                    'class_id': class_id
                })
                app_logger.error("Failed to create new teacher-class association during update")
                return error_response('Failed to update teacher-class association', 400)
        else:
            app_logger.error("Failed to delete old teacher-class association during update")
            return error_response('Failed to update teacher-class association', 400)
            
    except Exception as e:
        app_logger.error(f'Failed to update teacher-class association: {str(e)}')
        return error_response(f'Failed to update teacher-class association: {str(e)}', 500)


@auth_required
@role_required('admin')
def delete_teacher_class(teacher_id):
    """删除教师班级关联"""
    try:
        data = request.get_json()
        class_id = data.get('class_id')
        
        if not class_id:
            app_logger.warning("Delete teacher-class association attempt with missing class_id")
            return error_response('Missing required field: class_id', 400)
        
        # 使用教师班级服务删除教师班级关联
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.delete_teacher_class(teacher_id, class_id)
        
        if result:
            app_logger.info(f"Admin deleted teacher-class association: teacher_id={teacher_id}, class_id={class_id}")
            return success_response(result, 'Teacher-class association deleted successfully')
        else:
            app_logger.error("Failed to delete teacher-class association")
            return error_response('Failed to delete teacher-class association', 400)
            
    except Exception as e:
        app_logger.error(f'Failed to delete teacher-class association: {str(e)}')
        return error_response(f'Failed to delete teacher-class association: {str(e)}', 500)