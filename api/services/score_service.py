"""成绩服务模块，处理与成绩相关的业务逻辑"""
from utils import DatabaseService


class ScoreService:
    """成绩服务类"""
    
    def __init__(self):
        """初始化成绩服务"""
        self.db_service = DatabaseService()
    
    def get_scores(self, teacher_id=None, student_id=None, subject_id=None, exam_type_id=None):
        """
        获取成绩列表
        
        Args:
            teacher_id (int, optional): 教师ID，用于过滤教师所教班级的成绩
            student_id (str, optional): 学生ID
            subject_id (int, optional): 科目ID
            exam_type_id (int, optional): 考试类型ID
            
        Returns:
            list: 成绩列表
        """
        try:
            if teacher_id:
                # 教师只能查看自己班级的成绩
                query = """
                    SELECT sc.score_id, sc.student_id, st.student_name, 
                           sc.subject_id, sub.subject_name,
                           sc.exam_type_id, et.exam_type_name, sc.score
                    FROM Scores sc
                    JOIN Students st ON sc.student_id = st.student_id
                    JOIN Subjects sub ON sc.subject_id = sub.subject_id
                    JOIN ExamTypes et ON sc.exam_type_id = et.type_id
                    JOIN Classes c ON st.class_id = c.class_id
                    JOIN TeacherClasses tc ON c.class_id = tc.class_id
                    WHERE tc.teacher_id = %s
                """
                params = (teacher_id,)
            else:
                # 基本查询（可按学生、科目、考试类型筛选）
                query = """
                    SELECT s.score_id, s.student_id, st.student_name, 
                           s.subject_id, sub.subject_name,
                           s.exam_type_id, et.exam_type_name, s.score
                    FROM Scores s
                    JOIN Students st ON s.student_id = st.student_id
                    JOIN Subjects sub ON s.subject_id = sub.subject_id
                    JOIN ExamTypes et ON s.exam_type_id = et.type_id
                """
                params = ()
                
                # 添加筛选条件
                conditions = []
                if student_id:
                    conditions.append("s.student_id = %s")
                    params += (student_id,)
                if subject_id:
                    conditions.append("s.subject_id = %s")
                    params += (subject_id,)
                if exam_type_id:
                    conditions.append("s.exam_type_id = %s")
                    params += (exam_type_id,)
                
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY s.score_id DESC"
            
            # 执行查询
            score_list = self.db_service.execute_query(query, params)
            return score_list
            
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def create_score(self, student_id, subject_id, exam_type_id, score):
        """
        创建成绩记录
        
        Args:
            student_id (str): 学生ID
            subject_id (int): 科目ID
            exam_type_id (int): 考试类型ID
            score (float): 分数
            
        Returns:
            bool: 是否创建成功
        """
        try:
            query = """
                INSERT INTO Scores (student_id, subject_id, exam_type_id, score)
                VALUES (%s, %s, %s, %s)
            """
            params = (student_id, subject_id, exam_type_id, score)
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def update_score(self, score_id, score):
        """
        更新成绩记录
        
        Args:
            score_id (int): 成绩ID
            score (float): 新分数
            
        Returns:
            bool: 是否更新成功
        """
        try:
            query = "UPDATE Scores SET score = %s WHERE score_id = %s"
            params = (score, score_id)
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def is_student_in_teacher_class(self, student_id, teacher_id):
        """
        检查学生是否在教师所教的班级中
        
        Args:
            student_id (str): 学生ID
            teacher_id (int): 教师ID
            
        Returns:
            bool: 学生是否在教师所教的班级中
        """
        try:
            query = """
                SELECT COUNT(*) as count
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE s.student_id = %s AND tc.teacher_id = %s
            """
            params = (student_id, teacher_id)
            result = self.db_service.execute_query(query, params, fetch_one=True)
            return result['count'] > 0
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def is_score_in_teacher_class(self, score_id, teacher_id):
        """
        检查成绩是否属于教师所教的班级
        
        Args:
            score_id (int): 成绩ID
            teacher_id (int): 教师ID
            
        Returns:
            bool: 成绩是否属于教师所教的班级
        """
        try:
            query = """
                SELECT COUNT(*) as count
                FROM Scores s
                JOIN Students st ON s.student_id = st.student_id
                JOIN Classes c ON st.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE s.score_id = %s AND tc.teacher_id = %s
            """
            params = (score_id, teacher_id)
            result = self.db_service.execute_query(query, params, fetch_one=True)
            return result['count'] > 0
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def get_exam_results(self, teacher_id=None, exam_type_id=None, class_id=None):
        """
        获取考试结果（教师视角）
        
        Args:
            teacher_id (int, optional): 教师ID
            exam_type_id (int, optional): 考试类型ID
            class_id (int, optional): 班级ID
            
        Returns:
            list: 考试结果列表
        """
        try:
            query = """
                SELECT er.student_id, er.student_name, er.class_id, er.class_name,
                       er.exam_type_id, er.exam_type_name, er.subject_id, er.subject_name,
                       er.score, er.rank_in_class
                FROM exam_results er
            """
            
            params = ()
            conditions = []
            
            # 添加筛选条件
            if teacher_id:
                # 教师只能查看自己班级的考试结果
                conditions.append("""
                    er.class_id IN (
                        SELECT tc.class_id 
                        FROM TeacherClasses tc 
                        WHERE tc.teacher_id = %s
                    )
                """)
                params += (teacher_id,)
                
            if exam_type_id:
                conditions.append("er.exam_type_id = %s")
                params += (exam_type_id,)
                
            if class_id:
                conditions.append("er.class_id = %s")
                params += (class_id,)
            
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            query += " ORDER BY er.class_id, er.subject_id, er.rank_in_class"
            
            exam_results = self.db_service.execute_query(query, params)
            return exam_results
            
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def get_student_exam_results(self, student_id, exam_type_id=None):
        """
        获取学生个人考试结果
        
        Args:
            student_id (str): 学生ID
            exam_type_id (int, optional): 考试类型ID
            
        Returns:
            list: 学生考试结果列表
        """
        try:
            query = """
                SELECT er.student_id, er.student_name, er.class_id, er.class_name,
                       er.exam_type_id, er.exam_type_name, er.subject_id, er.subject_name,
                       er.score, er.rank_in_class
                FROM exam_results er
                WHERE er.student_id = %s
            """
            params = (student_id,)
            
            # 添加筛选条件
            if exam_type_id:
                query += " AND er.exam_type_id = %s"
                params += (exam_type_id,)
            
            query += " ORDER BY er.exam_type_id, er.subject_id"
            
            exam_results = self.db_service.execute_query(query, params)
            return exam_results
            
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def get_teacher_performance(self, teacher_id, exam_type_id=None, class_id=None):
        """
        获取教师教学表现统计
        
        Args:
            teacher_id (int): 教师ID
            exam_type_id (int, optional): 考试类型ID
            class_id (int, optional): 班级ID
            
        Returns:
            list: 教师表现统计数据
        """
        try:
            query = """
                SELECT tp.teacher_id, tp.teacher_name, tp.subject_id, tp.subject_name,
                       tp.class_id, tp.class_name, tp.exam_type_id, tp.exam_type_name,
                       tp.average_score, tp.rank_in_subject, tp.rank_in_school
                FROM teacher_performance tp
                WHERE tp.teacher_id = %s
            """
            params = (teacher_id,)
            
            conditions = []
            # 添加筛选条件
            if exam_type_id:
                conditions.append("tp.exam_type_id = %s")
                params += (exam_type_id,)
                
            if class_id:
                conditions.append("tp.class_id = %s")
                params += (class_id,)
            
            if conditions:
                query += " AND " + " AND ".join(conditions)
            
            query += " ORDER BY tp.exam_type_id, tp.class_id"
            
            performance = self.db_service.execute_query(query, params)
            return performance
            
        except Exception as e:
            raise e
        finally:
            self.db_service.close()