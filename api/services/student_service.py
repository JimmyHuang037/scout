"""学生服务模块"""
import logging
from utils.database_service import DatabaseService
# 移除不存在的模块导入

# 初始化日志器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StudentService:
    """学生服务类"""

    def __init__(self):
        """初始化学生服务"""
        self.db_service = DatabaseService()

    def get_all_students(self, page=1, per_page=10):
        """
        获取所有学生列表（分页）
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 学生列表和分页信息
        """
        try:
            # 计算偏移量
            offset = (page - 1) * per_page
            
            # 获取总数
            count_query = "SELECT COUNT(*) as total FROM Students"
            total_result = self.db_service.execute_query(count_query, fetch_one=True)
            total = total_result['total'] if total_result else 0
            
            # 获取学生列表
            query = """
                SELECT s.student_id, s.student_name, s.class_id, c.class_name
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                ORDER BY s.student_id
                LIMIT %s OFFSET %s
            """
            students = self.db_service.execute_query(query, (per_page, offset))
            
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
                LEFT JOIN Classes c ON s.class_id = c.class_id
                WHERE s.student_id = %s
            """
            result = self.db_service.execute_query(query, (student_id,), fetch_one=True)
            return result
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
            # 开始事务
            self.db_service.start_transaction()
            
            # 先删除相关的成绩记录
            delete_scores_query = "DELETE FROM Scores WHERE student_id = %s"
            self.db_service.execute_update(delete_scores_query, (student_id,))
            
            # 再删除学生记录
            query = "DELETE FROM Students WHERE student_id = %s"
            self.db_service.execute_update(query, (student_id,))
            
            # 提交事务
            self.db_service.commit()
            return True
        except Exception as e:
            # 回滚事务
            self.db_service.rollback()
            raise e
        finally:
            self.db_service.close()