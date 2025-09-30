"""成绩管理蓝图模块"""
from flask import Blueprint
from .score_management import update_score

scores_bp = Blueprint('scores', __name__, url_prefix='/scores')

# 注册路由
scores_bp.add_url_rule('/<int:score_id>', view_func=update_score, methods=['PUT'])