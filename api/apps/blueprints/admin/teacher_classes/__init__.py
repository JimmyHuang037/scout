from flask import Blueprint

# 创建教师班级关联管理蓝图
admin_teacher_classes_bp = Blueprint('admin_teacher_classes', __name__)

# 导入管理函数
from . import teacher_class_bp

# 注册路由
admin_teacher_classes_bp.add_url_rule('/', methods=['GET'], view_func=teacher_class_bp.get_teacher_classes)
admin_teacher_classes_bp.add_url_rule('/', methods=['POST'], view_func=teacher_class_bp.create_teacher_class)
admin_teacher_classes_bp.add_url_rule('/<int:teacher_id>/<int:class_id>', methods=['GET'], view_func=teacher_class_bp.get_teacher_class)
admin_teacher_classes_bp.add_url_rule('/<int:teacher_id>/<int:class_id>', methods=['PUT'], view_func=teacher_class_bp.update_teacher_class)
admin_teacher_classes_bp.add_url_rule('/<int:teacher_id>/<int:class_id>', methods=['DELETE'], view_func=teacher_class_bp.delete_teacher_class)