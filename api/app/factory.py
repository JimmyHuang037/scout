#!/usr/bin/env python3
"""
应用工厂模块，用于创建和配置Flask应用实例
"""
import os
import logging
import traceback
from flask import Flask, jsonify
from flask_cors import CORS
from flask_session import Session
from cachelib import FileSystemCache
from config.config import config
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
    app.config.from_object(config[config_name])
    
    # 确保会话目录存在，路径相对于app目录
    session_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'runtime', 'flask_session')
    os.makedirs(session_dir, exist_ok=True)
    
    # 设置日志
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'runtime', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    setup_logger('app', os.path.join(log_dir, 'app.log'), level=logging.INFO)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Flask application created successfully')
    
    # 添加全局错误处理
    @app.errorhandler(Exception)
    def handle_exception(e):
        # 记录完整的错误堆栈
        app.logger.error(f'Unhandled exception: {str(e)}')
        app.logger.error(traceback.format_exc())
        
        # 返回JSON格式的错误响应
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'message': str(e) if app.config.get('DEBUG') else 'An internal error occurred'
        }), 500
    
    # 初始化扩展
    CORS(app)
    Session(app)
    
    # 注册蓝图
    try:
        blueprint_modules = [
            ('auth', 'auth_bp'),
            ('admin', 'admin_bp'),
            ('teacher', 'teacher_bp'),
            ('student', 'student_bp')
        ]
        
        for module_name, blueprint_name in blueprint_modules:
            module = __import__(f'blueprints.{module_name}', fromlist=[blueprint_name])
            blueprint = getattr(module, blueprint_name)
            app.register_blueprint(blueprint)
            
    except Exception as e:
        app.logger.error(f'Error registering blueprints: {str(e)}')
        raise
    
    # 注册数据库关闭函数
    from utils import database_service
    app.teardown_appcontext(database_service.close_db)
    
    app.logger.info("Flask application created successfully")
    
    return app