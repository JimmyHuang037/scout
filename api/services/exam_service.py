"""考试服务模块，处理与考试相关的业务逻辑"""
from utils import database_service


class ExamService:
    """考试服务类"""
    
    def get_exams_by_teacher(self, teacher_id, page=1, per_page=10):
        """
        获取教师相关的考试列表（带分页）
        
        Args:
            teacher_id (int): 教师ID
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 考试列表和分页信息
        """
        db_service = database_service.DatabaseService()
        try:
            offset = (page - 1) * per_page
            
            # 获取总数
            count_query = """
                SELECT COUNT(*) as count 
                FROM Exams e
                JOIN TeacherClasses tc ON e.class_id = tc.class_id
                WHERE tc.teacher_id = %s
            """
            total = db_service.get_count(count_query, (teacher_id,))
            
            # 获取考试列表
            query = """
                SELECT e.exam_id, e.exam_name, e.exam_date, 
                       s.subject_name, c.class_name, et.type_name as exam_type_name
                FROM Exams e
                JOIN Subjects s ON e.subject_id = s.subject_id
                JOIN Classes c ON e.class_id = c.class_id
                JOIN ExamTypes et ON e.exam_type_id = et.type_id
                JOIN TeacherClasses tc ON e.class_id = tc.class_id
                WHERE tc.teacher_id = %s
                ORDER BY e.exam_date DESC, e.exam_id
                LIMIT %s OFFSET %s
            """
            exams = db_service.execute_query(query, (teacher_id, per_page, offset))
            
            return {
                'exams': exams,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }
            
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def create_exam(self, exam_data):
        """
        创建考试
        
        Args:
            exam_data (dict): 考试信息
            
        Returns:
            bool: 是否创建成功
        """
        db_service = database_service.DatabaseService()
        try:
            query = """
                INSERT INTO Exams (exam_name, subject_id, class_id, exam_type_id, exam_date, teacher_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                exam_data.get('exam_name'),
                exam_data.get('subject_id'),
                exam_data.get('class_id'),
                exam_data.get('exam_type_id'),
                exam_data.get('exam_date'),
                exam_data.get('teacher_id')
            )
            db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def get_exam_by_id_and_teacher(self, exam_id, teacher_id):
        """
        根据考试ID和教师ID获取考试详情
        
        Args:
            exam_id (int): 考试ID
            teacher_id (int): 教师ID
            
        Returns:
            dict: 考试详情
        """
        db_service = database_service.DatabaseService()
        try:
            query = """
                SELECT e.exam_id, e.exam_name, e.exam_date,
                       s.subject_name, c.class_name, et.type_name as exam_type_name
                FROM Exams e
                JOIN Subjects s ON e.subject_id = s.subject_id
                JOIN Classes c ON e.class_id = c.class_id
                JOIN ExamTypes et ON e.exam_type_id = et.type_id
                JOIN TeacherClasses tc ON e.class_id = tc.class_id
                WHERE e.exam_id = %s AND tc.teacher_id = %s
            """
            return db_service.execute_query(query, (exam_id, teacher_id), fetch_one=True)
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def update_exam(self, exam_id, teacher_id, exam_data):
        """
        更新考试信息
        
        Args:
            exam_id (int): 考试ID
            teacher_id (int): 教师ID
            exam_data (dict): 考试信息
            
        Returns:
            bool: 是否更新成功
        """
        db_service = database_service.DatabaseService()
        try:
            query = """
                UPDATE Exams e
                JOIN TeacherClasses tc ON e.class_id = tc.class_id
                SET exam_name = %s
                WHERE e.exam_id = %s AND tc.teacher_id = %s
            """
            params = (
                exam_data.get('exam_name'),
                exam_id,
                teacher_id
            )
            affected_rows = db_service.execute_update(query, params)
            return affected_rows > 0
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def delete_exam(self, exam_id, teacher_id):
        """
        删除考试
        
        Args:
            exam_id (int): 考试ID
            teacher_id (int): 教师ID
            
        Returns:
            bool: 是否删除成功
        """
        db_service = database_service.DatabaseService()
        try:
            query = """
                DELETE e FROM Exams e
                JOIN TeacherClasses tc ON e.class_id = tc.class_id
                WHERE e.exam_id = %s AND tc.teacher_id = %s
            """
            params = (exam_id, teacher_id)
            affected_rows = db_service.execute_update(query, params)
            return affected_rows > 0
        except Exception as e:
            raise e
        finally:
            db_service.close()