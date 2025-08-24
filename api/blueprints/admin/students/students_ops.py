from flask import Blueprint, jsonify, request
from ...extensions.database.database import get_db
import mysql.connector

admin_students_ops_bp = Blueprint('admin_students_ops', __name__, url_prefix='/api/admin')

@admin_students_ops_bp.route('/students', methods=['POST'])
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