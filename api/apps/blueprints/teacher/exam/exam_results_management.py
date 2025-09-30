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
        # 从session获取教师ID（保持原有身份验证）
        teacher_id = session.get('user_id')
        
        # 获取查询参数
        exam_type_id = request.args.get('exam_type_id', type=int)
        class_id = request.args.get('class_id', type=int)
        
        # 获取可选的teacher_id参数，如果提供了则使用它，否则使用session中的ID
        requested_teacher_id = request.args.get('teacher_id', type=int)
        
        # 安全性检查：只有管理员可以查询其他教师的数据，普通教师只能查询自己的数据
        query_teacher_id = requested_teacher_id if session.get('role') == 'admin' and requested_teacher_id else teacher_id
        
        # 获取考试结果
        score_service = ScoreService()
        results = score_service.get_exam_results(query_teacher_id, exam_type_id, class_id)
        if results is not None:
            current_app.logger.info(f"Teacher {teacher_id} retrieved exam results for teacher {query_teacher_id}")
            return success_response(results)
        else:
            current_app.logger.warning(f"Teacher {teacher_id} attempted to access exam results for teacher {query_teacher_id} (not found or unauthorized)")
            return error_response('Exam results not found or access denied', 404)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch exam results: {str(e)}')
        return error_response('Failed to fetch exam results', 500)