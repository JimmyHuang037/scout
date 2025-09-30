#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""应用工厂模块"""
from flask import Flask
from flask_cors import CORS
from typing import Optional
import logging
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入蓝图
from apps.blueprints.common import common_bp
from apps.blueprints.admin import admin_bp
from apps.blueprints.student import student_bp as student_main_bp
from apps.blueprints.teacher import teacher_bp as teacher_main_bp
from apps.blueprints.auth import auth_bp


class AppFactory:
    """应用工厂类"""

    @staticmethod
    def create_app(config_name: Optional[str] = None) -> Flask:
        """
        创建Flask应用实例
        
        Args:
            config_name (str, optional): 配置名称
            
        Returns:
            Flask: 配置好的Flask应用实例
        """
        # 创建Flask应用实例
        app = Flask(__name__)
        
        # 加载配置
        AppFactory._load_config(app, config_name)
        
        # 初始化扩展
        AppFactory._init_extensions(app)
        
        # 注册蓝图
        AppFactory._register_blueprints(app)
        
        # 配置日志
        AppFactory._configure_logging(app)
        
        # 注册错误处理器
        AppFactory._register_error_handlers(app)
        
        return app

    @staticmethod
    def _load_config(app: Flask, config_name: Optional[str]) -> None:
        """
        加载应用配置
        
        Args:
            app (Flask): Flask应用实例
            config_name (str): 配置名称
        """
        # 如果没有指定配置名称，则从环境变量获取
        if config_name is None:
            config_name = os.environ.get('FLASK_ENV', 'default')
            
        # 导入配置模块并应用配置
        from config import config
        app.config.from_object(config[config_name])
        
        # 确保日志目录存在
        logs_dir = app.config.get('LOGS_DIR')
        if logs_dir:
            os.makedirs(logs_dir, exist_ok=True)

    @staticmethod
    def _init_extensions(app: Flask) -> None:
        """
        初始化Flask扩展
        
        Args:
            app (Flask): Flask应用实例
        """
        # 初始化CORS
        CORS(app, resources={
            r"/api/*": {
                "origins": "*",
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"]
            }
        })

    @staticmethod
    def _register_blueprints(app: Flask) -> None:
        """
        注册应用蓝图
        
        Args:
            app (Flask): Flask应用实例
        """
        # 注册各个蓝图
        app.register_blueprint(auth_bp)
        app.register_blueprint(common_bp)
        app.register_blueprint(admin_bp)
        app.register_blueprint(student_main_bp)
        app.register_blueprint(teacher_main_bp)

    @staticmethod
    def _configure_logging(app: Flask) -> None:
        """
        配置应用日志
        
        Args:
            app (Flask): Flask应用实例
        """
        # 如果不是测试环境，则配置日志
        if not app.config.get('TESTING', False):
            # 创建文件处理器
            file_handler = logging.FileHandler(app.config['LOG_FILE_PATH'])
            file_handler.setLevel(app.config['LOG_LEVEL'])
            
            # 创建日志格式器并应用到文件处理器
            formatter = logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            )
            file_handler.setFormatter(formatter)
            
            # 将文件处理器添加到应用日志器
            app.logger.addHandler(file_handler)
            app.logger.setLevel(app.config['LOG_LEVEL'])

    @staticmethod
    def _register_error_handlers(app: Flask) -> None:
        """
        注册错误处理器
        
        Args:
            app (Flask): Flask应用实例
        """
        @app.errorhandler(404)
        def not_found(error):
            """处理404错误"""
            return {'error': 'Not found'}, 404
            
        @app.errorhandler(500)
        def internal_error(error):
            """处理500错误"""
            return {'error': 'Internal server error'}, 500

# 创建应用实例
app = AppFactory.create_app()

if __name__ == '__main__':
    # 从环境变量获取主机和端口配置，如果没有则使用默认值
    host = os.environ.get('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_RUN_PORT', 5000))
    debug = app.config.get('DEBUG', False)
    
    # 运行应用
    app.run(host=host, port=port, debug=debug)