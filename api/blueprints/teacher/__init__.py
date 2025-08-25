"""教师蓝图模块"""
from flask import Blueprint

teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')

# 导入学生管理相关路由
from .students.student_management import get_my_students

# 导入成绩管理相关路由
from .scores import get_scores
from .score_create import create_score
from .score_update import update_score

# 导入考试相关路由
from .exam.exam_results_management import get_exam_results
from .exam.performance_management import get_performance
from .exam.exam_class_management import get_exam_classes

# 注册学生管理路由
teacher_bp.add_url_rule('/students', view_func=get_my_students, methods=['GET'])

# 注册成绩管理路由
teacher_bp.add_url_rule('/scores', view_func=get_scores, methods=['GET'])
teacher_bp.add_url_rule('/scores', view_func=create_score, methods=['POST'])
teacher_bp.add_url_rule('/scores/<int:score_id>', view_func=update_score, methods=['PUT'])

# 注册考试相关路由
teacher_bp.add_url_rule('/exam/results', view_func=get_exam_results, methods=['GET'])
teacher_bp.add_url_rule('/exam/performance', view_func=get_performance, methods=['GET'])
teacher_bp.add_url_rule('/exam/classes', view_func=get_exam_classes, methods=['GET'])