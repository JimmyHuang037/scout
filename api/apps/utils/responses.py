from datetime import datetime
from flask import jsonify


def success_response(data=None, message="Success"):
    response = {
        'success': True,
        'message': message,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(response)


def error_response(message="Error", status_code=400):
    response = {
        'success': False,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(response), status_code


def success_response(data=None, message="Success"):
    response = {
        'success': True,
        'message': message,
        'data': data,
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(response)


def error_response(message="Error", status_code=400):
    response = {
        'success': False,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(response), status_code