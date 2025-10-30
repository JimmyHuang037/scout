from apps.services.class_service import ClassService
from apps.utils.database_service import DatabaseService
from flask import current_app


class TeacherService:
    def __init__(self):
        self.db_service = DatabaseService()
        self.class_service = ClassService()

    def get_teacher_profile(self, teacher_id):
        try:
            query = """
                SELECT t.teacher_id, t.teacher_name, s.subject_name
                FROM Teachers t
                LEFT JOIN Subjects s ON t.subject_id = s.subject_id
                WHERE t.teacher_id = %s
            """
            result = self.db_service.execute_query(query, (teacher_id,))
            return result[0] if result else None
        except Exception as e:
            current_app.logger.error(f"Error getting teacher profile {teacher_id}: {str(e)}")
            raise e

    def get_teacher_classes(self, teacher_id):
        try:
            query = """
                SELECT c.class_id, c.class_name
                FROM Classes c
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE tc.teacher_id = %s
                ORDER BY c.class_id
            """
            classes = self.db_service.execute_query(query, (teacher_id,))
            return classes
        except Exception as e:
            current_app.logger.error(f"Error getting teacher classes for {teacher_id}: {str(e)}")
            raise e

    def get_all_classes_students(self, teacher_id):
        try:
            query = """
                SELECT s.student_id, s.student_name, c.class_name, c.class_id
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE tc.teacher_id = %s
                ORDER BY c.class_id, s.student_id
            """
            students = self.db_service.execute_query(query, (teacher_id,))
            
            class_students = {}
            for student in students:
                class_id = student['class_id']
                if class_id not in class_students:
                    class_students[class_id] = {
                        'class_id': class_id,
                        'class_name': student['class_name'],
                        'students': []
                    }
                class_students[class_id]['students'].append({
                    'student_id': student['student_id'],
                    'student_name': student['student_name']
                })
            
            result = list(class_students.values())
            
            return {
                'classes': result
            }
        except Exception as e:
            raise e

    def get_all_teachers(self):
        try:
            query = """
                SELECT t.teacher_id, t.teacher_name, t.subject_id, s.subject_name
                FROM Teachers t
                LEFT JOIN Subjects s ON t.subject_id = s.subject_id
                ORDER BY t.teacher_id
            """
            teachers = self.db_service.execute_query(query)
            
            return teachers
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get all teachers: {str(e)}")
            raise e

    def get_teacher_by_id(self, teacher_id):
        try:
            query = """
                SELECT t.teacher_id, t.teacher_name, t.subject_id, s.subject_name
                FROM Teachers t
                LEFT JOIN Subjects s ON t.subject_id = s.subject_id
                WHERE t.teacher_id = %s
            """
            result = self.db_service.execute_query(query, (teacher_id,))
            return result[0] if result else None
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get teacher by id {teacher_id}: {str(e)}")
            raise e

    def create_teacher(self, teacher_data):
        try:
            # Check if teacher already exists
            check_query = "SELECT teacher_id FROM Teachers WHERE teacher_name = %s AND subject_id = %s"
            existing = self.db_service.execute_query(check_query, (teacher_data['teacher_name'], teacher_data['subject_id']))
            if existing:
                raise ValueError("Teacher with same name and subject already exists")
            
            # Insert new teacher
            insert_query = "INSERT INTO Teachers (teacher_name, subject_id, password) VALUES (%s, %s, %s)"
            teacher_id = self.db_service.execute_update(
                insert_query, 
                (teacher_data['teacher_name'], teacher_data['subject_id'], teacher_data.get('password', 'pass123'))
            )
            
            # Get the created teacher
            select_query = """
                SELECT t.teacher_id, t.teacher_name, t.subject_id, s.subject_name
                FROM Teachers t
                LEFT JOIN Subjects s ON t.subject_id = s.subject_id
                WHERE t.teacher_id = %s
            """
            result = self.db_service.execute_query(select_query, (teacher_id,))
            return result[0] if result else None
            
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to create teacher: {str(e)}")
            raise e

    def update_teacher(self, teacher_id, teacher_data):
        try:
            # Check if teacher exists
            if not self.get_teacher_by_id(teacher_id):
                return False
            
            # Build update query dynamically
            fields = []
            params = []
            
            for key, value in teacher_data.items():
                if key in ['teacher_name', 'subject_id', 'password']:
                    fields.append(f"{key} = %s")
                    params.append(value)
            
            if not fields:
                return True  # Nothing to update
            
            params.append(teacher_id)
            update_query = f"UPDATE Teachers SET {', '.join(fields)} WHERE teacher_id = %s"
            self.db_service.execute_update(update_query, params)
            
            return True
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to update teacher {teacher_id}: {str(e)}")
            return False
    
    def delete_teacher(self, teacher_id):
        connection = None
        try:
            connection = self.db_service.get_connection()
            connection.autocommit(False)
            
            with connection.cursor() as cursor:
                # 检查教师是否存在
                check_query = "SELECT COUNT(*) as count FROM Teachers WHERE teacher_id = %s"
                cursor.execute(check_query, (teacher_id,))
                check_result = cursor.fetchone()
                
                if not check_result or check_result['count'] == 0:
                    connection.rollback()
                    current_app.logger.warning(f"Teacher {teacher_id} does not exist")
                    return False
                
                # 删除与该教师相关的考试记录（如果表存在）
                try:
                    delete_exams_query = "DELETE FROM Exams WHERE teacher_id = %s"
                    cursor.execute(delete_exams_query, (teacher_id,))
                except Exception as e:
                    current_app.logger.warning(f"Could not delete exams for teacher {teacher_id}: {str(e)}")
                
                # 删除教师班级关联记录
                delete_tc_query = "DELETE FROM TeacherClasses WHERE teacher_id = %s"
                cursor.execute(delete_tc_query, (teacher_id,))
                
                # 删除教师本身
                delete_teacher_query = "DELETE FROM Teachers WHERE teacher_id = %s"
                affected_rows = cursor.execute(delete_teacher_query, (teacher_id,))
                
                connection.commit()
                return affected_rows > 0
                
        except Exception as e:
            if connection:
                connection.rollback()
            if current_app:
                current_app.logger.error(f"Failed to delete teacher {teacher_id}: {str(e)}")
            raise e
        finally:
            if connection:
                connection.autocommit(True)
