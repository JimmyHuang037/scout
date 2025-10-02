from datetime import datetime
from flask import jsonify, session, request
from apps.utils.responses import success_response, error_response
from apps.utils.validation import validate_json_input
from apps.utils.user import get_current_user
"""助手函数模块，包含各种通用工具函数"""

# 为了保持向后兼容性，继续导出所有函数
__all__ = ['success_response', 'error_response', 'get_current_user', 'validate_json_input']