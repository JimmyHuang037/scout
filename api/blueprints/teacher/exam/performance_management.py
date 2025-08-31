"""教师考试表现管理模块"""
from flask import Blueprint, request, jsonify, current_app
from utils.auth import role_required
from utils.helpers import success_response, error_response
from services.exam_service import ExamService

teacher_performance_bp = Blueprint('teacher_performance_bp', __name__)

@teacher_performance_bp.route('/exam/performance', methods=['GET'])
@role_required('teacher')
def get_teacher_performance():
    try:
        # 获取当前教师ID
        teacher_id = request.user['user_id']
        
        # 获取查询参数
        class_id = request.args.get('class_id')
        subject_id = request.args.get('subject_id')
        
        # 获取教师表现数据
        performance = ExamService.get_teacher_performance(teacher_id, class_id, subject_id)
        current_app.logger.info(f"Teacher {teacher_id} retrieved performance data")
        return success_response(performance)
    except Exception as e:
        current_app.logger.error(f'Failed to fetch teacher performance: {str(e)}')
        return error_response('Failed to fetch performance data', 500)
