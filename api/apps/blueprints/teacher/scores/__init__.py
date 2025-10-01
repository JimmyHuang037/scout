"""成绩管理蓝图模块"""
from flask import Blueprint
from .views import get_scores, update_score

# 教师成绩管理蓝图
teacher_scores_bp = Blueprint('teacher_scores', __name__)

# 注册路由
teacher_scores_bp.add_url_rule('/<string:teacher_id>/scores', view_func=get_scores, methods=['GET'])
teacher_scores_bp.add_url_rule('/<string:teacher_id>/scores/<int:score_id>', view_func=update_score, methods=['PUT'])