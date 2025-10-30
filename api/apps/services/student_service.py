from apps.utils.database_service import DatabaseService
from flask import current_app


class StudentService:

    def __init__(self):
        self.db_service = DatabaseService()

    def get_student_profile(self, student_id):
        try:
            query = """
                SELECT s.student_id, s.student_name, c.class_name
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                WHERE s.student_id = %s
            """
            result = self.db_service.execute_query(query, (student_id,))
            if result:
                return result[0]
            return None
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get student profile for {student_id}: {str(e)}")
            raise

    def get_teacher_students(self, teacher_id, class_id=None):
        try:
            base_query = """
                SELECT s.student_id, s.student_name, c.class_name
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE tc.teacher_id = %s
            """
            params = [teacher_id]
            
            if class_id:
                base_query += " AND c.class_id = %s"
                params.append(class_id)
            
            base_query += " ORDER BY s.student_id"
            
            students = self.db_service.execute_query(base_query, params)
            current_app.logger.info(f"Retrieved {len(students)} students for teacher {teacher_id}")
            
            return students
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get teacher students: {str(e)}")
            raise

    def get_student_by_id(self, student_id):
        try:
            query = """
                SELECT s.student_id, s.student_name, c.class_name
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                WHERE s.student_id = %s
            """
            result = self.db_service.execute_query(query, (student_id,))
            if result:
                return result[0]
            return None
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get student by id {student_id}: {str(e)}")
            raise e
        

    def get_student_by_name(self, student_name):
        try:
            query = """
                SELECT s.student_id, s.student_name, c.class_name
                FROM `Students` s
                JOIN `Classes` c ON s.class_id = c.class_id
                WHERE s.student_name = %s
            """
            result = self.db_service.execute_query(query, (student_name,))
            if result:
                return result[0]
            return None
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get student by name {student_name}: {str(e)}")
            raise e

    def get_all_students(self):
        try:
            base_query = """
                SELECT s.student_id, s.student_name, c.class_name
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                ORDER BY s.student_id
            """
            
            students = self.db_service.execute_query(base_query)
            current_app.logger.info(f"Retrieved {len(students)} students")
            
            return students
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get all students: {str(e)}")
            raise

    def update_student_name(self, student_id, student_name):
        try:
            query = "UPDATE Students SET student_name = %s WHERE student_id = %s"
            params = (student_name, student_id)
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to update student name for {student_id}: {str(e)}")
            return False

    def create_student(self, student_data):
        try:
            student_query = """
                INSERT INTO Students (student_id, student_name, class_id, password)
                VALUES (%s, %s, %s, %s)
            """
            student_params = (
                student_data['student_id'],
                student_data['student_name'],
                student_data['class_id'],
                student_data.get('password', 'pass123')
            )
            
            self.db_service.execute_update(student_query, student_params)
            
            current_app.logger.info(f"Student {student_data['student_id']} created successfully")
            return {"student_id": student_data['student_id']}
            
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to create student: {str(e)}")
            raise

    def update_student(self, student_id, update_data):
        try:
            set_clauses = []
            params = []
            
            for key, value in update_data.items():
                if key in ['student_name', 'class_id']:
                    set_clauses.append(f"{key} = %s")
                    params.append(value)
            
            if not set_clauses:
                return False
            
            query = f"UPDATE Students SET {', '.join(set_clauses)} WHERE student_id = %s"
            params.append(student_id)
            
            result = self.db_service.execute_update(query, params)
            return result > 0
            
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to update student {student_id}: {str(e)}")
            return False

    def delete_student(self, student_id):
        try:
            check_query = "SELECT student_id FROM Students WHERE student_id = %s"
            student_exists = self.db_service.execute_query(check_query, (student_id,))
            
            if not student_exists:
                if current_app:
                    current_app.logger.warning(f"Student {student_id} not found for deletion")
                return False
            
            scores_query = "DELETE FROM Scores WHERE student_id = %s"
            scores_result = self.db_service.execute_update(scores_query, (student_id,))
            
            if current_app:
                current_app.logger.info(f"Deleted {scores_result} score records for student {student_id}")
            
            student_query = "DELETE FROM Students WHERE student_id = %s"
            student_result = self.db_service.execute_update(student_query, (student_id,))
            
            if current_app:
                current_app.logger.info(f"Delete student {student_id} result: {student_result}")
            
            return student_result > 0
            
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to delete student {student_id}: {str(e)}")
            return False

    def get_student_scores(self, student_id):
        try:
            query = """
                SELECT 
                    s.score_id,
                    s.student_id,
                    s.subject_id,
                    sub.subject_name,
                    s.exam_id,
                    e.exam_name,
                    s.score,
                    s.exam_date
                FROM Scores s
                JOIN Subjects sub ON s.subject_id = sub.subject_id
                JOIN Exams e ON s.exam_id = e.exam_id
                WHERE s.student_id = %s
                ORDER BY s.exam_date DESC, sub.subject_name
            """
            result = self.db_service.execute_query(query, (student_id,))
            return result
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get student scores for {student_id}: {str(e)}")
            raise

    def get_student_exam_results(self, student_id, exam_id=None):
        try:
            query = """
                SELECT 
                    s.student_id,
                    st.student_name,
                    e.exam_id,
                    e.exam_name,
                    e.exam_date,
                    sub.subject_id,
                    sub.subject_name,
                    s.score,
                    e.total_score
                FROM Scores s
                JOIN Students st ON s.student_id = st.student_id
                JOIN Exams e ON s.exam_id = e.exam_id
                JOIN Subjects sub ON s.subject_id = sub.subject_id
                WHERE s.student_id = %s
            """
            params = [student_id]
            
            if exam_id:
                query += " AND s.exam_id = %s"
                params.append(exam_id)
                
            query += " ORDER BY e.exam_date DESC, sub.subject_name"
            
            result = self.db_service.execute_query(query, params)
            return result
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get student exam results for {student_id}: {str(e)}")
            raise