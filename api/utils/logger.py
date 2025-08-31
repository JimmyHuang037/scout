"""日志工具模块"""
import logging
import os
from logging.handlers import RotatingFileHandler
from flask import current_app


def setup_logger(name, log_file, level=logging.INFO):
    """
    创建并配置日志记录器
    
    Args:
        name (str): 日志记录器名称
        log_file (str): 日志文件路径
        level: 日志级别
        
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    # 创建日志目录（如果不存在）
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 创建日志记录器
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 避免重复添加处理器
    if not logger.handlers:
        # 创建文件处理器（带轮转）
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=1024*1024*10,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(level)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        
        # 创建格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器到记录器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger


# 兼容层 - 当在Flask应用上下文中时，使用current_app.logger，否则使用默认的日志记录器
class AppLogger:
    @property
    def logger(self):
        try:
            return current_app.logger
        except RuntimeError:
            # 不在Flask应用上下文中，返回默认日志记录器
            return setup_logger('app', '../logs/app.log')
    
    def __getattr__(self, name):
        return getattr(self.logger, name)


# 创建全局app_logger实例
app_logger = AppLogger()