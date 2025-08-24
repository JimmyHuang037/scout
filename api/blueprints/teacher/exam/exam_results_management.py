"""教师考试结果管理模块"""
from flask import jsonify, request, session
from services import ScoreService
from utils.logger import app_logger
from utils.helpers import success_response, error_response, require_auth


def get_exam_results():
    """获取考试结果"""
    try:
        # 检查认证
        auth_error = require_auth()
        if auth_error:
            return auth_error
            
        # 从session中获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return error_response('User not authenticated'), 401
        
        # 获取筛选参数
        exam_type_id = request.args.get('exam_type_id')
        class_id = request.args.get('class_id')
        
        # 使用成绩服务获取考试结果
        score_service = ScoreService()
        exam_results = score_service.get_exam_results(
            teacher_id=current_teacher_id,
            exam_type_id=exam_type_id,
            class_id=class_id
        )
        
        app_logger.info(f"Teacher {current_teacher_id} retrieved exam results")
        return success_response(exam_results)
        
    except Exception as e:
        app_logger.error(f"Failed to fetch exam results: {str(e)}")
        return error_response(f'Failed to fetch exam results: {str(e)}'), 500