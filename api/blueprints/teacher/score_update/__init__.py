"""教师成绩更新蓝图模块"""
from flask import Blueprint, request, jsonify, session
from utils import database_service
from utils.helpers import success_response, error_response
from utils.logger import app_logger


score_update_bp = Blueprint('score_update_bp', __name__)


@score_update_bp.route('/scores/<int:score_id>', methods=['PUT'])
def update_score(score_id):
    """更新成绩"""
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
        score_value = data.get('score')
        
        if score_value is None:
            return jsonify({
                'success': False,
                'error': 'MISSING_FIELDS',
                'message': 'Missing score field',
                'code': 400
            }), 400
        
        # 检查教师是否有权限更新该成绩
        from services.teacher_service import TeacherService
        teacher_service = TeacherService()
        teacher_id = session.get('user_id')
        
        if not teacher_service.is_teacher_authorized_for_score(teacher_id, score_id):
            app_logger.warning(f"Teacher {teacher_id} attempted to update unauthorized score {score_id}")
            return jsonify({
                'success': False,
                'error': 'UNAUTHORIZED',
                'message': 'Not authorized to update this score',
                'code': 403
            }), 403
        
        # 更新成绩
        from services.score_service import ScoreService
        score_service = ScoreService()
        result = score_service.update_score(score_id, score_value)
        
        if result:
            app_logger.info(f"Teacher {teacher_id} updated score {score_id}")
            return success_response(result, "Score updated successfully")
        else:
            app_logger.error("Failed to update score")
            return error_response('UPDATE_FAILED', 'Failed to update score', 500)
            
    except Exception as e:
        app_logger.error(f'Failed to update score: {str(e)}')
        return error_response('INTERNAL_ERROR', f'Failed to update score: {str(e)}', 500)