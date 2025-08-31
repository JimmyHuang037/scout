import os
from dotenv import load_dotenv
from cachelib import FileSystemCache

# 项目路径配置
basedir = os.path.abspath(os.path.dirname(__file__))
api_dir = os.path.abspath(os.path.join(basedir, '..'))
project_dir = os.path.abspath(os.path.join(api_dir, '..'))

# 加载 .env 文件
load_dotenv(os.path.join(basedir, '.env'))

# 默认环境配置
DEFAULT_ENV = 'development'


def get_config_name():
    """
    获取配置名称
    
    Returns:
        str: 配置名称
    """
    return os.getenv('FLASK_ENV', DEFAULT_ENV)


class Config:
    """应用基础配置"""
    
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = False
    TESTING = False
    
    # 数据库配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Newuser1')
    MYSQL_DB = os.getenv('MYSQL_DB', 'school_management')
    
    # 数据库连接URI
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 应用配置
    PORT = 5000
    
    # 日志和会话配置
    LOGS_DIR = os.path.join(project_dir, 'logs')
    LOG_FILE_PATH = os.path.join(LOGS_DIR, 'app.log')
    LOG_LEVEL = 'INFO'
    SESSION_TYPE = 'cachelib'
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 3600




class ProductionConfig(Config):
    """生产环境配置"""
    
    DEBUG = False
    PORT = 8000
    LOG_LEVEL = 'WARNING'
    
    # 日志和会话配置
    LOGS_DIR = os.path.abspath(os.path.join(project_dir, 'logs_production'))
    SESSION_TYPE = 'cachelib'
    SESSION_CACHELIB = FileSystemCache(
        os.path.join(project_dir, 'logs_production', 'flask_session'),
        threshold=500,
        mode=0o600
    )


class TestingConfig(Config):
    """测试环境配置"""
    
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'test-secret-key'
    LOG_LEVEL = 'INFO'
    
    # 测试数据库
    MYSQL_DB = os.getenv('MYSQL_DB', 'school_management_test')
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}/{MYSQL_DB}?charset=utf8mb4"
    
    # 测试配置
    PORT = 5010
    LOGS_DIR = os.path.abspath(os.path.join(project_dir, 'logs_testing'))
    
    # 会话配置
    SESSION_TYPE = 'cachelib'
    SESSION_CACHELIB = FileSystemCache(
        os.path.join(project_dir, 'logs_testing', 'flask_session'),
        threshold=500,
        mode=0o600
    )


# 配置映射
config = {
    'development': Config,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': Config
}