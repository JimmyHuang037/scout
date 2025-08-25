#!/usr/bin/env python3
"""
应用工厂模块，用于创建和配置Flask应用实例
"""
import os
import logging
from flask import Flask
from flask_cors import CORS
from flask_session import Session
from config.config import Config
from utils.logger import setup_logger


def create_app(config_name='default'):
    """
    创建Flask应用实例
    
    Args:
        config_name (str): 配置名称
        
    Returns:
        Flask: 配置好的Flask应用实例
    """
    # 初始化应用
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(Config)
    
    # 设置日志
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'runtime', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    setup_logger('app', os.path.join(log_dir, 'app.log'))
    app.logger.info('Flask application created successfully')
    
    # 初始化扩展
    CORS(app)
    Session(app)
    
    # 注册蓝图
    from blueprints.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    from blueprints.admin import admin_bp
    app.register_blueprint(admin_bp)
    
    from blueprints.teacher import teacher_bp
    app.register_blueprint(teacher_bp)
    
    from blueprints.student import student_bp
    app.register_blueprint(student_bp)
    
    # 注册数据库关闭函数
    from utils import database_service
    app.teardown_appcontext(database_service.close_db)
    
    app.logger.info("Flask application created successfully")
    
    return app