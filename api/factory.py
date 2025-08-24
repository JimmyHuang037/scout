"""应用工厂模块"""
import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from api.services import get_db, close_db

load_dotenv()


def create_app(config_name=None):
    """创建并配置Flask应用实例"""
    app = Flask(__name__)
    CORS(app)
    
    # 配置应用
    config_name = config_name or os.getenv('FLASK_CONFIG', 'default')
    from config.config import config
    app.config.from_object(config[config_name])
    
    # 初始化数据库
    app.teardown_appcontext(close_db)
    
    # 注册蓝图
    from api.routes import register_blueprints
    register_blueprints(app)
    
    # 添加健康检查端点
    @app.route('/api/health')
    def health_check():
        return {'status': 'OK', 'message': 'API is running'}
    
    return app


def _init_extensions(app):
    """初始化扩展"""
    pass


def _register_blueprints(app):
    """注册蓝图"""
    from api.routes import register_blueprints
    register_blueprints(app)