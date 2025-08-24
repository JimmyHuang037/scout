# This file makes the directory a Python package
from flask import Blueprint, jsonify, request
from ...extensions.database.database import get_db

admin_teachers_bp = Blueprint('admin_teachers', __name__, url_prefix='/api/admin')

@admin_teachers_bp.route('/teachers', methods=['GET'])
def get_teachers():
    """获取所有教师列表"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # 分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        offset = (page - 1) * per_page
        
        # 获取总数
        cursor.execute("SELECT COUNT(*) as count FROM Teachers")
        total = cursor.fetchone()['count']
        
        # 获取教师列表
        cursor.execute("""
            SELECT t.teacher_id, t.teacher_name, t.subject_id, s.subject_name
            FROM Teachers t
            LEFT JOIN Subjects s ON t.subject_id = s.subject_id
            ORDER BY t.teacher_id
            LIMIT %s OFFSET %s
        """, (per_page, offset))
        
        teachers = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'data': teachers,
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

@admin_teachers_bp.route('/teachers', methods=['POST'])
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