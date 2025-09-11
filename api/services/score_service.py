"""成绩服务模块，处理与成绩相关的业务逻辑"""


class ScoreService:
    """成绩服务类"""
    
    def __init__(self):
        """初始化成绩服务"""
        pass  # 不在初始化时创建数据库服务实例
    
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
        from utils import database_service
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            # 构建查询语句
            query = """
                SELECT s.score_id, s.student_id, st.student_name, s.subject_id, sub.subject_name,
                       s.exam_type_id, et.exam_type_name, s.score
                FROM Scores s
                JOIN Students st ON s.student_id = st.student_id
                JOIN Subjects sub ON s.subject_id = sub.subject_id
                JOIN ExamTypes et ON s.exam_type_id = et.exam_type_id
            """
            
            # 构建WHERE条件
            conditions = []
            params = []
            
            if student_id:
                conditions.append("s.student_id = %s")
                params.append(student_id)
            
            if subject_id:
                conditions.append("s.subject_id = %s")
                params.append(subject_id)
            
            if exam_type_id:
                conditions.append("s.exam_type_id = %s")
                params.append(exam_type_id)
            
            # 如果提供了教师ID，则只获取该教师所教班级的成绩
            if teacher_id:
                conditions.append("""
                    st.class_id IN (
                        SELECT class_id 
                        FROM TeacherClasses 
                        WHERE teacher_id = %s
                    )
                """)
                params.append(teacher_id)
            
            # 添加WHERE子句
            if conditions:
                query += " WHERE " + " AND ".join(conditions)
            
            # 添加排序
            query += " ORDER BY s.score_id DESC"
            
            # 执行查询
            return db_service.execute_query(query, tuple(params))
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def get_score_by_id(self, score_id):
        """
        根据成绩ID获取成绩详情
        
        Args:
            score_id (int): 成绩ID
            
        Returns:
            dict: 成绩详情
        """
        from utils import database_service
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            query = """
                SELECT s.score_id, s.student_id, st.student_name, s.subject_id, sub.subject_name,
                       s.exam_type_id, et.exam_type_name, s.score
                FROM Scores s
                JOIN Students st ON s.student_id = st.student_id
                JOIN Subjects sub ON s.subject_id = sub.subject_id
                JOIN ExamTypes et ON s.exam_type_id = et.exam_type_id
                WHERE s.score_id = %s
            """
            return db_service.execute_query(query, (score_id,), fetch_one=True)
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
            bool: 如果学生在教师所教班级中返回True，否则返回False
        """
        from utils import database_service
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            query = """
                SELECT COUNT(*) as count
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE s.student_id = %s AND tc.teacher_id = %s
            """
            result = db_service.execute_query(query, (student_id, teacher_id), fetch_one=True)
            return result['count'] > 0
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def create_score(self, student_id, subject_id, exam_type_id, score, teacher_id=None):
        """
        创建成绩记录
        
        Args:
            student_id (str): 学生ID
            subject_id (int): 科目ID
            exam_type_id (int): 考试类型ID
            score (float): 分数
            teacher_id (int, optional): 教师ID，用于权限验证
            
        Returns:
            bool: 是否创建成功
        """
        from utils import database_service
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            # 如果提供了教师ID，则验证教师是否有权限为该学生创建成绩
            if teacher_id is not None:
                is_valid = self.is_student_in_teacher_class(student_id, teacher_id)
                print(f"权限验证结果: student_id={student_id}, teacher_id={teacher_id}, is_valid={is_valid}")
                if not is_valid:
                    return False
            
            query = """
                INSERT INTO Scores (student_id, subject_id, exam_type_id, score)
                VALUES (%s, %s, %s, %s)
            """
            params = (student_id, subject_id, exam_type_id, score)
            print(f"执行插入操作: query={query}, params={params}")
            result = db_service.execute_update(query, params)
            print(f"插入操作结果: result={result}")
            return result > 0
        except Exception as e:
            print(f"创建成绩时发生异常: {e}")
            raise e
        finally:
            db_service.close()
    
    def update_score(self, score_id, score, teacher_id=None):
        """
        更新成绩
        
        Args:
            score_id (int): 成绩ID
            score (float): 新的分数
            teacher_id (int, optional): 教师ID，用于权限验证
            
        Returns:
            bool: 是否更新成功
        """
        from utils import database_service
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            # 如果提供了教师ID，则验证教师是否有权限更新该成绩
            if teacher_id is not None:
                is_valid = self.validate_teacher_for_score(score_id, teacher_id)
                if not is_valid:
                    return False
            
            query = "UPDATE Scores SET score = %s WHERE score_id = %s"
            result = db_service.execute_update(query, (score, score_id))
            return result > 0
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def delete_score(self, score_id, teacher_id=None):
        """
        删除成绩
        
        Args:
            score_id (int): 成绩ID
            teacher_id (int, optional): 教师ID，用于权限验证
            
        Returns:
            bool: 是否删除成功
        """
        from utils import database_service
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            # 如果提供了教师ID，则验证教师是否有权限删除该成绩
            if teacher_id is not None:
                is_valid = self.validate_teacher_for_score(score_id, teacher_id)
                if not is_valid:
                    return False
            
            query = "DELETE FROM Scores WHERE score_id = %s"
            result = db_service.execute_update(query, (score_id,))
            return result > 0
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def get_teacher_scores(self, teacher_id):
        """
        获取教师所教班级的成绩列表
        
        Args:
            teacher_id (int): 教师ID
            
        Returns:
            list: 成绩列表
        """
        from utils import database_service
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            query = """
                SELECT s.score_id, s.student_id, st.student_name, s.subject_id, sub.subject_name,
                       s.exam_type_id, et.exam_type_name, s.score
                FROM Scores s
                JOIN Students st ON s.student_id = st.student_id
                JOIN Subjects sub ON s.subject_id = sub.subject_id
                JOIN ExamTypes et ON s.exam_type_id = et.exam_type_id
                JOIN Classes c ON st.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE tc.teacher_id = %s
                ORDER BY s.score_id DESC
            """
            return db_service.execute_query(query, (teacher_id,))
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def validate_student_for_teacher(self, student_id, teacher_id):
        """
        验证学生是否属于教师的班级
        
        Args:
            student_id (str): 学生ID
            teacher_id (int): 教师ID
            
        Returns:
            bool: 如果学生属于教师的班级返回True，否则返回False
        """
        from utils import database_service
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            query = """
                SELECT COUNT(*) as count
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE s.student_id = %s AND tc.teacher_id = %s
            """
            result = db_service.execute_query(query, (student_id, teacher_id), fetch_one=True)
            return result['count'] > 0
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def validate_teacher_for_score(self, score_id, teacher_id):
        """
        验证教师是否有权限操作某个成绩
        
        Args:
            score_id (int): 成绩ID
            teacher_id (int): 教师ID
            
        Returns:
            bool: 如果教师有权限操作该成绩返回True，否则返回False
        """
        from utils import database_service
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
            result = db_service.execute_query(query, (score_id, teacher_id), fetch_one=True)
            return result['count'] > 0
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def get_exam_results(self, teacher_id, exam_type_id=None, class_id=None):
        """
        获取考试结果统计
        
        Args:
            teacher_id (int): 教师ID
            exam_type_id (int, optional): 考试类型ID
            class_id (int, optional): 班级ID
            
        Returns:
            dict: 考试结果统计
        """
        from utils import database_service
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            # 构建查询语句
            query = """
                SELECT s.student_id, st.student_name, s.score
                FROM Scores s
                JOIN Students st ON s.student_id = st.student_id
                JOIN Classes c ON st.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE tc.teacher_id = %s
            """
            params = [teacher_id]
            
            # 添加可选的过滤条件
            if exam_type_id:
                query += " AND s.exam_type_id = %s"
                params.append(exam_type_id)
            
            if class_id:
                query += " AND st.class_id = %s"
                params.append(class_id)
            
            query += " ORDER BY s.score DESC"
            
            # 获取考试成绩
            exam_results = db_service.execute_query(query, tuple(params))
            
            # 计算统计信息
            if exam_results:
                scores = [result['score'] for result in exam_results]
                total_students = len(scores)
                average_score = sum(scores) / total_students
                highest_score = max(scores)
                lowest_score = min(scores)
                
                # 计算分数段分布
                excellent = len([s for s in scores if s >= 90])
                good = len([s for s in scores if 80 <= s < 90])
                average = len([s for s in scores if 70 <= s < 80])
                passing = len([s for s in scores if 60 <= s < 70])
                failing = len([s for s in scores if s < 60])
                
                statistics = {
                    'total_students': total_students,
                    'average_score': round(average_score, 2),
                    'highest_score': highest_score,
                    'lowest_score': lowest_score,
                    'distribution': {
                        'excellent': excellent,
                        'good': good,
                        'average': average,
                        'passing': passing,
                        'failing': failing
                    }
                }
            else:
                statistics = {
                    'total_students': 0,
                    'average_score': 0,
                    'highest_score': 0,
                    'lowest_score': 0,
                    'distribution': {
                        'excellent': 0,
                        'good': 0,
                        'average': 0,
                        'passing': 0,
                        'failing': 0
                    }
                }
            
            return {
                'exam_results': exam_results,
                'statistics': statistics
            }
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def get_teacher_performance(self, teacher_id):
        """
        获取教师教学表现数据
        
        Args:
            teacher_id (int): 教师ID
            
        Returns:
            dict: 教师教学表现数据
        """
        from utils import database_service
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            # 获取教师所教班级的平均成绩
            query = """
                SELECT et.exam_type_name, AVG(s.score) as average_score
                FROM Scores s
                JOIN Students st ON s.student_id = st.student_id
                JOIN Classes c ON st.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                JOIN ExamTypes et ON s.exam_type_id = et.exam_type_id
                WHERE tc.teacher_id = %s
                GROUP BY et.exam_type_name
                ORDER BY et.exam_type_name
            """
            performance = db_service.execute_query(query, (teacher_id,))
            
            # 格式化数据
            formatted_performance = []
            for item in performance:
                formatted_performance.append({
                    'exam_type': item['exam_type_name'],
                    'average_score': round(item['average_score'], 2)
                })
            
            return {
                'performance': formatted_performance
            }
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def get_student_exam_results(self, student_id):
        """
        获取学生考试结果
        
        Args:
            student_id (str): 学生ID
            
        Returns:
            list: 学生考试结果列表
        """
        from utils import database_service
        db_service = database_service.DatabaseService()  # 在方法内创建数据库连接
        try:
            query = """
                SELECT s.score_id, sub.subject_name, et.exam_type_name, s.score
                FROM Scores s
                JOIN Subjects sub ON s.subject_id = sub.subject_id
                JOIN ExamTypes et ON s.exam_type_id = et.exam_type_id
                WHERE s.student_id = %s
                ORDER BY s.score_id DESC
            """
            return db_service.execute_query(query, (student_id,))
        except Exception as e:
            raise e
        finally:
            db_service.close()