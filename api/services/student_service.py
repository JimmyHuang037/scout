"""学生服务模块，处理与学生相关的业务逻辑"""
from utils import database_service


class StudentService:
    """学生服务类"""
    
    def __init__(self):
        """初始化学生服务"""
        self.db_service = database_service.DatabaseService()
    
    def get_all_students(self, page=1, per_page=10):
        """
        获取所有学生（带分页）
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 学生列表和分页信息
        """
        try:
            offset = (page - 1) * per_page
            
            # 获取总数
            count_query = "SELECT COUNT(*) as count FROM Students"
            total = self.db_service.get_count(count_query)
            
            # 获取学生列表
            query = """
                SELECT s.student_id, s.student_name, s.class_id, c.class_name
                FROM Students s
                LEFT JOIN Classes c ON s.class_id = c.class_id
                ORDER BY s.student_id
                LIMIT %s OFFSET %s
            """
            students = self.db_service.execute_query(query, (per_page, offset))
            
            return {
                'students': students,
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
            self.db_service.close()
    
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
                SELECT s.student_id, s.student_name, s.class_id, c.class_name
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                WHERE s.student_id = %s
            """
            return self.db_service.execute_query(query, (student_id,), fetch_one=True)
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def create_student(self, student_data):
        """
        创建学生
        
        Args:
            student_data (dict): 学生信息
            
        Returns:
            bool: 是否创建成功
        """
        try:
            query = """
                INSERT INTO Students (student_id, student_name, class_id, password)
                VALUES (%s, %s, %s, %s)
            """
            params = (
                student_data.get('student_id'),
                student_data.get('student_name'),
                student_data.get('class_id'),
                student_data.get('password')
            )
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def update_student(self, student_id, student_data):
        """
        更新学生信息
        
        Args:
            student_id (str): 学生ID
            student_data (dict): 学生信息
            
        Returns:
            bool: 是否更新成功
        """
        try:
            query = """
                UPDATE Students 
                SET student_name = %s, class_id = %s, password = %s
                WHERE student_id = %s
            """
            params = (
                student_data.get('student_name'),
                student_data.get('class_id'),
                student_data.get('password'),
                student_id
            )
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def delete_student(self, student_id):
        """
        删除学生
        
        Args:
            student_id (str): 学生ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            query = "DELETE FROM Students WHERE student_id = %s"
            self.db_service.execute_update(query, (student_id,))
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()