"""成绩管理模块，处理成绩相关的所有操作"""
from flask import Blueprint, request, jsonify, current_app
from utils.auth import role_required
from utils.helpers import success_response, error_response
from services.score_service import ScoreService

teacher_scores_bp = Blueprint('teacher_scores_bp', __name__)


@teacher_scores_bp.route('/scores', methods=['POST'])
@role_required('teacher')
def create_score():
    try:
        # 获取当前教师ID
        teacher_id = request.user['user_id']
        
        # 获取请求数据
        data = request.get_json()
        student_id = data.get('student_id')
        exam_id = data.get('exam_id')
        score = data.get('score')
        
        # 创建成绩
        new_score = ScoreService.create_score(student_id, exam_id, score, teacher_id)
        if new_score:
            current_app.logger.info(f"Teacher {teacher_id} created score for student {student_id}, exam {exam_id}")
            return success_response(new_score, 201)
        else:
            current_app.logger.warning(f"Teacher {teacher_id} failed to create score (unauthorized or invalid data)")
            return error_response('Failed to create score', 400)
    except Exception as e:
        current_app.logger.error(f'Failed to create score: {str(e)}')
        return error_response('Failed to create score', 500)


@teacher_scores_bp.route('/scores/<int:score_id>', methods=['PUT'])
@role_required('teacher')
def update_score(score_id):
    try:
        # 获取当前教师ID
        teacher_id = request.user['user_id']
        
        # 获取请求数据
        data = request.get_json()
        score = data.get('score')
        
        # 更新成绩
        updated_score = ScoreService.update_score(score_id, score, teacher_id)
        if updated_score:
            current_app.logger.info(f"Teacher {teacher_id} updated score {score_id}")
            return success_response(updated_score)
        else:
            current_app.logger.warning(f"Teacher {teacher_id} failed to update score {score_id} (not found or unauthorized)")
            return error_response('Failed to update score', 404)
    except Exception as e:
        current_app.logger.error(f'Failed to update score {score_id}: {str(e)}')
        return error_response('Failed to update score', 500)


@teacher_scores_bp.route('/scores/<int:score_id>', methods=['DELETE'])
@role_required('teacher')
def delete_score(score_id):
    try:
        # 获取当前教师ID
        teacher_id = request.user['user_id']
        
        # 删除成绩
        result = ScoreService.delete_score(score_id, teacher_id)
        if result:
            current_app.logger.info(f"Teacher {teacher_id} deleted score {score_id}")
            return success_response({'message': 'Score deleted successfully'})
        else:
            current_app.logger.warning(f"Teacher {teacher_id} failed to delete score {score_id} (not found or unauthorized)")
            return error_response('Failed to delete score', 404)
    except Exception as e:
        current_app.logger.error(f'Failed to delete score {score_id}: {str(e)}')
        return error_response('Failed to delete score', 500)


@teacher_scores_bp.route('/scores/exam/<int:exam_id>', methods=['GET'])
@role_required('teacher')
def get_exam_scores(exam_id):
    try:
        # 获取当前教师ID
        teacher_id = request.user['user_id']
        
        # 获取考试成绩
        scores = ScoreService.get_exam_scores(exam_id, teacher_id)
        if scores is not None:
            current_app.logger.info(f"Teacher {teacher_id} retrieved scores for exam {exam_id}")
            return success_response(scores)
        else:
            current_app.logger.warning(f"Teacher {teacher_id} attempted to access scores for exam {exam_id} (not found or unauthorized)")
            return error_response('Exam scores not found or access denied', 404)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch exam scores for exam {exam_id}: {str(e)}')
        return error_response('Failed to fetch exam scores', 500)


@teacher_scores_bp.route('/scores/exam/<int:exam_id>', methods=['PUT'])
@role_required('teacher')
def update_exam_scores(exam_id):
    try:
        # 获取当前教师ID
        teacher_id = request.user['user_id']
        
        # 获取请求数据
        data = request.get_json()
        scores = data.get('scores', [])
        
        # 更新考试成绩
        result = ScoreService.update_exam_scores(exam_id, scores, teacher_id)
        if result:
            current_app.logger.info(f"Teacher {teacher_id} updated scores for exam {exam_id}")
            return success_response({'message': 'Scores updated successfully'})
        else:
            current_app.logger.warning(f"Teacher {teacher_id} failed to update scores for exam {exam_id} (not found or unauthorized)")
            return error_response('Failed to update scores', 404)
    except Exception as e:
        current_app.logger.error(f'Failed to update exam scores for exam {exam_id}: {str(e)}')
        return error_response('Failed to update exam scores', 500)