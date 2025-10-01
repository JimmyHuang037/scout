from apps.services import StudentService
from apps.utils.helpers import success_response, error_response
from flask import request, current_app

def get_students():
    """
    获取所有学生列表
    
    Returns:
        JSON: 学生列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 调用服务获取学生列表
        student_service = StudentService()
        students_data = student_service.get_all_students(page, per_page)
        
        # 记录成功日志
        current_app.logger.info(f"成功获取学生列表，第{page}页，每页{per_page}条")
        
        return success_response(students_data)
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"获取学生列表时发生错误: {str(e)}")
        return error_response("获取学生列表失败", 500)


def create_student():
    """
    创建学生
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("请求数据不能为空", 400)
        
        student_id = data.get('student_id')
        student_name = data.get('student_name')
        class_id = data.get('class_id')
        password = data.get('password')
        
        # 检查必填字段
        if not student_id or not student_name or not class_id:
            return error_response("学生ID、学生姓名和班级ID不能为空", 400)
        
        # 准备学生数据字典
        student_data = {
            'student_id': student_id,
            'student_name': student_name,
            'class_id': class_id,
            'password': password
        }
        
        # 调用服务创建学生
        student_service = StudentService()
        result = student_service.create_student(student_data)
        
        # 记录成功日志
        current_app.logger.info(f"成功创建学生: {student_name}")
        
        return success_response(result, 201)
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"创建学生时发生错误: {str(e)}")
        return error_response("创建学生失败", 500)


def get_student(student_id):
    """
    根据ID获取学生信息
    
    Args:
        student_id (str): 学生ID
        
    Returns:
        JSON: 学生信息
    """
    try:
        # 调用服务获取学生信息
        student_service = StudentService()
        student_data = student_service.get_student_by_id(student_id)
        
        if not student_data:
            # 记录警告日志
            current_app.logger.warning(f"学生未找到，ID: {student_id}")
            return error_response("学生不存在", 404)
        
        # 记录成功日志
        current_app.logger.info(f"成功获取学生信息，ID: {student_id}")
        
        return success_response(student_data)
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"获取学生信息时发生错误: {str(e)}")
        return error_response("获取学生信息失败", 500)


def update_student(student_id):
    """
    更新学生信息
    
    Args:
        student_id (str): 学生ID
        
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
        if 'student_name' in data:
            update_data['student_name'] = data['student_name']
        if 'class_id' in data:
            update_data['class_id'] = data['class_id']
        if 'password' in data:
            update_data['password'] = data['password']
        
        # 调用服务更新学生
        student_service = StudentService()
        result = student_service.update_student(student_id, update_data)
        
        if not result:
            # 记录警告日志
            current_app.logger.warning(f"学生未找到，ID: {student_id}")
            return error_response("学生不存在", 404)
        
        # 记录成功日志
        current_app.logger.info(f"成功更新学生信息，ID: {student_id}")
        
        return success_response({"message": "学生信息更新成功"})
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"更新学生信息时发生错误: {str(e)}")
        return error_response("更新学生信息失败", 500)


def delete_student(student_id):
    """
    删除学生
    
    Args:
        student_id (str): 学生ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 调用服务删除学生
        student_service = StudentService()
        result = student_service.delete_student(student_id)
        
        if not result:
            # 记录警告日志
            current_app.logger.warning(f"学生未找到，ID: {student_id}")
            return error_response("学生不存在", 404)
        
        # 记录成功日志
        current_app.logger.info(f"成功删除学生，ID: {student_id}")
        
        return success_response({"message": "学生删除成功"})
        
    except Exception as e:
        # 记录错误日志
        current_app.logger.error(f"删除学生时发生错误: {str(e)}")
        return error_response("删除学生失败", 500)