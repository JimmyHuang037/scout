"""成绩管理蓝图模块"""
from flask import Blueprint
from .score_management import get_exam_scores, update_exam_scores

scores_bp = Blueprint('scores', __name__, url_prefix='/scores')

# 注册路由
scores_bp.add_url_rule('/exam/<int:exam_id>', view_func=get_exam_scores, methods=['GET'])
scores_bp.add_url_rule('/exam/<int:exam_id>', view_func=update_exam_scores, methods=['PUT'])
scores_bp.add_url_rule('', view_func=create_score, methods=['POST'])
scores_bp.add_url_rule('/<int:score_id>', view_func=get_score, methods=['GET'])
scores_bp.add_url_rule('/<int:score_id>', view_func=update_score, methods=['PUT'])
scores_bp.add_url_rule('/<int:score_id>', view_func=delete_score, methods=['DELETE'])