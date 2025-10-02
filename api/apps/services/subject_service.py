from apps.utils.database_service import DatabaseService
from flask import current_app


class SubjectService:

    def __init__(self):
        self.db_service = DatabaseService()

    def get_all_subjects(self, page=1, per_page=10):
        try:
            offset = (page - 1) * per_page
            
            count_query = "SELECT COUNT(*) as total FROM Subjects"
            total_result = self.db_service.execute_query(count_query)
            total = total_result[0]['total'] if total_result else 0
            
            query = "SELECT subject_id, subject_name FROM Subjects ORDER BY subject_id LIMIT %s OFFSET %s"
            subjects = self.db_service.execute_query(query, (per_page, offset))
            
            pages = (total + per_page - 1) // per_page
            
            return {
                'subjects': subjects,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages
                }
            }
        except Exception as e:
            current_app.logger.error(f"Failed to get all subjects: {str(e)}")
            raise e

    def get_subject_by_id(self, subject_id):
        try:
            query = "SELECT subject_id, subject_name FROM Subjects WHERE subject_id = %s"
            result = self.db_service.execute_query(query, (subject_id,))
            return result[0] if result else None
        except Exception as e:
            current_app.logger.error(f"Failed to get subject by id {subject_id}: {str(e)}")
            raise e
    
    def create_subject(self, subject_data):
        try:
            check_query = "SELECT subject_id FROM Subjects WHERE subject_name = %s"
            existing = self.db_service.execute_query(check_query, (subject_data['subject_name'],))
            if existing:
                raise ValueError("Subject name already exists")
            
            insert_query = "INSERT INTO Subjects (subject_name) VALUES (%s)"
            subject_id = self.db_service.execute_update(insert_query, (subject_data['subject_name'],))
            
            return subject_id
        except Exception as e:
            current_app.logger.error(f"Failed to create subject: {str(e)}")
            raise e
    
    def update_subject(self, subject_id, subject_data):
        try:
            if not self.get_subject_by_id(subject_id):
                return False
                
            update_query = "UPDATE Subjects SET subject_name = %s WHERE subject_id = %s"
            self.db_service.execute_update(update_query, (subject_data['subject_name'], subject_id))
            
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to update subject {subject_id}: {str(e)}")
            return False

    def delete_subject(self, subject_id):
        try:
            if not self.get_subject_by_id(subject_id):
                return False
            
            delete_query = "DELETE FROM Subjects WHERE subject_id = %s"
            self.db_service.execute_update(delete_query, (subject_id,))
            
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to delete subject {subject_id}: {str(e)}")
            return False