"""学生考试结果管理模块"""
from flask import jsonify, request, session
from services import ScoreService
from utils.logger import app_logger
from utils.helpers import success_response, error_response, require_auth


def get_my_exam_results():
    """获取当前学生考试结果"""
    try:
        # 检查认证
        auth_error = require_auth()
        if auth_error:
            return auth_error
            
        # 从session中获取当前学生ID
        current_student_id = session.get('user_id')
        if not current_student_id:
            return error_response('User not authenticated'), 401
        
        # 获取筛选参数
        exam_type_id = request.args.get('exam_type_id')
        
        # 使用成绩服务获取考试结果
        score_service = ScoreService()
        exam_results = score_service.get_student_exam_results(
            student_id=current_student_id,
            exam_type_id=exam_type_id
        )
        
        app_logger.info(f"Student {current_student_id} retrieved their exam results")
        return success_response(exam_results)
        
    except Exception as e:
        app_logger.error(f"Failed to fetch exam results: {str(e)}")
        return error_response(f'Failed to fetch exam results: {str(e)}'), 500