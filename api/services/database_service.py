"""数据库服务模块，提供统一的数据库操作接口"""
import mysql.connector
from flask import current_app, g


def get_db():
    """获取数据库连接"""
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
    return g.db


def close_db(e=None):
    """关闭数据库连接"""
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()


class DatabaseService:
    """数据库服务类"""
    
    def __init__(self):
        """初始化数据库服务"""
        self.db = get_db()
        self.cursor = self.db.cursor(dictionary=True)
    
    def execute_query(self, query, params=None, fetch_one=False):
        """
        执行数据库查询操作
        
        Args:
            query (str): SQL查询语句
            params (tuple, optional): 查询参数
            fetch_one (bool): 是否只获取一条记录
            
        Returns:
            dict or list: 查询结果
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
                
            if fetch_one:
                return self.cursor.fetchone()
            else:
                return self.cursor.fetchall()
        except Exception as e:
            raise e
    
    def execute_update(self, query, params=None):
        """
        执行数据库更新操作（INSERT, UPDATE, DELETE）
        
        Args:
            query (str): SQL更新语句
            params (tuple, optional): 更新参数
            
        Returns:
            int: 受影响的行数
        """
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
                
            self.db.commit()
            return self.cursor.rowcount
        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_count(self, query, params=None):
        """
        获取记录总数
        
        Args:
            query (str): SQL计数查询语句
            params (tuple, optional): 查询参数
            
        Returns:
            int: 记录总数
        """
        result = self.execute_query(query, params, fetch_one=True)
        return result['count'] if result else 0
    
    def close(self):
        """关闭数据库连接"""
        if self.cursor:
            self.cursor.close()