import os
from apps.utils.paths import ensure_dir_exists


class Config:
    """应用基础配置"""
    
    # Flask配置
    SECRET_KEY = 'dev-secret-key'
    
    # 数据库配置
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Newuser1'
    MYSQL_DB = 'school_management'
    
    # Flask-Session配置
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sessions')
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'scout:'
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # 日志配置
    LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logs'))
    LOG_FILE_PATH = os.path.join(LOGS_DIR, 'app.log')
    LOG_LEVEL = 'DEBUG'
    
    # 测试配置
    TEST_DIR = os.path.join(LOGS_DIR, 'test')
    
    # 应用配置
    TESTING = False
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5000
    
    # 确保所需目录存在
    ensure_dir_exists(SESSION_FILE_DIR)
    ensure_dir_exists(LOGS_DIR)
    ensure_dir_exists(TEST_DIR)


# 配置映射
config = {
    'default': Config
}