"""成绩服务模块，处理与成绩相关的业务逻辑"""
from utils import database_service


class ScoreService:
    """成绩服务类"""
    
    def __init__(self):
        """初始化成绩服务"""
        self.db_service = database_service.DatabaseService()
    
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
    
    def get_teacher_scores(self, teacher_id, student_id=None, subject_id=None, exam_type_id=None):
        """
        获取教师所教班级的成绩
        
        Args:
            teacher_id (int): 教师ID
            student_id (str, optional): 学生ID
            subject_id (int, optional): 科目ID
            exam_type_id (int, optional): 考试类型ID
            
        Returns:
            list: 成绩列表
        """
        try:
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
            
            # 添加筛选条件
            conditions = []
            if student_id:
                conditions.append("sc.student_id = %s")
                params += (student_id,)
            if subject_id:
                conditions.append("sc.subject_id = %s")
                params += (subject_id,)
            if exam_type_id:
                conditions.append("sc.exam_type_id = %s")
                params += (exam_type_id,)
            
            if conditions:
                query += " AND " + " AND ".join(conditions)
            
            query += " ORDER BY sc.score_id DESC"
            
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
    
    def delete_score(self, score_id):
        """
        删除成绩记录
        
        Args:
            score_id (int): 成绩ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            query = "DELETE FROM Scores WHERE score_id = %s"
            params = (score_id,)
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
    
    def validate_student_for_teacher(self, student_id, teacher_id):
        """
        验证学生是否属于教师所教的班级
        
        Args:
            student_id (str): 学生ID
            teacher_id (int): 教师ID
            
        Returns:
            bool: 验证结果
        """
        return self.is_student_in_teacher_class(student_id, teacher_id)
    
    def validate_teacher_for_score(self, teacher_id, score_id):
        """
        验证教师是否有权限操作该成绩记录
        
        Args:
            teacher_id (int): 教师ID
            score_id (int): 成绩ID
            
        Returns:
            bool: 验证结果
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