from ...extensions.database.database import get_db


def fetch_student_by_id(student_id):
    """根据学生ID获取学生信息"""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.student_id, s.student_name, s.class_id, c.class_name
        FROM Students s
        LEFT JOIN Classes c ON s.class_id = c.class_id
        WHERE s.student_id = %s
    """, (student_id,))
    
    return cursor.fetchone()