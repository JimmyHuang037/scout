#!/usr/bin/env python3
"""
应用工厂模块，用于创建和配置Flask应用实例
"""

import os
from flask import Flask
from flask_cors import CORS
from flask_session import Session
from werkzeug.middleware.shared_data import SharedDataMiddleware
from cachelib import FileSystemCache

from config.config import config
from utils.logger import app_logger
from utils import db


def create_app(config_name=None):
    """
    应用工厂函数
    
    Args:
        config_name (str, optional): 配置名称
        
    Returns:
        Flask: 配置好的Flask应用实例
    """
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'default')
    
    # 创建Flask应用实例
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 配置日志
    app_logger.info("Flask application created successfully")
    
    # 配置CORS
    CORS(app, supports_credentials=True)
    
    # 配置静态文件服务
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/static': os.path.join(os.path.dirname(__file__), '..', 'static')
    })
    
    # 配置Session
    cache_dir = app.config.get('SESSION_FILE_DIR')
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    cache = FileSystemCache(cache_dir)
    
    # 设置SESSION_TYPE为cachelib并使用cache实例
    app.config['SESSION_TYPE'] = 'cachelib'
    app.config['SESSION_CACHELIB'] = cache
    Session(app)
    
    # 注册蓝图
    from blueprints.admin import admin_bp
    from blueprints.teacher import teacher_bp
    from blueprints.student import student_bp
    from blueprints.auth import auth_bp
    
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(teacher_bp, url_prefix='/api/teacher')
    app.register_blueprint(student_bp, url_prefix='/api/student')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # 注册数据库关闭函数
    app.teardown_appcontext(db.close_db)
    
    app_logger.info("Flask application created successfully")
    
    return app