from .class_bp import get_class_endpoint
from .scores.score_bp import update_score, get_scores
from .students.student_bp import get_teacher_students, get_teacher_student
from .teacher_bp import get_teacher_classes, get_teacher_profile, get_class_students, get_teacher_all_classes_students
from flask import Blueprint
"""教师蓝图模块"""

teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')

# 导入教师相关路由

# 注册教师端点路由
teacher_bp.add_url_rule('/<string:teacher_id>/profile', view_func=get_teacher_profile, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/students', view_func=get_teacher_students, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/students/<string:student_id>', view_func=get_teacher_student, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/scores', view_func=get_scores, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/scores/<int:score_id>', view_func=update_score, methods=['PUT'])

# 注册班级管理路由（教师可访问）
teacher_bp.add_url_rule('/<string:teacher_id>/classes', view_func=get_teacher_classes, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/classes/<int:class_id>', view_func=get_class_endpoint, methods=['GET'])

# 为需要额外参数的函数创建包装函数
def _get_class_students_wrapper(teacher_id, class_id):
    return get_class_students(class_id, teacher_id)

def _get_all_classes_students_wrapper(teacher_id):
    return get_teacher_all_classes_students(teacher_id)

teacher_bp.add_url_rule('/<string:teacher_id>/classes/<int:class_id>/students', 
                       view_func=_get_class_students_wrapper, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/all_classes_students', 
                       view_func=_get_all_classes_students_wrapper, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/classes/students', 
                       view_func=_get_all_classes_students_wrapper, methods=['GET'])