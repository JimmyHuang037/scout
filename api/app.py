#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用主文件，包含配置、工厂和入口点
"""

import logging
import traceback
import sys
import os

# 添加项目根目录到sys.path，确保可以正确导入模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS

# Configuration
from config import config

# Blueprints
from apps.blueprints.common import common_bp
from apps.blueprints.admin import admin_bp
from apps.blueprints.student import student_bp as student_main_bp
from apps.blueprints.teacher import teacher_bp as teacher_main_bp
from apps.blueprints.auth import auth_bp


class AppFactory:
    """应用工厂类"""
    
    @staticmethod
    def _setup_logging(app: Flask) -> None:
        """设置应用日志配置"""
        file_handler = logging.FileHandler(app.config['LOG_FILE_PATH'], encoding='utf-8')
        file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(name)s %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        app.logger.addHandler(file_handler)
        app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        
        app.logger.info('Application started')
        app.logger.info(f'Using configuration: default')
        app.logger.info(f'Database: {app.config["MYSQL_DB"]} on {app.config["MYSQL_HOST"]} as {app.config["MYSQL_USER"]}')

    @staticmethod
    def _setup_error_handlers(app: Flask) -> None:
        """设置应用错误处理器"""
        @app.errorhandler(Exception)
        def handle_exception(e: Exception):
            """全局异常处理器"""
            app.logger.error(f'Unhandled exception: {str(e)}')
            app.logger.error(traceback.format_exc())
            return {'error': 'Internal Server Error'}, 500

    @staticmethod
    def create_app(config_name: Optional[str] = None) -> Flask:
        """创建Flask应用实例"""
        app = Flask(__name__)
        
        app.config.from_object(config['default'])
        
        AppFactory._setup_logging(app)
        
        CORS(app)
        
        # 注册所有蓝图
        app.register_blueprint(common_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(student_main_bp)
        app.register_blueprint(teacher_main_bp)
        app.register_blueprint(auth_bp)
        
        AppFactory._setup_error_handlers(app)
        
        return app


# 应用入口点
if __name__ == '__main__':
    # 创建并运行应用，始终使用默认配置
    app = AppFactory.create_app()
    port = app.config.get('PORT', 5000)
    debug_mode = app.config.get('DEBUG', True)  # 从配置中读取
    app.run(debug=debug_mode, host='0.0.0.0', port=port)