"""班级管理模块，处理班级相关的所有操作"""
from flask import jsonify, request
from api.services import ClassService


def get_classes():
    """获取班级列表（带分页）"""
    try:
        # 分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用班级服务获取班级列表
        class_service = ClassService()
        result = class_service.get_all_classes(page, per_page)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch classes: {str(e)}'
        }), 500


def create_class():
    """创建班级"""
    try:
        data = request.get_json()
        
        class_service = ClassService()
        result = class_service.create_class(data)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Class created successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create class'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create class: {str(e)}'
        }), 500


def get_class(class_id):
    """获取班级详情"""
    try:
        class_service = ClassService()
        class_info = class_service.get_class_by_id(class_id)
        
        if class_info:
            return jsonify({
                'success': True,
                'data': class_info
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Class not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch class: {str(e)}'
        }), 500


def update_class(class_id):
    """更新班级信息"""
    try:
        data = request.get_json()
        
        class_service = ClassService()
        result = class_service.update_class(class_id, data)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Class updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update class'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update class: {str(e)}'
        }), 500


def delete_class(class_id):
    """删除班级"""
    try:
        class_service = ClassService()
        result = class_service.delete_class(class_id)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Class deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete class'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to delete class: {str(e)}'
        }), 500