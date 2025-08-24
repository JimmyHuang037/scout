from flask import jsonify, request
from api.services import StudentService
import mysql.connector

def get_students():
    """获取所有学生列表"""
    db_service = None
    try:
        db_service = DatabaseService()
        
        # 分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        offset = (page - 1) * per_page
        
        # 获取总数
        total_result = db_service.execute_query("SELECT COUNT(*) as count FROM Students", fetch_one=True)
        total = total_result['count']
        
        # 获取学生列表
        students_query = """
            SELECT s.student_id, s.student_name, s.class_id, c.class_name
            FROM Students s
            JOIN Classes c ON s.class_id = c.class_id
            ORDER BY s.student_id
            LIMIT %s OFFSET %s
        """
        students = db_service.execute_query(students_query, (per_page, offset))
        
        return jsonify({
            'success': True,
            'data': {
                'students': students,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }
        })
        
    except mysql.connector.Error as e:
        return jsonify({
            'success': False,
            'error': f'Database error: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch students: {str(e)}'
        }), 500
    finally:


def create_student():
    """创建新学生"""
    try:
        data = request.get_json()
        student_id = data.get('student_id')
        student_name = data.get('student_name')
        class_id = data.get('class_id')
        
        if not student_id or not student_name or not class_id:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: student_id, student_name, class_id'
            }), 400
        
        db = get_db()
        cursor = db.cursor()
        
        # 插入新学生
        cursor.execute("""
            INSERT INTO Students (student_id, student_name, class_id)
            VALUES (%s, %s, %s)
        """, (student_id, student_name, class_id))
        
        db.commit()
        
        return jsonify({
            'success': True,
            'message': 'Student created successfully',
            'data': {
                'student_id': student_id,
                'student_name': student_name,
                'class_id': class_id
            }
        }), 201
    except mysql.connector.IntegrityError as e:
        return jsonify({
            'success': False,
            'error': 'Student ID already exists'
        }), 400
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500