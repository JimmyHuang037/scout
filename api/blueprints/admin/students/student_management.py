"""学生管理模块，处理学生相关的所有操作"""
from flask import jsonify, request, session, current_app
from services import StudentService
from utils.helpers import success_response, error_response, auth_required, role_required


@auth_required
@role_required('admin')
def create_student():
    """
    创建学生账户
    
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
        email = data.get('email')
        class_id = data.get('class_id')
        
        # 验证必填字段
        if not all([name, email, class_id]):
            return error_response("缺少必要字段", 400)
        
        # 创建学生
        student = StudentService.create_student(name=name, email=email, class_id=class_id)
        
        current_app.logger.info(f'Admin created student: {student.id}')
        return success_response("学生创建成功", {"student_id": student.id})
    
    except Exception as e:
        current_app.logger.error(f'Failed to create student: {str(e)}')
        return error_response("创建学生失败", 500)


@auth_required
@role_required('admin')
def get_student(student_id):
    """
    获取学生详情
    
    Args:
        student_id (int): 学生ID
        
    Returns:
        JSON: 学生详情
    """
    try:
        # 获取学生详情
        student = StudentService.get_student_by_id(student_id)
        if not student:
            return error_response("学生不存在", 404)
        
        current_app.logger.info(f'Admin retrieved student: {student_id}')
        return success_response("获取学生详情成功", student)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve student {student_id}: {str(e)}')
        return error_response("获取学生详情失败", 500)


@auth_required
@role_required('admin')
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
        
        # 获取学生列表
        students_data = StudentService.get_all_students(page, per_page)
        
        current_app.logger.info('Admin retrieved all students')
        return success_response("获取学生列表成功", students_data)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve students: {str(e)}')
        return error_response("获取学生列表失败", 500)


@auth_required
@role_required('admin')
def update_student(student_id):
    """
    更新学生信息
    
    Args:
        student_id (int): 学生ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 更新学生
        updated_student = StudentService.update_student(
            student_id=student_id,
            name=data.get('name'),
            email=data.get('email'),
            class_id=data.get('class_id')
        )
        
        if not updated_student:
            return error_response("学生不存在", 404)
        
        current_app.logger.info(f'Admin updated student: {student_id}')
        return success_response("学生更新成功", {"student_id": updated_student.id})
    
    except Exception as e:
        current_app.logger.error(f'Failed to update student {student_id}: {str(e)}')
        return error_response("更新学生失败", 500)


@auth_required
@role_required('admin')
def delete_student(student_id):
    """
    删除学生
    
    Args:
        student_id (int): 学生ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 删除学生
        result = StudentService.delete_student(student_id)
        if not result:
            return error_response("学生不存在", 404)
        
        current_app.logger.info(f'Admin deleted student: {student_id}')
        return success_response("学生删除成功", {"student_id": student_id})
    
    except Exception as e:
        current_app.logger.error(f'Failed to delete student {student_id}: {str(e)}')
        return error_response("删除学生失败", 500)