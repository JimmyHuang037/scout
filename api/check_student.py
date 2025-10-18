import pymysql

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='Newuser1',
    database='school_management',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with connection.cursor() as cursor:
        cursor.execute("SELECT student_id, student_name FROM Students WHERE student_name = %s", ('谷雪',))
        result = cursor.fetchall()
        print(result)
finally:
    connection.close()
