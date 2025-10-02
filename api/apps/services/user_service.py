from apps.utils.database_service import DatabaseService
from flask import current_app

"""用户服务类"""


class UserService:
    """用户服务类"""

    def __init__(self):
        """初始化用户服务"""
        self.db_service = DatabaseService()

    def authenticate_user(self, user_id, password):
        """
        验证用户凭证
        
        Args:
            user_id (str): 用户ID
            password (str): 密码
            
        Returns:
            dict: 用户信息，如果验证失败则返回None
        """
        try:
            query = """
                SELECT user_id, user_name as username, role, password 
                FROM users 
                WHERE user_id = %s AND password = %s
            """
            result = self.db_service.execute_query(query, (user_id, password))
            
            if result:
                return result[0]
            return None
        except Exception as e:
            current_app.logger.error(f"User authentication error: {str(e)}")
            raise