"""教师成绩管理蓝图模块"""
from flask import Blueprint

scores_bp = Blueprint('scores', __name__)

from .score_management import get_scores, create_score, update_score, delete_score

# 注册路由
scores_bp.add_url_rule('/scores', view_func=get_scores, methods=['GET'])
scores_bp.add_url_rule('/scores', view_func=create_score, methods=['POST'])
scores_bp.add_url_rule('/scores/<int:score_id>', view_func=update_score, methods=['PUT'])
scores_bp.add_url_rule('/scores/<int:score_id>', view_func=delete_score, methods=['DELETE'])