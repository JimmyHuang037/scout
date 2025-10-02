from flask import jsonify, request
from apps.utils.decorators import handle_exceptions

from . import views

"""公共蓝图模块"""

from flask import Blueprint
from .views import index, health_check, test_error

# 创建公共蓝图
common_bp = Blueprint('common', __name__)

# 注册路由
common_bp.add_url_rule('/', view_func=index, methods=['GET'])
common_bp.add_url_rule('/api/health', view_func=health_check, methods=['GET'])
common_bp.add_url_rule('/api/test_error', view_func=test_error, methods=['GET'])
