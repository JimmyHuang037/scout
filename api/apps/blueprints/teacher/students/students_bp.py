from flask import Blueprint

# 创建教师学生管理蓝图
teacher_students_bp = Blueprint('teacher_students', __name__)

# 直接导入视图函数，避免循环导入
from ..students.student_bp import get_teacher_students, get_teacher_student, get_teacher_all_classes_students

# 注册路由
teacher_students_bp.add_url_rule('/<string:teacher_id>/students', view_func=get_teacher_students, methods=['GET'])
teacher_students_bp.add_url_rule('/<string:teacher_id>/students/<string:student_id>', view_func=get_teacher_student, methods=['GET'])
teacher_students_bp.add_url_rule('/<string:teacher_id>/classes/students', view_func=get_teacher_all_classes_students, methods=['GET'])
teacher_students_bp.add_url_rule('/<string:teacher_id>/all_classes_students', view_func=get_teacher_all_classes_students, methods=['GET'])