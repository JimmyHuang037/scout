from apps.utils.database_service import DatabaseService
from flask import current_app


class ClassService:
    def __init__(self):
        self.db_service = DatabaseService()

    def get_all_classes(self):
        try:
            query = """
                SELECT c.class_id, c.class_name, 
                       COUNT(s.student_id) as student_count
                FROM Classes c
                LEFT JOIN Students s ON c.class_id = s.class_id
                GROUP BY c.class_id, c.class_name
                ORDER BY c.class_id
            """
            classes = self.db_service.execute_query(query)
            
            return classes
            
        except Exception as e:
            current_app.logger.error(f"Error getting all classes: {str(e)}")
            raise e
    
    def get_class_by_id(self, class_id):
        try:
            query = """
                SELECT c.class_id, c.class_name, 
                       COUNT(s.student_id) as student_count
                FROM Classes c
                LEFT JOIN Students s ON c.class_id = s.class_id
                WHERE c.class_id = %s
                GROUP BY c.class_id, c.class_name
            """
            result = self.db_service.execute_query(query, (class_id,))
            return result[0] if result else None
        except Exception as e:
            current_app.logger.error(f"Error getting class by id {class_id}: {str(e)}")
            raise e
    
    def create_class(self, class_data):
        try:
            query = "INSERT INTO Classes (class_name) VALUES (%s)"
            params = (class_data.get('class_name'),)
            self.db_service.execute_update(query, params)
            
            select_query = """
                SELECT class_id, class_name
                FROM Classes
                WHERE class_name = %s
                ORDER BY class_id DESC
                LIMIT 1
            """
            select_params = (class_data.get('class_name'),)
            result = self.db_service.execute_query(select_query, select_params)
            class_info = result[0] if result else None
            return class_info
        except Exception as e:
            current_app.logger.error(f"Error creating class: {str(e)}")
            raise e
    
    def update_class(self, class_id, class_data):
        try:
            fields = []
            params = []
            
            for key, value in class_data.items():
                if key in ['class_name']:
                    fields.append(f"{key} = %s")
                    params.append(value)
            
            if not fields:
                return True
                
            params.append(class_id)
            update_query = f"UPDATE Classes SET {', '.join(fields)} WHERE class_id = %s"
            self.db_service.execute_update(update_query, params)
            
            # Get updated class
            select_query = """
                SELECT c.class_id, c.class_name
                FROM Classes c
                WHERE c.class_id = %s
            """
            result = self.db_service.execute_query(select_query, (class_id,))
            return result[0] if result else None
        except Exception as e:
            current_app.logger.error(f"Error updating class {class_id}: {str(e)}")
            return False
    
    def delete_class(self, class_id):
        try:
            # Check if class exists and has students
            check_query = """
                SELECT COUNT(s.student_id) as student_count
                FROM Classes c
                LEFT JOIN Students s ON c.class_id = s.class_id
                WHERE c.class_id = %s
                GROUP BY c.class_id
            """
            result = self.db_service.execute_query(check_query, (class_id,))
            
            if result and result[0]['student_count'] > 0:
                return False, "Cannot delete class with students"
            
            delete_query = "DELETE FROM Classes WHERE class_id = %s"
            self.db_service.execute_update(delete_query, (class_id,))
            return True, "Class deleted successfully"
        except Exception as e:
            current_app.logger.error(f"Error deleting class {class_id}: {str(e)}")
            return False, str(e)
    
    def get_students_by_class(self, class_id, teacher_id=None):
        try:
            if teacher_id:
                query = """
                    SELECT s.student_id, s.student_name
                    FROM Students s
                    JOIN Classes c ON s.class_id = c.class_id
                    JOIN TeacherClasses tc ON c.class_id = tc.class_id
                    WHERE c.class_id = %s AND tc.teacher_id = %s
                    ORDER BY s.student_id
                """
                students = self.db_service.execute_query(query, (class_id, teacher_id))
            else:
                query = """
                    SELECT s.student_id, s.student_name
                    FROM Students s
                    WHERE s.class_id = %s
                    ORDER BY s.student_id
                """
                students = self.db_service.execute_query(query, (class_id,))
            
            return students
        except Exception as e:
            current_app.logger.error(f"Error getting students by class {class_id}: {str(e)}")
            raise e