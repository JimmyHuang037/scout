"""教师学生管理模块，处理教师查看学生信息相关操作"""
from flask import jsonify, request, session
from utils.helpers import success_response, error_response, auth_required, role_required
from utils.logger import app_logger
from utils import database_service
from services.student_service import StudentService


@auth_required
@role_required('teacher')
def get_my_students():
    """获取当前教师所教班级的学生列表"""
    try:
        # 从session中获取当前教师ID
        current_teacher_id = session.get('user_id')
        if not current_teacher_id:
            app_logger.warning("Teacher ID not found in session")  # 添加日志记录
            return error_response('User not authenticated'), 401
        
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用学生服务获取学生列表
        student_service = StudentService()
        # 这里我们直接使用数据库服务来获取教师相关的班级信息
        from utils import DatabaseService
        db_service = DatabaseService()
        
        try:
            offset = (page - 1) * per_page
            
            # 获取学生总数
            count_query = """
                SELECT COUNT(*) as count
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE tc.teacher_id = %s
            """
            total_result = db_service.execute_query(count_query, (current_teacher_id,), fetch_one=True)
            total = total_result['count'] if total_result else 0
            
            # 获取学生列表
            query = """
                SELECT s.student_id, s.student_name, c.class_id, c.class_name
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE tc.teacher_id = %s
                ORDER BY s.student_id
                LIMIT %s OFFSET %s
            """
            students = db_service.execute_query(query, (current_teacher_id, per_page, offset))
            
            result = {
                'students': students,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }
            
            app_logger.info(f"Teacher {current_teacher_id} retrieved their students")
            return success_response(result)
            
        finally:
            db_service.close()
        
    except Exception as e:
        app_logger.error(f"Failed to fetch students: {str(e)}")
        return error_response(f'Failed to fetch students: {str(e)}'), 500