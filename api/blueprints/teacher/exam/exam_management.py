"""考试管理模块，处理考试相关操作"""
from flask import jsonify, request, session
from utils.helpers import success_response, error_response, auth_required, role_required
from utils.logger import app_logger
from services.exam_service import ExamService


@auth_required
@role_required('teacher')
def get_exams():
    """获取教师相关的考试列表"""
    try:
        # 从session中获取当前教师ID
        current_teacher_id = session.get('user_id')
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用考试服务获取考试列表
        exam_service = ExamService()
        result = exam_service.get_exams_by_teacher(current_teacher_id, page, per_page)
        
        app_logger.info(f"Teacher {current_teacher_id} retrieved exams")
        return success_response(result)
        
    except Exception as e:
        app_logger.error(f"Failed to fetch exams: {str(e)}")
        return error_response(f'Failed to fetch exams: {str(e)}', 500)


@auth_required
@role_required('teacher')
def create_exam():
    """创建考试"""
    try:
        data = request.get_json()
        exam_name = data.get('exam_name')
        subject_id = data.get('subject_id')
        class_id = data.get('class_id')
        exam_type_id = data.get('exam_type_id')
        exam_date = data.get('exam_date')
        
        if not all([exam_name, subject_id, class_id, exam_type_id, exam_date]):
            app_logger.warning("Create exam attempt with missing fields")
            return error_response('Missing required fields', 400)
        
        # 从session中获取当前教师ID
        current_teacher_id = session.get('user_id')
        
        # 使用考试服务创建考试
        exam_service = ExamService()
        exam_data = {
            'exam_name': exam_name,
            'subject_id': subject_id,
            'class_id': class_id,
            'exam_type_id': exam_type_id,
            'exam_date': exam_date,
            'teacher_id': current_teacher_id
        }
        result = exam_service.create_exam(exam_data)
        
        if result:
            app_logger.info(f"Teacher {current_teacher_id} created exam: {exam_name}")
            return success_response(result, 'Exam created successfully', 201)
        else:
            app_logger.error("Failed to create exam")
            return error_response('Failed to create exam', 400)
            
    except Exception as e:
        app_logger.error(f"Failed to create exam: {str(e)}")
        return error_response(f'Failed to create exam: {str(e)}', 500)


@auth_required
@role_required('teacher')
def get_exam(exam_id):
    """获取特定考试信息"""
    try:
        # 从session中获取当前教师ID
        current_teacher_id = session.get('user_id')
        
        # 使用考试服务获取考试详情
        exam_service = ExamService()
        result = exam_service.get_exam_by_id_and_teacher(exam_id, current_teacher_id)
        
        if result:
            app_logger.info(f"Teacher {current_teacher_id} retrieved exam: {exam_id}")
            return success_response(result)
        else:
            app_logger.warning(f"Teacher {current_teacher_id} tried to access exam {exam_id} they don't own")
            return error_response('Exam not found', 404)
            
    except Exception as e:
        app_logger.error(f"Failed to fetch exam: {str(e)}")
        return error_response(f'Failed to fetch exam: {str(e)}', 500)


@auth_required
@role_required('teacher')
def update_exam(exam_id):
    """更新考试信息"""
    try:
        data = request.get_json()
        exam_name = data.get('exam_name')
        
        if not exam_name:
            app_logger.warning("Update exam attempt with missing fields")
            return error_response('Missing required fields', 400)
        
        # 从session中获取当前教师ID
        current_teacher_id = session.get('user_id')
        
        # 使用考试服务更新考试
        exam_service = ExamService()
        exam_data = {
            'exam_name': exam_name
        }
        result = exam_service.update_exam(exam_id, current_teacher_id, exam_data)
        
        if result:
            app_logger.info(f"Teacher {current_teacher_id} updated exam: {exam_id}")
            return success_response(result, 'Exam updated successfully')
        else:
            app_logger.warning(f"Teacher {current_teacher_id} tried to update exam {exam_id} they don't own")
            return error_response('Exam not found or update failed', 404)
            
    except Exception as e:
        app_logger.error(f"Failed to update exam: {str(e)}")
        return error_response(f'Failed to update exam: {str(e)}', 500)


@auth_required
@role_required('teacher')
def delete_exam(exam_id):
    """删除考试"""
    try:
        # 从session中获取当前教师ID
        current_teacher_id = session.get('user_id')
        
        # 使用考试服务删除考试
        exam_service = ExamService()
        result = exam_service.delete_exam(exam_id, current_teacher_id)
        
        if result:
            app_logger.info(f"Teacher {current_teacher_id} deleted exam: {exam_id}")
            return success_response(result, 'Exam deleted successfully')
        else:
            app_logger.warning(f"Teacher {current_teacher_id} tried to delete exam {exam_id} they don't own")
            return error_response('Exam not found or delete failed', 404)
            
    except Exception as e:
        app_logger.error(f"Failed to delete exam: {str(e)}")
        return error_response(f'Failed to delete exam: {str(e)}', 500)