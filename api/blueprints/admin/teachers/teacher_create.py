from flask import Blueprint, jsonify, request
from ...extensions.database.database import get_db

admin_teacher_create_bp = Blueprint('admin_teacher_create', __name__, url_prefix='/api/admin')

@admin_teacher_create_bp.route('/teachers', methods=['POST'])
def create_teacher():
    """创建新教师"""
    try:
        data = request.get_json()
        teacher_name = data.get('teacher_name')
        subject_id = data.get('subject_id')
        
        if not teacher_name or not subject_id:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: teacher_name, subject_id'
            }), 400
        
        db = get_db()
        cursor = db.cursor()
        
        # 插入新教师
        cursor.execute("""
            INSERT INTO Teachers (teacher_name, subject_id)
            VALUES (%s, %s)
        """, (teacher_name, subject_id))
        
        db.commit()
        
        # 获取插入的教师ID
        teacher_id = cursor.lastrowid
        
        return jsonify({
            'success': True,
            'message': 'Teacher created successfully',
            'data': {
                'teacher_id': teacher_id,
                'teacher_name': teacher_name,
                'subject_id': subject_id
            }
        }), 201
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500