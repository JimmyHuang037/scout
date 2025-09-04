"""成绩管理模块，处理成绩相关的所有操作"""
from flask import Blueprint, request, jsonify, current_app, session
from utils.auth import role_required
from utils.helpers import success_response, error_response
from services.score_service import ScoreService

teacher_scores_bp = Blueprint('teacher_scores_bp', __name__)


@teacher_scores_bp.route('/scores', methods=['GET'])
@role_required('teacher')
def get_scores():
    try:
        # 获取当前教师ID
        teacher_id = session.get('user_id')
        
        # 获取查询参数
        exam_id = request.args.get('exam_id', type=int)
        
        # 创建成绩服务实例
        score_service = ScoreService()
        
        # 获取成绩列表
        if exam_id:
            scores = score_service.get_exam_scores(exam_id, teacher_id)
        else:
            scores = score_service.get_teacher_scores(teacher_id)
            
        if scores is not None:
            current_app.logger.info(f"Teacher {teacher_id} retrieved scores")
            return success_response(scores)
        else:
            current_app.logger.warning(f"Teacher {teacher_id} failed to retrieve scores")
            return error_response('Failed to retrieve scores', 404)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch scores: {str(e)}')
        return error_response('Failed to fetch scores', 500)


@teacher_scores_bp.route('/scores', methods=['POST'])
@role_required('teacher')
def create_score():
    try:
        # 获取当前教师ID
        teacher_id = session.get('user_id')
        
        # 获取请求数据
        data = request.get_json()
        student_id = data.get('student_id')
        subject_id = data.get('subject_id')
        exam_type_id = data.get('exam_type_id')
        score = data.get('score')
        
        # 验证必填字段
        if not all([student_id, subject_id, exam_type_id, score]):
            return error_response('Missing required fields', 400)
        
        # 创建成绩服务实例
        score_service = ScoreService()
        
        # 创建成绩
        new_score = score_service.create_score(student_id, subject_id, exam_type_id, score)
        if new_score:
            current_app.logger.info(f"Teacher {teacher_id} created score for student {student_id}")
            return success_response({'message': 'Score created successfully'}, 201)
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
        teacher_id = session.get('user_id')
        
        # 获取请求数据
        data = request.get_json()
        score = data.get('score')
        
        # 创建成绩服务实例
        score_service = ScoreService()
        
        # 更新成绩
        updated_score = score_service.update_score(score_id, score)
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
        teacher_id = session.get('user_id')
        
        # 创建成绩服务实例
        score_service = ScoreService()
        
        # 删除成绩
        result = score_service.delete_score(score_id)
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
        teacher_id = session.get('user_id')
        
        # 创建成绩服务实例
        score_service = ScoreService()
        
        # 获取考试成绩
        scores = score_service.get_exam_scores(exam_id, teacher_id)
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
        teacher_id = session.get('user_id')
        
        # 获取请求数据
        data = request.get_json()
        scores_data = data.get('scores', [])
        
        # 创建成绩服务实例
        score_service = ScoreService()
        
        # 更新考试成绩
        updated_scores = score_service.update_exam_scores(exam_id, scores_data, teacher_id)
        if updated_scores is not None:
            current_app.logger.info(f"Teacher {teacher_id} updated scores for exam {exam_id}")
            return success_response(updated_scores)
        else:
            current_app.logger.warning(f"Teacher {teacher_id} failed to update scores for exam {exam_id} (not found or unauthorized)")
            return error_response('Failed to update exam scores', 404)
    except Exception as e:
        current_app.logger.error(f'Failed to update exam scores for exam {exam_id}: {str(e)}')
        return error_response('Failed to update exam scores', 500)