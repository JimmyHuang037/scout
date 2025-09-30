import os


class Config:
    """应用基础配置"""
    
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # 数据库配置
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Newuser1')
    MYSQL_DB = os.getenv('MYSQL_DB', 'school_management')
    
    # 数据库连接URI
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}?charset=utf8mb4"
    
    # 日志配置
    LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logs'))
    LOG_FILE_PATH = os.path.join(LOGS_DIR, 'app.log')
    LOG_LEVEL = 'DEBUG'
    
    # 确保日志目录存在
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    
    # 应用配置
    TESTING = False
    DEBUG = True
    PORT = 5000


# 配置映射
config = {
    'default': Config
}