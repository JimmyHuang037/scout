from apps.utils.database_service import DatabaseService
from flask import current_app


class TeacherClassService:

    def __init__(self):
        self.db_service = DatabaseService()

    def get_all_teacher_classes(self):
        query = """
            SELECT tc.teacher_id, tc.class_id,
                   t.teacher_name, c.class_name
            FROM TeacherClasses tc
            JOIN Teachers t ON tc.teacher_id = t.teacher_id
            JOIN Classes c ON tc.class_id = c.class_id
            ORDER BY tc.teacher_id, tc.class_id
        """
        teacher_classes = self.db_service.execute_query(query)
        return teacher_classes

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
        try:
            # Check if the relationship already exists
            check_query = "SELECT * FROM TeacherClasses WHERE teacher_id = %s AND class_id = %s"
            existing = self.db_service.execute_query(check_query, (teacher_id, class_id))
            if existing:
                raise ValueError("Teacher-class relationship already exists")

            # Create the relationship
            insert_query = "INSERT INTO TeacherClasses (teacher_id, class_id) VALUES (%s, %s)"
            self.db_service.execute_update(insert_query, (teacher_id, class_id))

            # Return the created relationship
            select_query = """
                SELECT tc.teacher_id, tc.class_id,
                       t.teacher_name, c.class_name
                FROM TeacherClasses tc
                JOIN Teachers t ON tc.teacher_id = t.teacher_id
                JOIN Classes c ON tc.class_id = c.class_id
                WHERE tc.teacher_id = %s AND tc.class_id = %s
            """
            result = self.db_service.execute_query(select_query, (teacher_id, class_id))
            return result[0] if result else None

        except Exception as e:
            current_app.logger.error(f"Error creating teacher class relationship: {str(e)}")
            raise e

    def update_teacher_class(self, teacher_id, class_id, new_teacher_id):
        try:
            # Check if the relationship exists
            existing = self.get_teacher_class(teacher_id, class_id)
            if not existing:
                return False

            # Update the relationship
            update_query = "UPDATE TeacherClasses SET teacher_id = %s WHERE teacher_id = %s AND class_id = %s"
            self.db_service.execute_update(update_query, (new_teacher_id, teacher_id, class_id))

            return True
        except Exception as e:
            current_app.logger.error(f"Error updating teacher class relationship: {str(e)}")
            return False

    def delete_teacher_class(self, teacher_id, class_id):
        try:
            # Check if the relationship exists
            existing = self.get_teacher_class(teacher_id, class_id)
            if not existing:
                return False
    
            # Delete the relationship
            delete_query = "DELETE FROM TeacherClasses WHERE teacher_id = %s AND class_id = %s"
            self.db_service.execute_update(delete_query, (teacher_id, class_id))
    
            return True
        except Exception as e:
            current_app.logger.error(f"Error deleting teacher class relationship: {str(e)}")
            return False