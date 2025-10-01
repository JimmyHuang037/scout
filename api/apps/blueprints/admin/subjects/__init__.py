from flask import Blueprint

"""科目管理蓝图模块"""

# 创建科目管理蓝图
admin_subjects_bp = Blueprint('admin_subjects', __name__)

# 导入管理函数
from . import subject_bp

# 注册路由
admin_subjects_bp.add_url_rule('/', methods=['POST'], view_func=subject_bp.create_subject)
admin_subjects_bp.add_url_rule('/', methods=['GET'], view_func=subject_bp.get_subjects)
admin_subjects_bp.add_url_rule('/<int:subject_id>', methods=['GET'], view_func=subject_bp.get_subject)
admin_subjects_bp.add_url_rule('/<int:subject_id>', methods=['PUT'], view_func=subject_bp.update_subject)
admin_subjects_bp.add_url_rule('/<int:subject_id>', methods=['DELETE'], view_func=subject_bp.delete_subject)