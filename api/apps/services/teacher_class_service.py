from apps.utils.database_service import DatabaseService
from flask import current_app


class TeacherClassService:

    def __init__(self):
        self.db_service = DatabaseService()

    def get_all_teacher_classes(self, page=1, per_page=10):
        offset = (page - 1) * per_page
        count_query = "SELECT COUNT(*) as count FROM TeacherClasses"
        total_result = self.db_service.execute_query(count_query, ())
        total = total_result[0]['count'] if total_result else 0
        query = """
            SELECT tc.teacher_id, tc.class_id,
                   t.teacher_name, c.class_name
            FROM TeacherClasses tc
            JOIN Teachers t ON tc.teacher_id = t.teacher_id
            JOIN Classes c ON tc.class_id = c.class_id
            ORDER BY tc.teacher_id, tc.class_id
            LIMIT %s OFFSET %s
        """
        teacher_classes = self.db_service.execute_query(query, (per_page, offset))
        return {
            'teacher_classes': teacher_classes,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }

    def get_teacher_class_by_teacher(self, teacher_id):
        query = """
            SELECT tc.teacher_id, tc.class_id,
                   t.teacher_name, c.class_name
            FROM TeacherClasses tc
            JOIN Teachers t ON tc.teacher_id = t.teacher_id
            JOIN Classes c ON tc.class_id = c.class_id
            WHERE tc.teacher_id = %s
            ORDER BY tc.class_id
        """
        return self.db_service.execute_query(query, (teacher_id,))

    def get_teacher_class(self, teacher_id, class_id):
        query = """
            SELECT tc.teacher_id, tc.class_id,
                   t.teacher_name, c.class_name
            FROM TeacherClasses tc
            JOIN Teachers t ON tc.teacher_id = t.teacher_id
            JOIN Classes c ON tc.class_id = c.class_id
            WHERE tc.teacher_id = %s AND tc.class_id = %s
        """
        result = self.db_service.execute_query(query, (teacher_id, class_id))
        return result[0] if result else None

    def create_teacher_class(self, teacher_id, class_id):
        teacher_query = "SELECT teacher_id FROM Teachers WHERE teacher_id = %s"
        class_query = "SELECT class_id FROM Classes WHERE class_id = %s"
        teacher_result = self.db_service.execute_query(teacher_query, (teacher_id,))
        class_result = self.db_service.execute_query(class_query, (class_id,))
        if not teacher_result:
            raise ValueError(f"Teacher with ID {teacher_id} not found")
        if not class_result:
            raise ValueError(f"Class with ID {class_id} not found")
        check_query = """
            SELECT teacher_id FROM TeacherClasses 
            WHERE teacher_id = %s AND class_id = %s
        """
        existing = self.db_service.execute_query(check_query, (teacher_id, class_id))
        if existing:
            raise ValueError("Teacher-class association already exists")
        insert_query = """
            INSERT INTO TeacherClasses (teacher_id, class_id)
            VALUES (%s, %s)
        """
        self.db_service.execute_update(insert_query, (teacher_id, class_id))
        return True

    def update_teacher_class(self, teacher_id, class_id, new_teacher_id):
        check_query = "SELECT teacher_id FROM TeacherClasses WHERE teacher_id = %s AND class_id = %s"
        existing = self.db_service.execute_query(check_query, (teacher_id, class_id))
        if not existing:
            return False
        if new_teacher_id:
            teacher_query = "SELECT teacher_id FROM Teachers WHERE teacher_id = %s"
            teacher_result = self.db_service.execute_query(teacher_query, (new_teacher_id,))
            if not teacher_result:
                raise ValueError("New teacher not found")
        update_query = """
            UPDATE TeacherClasses 
            SET teacher_id = %s
            WHERE teacher_id = %s AND class_id = %s
        """
        self.db_service.execute_update(
            update_query,
            (new_teacher_id, teacher_id, class_id)
        )
        return True

    def delete_teacher_class(self, teacher_id, class_id):
        check_query = "SELECT teacher_id FROM TeacherClasses WHERE teacher_id = %s AND class_id = %s"
        existing = self.db_service.execute_query(check_query, (teacher_id, class_id))
        if not existing:
            return False
        delete_query = "DELETE FROM TeacherClasses WHERE teacher_id = %s AND class_id = %s"
        self.db_service.execute_update(delete_query, (teacher_id, class_id))
        return True