from flask import request

from apps.utils.responses import error_response


def validate_json_input(required_fields=None, allow_empty=False):
    data = request.get_json()
    if not data:
        if allow_empty:
            return {}, None
        return None, error_response("请求数据不能为空", 400)
    
    if required_fields:
        for field in required_fields:
            if field not in data or not data[field]:
                return None, error_response(f"缺少必需字段: {field}", 400)
    
    return data, None