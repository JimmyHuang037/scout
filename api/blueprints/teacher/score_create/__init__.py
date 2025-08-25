"""教师成绩录入蓝图模块"""
from flask import Blueprint, request, jsonify, session
from utils import database_service
from utils.helpers import success_response, error_response
from utils.logger import app_logger


score_create_bp = Blueprint('score_create_bp', __name__)


@score_create_bp.route('/scores', methods=['POST'])
def create_score():
    """录入成绩"""
    from utils.auth import require_auth, require_role
    
    # 应用认证和角色检查
    auth_result = require_auth()
    if auth_result is not None:
        return auth_result
        
    role_result = require_role('teacher')
    if role_result is not None:
        return role_result
        
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        subject_id = data.get('subject_id')
        exam_type_id = data.get('exam_type_id')
        score = data.get('score')
        
        if not all([student_id, subject_id, exam_type_id, score is not None]):
            return jsonify({
                'success': False,
                'error': 'MISSING_FIELDS',
                'message': 'Missing required fields',
                'code': 400
            }), 400
        
        # 检查教师是否有权限录入该学生的成绩
        from services.teacher_service import TeacherService
        teacher_service = TeacherService()
        teacher_id = session.get('user_id')
        
        if not teacher_service.is_teacher_authorized_for_student(teacher_id, student_id):
            app_logger.warning(f"Teacher {teacher_id} attempted to enter scores for unauthorized student {student_id}")
            return jsonify({
                'success': False,
                'error': 'UNAUTHORIZED',
                'message': 'Not authorized to enter scores for this student',
                'code': 403
            }), 403
        
        # 录入成绩
        from services.score_service import ScoreService
        score_service = ScoreService()
        result = score_service.create_score(student_id, subject_id, exam_type_id, score)
        
        if result:
            app_logger.info(f"Teacher {teacher_id} entered score for student {student_id}")
            return success_response(result, "Score created successfully", 201)
        else:
            app_logger.error("Failed to create score")
            return error_response('CREATE_FAILED', 'Failed to create score', 500)
            
    except Exception as e:
        app_logger.error(f'Failed to create score: {str(e)}')
        return error_response('INTERNAL_ERROR', f'Failed to create score: {str(e)}', 500)