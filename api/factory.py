"""应用工厂模块"""
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()


def create_app(config_name=None):
    """创建并配置Flask应用实例"""
    app = Flask(__name__)
    CORS(app)
    
    # 配置应用
    config_name = config_name or os.getenv('FLASK_CONFIG', 'default')
    from .config.config import config
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    _init_extensions(app)
    
    # 注册蓝图
    _register_blueprints(app)
    
    # 添加健康检查端点
    @app.route('/api/health')
    def health_check():
        return {'status': 'OK', 'message': 'API is running'}
    
    return app


def _init_extensions(app):
    """初始化Flask扩展"""
    from .database import init_app
    init_app(app)


def _register_blueprints(app):
    """注册所有蓝图"""
    from .routes import main
    from .blueprints.admin import admin_bp
    from .blueprints.teacher import teacher_bp
    from .blueprints.student import student_bp
    
    app.register_blueprint(main)
    app.register_blueprint(admin_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(student_bp)