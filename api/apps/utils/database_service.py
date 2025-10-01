import os
from flask import current_app
import pymysql
"""
数据库服务模块"""

def get_db_connection():
    """
    获取数据库连接
    
    Returns:
        pymysql.Connection: 数据库连接对象
    """
    try:
        # 从当前应用配置中获取数据库信息
        config = current_app.config
        db_config = {
            'host': config['MYSQL_HOST'],
            'user': config['MYSQL_USER'],
            'password': config['MYSQL_PASSWORD'],
            'database': config['MYSQL_DB'],
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        
        connection = pymysql.connect(**db_config)
        current_app.logger.info("Database connection established")
        current_app.logger.info(f"Connected to database: {config['MYSQL_DB']} on {config['MYSQL_HOST']} as {config['MYSQL_USER']}")
        return connection
    except Exception as e:
        current_app.logger.error(f"Failed to establish database connection: {str(e)}")
        raise

def execute_query(query, params=None):
    """
    执行SELECT查询
    
    Args:
        query (str): SQL查询语句
        params (tuple): 查询参数
        
    Returns:
        list: 查询结果
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
    except Exception as e:
        current_app.logger.error(f"Database query error: {str(e)}")
        current_app.logger.error(f"Query: {query}")
        current_app.logger.error(f"Params: {params}")
        raise
    finally:
        if connection:
            connection.close()

def execute_update(query, params=None):
    """
    执行INSERT/UPDATE/DELETE操作
    
    Args:
        query (str): SQL操作语句
        params (tuple): 操作参数
        
    Returns:
        int: 受影响的行数或插入记录的ID
    """
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            result = cursor.execute(query, params)
            connection.commit()
            
            # 如果是INSERT操作，返回插入记录的ID
            if query.strip().upper().startswith('INSERT'):
                return cursor.lastrowid
            else:
                return result
    except Exception as e:
        if connection:
            connection.rollback()
        current_app.logger.error(f"Database update error: {str(e)}")
        current_app.logger.error(f"Query: {query}")
        current_app.logger.error(f"Params: {params}")
        raise
    finally:
        if connection:
            connection.close()

class DatabaseService:
    """
    数据库服务类
    提供统一的数据库访问接口
    """
    
    def get_connection(self):
        """
        获取数据库连接
        
        Returns:
            pymysql.Connection: 数据库连接对象
        """
        return get_db_connection()
    
    def execute_query(self, query, params=None):
        """
        执行SELECT查询
        
        Args:
            query (str): SQL查询语句
            params (tuple): 查询参数
            
        Returns:
            list: 查询结果
        """
        return execute_query(query, params)
    
    def execute_update(self, query, params=None):
        """
        执行INSERT/UPDATE/DELETE操作
        
        Args:
            query (str): SQL操作语句
            params (tuple): 操作参数
            
        Returns:
            int: 受影响的行数或插入记录的ID
        """
        return execute_update(query, params)


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
        # DatabaseService不再需要显式关闭连接，由上下文管理
        del get_db.db_service