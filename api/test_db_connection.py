from app.factory import create_app
from utils.database_service import DatabaseService

app = create_app('testing')

with app.app_context():
    db = DatabaseService()
    result = db.execute_query('SELECT user_id, user_name, password, role FROM users WHERE user_id IN (%s, %s, %s)', ('1', 'S0201', 'admin'))
    print(result)
    db.close()