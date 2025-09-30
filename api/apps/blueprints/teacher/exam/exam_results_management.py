"""教师考试结果管理模块"""
from flask import Blueprint, request, jsonify, current_app, session
from apps.utils.auth import role_required
from apps.utils.helpers import success_response, error_response
from apps.services.score_service import ScoreService

teacher_exam_results_bp = Blueprint('teacher_exam_results_bp', __name__)

@teacher_exam_results_bp.route('/exam/results', methods=['GET'])
@role_required('teacher')
def get_exam_results():
    try:
        # 获取当前教师ID
        teacher_id = session.get('user_id')
        
        # 获取查询参数
        exam_type_id = request.args.get('exam_type_id', type=int)
        class_id = request.args.get('class_id', type=int)
        
        # 获取考试结果
        score_service = ScoreService()
        results = score_service.get_exam_results(teacher_id, exam_type_id, class_id)
        if results is not None:
            current_app.logger.info(f"Teacher {teacher_id} retrieved exam results")
            return success_response(results)
        else:
            current_app.logger.warning(f"Teacher {teacher_id} attempted to access exam results (not found or unauthorized)")
            return error_response('Exam results not found or access denied', 404)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch exam results: {str(e)}')
        return error_response('Failed to fetch exam results', 500)