import logging
import os
import time
from flask import Flask, request
from flask_cors import CORS

from apps.blueprints.admin import admin_bp
from apps.blueprints.auth import auth_bp
from apps.blueprints.common import common_bp
from apps.blueprints.student import student_bp as student_main_bp
from apps.blueprints.teacher import teacher_bp as teacher_main_bp
from config import config

"""应用工厂模块"""


# 导入蓝图


class AppFactory:
    """应用工厂类"""

    @staticmethod
    def create_app(config_name: str = 'default') -> Flask:
        """创建Flask应用实例"""
        app = Flask(__name__)
        
        # 加载配置
        app.config.from_object(config[config_name])
        
        # 初始化Flask扩展
        CORS(app)
        
        # 注册蓝图
        app.register_blueprint(auth_bp)
        app.register_blueprint(common_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(student_main_bp)
        app.register_blueprint(teacher_main_bp)
        
        # 配置日志
        file_handler = logging.FileHandler(app.config['LOG_FILE_PATH'])
        file_handler.setLevel(app.config['LOG_LEVEL'])
        
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        )
        file_handler.setFormatter(formatter)
        
        app.logger.addHandler(file_handler)
        app.logger.setLevel(app.config['LOG_LEVEL'])
        
        # 记录应用启动信息
        app.logger.info('Flask application starting...')
        app.logger.info(f"Database: {app.config['MYSQL_USER']}@{app.config['MYSQL_HOST']}/{app.config['MYSQL_DB']}")
        
        # 注册全局请求日志记录
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
        
        # 注册错误处理器
        @app.errorhandler(404)
        def not_found(error):
            if hasattr(request, 'request_id'):
                app.logger.warning(f"[{request.request_id}] 404 Not Found: {request.path}")
            return {'error': 'Not found'}, 404
            
        @app.errorhandler(500)
        def internal_error(error):
            if hasattr(request, 'request_id'):
                app.logger.error(f"[{request.request_id}] 500 Internal Server Error: {str(error)}")
            return {'error': 'Internal server error'}, 500
            
        return app


# 创建应用实例
app = AppFactory.create_app()

if __name__ == '__main__':
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 5000),
        debug=app.config.get('DEBUG', False)
    )