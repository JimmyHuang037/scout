"""教师班级关联管理模块，处理教师班级关联相关的所有操作"""
from flask import jsonify, request
from api.services import TeacherClassService


def get_teacher_classes():
    """获取教师班级关联列表（带分页）"""
    try:
        # 分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用教师班级关联服务获取列表
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.get_all_teacher_classes(page, per_page)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch teacher classes: {str(e)}'
        }), 500


def create_teacher_class():
    """创建教师班级关联"""
    try:
        data = request.get_json()
        
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.create_teacher_class(data)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Teacher class association created successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create teacher class association'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create teacher class association: {str(e)}'
        }), 500


def get_teacher_class_by_teacher(teacher_id):
    """根据教师ID获取教师班级关联详情"""
    try:
        teacher_class_service = TeacherClassService()
        teacher_classes = teacher_class_service.get_teacher_classes_by_teacher_id(teacher_id)
        
        return jsonify({
            'success': True,
            'data': teacher_classes
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch teacher classes: {str(e)}'
        }), 500


def delete_teacher_class():
    """删除教师班级关联"""
    try:
        data = request.get_json()
        teacher_id = data.get('teacher_id')
        class_id = data.get('class_id')
        
        if not all([teacher_id, class_id]):
            return jsonify({
                'success': False,
                'error': 'Missing required fields: teacher_id, class_id'
            }), 400
        
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.delete_teacher_class(teacher_id, class_id)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Teacher class association deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete teacher class association'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to delete teacher class association: {str(e)}'
        }), 500