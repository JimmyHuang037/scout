from apps.services import TeacherService
from apps.utils.helpers import success_response, error_response
from flask import request, current_app

def get_teachers():
    """
    获取所有教师列表
    
    Returns:
        JSON: 教师列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 调用服务获取教师列表
        teacher_service = TeacherService()
        teachers_data = teacher_service.get_all_teachers(page, per_page)
        
        # 记录成功日志
        current_app.logger.info(f"成功获取教师列表，第{page}页，每页{per_page}条")
        
        return success_response(teachers_data)
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"获取教师列表时发生错误: {str(e)}")
        return error_response("获取教师列表失败", 500)


def create_teacher():
    """
    创建教师
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("请求数据不能为空", 400)
        
        teacher_name = data.get('teacher_name')
        subject_id = data.get('subject_id')
        password = data.get('password')
        
        # 检查必填字段
        if not teacher_name:
            return error_response("教师姓名不能为空", 400)
        
        # 准备教师数据字典
        teacher_data = {
            'teacher_name': teacher_name,
            'subject_id': subject_id,
            'password': password
        }
        
        # 调用服务创建教师
        teacher_service = TeacherService()
        result = teacher_service.create_teacher(teacher_data)
        
        # 记录成功日志
        current_app.logger.info(f"成功创建教师: {teacher_name}")
        
        return success_response(result, 201)
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"创建教师时发生错误: {str(e)}")
        return error_response("创建教师失败", 500)


def get_teacher(teacher_id: int):
    """
    根据ID获取教师信息
    
    Args:
        teacher_id (int): 教师ID
        
    Returns:
        JSON: 教师信息
    """
    try:
        # 调用服务获取教师信息
        teacher_service = TeacherService()
        teacher_data = teacher_service.get_teacher_by_id(teacher_id)
        
        if not teacher_data:
            # 记录警告日志
            current_app.logger.warning(f"教师未找到，ID: {teacher_id}")
            return error_response("教师不存在", 404)
        
        # 记录成功日志
        current_app.logger.info(f"成功获取教师信息，ID: {teacher_id}")
        
        return success_response(teacher_data)
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"获取教师信息时发生错误: {str(e)}")
        return error_response("获取教师信息失败", 500)


def update_teacher(teacher_id: int):
    """
    更新教师信息
    
    Args:
        teacher_id (int): 教师ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("请求数据不能为空", 400)
        
        # 准备更新数据字典
        update_data = {}
        if 'teacher_name' in data:
            update_data['teacher_name'] = data['teacher_name']
        if 'subject_id' in data:
            update_data['subject_id'] = data['subject_id']
        if 'password' in data:
            update_data['password'] = data['password']
        
        # 调用服务更新教师
        teacher_service = TeacherService()
        result = teacher_service.update_teacher(teacher_id, update_data)
        
        if not result:
            # 记录警告日志
            current_app.logger.warning(f"教师未找到，ID: {teacher_id}")
            return error_response("教师不存在", 404)
        
        # 记录成功日志
        current_app.logger.info(f"成功更新教师信息，ID: {teacher_id}")
        
        return success_response({"message": "教师信息更新成功"})
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"更新教师信息时发生错误: {str(e)}")
        return error_response("更新教师信息失败", 500)


def delete_teacher(teacher_id: int):
    """
    删除教师
    
    Args:
        teacher_id (int): 教师ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 调用服务删除教师
        teacher_service = TeacherService()
        result = teacher_service.delete_teacher(teacher_id)
        
        if not result:
            # 记录警告日志
            current_app.logger.warning(f"教师未找到，ID: {teacher_id}")
            return error_response("教师不存在", 404)
        
        # 记录成功日志
        current_app.logger.info(f"成功删除教师，ID: {teacher_id}")
        
        return success_response({"message": "教师删除成功"})
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"删除教师时发生错误: {str(e)}")
        return error_response("删除教师失败", 500)