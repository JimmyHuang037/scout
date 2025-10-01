from flask import Blueprint

# 创建教师成绩管理蓝图
teacher_scores_bp = Blueprint('teacher_scores', __name__)

# 直接导入视图函数，避免循环导入
from ..scores.score_bp import get_scores, update_score

# 注册路由
teacher_scores_bp.add_url_rule('/<string:teacher_id>/scores', view_func=get_scores, methods=['GET'])
teacher_scores_bp.add_url_rule('/<string:teacher_id>/scores/<int:score_id>', view_func=update_score, methods=['PUT'])