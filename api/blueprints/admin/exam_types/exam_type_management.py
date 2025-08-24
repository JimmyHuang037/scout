"""考试类型管理模块，处理考试类型相关的所有操作"""
from flask import jsonify, request
from api.services import ExamTypeService


def get_exam_types():
    """获取考试类型列表（带分页）"""
    try:
        # 分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用考试类型服务获取考试类型列表
        exam_type_service = ExamTypeService()
        result = exam_type_service.get_all_exam_types(page, per_page)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch exam types: {str(e)}'
        }), 500


def create_exam_type():
    """创建考试类型"""
    try:
        data = request.get_json()
        
        exam_type_service = ExamTypeService()
        result = exam_type_service.create_exam_type(data)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Exam type created successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create exam type'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to create exam type: {str(e)}'
        }), 500


def get_exam_type(type_id):
    """获取考试类型详情"""
    try:
        exam_type_service = ExamTypeService()
        exam_type_info = exam_type_service.get_exam_type_by_id(type_id)
        
        if exam_type_info:
            return jsonify({
                'success': True,
                'data': exam_type_info
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Exam type not found'
            }), 404
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to fetch exam type: {str(e)}'
        }), 500


def update_exam_type(type_id):
    """更新考试类型信息"""
    try:
        data = request.get_json()
        
        exam_type_service = ExamTypeService()
        result = exam_type_service.update_exam_type(type_id, data)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Exam type updated successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to update exam type'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to update exam type: {str(e)}'
        }), 500


def delete_exam_type(type_id):
    """删除考试类型"""
    try:
        exam_type_service = ExamTypeService()
        result = exam_type_service.delete_exam_type(type_id)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Exam type deleted successfully'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to delete exam type'
            }), 400
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to delete exam type: {str(e)}'
        }), 500