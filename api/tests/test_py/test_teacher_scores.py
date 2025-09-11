from app.factory import create_app
import json

app = create_app('testing')

with app.test_client() as client:
    # Login as teacher
    response = client.post('/api/auth/login', json={
        'user_id': '1',
        'password': 'test123'
    })
    print(f"Login response status: {response.status_code}")
    print(f"Login response data: {response.get_json()}")
    
    # Try to get scores
    response = client.get('/api/teacher/scores')
    print(f"Get scores response status: {response.status_code}")
    print(f"Get scores response data: {response.get_json()}")