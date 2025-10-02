from flask import request
from apps.utils.responses import error_response


def validate_json_input(required_fields=None, allow_empty=False):
    """
    验证JSON输入数据
    
    Args:
        required_fields (list): 必需的字段列表
        allow_empty (bool): 是否允许空数据
        
    Returns:
        tuple: (data, error_response) 如果验证成功，error_response为None；如果验证失败，data为None
    """
    # 获取请求数据
    data = request.get_json()
    if not data:
        if allow_empty:
            return {}, None
        return None, error_response("请求数据不能为空", 400)
    
    # 检查必需字段
    if required_fields:
        for field in required_fields:
            if field not in data or not data[field]:
                return None, error_response(f"缺少必需字段: {field}", 400)
    
    return data, None