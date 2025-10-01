import os
class Config:
    """应用基础配置"""
    
    # Flask配置
    SECRET_KEY = 'dev-secret-key'
    
    # 数据库配置
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Newuser1'
    MYSQL_DB = 'school_management'
    
    # 日志配置
    LOGS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logs'))
    LOG_FILE_PATH = os.path.join(LOGS_DIR, 'app.log')
    LOG_LEVEL = 'DEBUG'
    
    # 确保日志目录存在
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    
    # 测试配置
    TEST_DIR = os.path.join(LOGS_DIR, 'test')
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR)
    
    # 应用配置
    TESTING = False
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5000


# 配置映射
config = {
    'default': Config
}