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
        cursor.execute("""
            SELECT s.student_id, s.student_name, c.class_name
            FROM Students s
            JOIN Classes c ON s.class_id = c.class_id
            LIMIT 10
        """)
        result = cursor.fetchall()
        for row in result:
            print(row)
finally:
    connection.close()
