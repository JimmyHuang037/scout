import os
from dotenv import load_dotenv
from cachelib import FileSystemCache

# 项目根目录
basedir = os.path.abspath(os.path.dirname(__file__))
# API根目录（向上两级目录）
api_dir = os.path.abspath(os.path.join(basedir, '..'))

# 加载 .env 文件
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """应用配置基类"""
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Session配置 - 使用新的方式避免弃用警告，并确_session会话数据存储在api/runtime目录中
    SESSION_TYPE = 'cachelib'
    SESSION_CACHELIB = FileSystemCache(
        os.path.join(api_dir, 'runtime', 'flask_session'),
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


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    # 使用专门的测试数据库
    MYSQL_DB = os.getenv('MYSQL_TEST_DB', 'school_management_test')


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}