from flask import current_app
import pymysql


def get_db_connection():
    try:
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
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            result = cursor.execute(query, params)
            connection.commit()
            
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
    
    def get_connection(self):
        return get_db_connection()
    
    def execute_query(self, query, params=None):
        return execute_query(query, params)
    
    def execute_update(self, query, params=None):
        return execute_update(query, params)


