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
                           sc.subject_id, su.subject_name,
                           sc.exam_type_id, et.exam_type_name, sc.score
                    FROM Scores sc
                    JOIN Students st ON sc.student_id = st.student_id
                    JOIN Subjects su ON sc.subject_id = su.subject_id
                    JOIN ExamTypes et ON sc.exam_type_id = et.exam_type_id
                    JOIN Classes c ON st.class_id = c.class_id
                    JOIN TeacherClasses tc ON c.class_id = tc.class_id
                    WHERE tc.teacher_id = %s
                """
                params = [teacher_id]
                
                if student_id:
                    query += " AND sc.student_id = %s"
                    params.append(student_id)
                    
                if subject_id:
                    query += " AND sc.subject_id = %s"
                    params.append(subject_id)
                    
                if exam_type_id:
                    query += " AND sc.exam_type_id = %s"
                    params.append(exam_type_id)
                    
                query += " ORDER BY sc.score_id DESC"
                
                return self.db_service.execute_query(query, params)
            else:
                # 管理员或其他角色可以查看所有成绩
                query = """
                    SELECT sc.score_id, sc.student_id, st.student_name, 
                           sc.subject_id, su.subject_name,
                           sc.exam_type_id, et.exam_type_name, sc.score
                    FROM Scores sc
                    JOIN Students st ON sc.student_id = st.student_id
                    JOIN Subjects su ON sc.subject_id = su.subject_id
                    JOIN ExamTypes et ON sc.exam_type_id = et.exam_type_id
                """
                params = []
                
                if student_id:
                    query += " WHERE sc.student_id = %s"
                    params.append(student_id)
                    
                if subject_id:
                    if student_id:
                        query += " AND sc.subject_id = %s"
                    else:
                        query += " WHERE sc.subject_id = %s"
                    params.append(subject_id)
                    
                if exam_type_id:
                    if student_id or subject_id:
                        query += " AND sc.exam_type_id = %s"
                    else:
                        query += " WHERE sc.exam_type_id = %s"
                    params.append(exam_type_id)
                    
                query += " ORDER BY sc.score_id DESC"
                
                return self.db_service.execute_query(query, params)
                
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
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            # 教师只能查看自己班级的成绩
            query = """
                SELECT sc.score_id, sc.student_id, st.student_name, 
                       sc.subject_id, su.subject_name,
                       sc.exam_type_id, et.exam_type_name, sc.score
                FROM Scores sc
                JOIN Students st ON sc.student_id = st.student_id
                JOIN Subjects su ON sc.subject_id = su.subject_id
                JOIN ExamTypes et ON sc.exam_type_id = et.exam_type_id
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
            score_list = db_service.execute_query(query, params)
            return score_list
            
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
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
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            query = """
                INSERT INTO Scores (student_id, subject_id, exam_type_id, score)
                VALUES (%s, %s, %s, %s)
            """
            params = (student_id, subject_id, exam_type_id, score)
            db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def update_score(self, score_id, score):
        """
        更新成绩记录
        
        Args:
            score_id (int): 成绩ID
            score (float): 新分数
            
        Returns:
            bool: 是否更新成功
        """
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            query = "UPDATE Scores SET score = %s WHERE score_id = %s"
            params = (score, score_id)
            db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def delete_score(self, score_id):
        """
        删除成绩记录
        
        Args:
            score_id (int): 成绩ID
            
        Returns:
            bool: 是否删除成功
        """
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            query = "DELETE FROM Scores WHERE score_id = %s"
            params = (score_id,)
            db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def is_student_in_teacher_class(self, student_id, teacher_id):
        """
        检查学生是否在教师所教的班级中
        
        Args:
            student_id (str): 学生ID
            teacher_id (int): 教师ID
            
        Returns:
            bool: 学生是否在教师所教的班级中
        """
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            query = """
                SELECT COUNT(*) as count
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE s.student_id = %s AND tc.teacher_id = %s
            """
            params = (student_id, teacher_id)
            result = db_service.execute_query(query, params, fetch_one=True)
            return result['count'] > 0
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
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
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
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
            result = db_service.execute_query(query, params, fetch_one=True)
            return result['count'] > 0
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def get_exam_results(self, teacher_id, exam_type_id=None, class_id=None):
        """
        获取考试结果
        
        Args:
            teacher_id (int): 教师ID
            exam_type_id (int, optional): 考试类型ID
            class_id (int, optional): 班级ID
            
        Returns:
            dict: 包含exam_results键的字典
        """
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            query = """
                SELECT er.*
                FROM exam_results er
                JOIN Students s ON er.student_name = s.student_name
                JOIN TeacherClasses tc ON s.class_id = tc.class_id
                WHERE tc.teacher_id = %s
            """
            params = (teacher_id,)
            
            # 添加筛选条件
            if exam_type_id:
                query += " AND er.exam_type_name = %s"
                params += (exam_type_id,)
                
            if class_id:
                query += " AND er.class_id = %s"
                params += (class_id,)
            
            query += " ORDER BY er.ranking"
            
            exam_results = db_service.execute_query(query, params)
            return {'exam_results': exam_results}
            
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def get_score_by_id(self, score_id, teacher_id=None):
        """
        根据成绩ID获取特定成绩
        
        Args:
            score_id (int): 成绩ID
            teacher_id (int, optional): 教师ID，用于权限验证
            
        Returns:
            dict: 成绩信息
        """
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            if teacher_id:
                # 教师只能查看自己班级的成绩
                query = """
                    SELECT sc.score_id, sc.student_id, st.student_name, 
                           sc.subject_id, su.subject_name,
                           sc.exam_type_id, et.exam_type_name, sc.score
                    FROM Scores sc
                    JOIN Students st ON sc.student_id = st.student_id
                    JOIN Subjects su ON sc.subject_id = su.subject_id
                    JOIN ExamTypes et ON sc.exam_type_id = et.exam_type_id
                    JOIN Classes c ON st.class_id = c.class_id
                    JOIN TeacherClasses tc ON c.class_id = tc.class_id
                    WHERE sc.score_id = %s AND tc.teacher_id = %s
                """
                params = (score_id, teacher_id)
            else:
                # 管理员或其他角色可以查看所有成绩
                query = """
                    SELECT sc.score_id, sc.student_id, st.student_name, 
                           sc.subject_id, su.subject_name,
                           sc.exam_type_id, et.exam_type_name, sc.score
                    FROM Scores sc
                    JOIN Students st ON sc.student_id = st.student_id
                    JOIN Subjects su ON sc.subject_id = su.subject_id
                    JOIN ExamTypes et ON sc.exam_type_id = et.exam_type_id
                    WHERE sc.score_id = %s
                """
                params = (score_id,)
            
            result = db_service.execute_query(query, params, fetch_one=True)
            return result
            
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    @staticmethod
    def get_student_exam_results(student_id):
        """
        获取学生考试结果
        
        Args:
            student_id (str): 学生ID
            
        Returns:
            list: 学生考试结果列表
        """
        try:
            db_service = database_service.DatabaseService()
            
            # 首先获取学生姓名
            student_query = "SELECT student_name FROM Students WHERE student_id = %s"
            student_params = (student_id,)
            student_result = db_service.execute_query(student_query, student_params, fetch_one=True)
            
            if not student_result:
                return []
                
            student_name = student_result['student_name']
            
            # 查询exam_results视图
            query = """
                SELECT *
                FROM exam_results
                WHERE student_name = %s
                ORDER BY exam_type
            """
            params = (student_name,)
            
            exam_results = db_service.execute_query(query, params)
            return exam_results
        except Exception as e:
            raise e
        finally:
            db_service.close()
            
    @staticmethod
    def get_student_scores(student_id):
        """
        获取学生成绩列表
        
        Args:
            student_id (str): 学生ID
            
        Returns:
            list: 学生成绩列表
        """
        try:
            db_service = database_service.DatabaseService()
            query = """
                SELECT sc.score_id, sc.student_id, sc.student_name, 
                       sc.subject_id, sc.subject_name,
                       sc.exam_type_id, sc.exam_type_name, sc.score
                FROM Scores sc
                WHERE sc.student_id = %s
                ORDER BY sc.exam_type_id, sc.subject_id
            """
            params = [student_id]
            
            scores = db_service.execute_query(query, params)
            return scores
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def get_teacher_performance(self, teacher_id):
        """
        获取教师表现数据
        
        Args:
            teacher_id (int): 教师ID
            
        Returns:
            dict: 包含performance键的字典
        """
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            query = """
                SELECT tp.*
                FROM teacher_performance tp
                JOIN teachers t ON tp.teacher_name = t.teacher_name
                WHERE t.teacher_id = %s
             ORDER BY tp.rank_in_school"""
            
            result = db_service.execute_query(query, (teacher_id,))
            # 确保返回的是列表而不是元组
            performance_data = list(result) if result else []
            return {'performance': performance_data}
        except Exception as e:
            # 确保在出错时也返回正确的字典结构
            return {'performance': []}
        finally:
            db_service.close()