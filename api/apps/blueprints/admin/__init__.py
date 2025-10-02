from flask import Blueprint
from apps.blueprints.admin.classes import admin_classes_bp
from apps.blueprints.admin.subjects import admin_subjects_bp
from apps.blueprints.admin.exam_types import admin_exam_types_bp
from apps.blueprints.admin.teacher_classes import admin_teacher_classes_bp
from apps.blueprints.admin.students import admin_students_bp
from apps.blueprints.admin.teachers import admin_teachers_bp

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# 注册各个子蓝图
admin_bp.register_blueprint(admin_classes_bp, url_prefix='/classes')
admin_bp.register_blueprint(admin_subjects_bp, url_prefix='/subjects')
admin_bp.register_blueprint(admin_exam_types_bp, url_prefix='/exam_types')
admin_bp.register_blueprint(admin_teacher_classes_bp, url_prefix='/teacher_classes')
admin_bp.register_blueprint(admin_students_bp, url_prefix='/students')
admin_bp.register_blueprint(admin_teachers_bp, url_prefix='/teachers')