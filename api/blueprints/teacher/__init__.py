"""教师蓝图模块"""
from flask import Blueprint

teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')

# 导入教师考试相关路由
from .exam.exam_management import create_exam, get_exams, get_exam, update_exam, delete_exam
from .exam.exam_class_management import get_teacher_classes
from .exam.exam_results_management import get_exam_results
from .exam.performance_management import get_teacher_performance
from .students.student_management import get_teacher_students
from .scores.score_management import create_score, update_score, delete_score

# 注册路由
teacher_bp.add_url_rule('/exams', view_func=create_exam, methods=['POST'])
teacher_bp.add_url_rule('/exams', view_func=get_exams, methods=['GET'])
teacher_bp.add_url_rule('/exams/<int:exam_id>', view_func=get_exam, methods=['GET'])
teacher_bp.add_url_rule('/exams/<int:exam_id>', view_func=update_exam, methods=['PUT'])
teacher_bp.add_url_rule('/exams/<int:exam_id>', view_func=delete_exam, methods=['DELETE'])
teacher_bp.add_url_rule('/exam-class', view_func=get_teacher_classes, methods=['GET'])
teacher_bp.add_url_rule('/exam-results', view_func=get_exam_results, methods=['GET'])
teacher_bp.add_url_rule('/performance', view_func=get_teacher_performance, methods=['GET'])
teacher_bp.add_url_rule('/students', view_func=get_teacher_students, methods=['GET'])
teacher_bp.add_url_rule('/scores', view_func=create_score, methods=['POST'])
teacher_bp.add_url_rule('/scores/<int:score_id>', view_func=update_score, methods=['PUT'])
teacher_bp.add_url_rule('/scores/<int:score_id>', view_func=delete_score, methods=['DELETE'])