"""成绩服务模块，处理与成绩相关的业务逻辑"""

from flask import current_app
from apps.utils.database_service import DatabaseService


class ScoreService:
    """成绩服务类"""

    def __init__(self):
        """初始化成绩服务"""
        self.db_service = DatabaseService()

    def get_student_scores(self, student_id):
        """
        获取学生成绩列表
        
        Args:
            student_id (int): 学生ID
            
        Returns:
            list: 成绩列表
        """
        query = """
            SELECT s.score_id, s.score_value as score, s.exam_type_name as exam_name, 
                   s.subject_name as subject_name, s.student_name
            FROM scores s
            WHERE s.student_name = (
                SELECT student_name FROM students WHERE student_id = %s
            )
            ORDER BY s.exam_type_name
        """
        return self.db_service.execute_query(query, (student_id,))

    def get_student_exam_score(self, student_id, exam_id):
        """
        获取学生指定考试的成绩
        
        Args:
            student_id (int): 学生ID
            exam_id (int): 考试ID
            
        Returns:
            dict: 考试成绩
        """
        query = """
            SELECT s.score_id, s.score, s.exam_id, s.subject_id, s.student_id,
                   e.exam_name, e.exam_date, sub.subject_name
            FROM scores s
            JOIN exams e ON s.exam_id = e.exam_id
            JOIN subjects sub ON s.subject_id = sub.subject_id
            WHERE s.student_id = %s AND s.exam_id = %s
        """
        result = self.db_service.execute_query(query, (student_id, exam_id))
        return result[0] if result else None

    def enter_scores(self, exam_id, scores_data):
        """
        录入考试成绩
        
        Args:
            exam_id (int): 考试ID
            scores_data (list): 成绩数据列表
            
        Returns:
            dict: 录入结果
        """
        try:
            inserted_count = 0
            updated_count = 0
            
            for score_data in scores_data:
                student_id = score_data['student_id']
                score = score_data['score']
                
                # 检查成绩是否已存在
                check_query = """
                    SELECT score_id FROM scores 
                    WHERE exam_id = %s AND student_id = %s
                """
                existing = self.db_service.execute_query(check_query, (exam_id, student_id))
                
                if existing:
                    # 更新已存在的成绩
                    update_query = """
                        UPDATE scores 
                        SET score = %s 
                        WHERE exam_id = %s AND student_id = %s
                    """
                    self.db_service.execute_update(update_query, (score, exam_id, student_id))
                    updated_count += 1
                else:
                    # 插入新成绩
                    # 首先获取科目ID
                    subject_query = "SELECT subject_id FROM exams WHERE exam_id = %s"
                    subject_result = self.db_service.execute_query(subject_query, (exam_id,))
                    if not subject_result:
                        continue
                        
                    subject_id = subject_result[0]['subject_id']
                    
                    insert_query = """
                        INSERT INTO scores (score, exam_id, subject_id, student_id)
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
        """
        获取考试成绩列表
        
        Args:
            exam_id (int): 考试ID
            
        Returns:
            list: 成绩列表
        """
        query = """
            SELECT s.score_id, s.score, s.exam_id, s.subject_id, s.student_id,
                   e.exam_name, e.exam_date, sub.subject_name, st.student_name, st.student_number
            FROM scores s
            JOIN exams e ON s.exam_id = e.exam_id
            JOIN subjects sub ON s.subject_id = sub.subject_id
            JOIN students st ON s.student_id = st.student_id
            WHERE s.exam_id = %s
            ORDER BY st.student_number
        """
        return self.db_service.execute_query(query, (exam_id,))

    def update_score(self, score_id, score_data):
        """
        更新成绩
        
        Args:
            score_id (int): 成绩ID
            score_data (dict): 成绩数据
            
        Returns:
            dict: 更新后的成绩信息
        """
        # 更新成绩
        update_query = "UPDATE scores SET score = %s WHERE score_id = %s"
        self.db_service.execute_update(update_query, (score_data['score'], score_id))
        
        # 返回更新后的成绩信息
        query = """
            SELECT s.score_id, s.score, s.exam_id, s.subject_id, s.student_id,
                   e.exam_name, e.exam_date, sub.subject_name, st.student_name, st.student_number
            FROM scores s
            JOIN exams e ON s.exam_id = e.exam_id
            JOIN subjects sub ON s.subject_id = sub.subject_id
            JOIN students st ON s.student_id = st.student_id
            WHERE s.score_id = %s
        """
        result = self.db_service.execute_query(query, (score_id,))
        return result[0] if result else None

    def get_exam_statistics(self, exam_id):
        """
        获取考试统计信息
        
        Args:
            exam_id (int): 考试ID
            
        Returns:
            dict: 统计信息
        """
        # 获取考试基本信息
        exam_query = """
            SELECT exam_name, subject_id FROM exams 
            WHERE exam_id = %s
        """
        exam_result = self.db_service.execute_query(exam_query, (exam_id,))
        if not exam_result:
            return None
            
        # 获取成绩统计
        stats_query = """
            SELECT 
                COUNT(*) as total_students,
                AVG(score) as average_score,
                MAX(score) as highest_score,
                MIN(score) as lowest_score
            FROM scores 
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
        """
        获取考试班级成绩列表
        
        Args:
            exam_id (int): 考试ID
            class_id (int): 班级ID
            teacher_id (int): 教师ID
            
        Returns:
            list: 成绩列表
        """
        query = """
            SELECT s.score_id, s.score, s.exam_id, s.subject_id, s.student_id,
                   e.exam_name, e.exam_date, sub.subject_name, st.student_name, st.student_number
            FROM scores s
            JOIN exams e ON s.exam_id = e.exam_id
            JOIN subjects sub ON s.subject_id = sub.subject_id
            JOIN students st ON s.student_id = st.student_id
            WHERE s.exam_id = %s AND st.class_id = %s
            ORDER BY st.student_number
        """
        return self.db_service.execute_query(query, (exam_id, class_id))

    def get_student_exam_results(self, student_id):
        """
        获取学生考试结果列表
        
        Args:
            student_id (str): 学生ID
            
        Returns:
            list: 考试结果列表
        """
        query = """
            SELECT er.exam_type as exam_name, er.student_name, 
                   er.chinese, er.math, er.english, 
                   er.physics, er.chemistry, er.politics,
                   er.total_score, er.ranking
            FROM exam_results er
            WHERE er.student_name = (
                SELECT student_name FROM students WHERE student_id = %s
            )
            ORDER BY er.exam_type
        """
        return self.db_service.execute_query(query, (student_id,))

    def get_teacher_scores(self, teacher_id, page=1, per_page=10):
        """
        获取教师相关的成绩列表
        
        Args:
            teacher_id (str): 教师ID
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 成绩列表和分页信息
        """
        # 计算偏移量
        offset = (page - 1) * per_page
        
        # 获取教师相关的成绩总数
        count_query = """
            SELECT COUNT(*) as total
            FROM Scores s
            JOIN Students st ON s.student_id = st.student_id
            JOIN TeacherClasses tc ON st.class_id = tc.class_id
            WHERE tc.teacher_id = %s
        """
        count_result = self.db_service.execute_query(count_query, (teacher_id,))
        total = count_result[0]['total'] if count_result else 0
        
        # 获取教师相关的成绩列表
        scores_query = """
            SELECT s.score_id, s.score, s.exam_type_id, s.subject_id, s.student_id,
                   et.exam_type_name as exam_name, sub.subject_name, st.student_name, st.student_id as student_number
            FROM Scores s
            JOIN Students st ON s.student_id = st.student_id
            JOIN Subjects sub ON s.subject_id = sub.subject_id
            JOIN ExamTypes et ON s.exam_type_id = et.exam_type_id
            JOIN TeacherClasses tc ON st.class_id = tc.class_id
            WHERE tc.teacher_id = %s
            ORDER BY et.exam_type_name, st.student_id
            LIMIT %s OFFSET %s
        """
        scores = self.db_service.execute_query(scores_query, (teacher_id, per_page, offset))
        
        return {
            'scores': scores,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }
