import os
from dotenv import load_dotenv
from cachelib import FileSystemCache

# 项目根目录
basedir = os.path.abspath(os.path.dirname(__file__))
# API根目录（向上两级目录）
api_dir = os.path.abspath(os.path.join(basedir, '..'))
# 项目根目录（scout目录）
project_dir = os.path.abspath(os.path.join(api_dir, '..'))

# 加载 .env 文件
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """应用配置基类"""
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Session配置 - 使用新的方式避免弃用警告
    SESSION_TYPE = 'cachelib'
    SESSION_CACHELIB = FileSystemCache(
        os.path.join(project_dir, 'logs', 'flask_session'),
        threshold=500,
        mode=0o600
    )
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 3600  # 1小时
    
    # MySQL数据库配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Newuser1')
    MYSQL_DB = os.getenv('MYSQL_DB', 'school_management')
    
    # 数据库连接URI
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 应用端口
    PORT = 5000
    
    # 日志目录
    LOGS_DIR = os.path.join(project_dir, 'logs')


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    PORT = 8000
    LOGS_DIR = os.path.join(project_dir, 'logs_production')
    SESSION_FILE_DIR = os.path.join(project_dir, 'logs_production', 'flask_session')
    SESSION_TYPE = 'filesystem'


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SECRET_KEY = 'test-secret-key'
    # 使用专门的测试数据库
    MYSQL_DB = os.getenv('MYSQL_DB', 'school_management_test')
    PORT = 5010
    LOGS_DIR = os.path.join(project_dir, 'logs_testing')
    SESSION_FILE_DIR = os.path.join(project_dir, 'logs_testing', 'flask_session')
    SESSION_TYPE = 'filesystem'


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}