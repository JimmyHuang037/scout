"""教师蓝图模块"""
from flask import Blueprint

teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')

# 学生管理模块
from .students.student_management import get_my_students  # 学生列表

# 成绩管理模块
from .scores import scores_bp

# 考试管理模块
from .exam.exam_results_management import get_exam_results  # 考试成绩
from .exam.performance_management import get_performance  # 学习表现
from .exam.exam_class_management import get_exam_classes  # 考试班级
from .exam.exam_management import get_exams, create_exam, get_exam, update_exam, delete_exam  # 考试管理

# 注册学生管理路由
teacher_bp.add_url_rule('/students', view_func=get_my_students, methods=['GET'])

# 注册成绩管理路由
teacher_bp.register_blueprint(scores_bp)

# 注册考试相关路由
teacher_bp.add_url_rule('/exam/results', view_func=get_exam_results, methods=['GET'])
teacher_bp.add_url_rule('/exam/performance', view_func=get_performance, methods=['GET'])
teacher_bp.add_url_rule('/exam/classes', view_func=get_exam_classes, methods=['GET'])

# 注册考试管理路由
teacher_bp.add_url_rule('/exams', view_func=get_exams, methods=['GET'])
teacher_bp.add_url_rule('/exams', view_func=create_exam, methods=['POST'])
teacher_bp.add_url_rule('/exams/<int:exam_id>', view_func=get_exam, methods=['GET'])
teacher_bp.add_url_rule('/exams/<int:exam_id>', view_func=update_exam, methods=['PUT'])
teacher_bp.add_url_rule('/exams/<int:exam_id>', view_func=delete_exam, methods=['DELETE'])