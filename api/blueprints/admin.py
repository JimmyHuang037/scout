from flask import Blueprint, jsonify, request
from ..database import get_db
import mysql.connector

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# 学生管理API
@admin_bp.route('/students', methods=['GET'])
def get_students():
    """获取所有学生列表"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        # 分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        offset = (page - 1) * per_page
        
        # 获取总数
        cursor.execute("SELECT COUNT(*) as count FROM Students")
        total = cursor.fetchone()['count']
        
        # 获取学生列表
        cursor.execute("""
            SELECT s.student_id, s.student_name, s.class_id, c.class_name
            FROM Students s
            LEFT JOIN Classes c ON s.class_id = c.class_id
            ORDER BY s.student_id
            LIMIT %s OFFSET %s
        """, (per_page, offset))
        
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


@admin_bp.route('/students', methods=['POST'])
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


@admin_bp.route('/students/<string:student_id>', methods=['GET'])
def get_student(student_id):
    """获取特定学生信息"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT s.student_id, s.student_name, s.class_id, c.class_name
            FROM Students s
            LEFT JOIN Classes c ON s.class_id = c.class_id
            WHERE s.student_id = %s
        """, (student_id,))
        
        student = cursor.fetchone()
        
        if not student:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': student
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/students/<string:student_id>', methods=['PUT'])
def update_student(student_id):
    """更新学生信息"""
    try:
        data = request.get_json()
        student_name = data.get('student_name')
        class_id = data.get('class_id')
        
        if not student_name and not class_id:
            return jsonify({
                'success': False,
                'error': 'Nothing to update'
            }), 400
        
        db = get_db()
        cursor = db.cursor()
        
        # 更新学生信息
        update_fields = []
        params = []
        
        if student_name:
            update_fields.append("student_name = %s")
            params.append(student_name)
            
        if class_id:
            update_fields.append("class_id = %s")
            params.append(class_id)
            
        params.append(student_id)
        
        query = "UPDATE Students SET " + ", ".join(update_fields) + " WHERE student_id = %s"
        cursor.execute(query, params)
        
        if cursor.rowcount == 0:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        db.commit()
        
        return jsonify({
            'success': True,
            'message': 'Student updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/students/<string:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """删除学生"""
    try:
        db = get_db()
        cursor = db.cursor()
        
        # 删除学生
        cursor.execute("DELETE FROM Students WHERE student_id = %s", (student_id,))
        
        if cursor.rowcount == 0:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
        
        db.commit()
        
        return jsonify({
            'success': True,
            'message': 'Student deleted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# 教师管理API
@admin_bp.route('/teachers', methods=['GET'])
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


@admin_bp.route('/teachers', methods=['POST'])
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


@admin_bp.route('/teachers/<int:teacher_id>', methods=['GET'])
def get_teacher(teacher_id):
    """获取特定教师信息"""
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT t.teacher_id, t.teacher_name, t.subject_id, s.subject_name
            FROM Teachers t
            LEFT JOIN Subjects s ON t.subject_id = s.subject_id
            WHERE t.teacher_id = %s
        """, (teacher_id,))
        
        teacher = cursor.fetchone()
        
        if not teacher:
            return jsonify({
                'success': False,
                'error': 'Teacher not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': teacher
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/teachers/<int:teacher_id>', methods=['PUT'])
def update_teacher(teacher_id):
    """更新教师信息"""
    try:
        data = request.get_json()
        teacher_name = data.get('teacher_name')
        subject_id = data.get('subject_id')
        
        if not teacher_name and not subject_id:
            return jsonify({
                'success': False,
                'error': 'Nothing to update'
            }), 400
        
        db = get_db()
        cursor = db.cursor()
        
        # 更新教师信息
        update_fields = []
        params = []
        
        if teacher_name:
            update_fields.append("teacher_name = %s")
            params.append(teacher_name)
            
        if subject_id:
            update_fields.append("subject_id = %s")
            params.append(subject_id)
            
        params.append(teacher_id)
        
        query = "UPDATE Teachers SET " + ", ".join(update_fields) + " WHERE teacher_id = %s"
        cursor.execute(query, params)
        
        if cursor.rowcount == 0:
            return jsonify({
                'success': False,
                'error': 'Teacher not found'
            }), 404
        
        db.commit()
        
        return jsonify({
            'success': True,
            'message': 'Teacher updated successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@admin_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def delete_teacher(teacher_id):
    """删除教师"""
    try:
        db = get_db()
        cursor = db.cursor()
        
        # 删除教师
        cursor.execute("DELETE FROM Teachers WHERE teacher_id = %s", (teacher_id,))
        
        if cursor.rowcount == 0:
            return jsonify({
                'success': False,
                'error': 'Teacher not found'
            }), 404
        
        db.commit()
        
        return jsonify({
            'success': True,
            'message': 'Teacher deleted successfully'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500