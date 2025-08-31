"""数据库工具模块，提供统一的数据库操作接口"""
import mysql.connector
import logging
from flask import current_app, g

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 创建logger
logger = logging.getLogger('app')

# 在测试环境中降低数据库相关日志级别
from flask import has_app_context
if has_app_context() and current_app.config.get('TESTING'):
    logger.setLevel(logging.CRITICAL)
    logging.getLogger('mysql.connector').setLevel(logging.CRITICAL)


def get_db():
    """获取数据库连接"""
    if 'db' not in g:
        try:
            g.db = mysql.connector.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['MYSQL_DB']
            )
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Failed to connect to database: {str(e)}")
            raise e
    return g.db


def close_db(e=None):
    """关闭数据库连接"""
    db = g.pop('db', None)
    if db is not None and db.is_connected():
        db.close()
        logger.info("Database connection closed")


class DatabaseService:
    """数据库服务类"""
    
    def __init__(self):
        """初始化数据库服务"""
        try:
            self.db = get_db()
            self.cursor = self.db.cursor(dictionary=True)
            self._in_transaction = False  # 添加事务状态跟踪
            logger.info("DatabaseService initialized")
        except Exception as e:
            logger.error(f"Failed to initialize DatabaseService: {str(e)}")
            raise e
    
    @property
    def transaction_active(self):
        """检查是否有活动的事务"""
        try:
            # 首先检查我们自己的事务状态跟踪
            if self._in_transaction:
                logger.debug(f"Transaction active: self tracked = {self._in_transaction}")
                return True
            # 然后检查连接的事务状态
            if (self.db is not None and 
                hasattr(self.db, 'in_transaction') and 
                self.db.in_transaction):
                logger.debug(f"Transaction active: connection tracked = {self.db.in_transaction}")
                return True
            logger.debug(f"Transaction not active. Self tracked: {self._in_transaction}")
            return False
        except Exception as e:
            logger.error(f"Error checking transaction status: {str(e)}")
            # 如果无法检查事务状态，返回False
            return False
    
    def start_transaction(self):
        """开始事务"""
        try:
            if self.transaction_active:
                app_logger.warning("Transaction already in progress")
                logger.debug("Transaction already in progress, not starting new one")
                return  # 如果事务已经在进行中，则不重复启动
            self.db.start_transaction()
            self._in_transaction = True  # 更新事务状态跟踪
            logger.debug("Transaction started")
        except Exception as e:
            logger.error(f"Failed to start transaction: {str(e)}")
            raise e
    
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
            logger.debug(f"Executing query: {query} with params: {params}")
            self.cursor.execute(query, params or ())
            result = self.cursor.fetchone() if fetch_one else self.cursor.fetchall()
            logger.debug(f"Query executed successfully, returned {len(result) if isinstance(result, list) else 1} rows")
            return result
        except Exception as e:
            logger.error(f"Failed to execute query: {str(e)}")
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
            logger.debug(f"Executing update: {query} with params: {params}")
            self.cursor.execute(query, params or ())
            # 只有在不在事务中时才自动提交
            if not self.transaction_active:
                self.db.commit()
                self._in_transaction = False  # 确保事务状态正确
            affected_rows = self.cursor.rowcount
            logger.debug(f"Update executed successfully, affected {affected_rows} rows")
            return affected_rows
        except Exception as e:
            logger.error(f"Failed to execute update: {str(e)}")
            self.db.rollback()
            self._in_transaction = False  # 确保事务状态正确
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
    
    def commit(self):
        """提交事务"""
        try:
            self.db.commit()
            self._in_transaction = False  # 更新事务状态跟踪
            logger.debug("Transaction committed")
        except Exception as e:
            logger.error(f"Failed to commit transaction: {str(e)}")
            self.rollback()
            raise e
    
    def rollback(self):
        """回滚事务"""
        try:
            self.db.rollback()
            self._in_transaction = False  # 更新事务状态跟踪
            logger.debug("Transaction rolled back")
        except Exception as e:
            logger.error(f"Failed to rollback transaction: {str(e)}")
            raise e
    
    def in_transaction(self):
        """检查是否在事务中"""
        try:
            return self.db.in_transaction
        except Exception as e:
            logger.error(f"Failed to check transaction status: {str(e)}")
            return False
    
    def close(self):
        """关闭数据库连接"""
        try:
            if self.cursor:
                self.cursor.close()
            logger.info("DatabaseService closed")
        except Exception as e:
            logger.error(f"数据库服务关闭失败: {str(e)}")