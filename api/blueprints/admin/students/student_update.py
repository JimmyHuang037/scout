from flask import Blueprint, jsonify, request
from ...extensions.database.database import get_db

admin_student_update_bp = Blueprint('admin_student_update', __name__, url_prefix='/api/admin')

@admin_student_update_bp.route('/students/<string:student_id>', methods=['PUT'])
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

@admin_student_update_bp.route('/students/<string:student_id>', methods=['DELETE'])
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