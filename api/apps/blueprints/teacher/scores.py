from flask import Blueprint, request, current_app
from apps.services import ScoreService
from apps.utils.helpers import success_response, error_response


# 教师成绩管理蓝图
teacher_scores_bp = Blueprint('teacher_scores', __name__, url_prefix='/scores')


def get_scores(teacher_id):
    """
    获取成绩列表
    
    Args:
        teacher_id (string): 教师ID
        
    Returns:
        JSON: 成绩列表
    """
    try:
        # 获取查询参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 创建成绩服务实例并获取成绩列表
        score_service = ScoreService()
        scores_data = score_service.get_teacher_scores(teacher_id, page, per_page)
        
        current_app.logger.info(f"Teacher {teacher_id} retrieved scores list")
        return success_response(scores_data)
    
    except Exception as e:
        current_app.logger.error(f"Failed to retrieve scores: {str(e)}")
        return error_response("获取成绩列表失败")


def update_score(teacher_id, score_id):
    """
    更新成绩记录
    
    Args:
        teacher_id (string): 教师ID
        score_id (int): 成绩ID
        
    Returns:
        JSON: 更新结果
    """
    try:
        # 获取请求数据
        data = request.get_json()
        if not data:
            return error_response("无效的请求数据", 400)
        
        # 创建成绩服务实例并更新成绩
        score_service = ScoreService()
        result = score_service.update_score(score_id, data)
        
        current_app.logger.info(f"Teacher {teacher_id} updated score {score_id}")
        return success_response(result)
    
    except Exception as e:
        current_app.logger.error(f"Failed to update score {score_id}: {str(e)}")
        return error_response("成绩更新失败", 500)


def delete_score(teacher_id, score_id):
    """
    删除成绩记录
    
    Args:
        teacher_id (string): 教师ID
        score_id (int): 成绩ID
        
    Returns:
        JSON: 删除结果
    """
    try:
        # 创建成绩服务实例并删除成绩
        score_service = ScoreService()
        result = score_service.delete_score(score_id)
        
        current_app.logger.info(f"Teacher {teacher_id} deleted score {score_id}")
        return success_response(result)
    
    except Exception as e:
        current_app.logger.error(f"Failed to delete score {score_id}: {str(e)}")
        return error_response("成绩删除失败", 500)


# 注册路由
teacher_scores_bp.add_url_rule('/', view_func=get_scores, methods=['GET'], defaults={'teacher_id': None})
teacher_scores_bp.add_url_rule('/<string:teacher_id>', view_func=get_scores, methods=['GET'])
teacher_scores_bp.add_url_rule('/<string:teacher_id>/<int:score_id>', view_func=update_score, methods=['PUT'])
teacher_scores_bp.add_url_rule('/<string:teacher_id>/<int:score_id>', view_func=delete_score, methods=['DELETE'])