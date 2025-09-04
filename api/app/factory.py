#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
应用工厂模块

该模块包含创建Flask应用实例的工厂函数
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_session import Session
import traceback

# 确保logs目录存在
from config.config import config
from utils.database_service import DatabaseService




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