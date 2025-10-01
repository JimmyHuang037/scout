from apps.services.student_service import StudentService
from apps.utils.helpers import success_response, error_response
from flask import Blueprint

# 从本地 views 模块导入视图函数
from .views import get_my_profile

# 创建学生个人资料管理蓝图
student_profile_bp = Blueprint('student_profile', __name__)

# 注册路由
student_profile_bp.add_url_rule('/<string:student_id>/profile', view_func=get_my_profile, methods=['GET'])
