"""成绩服务模块，处理与成绩相关的业务逻辑"""
from .database_service import DatabaseService


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
                           sc.subject_id, sub.subject_name,
                           sc.exam_type_id, et.exam_type_name, sc.score
                    FROM Scores sc
                    JOIN Students st ON sc.student_id = st.student_id
                    JOIN Subjects sub ON sc.subject_id = sub.subject_id
                    JOIN ExamTypes et ON sc.exam_type_id = et.type_id
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
    
    def create_score(self, score_data, teacher_id=None):
        """
        创建成绩
        
        Args:
            score_data (dict): 成绩信息
            teacher_id (int, optional): 教师ID，用于权限验证
            
        Returns:
            bool: 是否创建成功
        """
        try:
            # 如果提供了教师ID，验证学生是否在教师所教班级中
            if teacher_id:
                check_query = """
                    SELECT 1 FROM Students s
                    JOIN Classes c ON s.class_id = c.class_id
                    JOIN TeacherClasses tc ON c.class_id = tc.class_id
                    WHERE s.student_id = %s AND tc.teacher_id = %s
                """
                check_result = self.db_service.execute_query(
                    check_query, 
                    (score_data.get('student_id'), teacher_id), 
                    fetch_one=True
                )
                
                if not check_result:
                    raise Exception('Student not found in your classes')
            
            # 检查成绩是否已存在
            exist_query = """
                SELECT score_id FROM Scores 
                WHERE student_id = %s AND subject_id = %s AND exam_type_id = %s
            """
            exist_result = self.db_service.execute_query(
                exist_query, 
                (score_data.get('student_id'), score_data.get('subject_id'), score_data.get('exam_type_id')), 
                fetch_one=True
            )
            
            if exist_result:
                # 更新已存在的成绩
                update_query = """
                    UPDATE Scores 
                    SET score = %s 
                    WHERE score_id = %s
                """
                self.db_service.execute_update(
                    update_query, 
                    (score_data.get('score'), exist_result['score_id'])
                )
            else:
                # 插入新成绩
                insert_query = """
                    INSERT INTO Scores (student_id, subject_id, exam_type_id, score)
                    VALUES (%s, %s, %s, %s)
                """
                self.db_service.execute_update(
                    insert_query, 
                    (score_data.get('student_id'), score_data.get('subject_id'), 
                     score_data.get('exam_type_id'), score_data.get('score'))
                )
            
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def update_score(self, score_id, score_data, teacher_id=None):
        """
        更新成绩
        
        Args:
            score_id (int): 成绩ID
            score_data (dict): 成绩信息
            teacher_id (int, optional): 教师ID，用于权限验证
            
        Returns:
            bool: 是否更新成功
        """
        try:
            # 如果提供了教师ID，验证成绩是否属于教师所教班级
            if teacher_id:
                check_query = """
                    SELECT 1 FROM Scores sc
                    JOIN Students s ON sc.student_id = s.student_id
                    JOIN Classes c ON s.class_id = c.class_id
                    JOIN TeacherClasses tc ON c.class_id = tc.class_id
                    WHERE sc.score_id = %s AND tc.teacher_id = %s
                """
                check_result = self.db_service.execute_query(
                    check_query, 
                    (score_id, teacher_id), 
                    fetch_one=True
                )
                
                if not check_result:
                    raise Exception('Score not found in your classes')
            
            query = """
                UPDATE Scores 
                SET score = %s 
                WHERE score_id = %s
            """
            params = (score_data.get('score'), score_id)
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()