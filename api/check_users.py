import pymysql

# Connect to the test database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='Newuser1',
    database='school_management_test'
)

cursor = conn.cursor()

# Check the number of users
cursor.execute('SELECT COUNT(*) FROM users')
count = cursor.fetchone()[0]
print(f'Number of users: {count}')

# Get the first 5 users
cursor.execute('SELECT user_id, user_name, password, role FROM users LIMIT 5')
results = cursor.fetchall()
for row in results:
    print(row)

conn.close()