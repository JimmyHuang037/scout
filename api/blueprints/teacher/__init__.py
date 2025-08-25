"""教师蓝图模块"""
from flask import Blueprint

teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')

# 学生管理模块
from .students.student_management import get_my_students  # 学生列表

# 成绩管理模块
from .scores import get_scores  # 获取成绩列表
from .score_create import create_score  # 创建成绩
from .score_update import update_score  # 更新成绩

# 考试管理模块
from .exam.exam_results_management import get_exam_results  # 考试成绩
from .exam.performance_management import get_performance  # 学习表现
from .exam.exam_class_management import get_exam_classes  # 考试班级

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