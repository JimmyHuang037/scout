from flask import Blueprint, request, current_app
from apps.utils.decorators import handle_exceptions
from apps.utils.responses import success_response, error_response
from apps.utils.validation import validate_json_input
from apps.services.student_service import StudentService
from apps.services.score_service import ScoreService

student_bp = Blueprint('student', __name__)


@handle_exceptions
def get_my_profile(student_id):
    # 首先检查学生是否存在
    student_service = StudentService()
    student_data = student_service.get_student_by_id(student_id)
    
    if not student_data:
        return error_response('学生未找到', 404)
        
    profile_data = student_service.get_student_profile(student_id)
    
    if not profile_data:
        return error_response('学生个人资料未找到', 404)
        
    current_app.logger.info(f"Student {student_id} profile retrieved")
    return success_response(profile_data)


@handle_exceptions
def get_my_scores(student_id):
    # 首先检查学生是否存在
    student_service = StudentService()
    student_data = student_service.get_student_by_id(student_id)
    
    if not student_data:
        return error_response('学生未找到', 404)
        
    score_service = ScoreService()
    scores = score_service.get_student_scores(student_id)

    if not scores:
        return error_response('学生个人成绩未找到', 404)

    current_app.logger.info(f"Student {student_id} retrieved scores")
    return success_response(scores)


@handle_exceptions
def get_my_scores_chinese(student_id):
    # 首先检查学生是否存在
    student_service = StudentService()
    student_data = student_service.get_student_by_id(student_id)
    
    if not student_data:
        return error_response('学生未找到', 404)
        
    score_service = ScoreService()
    scores = score_service.get_student_scores_as_chinese_column(student_id)

    if not scores:
        return error_response('学生个人成绩未找到', 404)

    current_app.logger.info(f"Student {student_id} retrieved scores with Chinese column names")
    return success_response(scores)


@handle_exceptions
def get_my_exam_results(student_id):
    # 首先检查学生是否存在
    student_service = StudentService()
    student_data = student_service.get_student_by_id(student_id)
    
    # 不管学生是否存在都继续查询，因为exam_results视图可能有数据
    score_service = ScoreService()
    exam_results = score_service.get_student_exam_results(student_id)
    
    # 只有当没有考试结果且学生不存在时才返回404
    if not exam_results and not student_data:
        return error_response('学生未找到', 404)
        
    current_app.logger.info(f"Student {student_id} retrieved exam results")
    return success_response(exam_results)


student_bp.add_url_rule('/profile/<string:student_id>', view_func=get_my_profile, methods=['GET'])
student_bp.add_url_rule('/scores/<string:student_id>', view_func=get_my_scores, methods=['GET'])
student_bp.add_url_rule('/scores/chinese/<string:student_id>', view_func=get_my_scores_chinese, methods=['GET'])
student_bp.add_url_rule('/exam_results/<string:student_id>', view_func=get_my_exam_results, methods=['GET'])