import os
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()


class Config:
    """应用配置基类"""
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # MySQL数据库配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Newuser1')
    MYSQL_DB = os.getenv('MYSQL_DB', 'school_management')
    
    # 数据库连接URI
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}"
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
    MYSQL_DB = os.getenv('TEST_MYSQL_DB', 'school_management_test')


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}