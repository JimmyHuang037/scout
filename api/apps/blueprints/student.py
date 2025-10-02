from flask import Blueprint, request, current_app
from apps.utils.decorators import handle_exceptions
from apps.utils.responses import success_response, error_response
from apps.utils.validation import validate_json_input
from apps.services.student_service import StudentService
from apps.services.score_service import ScoreService

student_bp = Blueprint('student', __name__)


@handle_exceptions
def get_my_profile(student_id):
    student_service = StudentService()
    profile_data = student_service.get_student_profile(student_id)
    
    if not profile_data:
        return error_response('学生个人资料未找到', 404)
        
    current_app.logger.info(f"Student {student_id} profile retrieved")
    return success_response(profile_data)


@handle_exceptions
def get_my_scores(student_id):
    score_service = ScoreService()
    scores = score_service.get_student_scores(student_id)

    if not scores:
        return error_response('学生个人成绩未找到', 404)

    current_app.logger.info(f"Student {student_id} retrieved scores")
    return success_response(scores)


@handle_exceptions
def get_my_exam_results(student_id):
    # 首先检查学生是否存在
    student_service = StudentService()
    student_data = student_service.get_student_by_id(student_id)
    
    if not student_data:
        return error_response('学生未找到', 404)
        
    score_service = ScoreService()
    exam_results = score_service.get_student_exam_results(student_id)
    current_app.logger.info(f"Student {student_id} retrieved exam results")
    return success_response(exam_results)


student_bp.add_url_rule('/profile/<string:student_id>', view_func=get_my_profile, methods=['GET'])
student_bp.add_url_rule('/scores/<string:student_id>', view_func=get_my_scores, methods=['GET'])
student_bp.add_url_rule('/exam_results/<string:student_id>', view_func=get_my_exam_results, methods=['GET'])