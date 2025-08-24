from flask import Blueprint, jsonify, request
from .database import get_db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return jsonify({
        'message': 'Welcome to School Management API',
        'version': '1.0.0'
    })