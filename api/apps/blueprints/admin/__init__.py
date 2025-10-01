"""管理员蓝图模块"""
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# 导入学生管理相关路由
from .students.student_management import get_students, create_student, get_student, update_student, delete_student

# 导入教师管理相关路由
from .teachers.teacher_management import get_teachers, create_teacher, get_teacher, update_teacher, delete_teacher

# 导入班级管理相关路由
from .classes.class_management import get_classes, create_class, get_class, update_class, delete_class

# 导入科目管理相关路由
from .subjects.subject_management import get_subjects, create_subject, get_subject, update_subject, delete_subject

# 导入考试类型管理相关路由
from .exam_types.exam_type_management import get_exam_types, create_exam_type, get_exam_type, update_exam_type, delete_exam_type

# 导入教师班级关联管理相关路由
from .teacher_classes.teacher_class_management import get_teacher_classes, create_teacher_class, get_teacher_class, update_teacher_class, delete_teacher_class

# 注册学生管理路由
admin_bp.add_url_rule('/students', view_func=get_students, methods=['GET'])
admin_bp.add_url_rule('/students', view_func=create_student, methods=['POST'])
admin_bp.add_url_rule('/students/<string:student_id>', view_func=get_student, methods=['GET'])
admin_bp.add_url_rule('/students/<string:student_id>', view_func=update_student, methods=['PUT'])
admin_bp.add_url_rule('/students/<string:student_id>', view_func=delete_student, methods=['DELETE'])

# 注册教师管理路由
admin_bp.add_url_rule('/teachers', view_func=get_teachers, methods=['GET'])
admin_bp.add_url_rule('/teachers', view_func=create_teacher, methods=['POST'])
admin_bp.add_url_rule('/teachers/<int:teacher_id>', view_func=get_teacher, methods=['GET'])
admin_bp.add_url_rule('/teachers/<int:teacher_id>', view_func=update_teacher, methods=['PUT'])
admin_bp.add_url_rule('/teachers/<int:teacher_id>', view_func=delete_teacher, methods=['DELETE'])

# 注册班级管理路由
admin_bp.add_url_rule('/classes', view_func=get_classes, methods=['GET'])
admin_bp.add_url_rule('/classes', view_func=create_class, methods=['POST'])
admin_bp.add_url_rule('/classes/<int:class_id>', view_func=get_class, methods=['GET'])
admin_bp.add_url_rule('/classes/<int:class_id>', view_func=update_class, methods=['PUT'])
admin_bp.add_url_rule('/classes/<int:class_id>', view_func=delete_class, methods=['DELETE'])

# 注册科目管理路由
admin_bp.add_url_rule('/subjects', view_func=get_subjects, methods=['GET'])
admin_bp.add_url_rule('/subjects', view_func=create_subject, methods=['POST'])
admin_bp.add_url_rule('/subjects/<int:subject_id>', view_func=get_subject, methods=['GET'])
admin_bp.add_url_rule('/subjects/<int:subject_id>', view_func=update_subject, methods=['PUT'])
admin_bp.add_url_rule('/subjects/<int:subject_id>', view_func=delete_subject, methods=['DELETE'])

# 注册考试类型管理路由
admin_bp.add_url_rule('/exam-types', view_func=get_exam_types, methods=['GET'])
admin_bp.add_url_rule('/exam-types', view_func=create_exam_type, methods=['POST'])
admin_bp.add_url_rule('/exam-types/<int:exam_type_id>', view_func=get_exam_type, methods=['GET'])
admin_bp.add_url_rule('/exam-types/<int:exam_type_id>', view_func=update_exam_type, methods=['PUT'])
admin_bp.add_url_rule('/exam-types/<int:exam_type_id>', view_func=delete_exam_type, methods=['DELETE'])

# 注册教师班级关联管理路由
admin_bp.add_url_rule('/teacher-classes', view_func=get_teacher_classes, methods=['GET'])
admin_bp.add_url_rule('/teacher-classes', view_func=create_teacher_class, methods=['POST'])
admin_bp.add_url_rule('/teacher-classes/teacher/<int:teacher_id>', view_func=get_teacher_class, methods=['GET'])
admin_bp.add_url_rule('/teacher-classes/<int:teacher_class_id>', view_func=get_teacher_class, methods=['GET'])
admin_bp.add_url_rule('/teacher-classes/<int:teacher_id>/<int:class_id>', view_func=delete_teacher_class, methods=['DELETE'])
admin_bp.add_url_rule('/teacher-classes/<int:teacher_class_id>', view_func=update_teacher_class, methods=['PUT'])
admin_bp.add_url_rule('/teacher-classes/<int:teacher_class_id>', view_func=delete_teacher_class, methods=['DELETE'])