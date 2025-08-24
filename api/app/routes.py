from flask import Blueprint, jsonify, request

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return jsonify({
        'message': 'Welcome to School Management API',
        'version': '1.0.0'
    })


def register_blueprints(app):
    """注册所有蓝图"""
    from api.blueprints.admin import admin_bp
    from api.blueprints.teacher import teacher_bp
    from api.blueprints.student import student_bp
    from api.blueprints.auth import auth_bp
    
    app.register_blueprint(main)
    app.register_blueprint(admin_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(auth_bp)