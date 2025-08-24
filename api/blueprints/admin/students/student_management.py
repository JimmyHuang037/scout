"""学生管理模块，处理学生相关的所有操作"""
from flask import jsonify, request
from api.services import StudentService


def get_students():
    """获取学生列表（带分页）"""
    try:
        # 分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用学生服务获取学生列表
        student_service = StudentService()
        result = student_service.get_all_students(page, per_page)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch students: {str(e)}'
        }), 500


def create_student():
    """创建学生"""
    try:
        data = request.get_json()
        
        student_service = StudentService()
        result = student_service.create_student(data)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Student created successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create student'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create student: {str(e)}'
        }), 500


def get_student(student_id):
    """获取学生详情"""
    try:
        student_service = StudentService()
        student = student_service.get_student_by_id(student_id)
        
        if student:
            return jsonify({
                'success': True,
                'data': student
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Student not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch student: {str(e)}'
        }), 500


def update_student(student_id):
    """更新学生信息"""
    try:
        data = request.get_json()
        
        student_service = StudentService()
        result = student_service.update_student(student_id, data)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Student updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update student'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update student: {str(e)}'
        }), 500


def delete_student(student_id):
    """删除学生"""
    try:
        student_service = StudentService()
        result = student_service.delete_student(student_id)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Student deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete student'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to delete student: {str(e)}'
        }), 500