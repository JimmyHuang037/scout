from flask import Blueprint
from .views import create_subject, get_subjects, get_subject, update_subject, delete_subject

# 科目管理蓝图模块
admin_subjects_bp = Blueprint('admin_subjects', __name__)

# 注册路由
admin_subjects_bp.add_url_rule('/', methods=['POST'], view_func=create_subject)
admin_subjects_bp.add_url_rule('/', methods=['GET'], view_func=get_subjects)
admin_subjects_bp.add_url_rule('/<int:subject_id>', methods=['GET'], view_func=get_subject)
admin_subjects_bp.add_url_rule('/<int:subject_id>', methods=['PUT'], view_func=update_subject)
admin_subjects_bp.add_url_rule('/<int:subject_id>', methods=['DELETE'], view_func=delete_subject)