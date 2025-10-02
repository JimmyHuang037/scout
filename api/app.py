import logging
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

from apps.blueprints.admin import admin_bp
from apps.blueprints.auth import auth_bp
from apps.blueprints.common import common_bp
from apps.blueprints.student import student_bp
from apps.blueprints.teacher import teacher_bp
from apps.utils.helpers import error_response
from config import config


class AppFactory:
    @staticmethod
    def create_app(config_name: str = 'default') -> Flask:
        app = Flask(__name__)
        app.config.from_object(config[config_name])
        CORS(app)
        
        AppFactory._init_blueprints(app)
        AppFactory._setup_logging(app)
        AppFactory._log_startup_info(app)
        AppFactory._register_request_handlers(app)
        AppFactory._register_error_handlers(app)
            
        return app

    @staticmethod
    def _init_blueprints(app):
        app.register_blueprint(auth_bp)
        app.register_blueprint(common_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(student_bp)
        app.register_blueprint(teacher_bp)

    @staticmethod
    def _setup_logging(app):
        file_handler = logging.FileHandler(app.config['LOG_FILE_PATH'])
        file_handler.setLevel(app.config['LOG_LEVEL'])
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(app.config['LOG_LEVEL'])

    @staticmethod
    def _log_startup_info(app):
        app.logger.info('Flask application starting...')
        app.logger.info(f"Database: {app.config['MYSQL_USER']}@{app.config['MYSQL_HOST']}/{app.config['MYSQL_DB']}")

    @staticmethod
    def _register_request_handlers(app):
        @app.before_request
        def log_request_info():
            request.start_time = time.time()
            request.request_id = f"{int(request.start_time * 1000000) % 1000000:06d}"
            app.logger.info(f"[{request.request_id}] {request.method} {request.path} - "
                           f"Args: {request.args.to_dict()}, Form: {request.form.to_dict()}, "
                           f"JSON: {request.get_json(silent=True)}")

        @app.after_request
        def log_response_info(response):
            if hasattr(request, 'start_time') and hasattr(request, 'request_id'):
                execution_time = time.time() - request.start_time
                app.logger.info(f"[{request.request_id}] Response: {response.status_code} - "
                               f"Execution time: {execution_time:.2f}s")
            return response

    @staticmethod
    def _register_error_handlers(app):
        @app.errorhandler(404)
        def not_found(error):
            request_id = getattr(request, 'request_id', 'N/A')
            app.logger.warning(f"[{request_id}] 404 Not Found: {request.path}")
            return error_response('Not found', 404)
            
        @app.errorhandler(500)
        def internal_error(error):
            request_id = getattr(request, 'request_id', 'N/A')
            app.logger.error(f"[{request_id}] 500 Internal Server Error: {str(error)}")
            return error_response('Internal server error', 500)


app = AppFactory.create_app()

if __name__ == '__main__':
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 5000),
        debug=app.config.get('DEBUG', False)
    )