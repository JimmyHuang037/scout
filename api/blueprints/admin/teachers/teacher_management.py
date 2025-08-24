"""教师管理模块，处理教师相关的所有操作"""
from flask import jsonify, request
from api.services import TeacherService


def get_teachers():
    """获取教师列表（带分页）"""
    try:
        # 分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用教师服务获取教师列表
        teacher_service = TeacherService()
        result = teacher_service.get_all_teachers(page, per_page)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch teachers: {str(e)}'
        }), 500


def create_teacher():
    """创建教师"""
    try:
        data = request.get_json()
        
        teacher_service = TeacherService()
        result = teacher_service.create_teacher(data)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Teacher created successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create teacher'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create teacher: {str(e)}'
        }), 500


def get_teacher(teacher_id):
    """获取教师详情"""
    try:
        teacher_service = TeacherService()
        teacher = teacher_service.get_teacher_by_id(teacher_id)
        
        if teacher:
            return jsonify({
                'success': True,
                'data': teacher
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Teacher not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch teacher: {str(e)}'
        }), 500


def update_teacher(teacher_id):
    """更新教师信息"""
    try:
        data = request.get_json()
        
        teacher_service = TeacherService()
        result = teacher_service.update_teacher(teacher_id, data)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Teacher updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update teacher'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update teacher: {str(e)}'
        }), 500


def delete_teacher(teacher_id):
    """删除教师"""
    try:
        teacher_service = TeacherService()
        result = teacher_service.delete_teacher(teacher_id)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Teacher deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete teacher'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to delete teacher: {str(e)}'
        }), 500