from apps.utils.database_service import DatabaseService
from flask import current_app


class ScoreService:

    def __init__(self):
        self.db_service = DatabaseService()

    def get_student_scores(self, student_id):
        query = """
            SELECT s.score_id, s.score as score, s.exam_type_id as exam_name, 
                   s.subject_id as subject_name, s.student_id as student_name
            FROM Scores s
            WHERE s.student_id = %s
            ORDER BY s.exam_type_id
        """
        return self.db_service.execute_query(query, (student_id,))

    def get_student_scores_as_chinese_column(self, student_id):
        query = """
            SELECT s.score_id as 成绩编号, s.score as 成绩, et.exam_type_name as 考试类型, 
                   sub.subject_name as 科目, st.student_name as 学生姓名
            FROM Scores s
            JOIN Students st ON s.student_id = st.student_id
            JOIN Subjects sub ON s.subject_id = sub.subject_id
            JOIN ExamTypes et ON s.exam_type_id = et.exam_type_id
            WHERE s.student_id = %s
            ORDER BY s.exam_type_id
        """
        return self.db_service.execute_query(query, (student_id,))

    def get_student_exam_score(self, student_id, exam_id):
        query = """
            SELECT s.score_id, s.score, e.exam_id as exam_name, 
                   sub.subject_id as subject_name, st.student_id as student_name
            FROM Scores s
            JOIN Exams e ON s.exam_id = e.exam_id
            JOIN Subjects sub ON s.subject_id = sub.subject_id
            JOIN Students st ON s.student_id = st.student_id
            WHERE s.student_id = %s AND s.exam_id = %s
        """
        result = self.db_service.execute_query(query, (student_id, exam_id))
        return result[0] if result else None

    def enter_scores(self, exam_id, scores_data):
        try:
            inserted_count = 0
            updated_count = 0
            
            for score_data in scores_data:
                student_id = score_data['student_id']
                score = score_data['score']
                
                check_query = """
                    SELECT score_id FROM Scores 
                    WHERE exam_id = %s AND student_id = %s
                """
                existing = self.db_service.execute_query(check_query, (exam_id, student_id))
                
                if existing:
                    update_query = """
                        UPDATE Scores 
                        SET score = %s 
                        WHERE exam_id = %s AND student_id = %s
                    """
                    self.db_service.execute_update(update_query, (score, exam_id, student_id))
                    updated_count += 1
                else:
                    subject_query = "SELECT subject_id FROM Exams WHERE exam_id = %s"
                    subject_result = self.db_service.execute_query(subject_query, (exam_id,))
                    if not subject_result:
                        continue
                        
                    subject_id = subject_result[0]['subject_id']
                    
                    insert_query = """
                        INSERT INTO Scores (score, exam_id, subject_id, student_id)
                        VALUES (%s, %s, %s, %s)
                    """
                    self.db_service.execute_update(insert_query, (score, exam_id, subject_id, student_id))
                    inserted_count += 1
            
            return {
                'inserted_count': inserted_count,
                'updated_count': updated_count,
                'total_processed': inserted_count + updated_count
            }
        except Exception as e:
            current_app.logger.error(f"Error entering scores: {str(e)}")
            raise

    def get_exam_scores(self, exam_id):
        query = """
            SELECT s.score_id, s.score, s.exam_id, s.subject_id, s.student_id,
                   e.exam_name, e.exam_date, sub.subject_name, st.student_name, st.student_number
            FROM Scores s
            JOIN Exams e ON s.exam_id = e.exam_id
            JOIN Subjects sub ON s.subject_id = sub.subject_id
            JOIN Students st ON s.student_id = st.student_id
            WHERE s.exam_id = %s
            ORDER BY st.student_number
        """
        return self.db_service.execute_query(query, (exam_id,))

    def update_score(self, score_id, score_data):
        check_query = "SELECT 1 FROM Scores WHERE score_id = %s"
        check_result = self.db_service.execute_query(check_query, (score_id,))
        if not check_result:
            return None
            
        update_query = "UPDATE Scores SET score = %s WHERE score_id = %s"
        self.db_service.execute_update(update_query, (score_data['score'], score_id))
        
        query = """
            SELECT s.score_id, s.score, s.exam_type_id, s.subject_id, s.student_id,
                   et.exam_type_name as exam_name, sub.subject_name, st.student_name, st.student_id as student_number
            FROM Scores s
            JOIN ExamTypes et ON s.exam_type_id = et.exam_type_id
            JOIN Subjects sub ON s.subject_id = sub.subject_id
            JOIN Students st ON s.student_id = st.student_id
            WHERE s.score_id = %s
        """
        result = self.db_service.execute_query(query, (score_id,))
        return result[0] if result else None

    def get_exam_statistics(self, exam_id):
        exam_query = """
            SELECT exam_name, subject_id FROM Exams 
            WHERE exam_id = %s
        """
        exam_result = self.db_service.execute_query(exam_query, (exam_id,))
        if not exam_result:
            return None
            
        stats_query = """
            SELECT 
                COUNT(*) as total_students,
                AVG(score) as average_score,
                MAX(score) as highest_score,
                MIN(score) as lowest_score
            FROM Scores 
            WHERE exam_id = %s
        """
        stats_result = self.db_service.execute_query(stats_query, (exam_id,))
        
        statistics = {
            'exam_name': exam_result[0]['exam_name'],
            'subject_id': exam_result[0]['subject_id'],
            'statistics': stats_result[0] if stats_result else None
        }
        
        return statistics

    def get_exam_class_scores(self, exam_id, class_id, teacher_id):
        query = """
            SELECT s.score_id, s.score, s.exam_id, s.subject_id, s.student_id,
                   e.exam_name, e.exam_date, sub.subject_name, st.student_name, st.student_number
            FROM Scores s
            JOIN Exams e ON s.exam_id = e.exam_id
            JOIN Subjects sub ON s.subject_id = sub.subject_id
            JOIN Students st ON s.student_id = st.student_id
            WHERE s.exam_id = %s AND st.class_id = %s
            ORDER BY st.student_number
        """
        return self.db_service.execute_query(query, (exam_id, class_id))

    def get_student_exam_results(self, student_id):
        query = """
            SELECT er.exam_type as exam_name, er.student_name, 
                   er.chinese, er.math, er.english, 
                   er.physics, er.chemistry, er.politics,
                   er.total_score, er.ranking
            FROM exam_results er
            WHERE er.student_name = (
                SELECT student_name FROM Students WHERE student_id = %s
            )
            ORDER BY er.exam_type
        """
        return self.db_service.execute_query(query, (student_id,))

    def create_score(self, score_data):
        try:
            student_id = score_data.get('student_id')
            subject_id = score_data.get('subject_id')
            exam_type_id = score_data.get('exam_type_id')
            score_value = score_data.get('score')
            
            if not all([student_id, subject_id, exam_type_id, score_value is not None]):
                raise ValueError("Missing required parameters")
            
            insert_query = """
                INSERT INTO Scores (student_id, subject_id, exam_type_id, score)
                VALUES (%s, %s, %s, %s)
            """
            score_id = self.db_service.execute_update(
                insert_query, 
                (student_id, subject_id, exam_type_id, score_value)
            )
            
            return score_id
        except Exception as e:
            current_app.logger.error(f"Failed to create score: {str(e)}")
            raise

    def delete_score(self, score_id):
        try:
            query = "DELETE FROM Scores WHERE score_id = %s"
            self.db_service.execute_update(query, (score_id,))
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to delete score: {str(e)}")
            raise
        finally:
            self.db_service.close()

    def get_teacher_scores(self, teacher_id):
        try:
            query = """
                SELECT s.score_id, s.score, s.exam_type_id, s.subject_id, s.student_id,
                       et.exam_type_name as exam_name, sub.subject_name, 
                       st.student_name, st.student_id as student_number
                FROM Scores s
                JOIN Students st ON s.student_id = st.student_id
                JOIN Subjects sub ON s.subject_id = sub.subject_id
                JOIN ExamTypes et ON s.exam_type_id = et.exam_type_id
                JOIN TeacherClasses tc ON st.class_id = tc.class_id
                WHERE tc.teacher_id = %s
                ORDER BY s.score_id DESC
            """
            scores = self.db_service.execute_query(query, (teacher_id,))
            
            return scores
        except Exception as e:
            raise e
