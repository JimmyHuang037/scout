"""考试管理模块，处理考试相关的所有操作"""
from flask import jsonify, request, session, current_app
from services import ExamService
from utils.helpers import success_response, error_response, auth_required, role_required


@auth_required
@role_required('teacher')
def create_exam():
    """
    创建考试
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return error_response("未授权访问", 401)
        
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 提取必要字段
        name = data.get('name')
        subject_id = data.get('subject_id')
        class_ids = data.get('class_ids', [])
        exam_type_id = data.get('exam_type_id')
        date = data.get('date')
        total_score = data.get('total_score')
        
        # 验证必填字段
        if not all([name, subject_id, class_ids, exam_type_id, date, total_score]):
            return error_response("缺少必要字段", 400)
        
        # 创建考试数据字典
        exam_data = {
            'name': name,
            'subject_id': subject_id,
            'class_ids': class_ids,
            'exam_type_id': exam_type_id,
            'date': date,
            'total_score': total_score,
            'creator_id': current_teacher_id
        }
        
        # 创建考试服务实例并调用create_exam方法
        exam_service = ExamService()
        exam = exam_service.create_exam(exam_data)
        
        current_app.logger.info(f"Teacher {current_teacher_id} created exam: {exam}")
        return success_response({"exam_id": exam}, "考试创建成功")
    
    except Exception as e:
        current_app.logger.error(f"Failed to create exam: {str(e)}")
        return error_response("创建考试失败", 500)


@auth_required
@role_required('teacher')
def get_exams():
    """
    获取教师的考试列表
    
    Returns:
        JSON: 考试列表
    """
    try:
        # 获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return error_response("未授权访问", 401)
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 创建考试服务实例并获取考试列表
        exam_service = ExamService()
        exams_data = exam_service.get_exams_by_teacher(current_teacher_id, page, per_page)
        
        current_app.logger.info(f"Teacher {current_teacher_id} retrieved exams list")
        return success_response(exams_data, "获取考试列表成功")
    
    except Exception as e:
        current_app.logger.error(f"Failed to retrieve exams: {str(e)}")
        return error_response("获取考试列表失败", 500)


@auth_required
@role_required('teacher')
def get_exam(exam_id):
    """
    获取考试详情
    
    Args:
        exam_id (int): 考试ID
        
    Returns:
        JSON: 考试详情
    """
    try:
        # 获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return error_response("未授权访问", 401)
        
        # 创建考试服务实例并获取考试详情
        exam_service = ExamService()
        exam = exam_service.get_exam_by_id_and_teacher(exam_id, current_teacher_id)
        
        current_app.logger.info(f"Teacher {current_teacher_id} retrieved exam {exam_id}")
        return success_response(exam, "获取考试详情成功")
    
    except Exception as e:
        current_app.logger.error(f"Failed to retrieve exam {exam_id}: {str(e)}")
        return error_response("获取考试详情失败", 500)


@auth_required
@role_required('teacher')
def update_exam(exam_id):
    """
    更新考试信息
    
    Args:
        exam_id (int): 考试ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return error_response("未授权访问", 401)
        
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 创建考试服务实例并更新考试
        exam_service = ExamService()
        result = exam_service.update_exam(exam_id, data, current_teacher_id)
        
        current_app.logger.info(f"Teacher {current_teacher_id} updated exam {exam_id}")
        return success_response(result, "考试更新成功")
    
    except Exception as e:
        current_app.logger.error(f"Failed to update exam {exam_id}: {str(e)}")
        return error_response("考试更新失败", 500)


@auth_required
@role_required('teacher')
def delete_exam(exam_id):
    """
    删除考试
    
    Args:
        exam_id (int): 考试ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return error_response("未授权访问", 401)
        
        # 创建考试服务实例并删除考试
        exam_service = ExamService()
        result = exam_service.delete_exam(exam_id, current_teacher_id)
        
        current_app.logger.info(f"Teacher {current_teacher_id} deleted exam {exam_id}")
        return success_response(result, "考试删除成功")
    
    except Exception as e:
        current_app.logger.error(f"Failed to delete exam {exam_id}: {str(e)}")
        return error_response("考试删除失败", 500)