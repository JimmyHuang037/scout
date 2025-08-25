#!/usr/bin/env python3
"""
应用工厂模块，用于创建和配置Flask应用实例
"""

import os
import logging
from flask import Flask
from flask_cors import CORS
from flask_session import Session
from werkzeug.middleware.shared_data import SharedDataMiddleware
from cachelib import FileSystemCache

from config.config import config
from utils.logger import app_logger
from utils import db

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 创建logger
logger = logging.getLogger('app')

# 在测试环境中降低数据库相关日志级别
if os.environ.get('FLASK_ENV') == 'testing':
    logging.getLogger('app').setLevel(logging.CRITICAL)


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
    logger.info("Flask application created successfully")

    # 自定义日志过滤器，过滤掉数据库连接的INFO日志
    class NoDbInfoFilter(logging.Filter):
        def filter(self, record):
            return 'Connected to' not in record.getMessage()

    # 获取根日志记录器并添加过滤器
    logging.getLogger().addFilter(NoDbInfoFilter())
    
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