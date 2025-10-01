from apps.utils.database_service import DatabaseService
from flask import current_app
"""学生服务类"""



class StudentService:
    """学生服务类"""

    def __init__(self):
        """初始化学生服务"""
        self.db_service = DatabaseService()

    def get_student_profile(self, student_id):
        """
        获取学生个人信息
        
        Args:
            student_id (str): 学生ID
            
        Returns:
            dict: 学生个人信息
        """
        try:
            query = """
                SELECT s.student_id, s.student_name, c.class_name
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                WHERE s.student_id = %s
            """
            result = self.db_service.execute_query(query, (student_id,))
            if result:
                return result[0]  # 返回第一个结果（应该只有一个）
            return None
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get student profile for {student_id}: {str(e)}")
            raise

    def get_teacher_students(self, teacher_id, class_id=None, page=1, per_page=10):
        """
        获取教师所教班级的学生列表
        
        Args:
            teacher_id (str): 教师ID
            class_id (str, optional): 班级ID
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 学生列表和分页信息
        """
        try:
            # 计算偏移量
            offset = (page - 1) * per_page
            
            # 构建查询语句
            base_query = """
                SELECT s.student_id, s.student_name, c.class_name
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE tc.teacher_id = %s
            """
            count_query = """
                SELECT COUNT(*) as total
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE tc.teacher_id = %s
            """
            params = [teacher_id]
            count_params = [teacher_id]
            
            # 如果指定了班级ID，则添加到查询条件中
            if class_id:
                base_query += " AND c.class_id = %s"
                count_query += " AND c.class_id = %s"
                params.append(class_id)
                count_params.append(class_id)
            
            base_query += " ORDER BY s.student_id LIMIT %s OFFSET %s"
            params.extend([per_page, offset])
            
            # 获取总数
            total_result = self.db_service.execute_query(count_query, count_params)
            total = total_result[0]['total'] if total_result else 0
            
            # 执行查询
            students = self.db_service.execute_query(base_query, params)
            current_app.logger.info(f"Retrieved {len(students)} students for teacher {teacher_id}")
            
            # 计算总页数
            pages = (total + per_page - 1) // per_page
            
            return {
                'students': students,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages
                }
            }
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get teacher students: {str(e)}")
            raise

    def get_student_by_id(self, student_id):
        """
        根据学生ID获取学生详情
        
        Args:
            student_id (str): 学生ID
            
        Returns:
            dict: 学生信息
        """
        try:
            query = """
                SELECT s.student_id, s.student_name, c.class_name
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                WHERE s.student_id = %s
            """
            result = self.db_service.execute_query(query, (student_id,))
            if result:
                return result[0]  # 返回第一个结果（应该只有一个）
            return None
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get student by id {student_id}: {str(e)}")
            raise e
            
    def get_all_students(self, page=1, per_page=1000):
        """
        获取所有学生列表（供管理员使用）
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 学生列表和分页信息
        """
        try:
            # 计算偏移量
            offset = (page - 1) * per_page
            
            # 构建查询语句
            base_query = """
                SELECT s.student_id, s.student_name, c.class_name
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                ORDER BY s.student_id
                LIMIT %s OFFSET %s
            """
            
            count_query = """
                SELECT COUNT(*) as total
                FROM Students
            """
            
            # 获取总数
            total_result = self.db_service.execute_query(count_query)
            total = total_result[0]['total'] if total_result else 0
            
            # 执行查询
            students = self.db_service.execute_query(base_query, (per_page, offset))
            current_app.logger.info(f"Retrieved {len(students)} students")
            
            # 计算总页数
            pages = (total + per_page - 1) // per_page
            
            return {
                'students': students,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages
                }
            }
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get all students: {str(e)}")
            raise
    
    def update_student_name(self, student_id, student_name):
        """
        更新学生姓名
        
        Args:
            student_id (str): 学生ID
            student_name (str): 新的学生姓名
            
        Returns:
            bool: 更新是否成功
        """
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
        """
        创建学生
        
        Args:
            student_data (dict): 学生信息字典，包含student_id, student_name, class_id, password
            
        Returns:
            dict: 创建的学生信息
        """
        try:
            # 先插入学生信息到Students表
            student_query = """
                INSERT INTO Students (student_id, student_name, class_id, password)
                VALUES (%s, %s, %s, %s)
            """
            student_params = (
                student_data['student_id'],
                student_data['student_name'],
                student_data['class_id'],
                student_data.get('password', 'pass123')  # 默认密码为pass123
            )
            
            self.db_service.execute_update(student_query, student_params)
            
            # Note: users is a view, not a table, so we don't insert directly into it
            # The users view automatically includes data from the Students table
            
            current_app.logger.info(f"Student {student_data['student_id']} created successfully")
            return {"student_id": student_data['student_id']}
            
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to create student: {str(e)}")
            raise

    def update_student(self, student_id, update_data):
        """
        更新学生信息
        
        Args:
            student_id (str): 学生ID
            update_data (dict): 要更新的学生信息
            
        Returns:
            bool: 更新是否成功
        """
        try:
            # 构建动态更新语句
            set_clauses = []
            params = []
            
            for key, value in update_data.items():
                # 只允许更新特定字段
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
        """
        删除学生
        
        Args:
            student_id (str): 学生ID
            
        Returns:
            bool: 删除是否成功
        """
        try:
            # 首先检查学生是否存在
            check_query = "SELECT student_id FROM Students WHERE student_id = %s"
            student_exists = self.db_service.execute_query(check_query, (student_id,))
            
            if not student_exists:
                if current_app:
                    current_app.logger.warning(f"Student {student_id} not found for deletion")
                return False
            
            # 首先删除学生的成绩记录（由于外键约束）
            scores_query = "DELETE FROM Scores WHERE student_id = %s"
            scores_result = self.db_service.execute_update(scores_query, (student_id,))
            
            if current_app:
                current_app.logger.info(f"Deleted {scores_result} score records for student {student_id}")
            
            # 然后删除学生记录
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
        """
        获取学生的所有成绩
        
        Args:
            student_id (str): 学生ID
            
        Returns:
            list: 学生成绩列表
        """
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
        """
        获取学生考试结果
        
        Args:
            student_id (str): 学生ID
            exam_id (int, optional): 考试ID
            
        Returns:
            list: 学生考试结果列表
        """
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