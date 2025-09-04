#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用工厂模块

该模块包含创建Flask应用实例的工厂函数
"""

import os
import logging
import sys
from flask import Flask
from flask_cors import CORS
from flask_session import Session
import traceback

# 确保logs目录存在
from config.config import config
from utils.database_service import DatabaseService


def _setup_logging(app):
    """设置应用日志配置"""
    # 在测试环境中，将日志输出到标准输出，便于重定向捕获
    if os.environ.get('FLASK_ENV') == 'testing':
        # 配置日志输出到标准输出和标准错误
        logging.basicConfig(
            level=getattr(logging, app.config['LOG_LEVEL']),
            format='%(asctime)s %(levelname)s %(name)s %(message)s',
            stream=sys.stdout
        )
        
        # 确保日志消息立即刷新
        for handler in logging.root.handlers:
            if hasattr(handler, 'stream'):
                handler.stream.flush()
    else:
        # 非测试环境保持原有的日志配置
        # 确保日志目录存在
        if not os.path.exists(app.config['LOGS_DIR']):
            os.makedirs(app.config['LOGS_DIR'])
        
        # 创建文件处理器
        file_handler = logging.FileHandler(app.config['LOG_FILE_PATH'], encoding='utf-8')
        file_handler.setLevel(getattr(logging, app.config['LOG_LEVEL']))
        
        # 创建格式化器并将其添加到处理器
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(name)s %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        # 将处理器添加到应用日志记录器
        app.logger.addHandler(file_handler)
        app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    
    # 记录应用启动日志
    app.logger.info('Application started')


def _setup_error_handlers(app):
    """设置应用错误处理器"""
    @app.errorhandler(Exception)
    def handle_exception(e):
        """全局异常处理器"""
        app.logger.error(f'Unhandled exception: {str(e)}')
        app.logger.error(traceback.format_exc())
        return {'error': 'Internal Server Error'}, 500


def _initialize_extensions(app):
    """初始化Flask扩展"""
    CORS(app)
    Session(app)
    
    # 确保会话目录存在
    session_dir = app.config.get('SESSION_FILE_DIR')
    if session_dir and not os.path.exists(session_dir):
        os.makedirs(session_dir)


def create_app(config_name=None):
    """
    创建Flask应用实例
    
    Args:
        config_name (str): 配置名称，如果未提供则从环境变量FLASK_ENV获取，默认为'default'
        
    Returns:
        Flask: 配置好的Flask应用实例
    """
    # 如果未提供配置名称，则从配置模块获取
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')
    
    # 初始化应用
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 设置日志
    _setup_logging(app)
    
    # 初始化扩展
    _initialize_extensions(app)
    
    # 注册蓝图
    from app.routes import main  # 导入主蓝图
    from blueprints.admin import admin_bp
    from blueprints.auth import auth_bp
    from blueprints.student import student_bp as student_main_bp
    from blueprints.teacher import teacher_bp as teacher_main_bp
    
    app.register_blueprint(main)  # 注册主蓝图（包含健康检查端点）
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_main_bp)
    app.register_blueprint(teacher_main_bp)
    
    # 设置错误处理器
    _setup_error_handlers(app)
    
    return app