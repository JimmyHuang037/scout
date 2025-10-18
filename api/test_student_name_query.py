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
        # 使用参数化查询测试get_student_by_name方法中的查询
        query = """
            SELECT s.student_id, s.student_name, c.class_name
            FROM `Students` s
            JOIN `Classes` c ON s.class_id = c.class_id
            WHERE s.student_name = %s
        """
        cursor.execute(query, ('谷雪',))
        result = cursor.fetchall()
        print("使用参数化查询的结果:")
        print(result)
        
        # 测试原始方法中的查询语句（有错误的）
        query_original = """
            SELECT s. student_id , s.student_name, c.class_name
            FROM `Students` s
            JOIN `Classes` c on s.class_id = c.class_id
            WHERE s.student_name = "%s"
        """
        cursor.execute(query_original, ('谷雪',))
        result_original = cursor.fetchall()
        print("\n使用原始方法中的查询语句的结果:")
        print(result_original)
finally:
    connection.close()
