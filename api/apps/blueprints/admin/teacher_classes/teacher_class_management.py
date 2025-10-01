from apps.services import TeacherClassService
from apps.utils.helpers import success_response, error_response
from flask import request, current_app, Blueprint

# 创建教师班级关联管理蓝图
admin_teacher_classes_bp = Blueprint('admin_teacher_classes', __name__, url_prefix='/teacher_classes')

"""教师班级关联管理模块，处理教师和班级关联相关的所有操作"""


@admin_teacher_classes_bp.route('/', methods=['POST'])
def create_teacher_class():
    """
    创建教师班级关联
    
    Returns:
        JSON: 创建结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        teacher_id = data.get('teacher_id')
        class_id = data.get('class_id')
        
        # 验证必要字段
        if teacher_id is None or class_id is None:
            return error_response("缺少必要字段", 400)
        
        # 创建教师班级关联
        teacher_class_service = TeacherClassService()
        try:
            teacher_class_service.create_teacher_class(teacher_id=teacher_id, class_id=class_id)
            current_app.logger.info(f'Admin created teacher-class association: {teacher_id}:{class_id}')
            return success_response({"teacher_id": teacher_id, "class_id": class_id}, "教师班级关联创建成功"), 201
        except Exception as e:
            if "Duplicate entry" in str(e):
                return error_response("教师班级关联已存在", 409)
            else:
                raise

    except Exception as e:
        current_app.logger.error(f'Failed to create teacher-class association: {str(e)}')
        return error_response("创建教师班级关联失败", 500)


@admin_teacher_classes_bp.route('/', methods=['GET'])
def get_teacher_classes():
    """
    获取所有教师班级关联列表
    
    Returns:
        JSON: 教师班级关联列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取教师班级关联列表
        teacher_class_service = TeacherClassService()
        teacher_classes_data = teacher_class_service.get_all_teacher_classes(page, per_page)
        
        current_app.logger.info('Admin retrieved all teacher-class associations')
        return success_response(teacher_classes_data)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve teacher-class associations: {str(e)}')
        return error_response("获取教师班级关联列表失败", 500)


@admin_teacher_classes_bp.route('/<int:teacher_class_id>', methods=['GET'])
def get_teacher_class(teacher_class_id):
    """
    获取单个教师班级关联信息
    
    Args:
        teacher_class_id (int): 教师班级关联ID
        
    Returns:
        JSON: 教师班级关联信息
    """
    try:
        # 获取教师班级关联信息
        teacher_class = TeacherClassService().get_teacher_class_by_id(teacher_class_id)
        if not teacher_class:
            return error_response("教师班级关联不存在", 404)
        
        current_app.logger.info(f'Admin retrieved teacher-class association: {teacher_class_id}')
        return success_response(teacher_class)
    
    except Exception as e:
        current_app.logger.error(f'Failed to retrieve teacher-class association {teacher_class_id}: {str(e)}')
        return error_response("获取教师班级关联信息失败", 500)


@admin_teacher_classes_bp.route('/<int:teacher_class_id>', methods=['PUT'])
def update_teacher_class(teacher_class_id):
    """
    更新教师班级关联信息
    
    Args:
        teacher_class_id (int): 教师班级关联ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 提取必要字段
        teacher_id = data.get('teacher_id')
        class_id = data.get('class_id')
        
        # 验证必要字段
        if teacher_id is None or class_id is None:
            return error_response("缺少必要字段", 400)
        
        # 更新教师班级关联
        teacher_class_service = TeacherClassService()
        result = teacher_class_service.update_teacher_class(teacher_class_id, teacher_id, class_id)
        
        if not result:
            return error_response("教师班级关联不存在", 404)
        
        current_app.logger.info(f'Admin updated teacher-class association: {teacher_class_id}')
        return success_response({"teacher_class_id": teacher_class_id}, "教师班级关联更新成功")
    
    except Exception as e:
        current_app.logger.error(f'Failed to update teacher-class association {teacher_class_id}: {str(e)}')
        return error_response("更新教师班级关联失败", 500)


@admin_teacher_classes_bp.route('/<int:teacher_class_id>', methods=['DELETE'])
def delete_teacher_class(teacher_class_id):
    """
    删除教师班级关联
    
    Args:
        teacher_class_id (int): 教师班级关联ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 删除教师班级关联
        result = TeacherClassService().delete_teacher_class(teacher_class_id)
        if not result:
            return error_response("教师班级关联不存在", 404)
        
        current_app.logger.info(f'Admin deleted teacher-class association: {teacher_class_id}')
        return success_response({"teacher_class_id": teacher_class_id}, "教师班级关联删除成功")
    
    except Exception as e:
        current_app.logger.error(f'Failed to delete teacher-class association {teacher_class_id}: {str(e)}')
        return error_response("删除教师班级关联失败", 500)