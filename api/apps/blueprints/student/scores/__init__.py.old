from flask import Blueprint
from .views import get_my_scores

# 学生成绩管理蓝图
scores_bp = Blueprint('student_scores', __name__)

# 注册路由
scores_bp.add_url_rule('/<string:student_id>/scores', view_func=get_my_scores, methods=['GET'])