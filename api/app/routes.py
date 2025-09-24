from flask import Blueprint, jsonify, request

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return jsonify({
        'message': 'Welcome to School Management API',
        'version': '1.0.0'
    })


@main.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'API server is running'
    })

