"""成绩管理模块，处理成绩相关的所有操作"""
from flask import jsonify, request, session
from services import ScoreService
from utils.logger import app_logger
from utils.helpers import success_response, error_response, require_auth


def create_score():
    """录入成绩"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        subject_id = data.get('subject_id')
        exam_type_id = data.get('exam_type_id')
        score = data.get('score')
        
        if not all([student_id, subject_id, exam_type_id, score is not None]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: student_id, subject_id, exam_type_id, score'
            }), 400
        
        # 验证分数范围
        if not (0 <= score <= 100):
            return jsonify({
                'success': False,
                'error': 'Score must be between 0 and 100'
            }), 400
        
        # 检查认证
        auth_error = require_auth()
        if auth_error:
            return auth_error
        
        data = request.get_json()
        student_id = data.get('student_id')
        subject_id = data.get('subject_id')
        exam_type_id = data.get('exam_type_id')
        score = data.get('score')
        
        if not all([student_id, subject_id, exam_type_id, score is not None]):
            app_logger.warning("Create score attempt with missing fields")
            return error_response('Missing required fields: student_id, subject_id, exam_type_id, score'), 400
        
        # 验证分数范围
        if not (0 <= score <= 100):
            app_logger.warning(f"Create score attempt with invalid score: {score}")
            return error_response('Score must be between 0 and 100'), 400
        
        # 从session中获取当前教师ID
        current_teacher_id = session.get('user_id')
        score_service = ScoreService()
        # 检查学生是否在教师所教的班级中
        # 验证教师是否有权限为该学生录入成绩
        # 检查学生是否在教师所教的班级中
        if not score_service.is_student_in_teacher_class(student_id, current_teacher_id):
            app_logger.warning(f"Teacher {current_teacher_id} attempted to create score for student {student_id} not in their class")
            return error_response('You do not have permission to enter scores for this student'), 403
        
        # 录入成绩
        result = score_service.create_score(student_id, subject_id, exam_type_id, score)
        
        if result:
            app_logger.info(f"Teacher {current_teacher_id} created score for student {student_id}")
            return success_response(message='Score created successfully'), 201
        else:
            app_logger.error("Failed to create score")
            return error_response('Failed to create score'), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create score: {str(e)}'
        }), 500


def update_score(score_id):
    """更新成绩"""
    try:
        data = request.get_json()
        score = data.get('score')
        
        if score is None:
            return jsonify({
                'success': False,
                'error': 'Missing required field: score'
            }), 400
        
        # 验证分数范围
        if not (0 <= score <= 100):
            return jsonify({
                'success': False,
                'error': 'Score must be between 0 and 100'
            }), 400
        
        # 检查认证
        auth_error = require_auth()
        if auth_error:
            return auth_error
        
        data = request.get_json()
        score = data.get('score')
        
        if score is None:
            app_logger.warning("Update score attempt with missing score field")
            return error_response('Missing required field: score'), 400
        
        # 验证分数范围
        if not (0 <= score <= 100):
            app_logger.warning(f"Update score attempt with invalid score: {score}")
            return error_response('Score must be between 0 and 100'), 400
        
        # 从session中获取当前教师ID
        current_teacher_id = session.get('user_id')
        score_service = ScoreService()
        # 检查成绩是否属于教师所教的班级
        # 验证教师是否有权限更新该成绩
        # 检查成绩是否属于教师所教的班级
        if not score_service.is_score_in_teacher_class(score_id, current_teacher_id):
            app_logger.warning(f"Teacher {current_teacher_id} attempted to update score {score_id} not in their class")
            return error_response('You do not have permission to update this score'), 403
        
        # 更新成绩
        result = score_service.update_score(score_id, score)
        
        if result:
            app_logger.info(f"Teacher {current_teacher_id} updated score {score_id}")
            return success_response(message='Score updated successfully')
        else:
            app_logger.error("Failed to update score")
            return error_response('Failed to update score'), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update score: {str(e)}'
        }), 500