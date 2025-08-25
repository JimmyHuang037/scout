"""教师成绩管理模块"""
from flask import Blueprint, jsonify, request, session
from utils.helpers import success_response, error_response
from utils.logger import app_logger
from utils.auth import require_auth, require_role
from utils import database_service


teacher_scores_bp = Blueprint('teacher_scores', __name__, url_prefix='/api/teacher')


@teacher_scores_bp.route('/scores', methods=['GET'])
def get_scores():
    """获取所教班级的成绩"""
    try:
        # 检查认证
        auth_error = require_auth()
        if auth_error:
            return auth_error
        
        # 从session中获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            return jsonify({
                'success': False,
                'error': 'User not authenticated'
            }), 401
        
        # 获取筛选参数
        student_id = request.args.get('student_id')
        subject_id = request.args.get('subject_id')
        exam_type_id = request.args.get('exam_type_id')
        
        # 使用数据库服务
        db_service = DatabaseService()
        
        # 构建查询
        query = """
            SELECT sc.score_id, sc.student_id, s.student_name, 
                   sc.subject_id, sub.subject_name,
                   sc.exam_type_id, et.exam_type_name, sc.score
            FROM Scores sc
            JOIN Students s ON sc.student_id = s.student_id
            JOIN Subjects sub ON sc.subject_id = sub.subject_id
            JOIN ExamTypes et ON sc.exam_type_id = et.type_id
            JOIN TeacherClasses tc ON s.class_id = tc.class_id
            WHERE tc.teacher_id = %s
        """
        
        # 添加筛选条件
        params = [current_teacher_id]
        if student_id:
            query += " AND sc.student_id = %s"
            params.append(student_id)
        if subject_id:
            query += " AND sc.subject_id = %s"
            params.append(subject_id)
        if exam_type_id:
            query += " AND sc.exam_type_id = %s"
            params.append(exam_type_id)
            
        query += " ORDER BY sc.student_id, sc.subject_id, sc.exam_type_id"
        
        # 执行查询
        results = db_service.execute_query(query, params)
        db_service.close()
        
        return jsonify({
            'success': True,
            'data': results
        })
        
    except Exception as e:
        # 确保数据库连接被关闭
        try:
            db_service.close()
        except:
            pass
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
