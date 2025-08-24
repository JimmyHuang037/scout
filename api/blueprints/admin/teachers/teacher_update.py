from flask import Blueprint, jsonify, request
from ...extensions.database.database import get_db

admin_teacher_update_bp = Blueprint('admin_teacher_update', __name__, url_prefix='/api/admin')

@admin_teacher_update_bp.route('/teachers/<int:teacher_id>', methods=['PUT'])
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

@admin_teacher_update_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
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