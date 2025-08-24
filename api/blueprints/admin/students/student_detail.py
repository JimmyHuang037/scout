from flask import jsonify, request
from api.extensions.database.database import get_db

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
