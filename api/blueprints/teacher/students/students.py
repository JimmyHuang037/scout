from flask import Blueprint, request
from .views import get_my_students

teacher_students_bp = Blueprint('teacher_students', __name__, url_prefix='/api/teacher')

@teacher_students_bp.route('/students', methods=['GET'])
def get_my_students_route():
    return get_my_students()
from ...extensions.database import get_db
from flask import jsonify

def get_my_students():
    """获取当前教师所教班级的学生信息"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # 在实际应用中，这里会从JWT token或session中获取当前教师ID
        # 这里假设教师ID为1
        current_teacher_id = 1
        
        # 分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        offset = (page - 1) * per_page
        
        # 获取该教师所教班级的学生总数
        cursor.execute("""
            SELECT COUNT(*) as count
            FROM Students s
            JOIN TeacherClasses tc ON s.class_id = tc.class_id
            WHERE tc.teacher_id = %s
        """, (current_teacher_id,))
        
        total = cursor.fetchone()['count']
        
        # 获取该教师所教班级的学生列表
        cursor.execute("""
            SELECT s.student_id, s.student_name, s.class_id, c.class_name
            FROM Students s
            JOIN Classes c ON s.class_id = c.class_id
            JOIN TeacherClasses tc ON s.class_id = tc.class_id
            WHERE tc.teacher_id = %s
            ORDER BY s.class_id, s.student_id
            LIMIT %s OFFSET %s
        """, (current_teacher_id, per_page, offset))
        
        students = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'data': students,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500