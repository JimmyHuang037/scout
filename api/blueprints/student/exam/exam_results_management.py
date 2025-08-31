from flask import Blueprint, request, jsonify, current_app
from utils.auth import role_required
from utils.helpers import success_response, error_response
from services.exam_service import ExamService

student_exam_results_bp = Blueprint('student_exam_results_bp', __name__)

@student_exam_results_bp.route('/exam/results', methods=['GET'])
@role_required('student')
def get_student_exam_results():
    try:
        # 获取当前学生ID
        student_id = request.user['user_id']
        
        # 获取查询参数
        exam_id = request.args.get('exam_id')
        
        if exam_id:
            # 获取特定考试的成绩
            results = ExamService.get_student_exam_result(student_id, exam_id)
            if results:
                current_app.logger.info(f"Student {student_id} retrieved results for exam {exam_id}")
                return success_response(results)
            else:
                current_app.logger.warning(f"Student {student_id} has no results for exam {exam_id}")
                return error_response('No results found', 404)
        else:
            # 获取所有考试成绩
            results = ExamService.get_student_all_exam_results(student_id)
            current_app.logger.info(f"Student {student_id} retrieved all exam results")
            return success_response(results)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch student exam results: {str(e)}')
        return error_response('Failed to fetch exam results', 500)