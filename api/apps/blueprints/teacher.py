from flask import Blueprint, request, current_app
from apps.services import TeacherService, ScoreService
from apps.services.student_service import StudentService
from apps.services.class_service import ClassService
from apps.utils.decorators import handle_exceptions
from apps.utils.helpers import success_response, error_response


# 教师管理蓝图
teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')


@handle_exceptions
def get_teacher_profile(teacher_id):
    """获取指定教师的个人资料"""
    teacher_service = TeacherService()
    profile_data = teacher_service.get_teacher_profile(teacher_id)

    if not profile_data:
        return error_response('教师个人资料未找到', 404)

    current_app.logger.info(f"Teacher {teacher_id} profile retrieved")
    return success_response(profile_data)


@handle_exceptions
def get_teacher_scores(teacher_id):
    """
    获取成绩列表
    
    Args:
        teacher_id (string): 教师ID
        
    Returns:
        JSON: 成绩列表
    """
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 创建成绩服务实例并获取成绩列表
    score_service = ScoreService()
    scores_data = score_service.get_teacher_scores(teacher_id, page, per_page)
    
    current_app.logger.info(f"Teacher {teacher_id} retrieved scores list")
    return success_response(scores_data)


@handle_exceptions
def update_score(teacher_id, score_id):
    """
    更新成绩记录
    
    Args:
        teacher_id (string): 教师ID
        score_id (int): 成绩ID
        
    Returns:
        JSON: 更新结果
    """
    # 获取请求数据
    data = request.get_json()
    if not data:
        return error_response("无效的请求数据", 400)
    
    # 创建成绩服务实例并更新成绩
    score_service = ScoreService()
    result = score_service.update_score(score_id, data)
    
    current_app.logger.info(f"Teacher {teacher_id} updated score {score_id}")
    return success_response(result)


@handle_exceptions
def get_classes(teacher_id):
    # 获取教师班级列表
    classes = TeacherService().get_teacher_classes(teacher_id)
    current_app.logger.info(f"Teacher {teacher_id} retrieved classes")
    return success_response(classes)


@handle_exceptions
def get_class_students(teacher_id, class_id):
    # 获取班级学生列表
    students = ClassService().get_students_by_class(class_id, teacher_id)
    current_app.logger.info(f"Teacher {teacher_id} retrieved students for class {class_id}")
    return success_response(students)


@handle_exceptions
def get_class(teacher_id, class_id):
    # 获取班级信息
    # 先检查班级是否存在
    class_service = ClassService()
    class_data = class_service.get_class_by_id(class_id)
    if not class_data:
        return error_response('班级未找到', 404)
        
    # 验证该教师是否有权访问此班级
    # 这里简化处理，实际应该检查教师与班级的关联关系
    current_app.logger.info(f"Teacher {teacher_id} retrieved class {class_id}")
    return success_response(class_data)


@handle_exceptions
def get_teacher_students(teacher_id):
    # 获取查询参数
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # 获取教师学生列表
    students_data = StudentService().get_teacher_students(teacher_id, None, page, per_page)
    current_app.logger.info(f"Teacher {teacher_id} retrieved students")
    return success_response(students_data)


@handle_exceptions
def get_teacher_student(teacher_id, student_id):
    # 获取学生详情
    student_data = StudentService().get_student_by_id(student_id)
    if not student_data:
        return error_response('学生未找到', 404)
        
    current_app.logger.info(f"Teacher {teacher_id} retrieved student {student_id}")
    return success_response(student_data)


@handle_exceptions
def get_teacher_all_classes_students(teacher_id):
    """
    获取教师所有班级的学生列表
    
    Args:
        teacher_id (str): 教师ID
        
    Returns:
        JSON: 教师所有班级的学生列表
    """
    # 检查是否提供了teacher_id
    if teacher_id is None:
        return error_response('教师ID是必需的', 400)
        
    teacher_service = TeacherService()
    students_data = teacher_service.get_all_classes_students(teacher_id)
    
    return success_response(students_data)


@handle_exceptions
def get_teacher_class_students(teacher_id, class_id):
    """
    获取教师特定班级的学生列表
    
    Args:
        teacher_id (str): 教师ID
        class_id (str): 班级ID
        
    Returns:
        JSON: 教师特定班级的学生列表
    """
    # 检查是否提供了teacher_id
    if teacher_id is None:
        return error_response('教师ID是必需的', 400)
        
    # 检查是否提供了class_id
    if class_id is None:
        return error_response('班级ID是必需的', 400)
        
    # 使用ClassService获取班级学生列表
    class_service = ClassService()
    students_data = class_service.get_students_by_class(class_id, teacher_id)
    
    return success_response(students_data)


# 注册路由规则
teacher_bp.add_url_rule('/profile/<string:teacher_id>', view_func=get_teacher_profile, methods=['GET'])
teacher_bp.add_url_rule('/scores/<string:teacher_id>', view_func=get_teacher_scores, methods=['GET'])
teacher_bp.add_url_rule('/scores/<string:teacher_id>/<int:score_id>', view_func=update_score, methods=['PUT'])
teacher_bp.add_url_rule('/classes/<string:teacher_id>', view_func=get_classes, methods=['GET'])
teacher_bp.add_url_rule('/classes/<string:teacher_id>/<int:class_id>/students', view_func=get_class_students, methods=['GET'])
teacher_bp.add_url_rule('/classes/<string:teacher_id>/<int:class_id>', view_func=get_class, methods=['GET'])
teacher_bp.add_url_rule('/students/<string:teacher_id>', view_func=get_teacher_students, methods=['GET'])
teacher_bp.add_url_rule('/students/<string:teacher_id>/<string:student_id>', view_func=get_teacher_student, methods=['GET'])
teacher_bp.add_url_rule('/students/<string:teacher_id>/all_classes_students', view_func=get_teacher_all_classes_students, methods=['GET'])
teacher_bp.add_url_rule('/students/<string:teacher_id>/class/<string:class_id>', view_func=get_teacher_class_students, methods=['GET'])