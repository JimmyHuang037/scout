#!/usr/bin/env python3
"""
数据库服务模块，提供数据库连接和操作功能
"""
import pymysql
import os
from utils.logger import app_logger as logger
from config.config import Config


class DatabaseService:
    """
    数据库服务类，用于管理数据库连接
    """
    
    def __init__(self):
        """初始化数据库服务"""
        self.connection = None
        self.transaction_active = False
        self.connect()
    
    def connect(self):
        """建立数据库连接"""
        try:
            # 建立数据库连接
            self.connection = pymysql.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DB,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True
            )
            # 只在初始化时记录一次日志
            logger.info("DatabaseService initialized")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def get_connection(self):
        """
        获取数据库连接
        
        Returns:
            pymysql.Connection: 数据库连接对象
        """
        if not self.connection or not self.connection.open:
            self.connect()
        return self.connection
    
    def close(self):
        """关闭数据库连接"""
        if self.connection and self.connection.open:
            self.connection.close()
    
    def execute_query(self, query, params=None, fetch_one=False):
        """
        执行数据库查询
        
        Args:
            query (str): SQL查询语句
            params (tuple): 查询参数
            fetch_one (bool): 是否只获取一条记录
            
        Returns:
            查询结果
        """
        try:
            with self.get_connection().cursor() as cursor:
                cursor.execute(query, params or ())
                if fetch_one:
                    return cursor.fetchone()
                else:
                    return cursor.fetchall()
        except Exception as e:
            logger.error(f"Database query failed: {e}")
            raise
    
    def execute_update(self, query, params=None):
        """
        执行数据库更新操作（INSERT, UPDATE, DELETE）
        
        Args:
            query (str): SQL更新语句
            params (tuple): 更新参数
            
        Returns:
            int: 受影响的行数
        """
        try:
            with self.get_connection().cursor() as cursor:
                row_count = cursor.execute(query, params or ())
                self.get_connection().commit()
                return row_count
        except Exception as e:
            self.get_connection().rollback()
            logger.error(f"Database update failed: {e}")
            raise
    
    def get_count(self, query, params=None):
        """
        获取查询结果的计数
        
        Args:
            query (str): SQL查询语句
            params (tuple): 查询参数
            
        Returns:
            int: 查询结果的计数
        """
        result = self.execute_query(query, params, fetch_one=True)
        return result.get('count', 0) if result else 0
    
    def start_transaction(self):
        """开始事务"""
        if not self.transaction_active:
            self.get_connection().autocommit(False)
            self.transaction_active = True
    
    def commit(self):
        """提交事务"""
        if self.transaction_active:
            self.get_connection().commit()
            self.get_connection().autocommit(True)
            self.transaction_active = False
    
    def rollback(self):
        """回滚事务"""
        if self.transaction_active:
            self.get_connection().rollback()
            self.get_connection().autocommit(True)
            self.transaction_active = False


def get_db():
    """
    获取数据库连接实例
    
    Returns:
        DatabaseService: 数据库服务实例
    """
    # 检查应用上下文中是否已存在数据库服务实例
    if 'db_service' not in get_db.__dict__:
        get_db.db_service = DatabaseService()
    return get_db.db_service


def close_db(error=None):
    """
    关闭数据库连接
    
    Args:
        error: 异常信息（可选）
    """
    # 检查应用上下文中是否存在数据库服务实例
    if 'db_service' in get_db.__dict__:
        get_db.db_service.close()
        # 清除实例
        del get_db.db_service