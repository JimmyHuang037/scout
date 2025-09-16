import pymysql

# 连接到测试数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='Newuser1',
    database='school_management_test'
)

cursor = conn.cursor()

# 检查用户数量
cursor.execute('SELECT COUNT(*) FROM users')
count = cursor.fetchone()[0]
print(f'用户数量: {count}')

# 获取所有用户
cursor.execute('SELECT user_id, user_name, password, role FROM users')
results = cursor.fetchall()
for row in results:
    print(f"用户ID: {row[0]}, 姓名: {row[1]}, 密码: {row[2]}, 角色: {row[3]}")

conn.close()