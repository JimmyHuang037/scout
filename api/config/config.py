import os

# 获取项目根目录
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))


def get_config_name():
    """
    获取配置名称
    
    Returns:
        str: 配置名称
    """
    return os.getenv('FLASK_ENV', 'default')


def _get_database_uri(user, password, host, database):
    """生成数据库连接URI"""
    return f"mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4"


def _get_logs_config(env):
    """获取日志配置"""
    if env == 'production':
        logs_dir = os.path.abspath(os.path.join(project_dir, 'logs_production'))
    elif env == 'testing':
        logs_dir = os.path.abspath(os.path.join(project_dir, 'logs_testing'))
    else:
        logs_dir = os.path.join(project_dir, 'logs')
    
    # 在测试环境中仍然创建日志目录和文件，但app.log不会被使用
    log_file_path = os.path.join(logs_dir, 'app.log')
    session_dir = os.path.join(logs_dir, 'flask_session')  # 会话目录应该在logs_testing下
    
    return logs_dir, log_file_path, session_dir


def _get_curl_test_dir(env, logs_dir):
    """获取curl测试结果目录"""
    return os.path.join(logs_dir, 'curl_test')


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
    SQLALCHEMY_DATABASE_URI = _get_database_uri(
        MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB
    )
    
    # 应用配置
    PORT = 5000
    
    # 日志级别配置
    LOG_LEVEL = 'DEBUG'
    
    # 日志和会话配置
    LOGS_DIR, LOG_FILE_PATH, SESSION_FILE_DIR = _get_logs_config('development')
    LOG_FILE_MAX_BYTES = 1024 * 1024 * 10  # 10MB
    LOG_FILE_BACKUP_COUNT = 5
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 3600
    
    # test_curl配置
    CURL_TEST_DIR = _get_curl_test_dir('', LOGS_DIR)


class ProductionConfig(Config):
    """生产环境配置"""
    
    DEBUG = False
    LOG_LEVEL = 'WARNING'  # 生产环境使用WARNING级别
    
    # 生产数据库
    MYSQL_DB = os.getenv('MYSQL_DB', 'school_management')
    
    # 数据库连接URI
    SQLALCHEMY_DATABASE_URI = _get_database_uri(
        Config.MYSQL_USER, Config.MYSQL_PASSWORD, Config.MYSQL_HOST, MYSQL_DB
    )
    
    # 生产环境端口
    PORT = 5000
    
    # 日志和会话配置
    LOGS_DIR, LOG_FILE_PATH, SESSION_FILE_DIR = _get_logs_config('production')
    
    # test_curl配置
    CURL_TEST_DIR = _get_curl_test_dir('production', LOGS_DIR)


class TestingConfig(Config):
    """测试环境配置"""
    
    def  hello():
        print('hello world')
        
    DEBUG = True
    TESTING = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'test-secret-key')
    LOG_LEVEL = 'DEBUG'  # 测试环境使用DEBUG级别
    
    # 测试数据库
    MYSQL_DB = os.getenv('MYSQL_DB', 'school_management_test')
    
    # 数据库连接URI
    SQLALCHEMY_DATABASE_URI = _get_database_uri(
        Config.MYSQL_USER, Config.MYSQL_PASSWORD, Config.MYSQL_HOST, MYSQL_DB
    )
    
    # 测试配置
    PORT = 5000
    
    # 日志和会话配置
    LOGS_DIR, LOG_FILE_PATH, SESSION_FILE_DIR = _get_logs_config('testing')
    
    # test_curl配置
    CURL_TEST_DIR = _get_curl_test_dir('testing', LOGS_DIR)


# 配置映射
config = {
    'development': Config,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': Config
}