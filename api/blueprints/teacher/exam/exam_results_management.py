"""教师考试结果管理模块"""
from flask import Blueprint, request, jsonify, current_app
from utils.auth import role_required
from utils.helpers import success_response, error_response
from services.exam_service import ExamService

teacher_exam_results_bp = Blueprint('teacher_exam_results_bp', __name__)

@teacher_exam_results_bp.route('/exam/results', methods=['GET'])
@role_required('teacher')
def get_exam_results():
    try:
        # 获取当前教师ID
        teacher_id = request.user['user_id']
        
        # 获取查询参数
        exam_id = request.args.get('exam_id', type=int)
        
        # 获取考试结果
        results = ExamService.get_exam_results(exam_id, teacher_id)
        if results is not None:
            current_app.logger.info(f"Teacher {teacher_id} retrieved results for exam {exam_id}")
            return success_response(results)
        else:
            current_app.logger.warning(f"Teacher {teacher_id} attempted to access results for exam {exam_id} (not found or unauthorized)")
            return error_response('Exam results not found or access denied', 404)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch exam results: {str(e)}')
        return error_response('Failed to fetch exam results', 500)