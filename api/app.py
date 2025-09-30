#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""应用工厂模块"""

import logging
import os
from flask import Flask
from flask_cors import CORS

# 导入蓝图
from apps.blueprints.common import common_bp
from apps.blueprints.admin import admin_bp
from apps.blueprints.student import student_bp as student_main_bp
from apps.blueprints.teacher import teacher_bp as teacher_main_bp
from apps.blueprints.auth import auth_bp


class AppFactory:
    """应用工厂类"""

    @staticmethod
    def create_app(config_name: str = 'default') -> Flask:
        """创建Flask应用实例"""
        app = Flask(__name__)
        
        # 加载配置
        from config import config
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
        
        # 注册错误处理器
        @app.errorhandler(404)
        def not_found(error):
            return {'error': 'Not found'}, 404
            
        @app.errorhandler(500)
        def internal_error(error):
            return {'error': 'Internal server error'}, 500
            
        return app


# 创建应用实例
app = AppFactory.create_app()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=app.config.get('PORT', 5000),
        debug=app.config.get('DEBUG', False)
    )