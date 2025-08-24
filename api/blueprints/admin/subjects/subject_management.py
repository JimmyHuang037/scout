"""科目管理模块，处理科目相关的所有操作"""
from flask import jsonify, request
from api.services import SubjectService


def get_subjects():
    """获取科目列表（带分页）"""
    try:
        # 分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用科目服务获取科目列表
        subject_service = SubjectService()
        result = subject_service.get_all_subjects(page, per_page)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch subjects: {str(e)}'
        }), 500


def create_subject():
    """创建科目"""
    try:
        data = request.get_json()
        
        subject_service = SubjectService()
        result = subject_service.create_subject(data)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Subject created successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create subject'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create subject: {str(e)}'
        }), 500


def get_subject(subject_id):
    """获取科目详情"""
    try:
        subject_service = SubjectService()
        subject_info = subject_service.get_subject_by_id(subject_id)
        
        if subject_info:
            return jsonify({
                'success': True,
                'data': subject_info
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Subject not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch subject: {str(e)}'
        }), 500


def update_subject(subject_id):
    """更新科目信息"""
    try:
        data = request.get_json()
        
        subject_service = SubjectService()
        result = subject_service.update_subject(subject_id, data)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Subject updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update subject'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update subject: {str(e)}'
        }), 500


def delete_subject(subject_id):
    """删除科目"""
    try:
        subject_service = SubjectService()
        result = subject_service.delete_subject(subject_id)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Subject deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete subject'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to delete subject: {str(e)}'
        }), 500