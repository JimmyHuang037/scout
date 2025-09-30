"""教师蓝图模块"""
from flask import Blueprint

teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')

# 导入教师相关路由
from .exam.exam_management import create_exam, get_exams as get_exam_list, get_exam, update_exam, delete_exam
from .exam.exam_class_management import get_exam_classes
from .exam.exam_results_management import get_exam_results
from .exam.performance_management import get_teacher_performance
from .students.student_management import get_teacher_students, get_teacher_student, update_teacher_student
from .scores.score_management import create_score, update_score, delete_score, get_scores, get_exam_scores
from .teacher_management import get_teacher_classes, get_teacher_exams, get_teacher_profile
from .class_management import get_classes, get_class_students
teacher_bp.add_url_rule('/<string:teacher_id>/profile', view_func=get_teacher_profile, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/exams', view_func=create_exam, methods=['POST'])
teacher_bp.add_url_rule('/<string:teacher_id>/exams', view_func=get_exam_list, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/exams/<int:exam_id>', view_func=get_exam, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/exams/<int:exam_id>', view_func=update_exam, methods=['PUT'])
teacher_bp.add_url_rule('/<string:teacher_id>/exams/<int:exam_id>', view_func=delete_exam, methods=['DELETE'])
teacher_bp.add_url_rule('/<string:teacher_id>/exam_classes', view_func=get_exam_classes, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/exam_results', view_func=get_exam_results, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/performance', view_func=get_teacher_performance, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/students', view_func=get_teacher_students, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/students/<int:student_id>', view_func=get_teacher_student, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/students/<int:student_id>', view_func=update_teacher_student, methods=['PUT'])
teacher_bp.add_url_rule('/<string:teacher_id>/scores', view_func=get_scores, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/scores', view_func=create_score, methods=['POST'])
teacher_bp.add_url_rule('/<string:teacher_id>/scores/<int:score_id>', view_func=update_score, methods=['PUT'])
teacher_bp.add_url_rule('/<string:teacher_id>/scores/<int:score_id>', view_func=delete_score, methods=['DELETE'])
teacher_bp.add_url_rule('/<string:teacher_id>/exams/<int:exam_id>/scores', view_func=get_exam_scores, methods=['GET'])

# 注册班级管理路由（教师可访问）
teacher_bp.add_url_rule('/<string:teacher_id>/classes', view_func=get_classes, methods=['GET'])
teacher_bp.add_url_rule('/<string:teacher_id>/classes/<int:class_id>/students', view_func=get_class_students, methods=['GET'])