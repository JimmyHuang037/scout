#!/usr/bin/env python3
"""
应用工厂模块，用于创建和配置Flask应用实例
"""
import os
import logging
import traceback
import sys
from flask import Flask, jsonify
from flask_cors import CORS
from flask_session import Session
from config.config import config, get_config_name
from utils.logger import setup_logger


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
        config_name = get_config_name()
    
    # 初始化应用
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 创建应用日志记录器
    app_logger = setup_logger('app', app.config['LOG_FILE_PATH'], level=logging.INFO)
    app.logger.setLevel(getattr(logging, app.config['LOG_LEVEL']))
    app.logger.info(f'Flask application initialized with config: {config_name}')
    
    # 初始化扩展
    CORS(app)
    Session(app)
    
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
    
    return app