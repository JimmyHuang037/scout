"""考试类型管理模块，处理考试类型的增删改查操作"""
from flask import jsonify, request, session
from services.exam_type_service import ExamTypeService
from utils.helpers import success_response, error_response, auth_required, role_required
from utils.logger import app_logger


@auth_required
@role_required('admin')
def get_exam_types():
    """获取考试类型列表"""
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 使用考试类型服务获取考试类型列表
        exam_type_service = ExamTypeService()
        result = exam_type_service.get_all_exam_types(page, per_page)  # 修复方法名
        exam_type_service.db_service.close()  # 手动关闭数据库连接
        
        app_logger.info("Admin retrieved exam types")
        return success_response(result)
        
    except Exception as e:
        app_logger.error(f'Failed to fetch exam types: {str(e)}')
        return error_response(f'Failed to fetch exam types: {str(e)}', 500)


@auth_required
@role_required('admin')
def create_exam_type():
    """创建考试类型"""
    try:
        data = request.get_json()
        exam_type_name = data.get('exam_type_name')
        
        if not exam_type_name:
            return error_response('Missing required field: exam_type_name', 400)
        
        # 使用考试类型服务创建考试类型
        exam_type_service = ExamTypeService()
        exam_type_data = {'exam_type_name': exam_type_name}
        result = exam_type_service.create_exam_type(exam_type_data)
        exam_type_service.db_service.close()  # 手动关闭数据库连接
        
        if result:
            app_logger.info("Admin created exam type")
            return success_response(result, 'Exam type created successfully', 201)
        else:
            app_logger.error("Failed to create exam type")
            return error_response('Failed to create exam type', 400)
            
    except Exception as e:
        # 确保即使出现异常也关闭数据库连接
        try:
            exam_type_service.db_service.close()
        except:
            pass
        app_logger.error(f'Failed to create exam type: {str(e)}')
        return error_response(f'Failed to create exam type: {str(e)}', 500)


@auth_required
@role_required('admin')
def get_exam_type(exam_type_id):
    """获取考试类型详情"""
    try:
        # 使用考试类型服务获取考试类型信息
        exam_type_service = ExamTypeService()
        result = exam_type_service.get_exam_type_by_id(exam_type_id)
        exam_type_service.db_service.close()  # 手动关闭数据库连接
        
        if result:
            app_logger.info(f"Admin retrieved exam type {exam_type_id}")
            return success_response(result)
        else:
            app_logger.warning(f"Exam type {exam_type_id} not found")
            return error_response('Exam type not found', 404)
            
    except Exception as e:
        app_logger.error(f'Failed to fetch exam type: {str(e)}')
        return error_response(f'Failed to fetch exam type: {str(e)}', 500)


@auth_required
@role_required('admin')
def update_exam_type(exam_type_id):
    """更新考试类型"""
    try:
        data = request.get_json()
        exam_type_name = data.get('exam_type_name')  # 使用正确的字段名
        
        if not exam_type_name:
            return error_response('Missing required field: exam_type_name', 400)
        
        # 使用考试类型服务更新考试类型信息
        exam_type_service = ExamTypeService()
        result = exam_type_service.update_exam_type(exam_type_id, {'exam_type_name': exam_type_name})
        exam_type_service.db_service.close()  # 手动关闭数据库连接
        
        if result:
            return success_response({'message': 'Exam type updated successfully'}, 'Exam type updated successfully')
        else:
            return error_response('Failed to update exam type', 400)
            
    except Exception as e:
        return error_response(f'Failed to update exam type: {str(e)}', 500)


@auth_required
@role_required('admin')
def delete_exam_type(exam_type_id):
    """删除考试类型"""
    try:
        # 使用考试类型服务删除考试类型
        exam_type_service = ExamTypeService()
        result = exam_type_service.delete_exam_type(exam_type_id)
        exam_type_service.db_service.close()  # 手动关闭数据库连接
        
        if result:
            return success_response({'message': 'Exam type deleted successfully'}, 'Exam type deleted successfully')
        else:
            return error_response('Failed to delete exam type', 400)
            
    except Exception as e:
        # 确保即使出现异常也关闭数据库连接
        try:
            exam_type_service.db_service.close()
        except:
            pass
        return error_response(f'Failed to delete exam type: {str(e)}', 500)