from apps.utils.database_service import DatabaseService
from flask import current_app


class UserService:

    def __init__(self):
        self.db_service = DatabaseService()

    def authenticate_user(self, user_id, password):
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