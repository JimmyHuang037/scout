from flask import Blueprint, jsonify, request
from apps.utils.decorators import handle_exceptions
from apps.utils.responses import success_response, error_response

common_bp = Blueprint('common', __name__)


def index():
    return jsonify({
        'message': 'Welcome to School Management API',
        'version': '1.0.0'
    })


def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'API server is running'
    })


@handle_exceptions
def test_error():
    raise Exception("This is a test error for exception handling")


common_bp.add_url_rule('/', view_func=index, methods=['GET'])
common_bp.add_url_rule('/health', view_func=health_check, methods=['GET'])
common_bp.add_url_rule('/test_error', view_func=test_error, methods=['GET'])