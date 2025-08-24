from flask import Blueprint
from .admin.students import get_students, create_student
from .admin.student_detail import get_student, update_student, delete_student
from .admin.teachers import get_teachers, create_teacher
from .admin.teacher_detail import get_teacher, update_teacher, delete_teacher

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/')
def admin_index():
    """管理员API根路径"""
    return {
        'message': 'Admin API',
        'version': '1.0.0'
    }

# 学生管理API
@admin_bp.route('/students', methods=['GET'])
def students_list():
    return get_students()

@admin_bp.route('/students', methods=['POST'])
def students_create():
    return create_student()

@admin_bp.route('/students/<int:student_id>', methods=['GET'])
def student_detail(student_id):
    return get_student(student_id)

@admin_bp.route('/students/<int:student_id>', methods=['PUT'])
def student_update(student_id):
    return update_student(student_id)

@admin_bp.route('/students/<int:student_id>', methods=['DELETE'])
def student_delete(student_id):
    return delete_student(student_id)

# 教师管理API
@admin_bp.route('/teachers', methods=['GET'])
def teachers_list():
    return get_teachers()

@admin_bp.route('/teachers', methods=['POST'])
def teachers_create():
    return create_teacher()

@admin_bp.route('/teachers/<int:teacher_id>', methods=['GET'])
def teacher_detail(teacher_id):
    return get_teacher(teacher_id)

@admin_bp.route('/teachers/<int:teacher_id>', methods=['PUT'])
def teacher_update(teacher_id):
    return update_teacher(teacher_id)

@admin_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
def teacher_delete(teacher_id):
    return delete_teacher(teacher_id)