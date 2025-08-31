"""教师服务模块"""
import logging
from utils import database_service

# 初始化日志器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TeacherService:
    """教师服务类"""

    def __init__(self):
        """初始化教师服务"""
        self.db_service = database_service.DatabaseService()
    
    def get_all_teachers(self, page=1, per_page=10):
        """
        获取所有教师（带分页）
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 教师列表和分页信息
        """
        try:
            offset = (page - 1) * per_page
            
            # 获取总数
            count_query = "SELECT COUNT(*) as count FROM Teachers"
            total = self.db_service.get_count(count_query)
            
            # 获取教师列表
            query = """
                SELECT t.teacher_id, t.teacher_name, t.subject_id, s.subject_name
                FROM Teachers t
                LEFT JOIN Subjects s ON t.subject_id = s.subject_id
                ORDER BY t.teacher_id
                LIMIT %s OFFSET %s
            """
            teachers = self.db_service.execute_query(query, (per_page, offset))
            
            return {
                'teachers': teachers,
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
    
    def get_teacher_by_id(self, teacher_id):
        """
        根据教师ID获取教师详情
        
        Args:
            teacher_id (int or str): 教师ID
            
        Returns:
            dict: 教师信息
        """
        try:
            query = """
                SELECT t.teacher_id, t.teacher_name, t.subject_id, s.subject_name
                FROM Teachers t
                LEFT JOIN Subjects s ON t.subject_id = s.subject_id
                WHERE t.teacher_id = %s
            """
            result = self.db_service.execute_query(query, (teacher_id,), fetch_one=True)
            return result
        except Exception as e:
            raise e
        finally:
            self.db_service.close()

    def create_teacher(self, teacher_data):
        """
        创建教师
        
        Args:
            teacher_data (dict): 教师信息
            
        Returns:
            bool: 是否创建成功
        """
        try:
            query = """
                INSERT INTO Teachers (teacher_name, subject_id, password)
                VALUES (%s, %s, %s)
            """
            params = (
                teacher_data.get('teacher_name'),
                teacher_data.get('subject_id'),
                teacher_data.get('password')
            )
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def update_teacher(self, teacher_id, teacher_data):
        """
        更新教师信息
        
        Args:
            teacher_id (int): 教师ID
            teacher_data (dict): 教师信息
            
        Returns:
            dict: 更新后的教师信息
        """
        db_service = None
        try:
            db_service = database_service.DatabaseService()
            # 构建动态更新语句
            update_fields = []
            params = []
            
            if 'teacher_name' in teacher_data:
                update_fields.append("teacher_name = %s")
                params.append(teacher_data['teacher_name'])
            
            if 'subject_id' in teacher_data:
                update_fields.append("subject_id = %s")
                params.append(teacher_data['subject_id'])
            
            if 'password' in teacher_data:
                update_fields.append("password = %s")
                params.append(teacher_data['password'])
            
            if not update_fields:
                return False
            
            params.append(teacher_id)
            query = f"UPDATE Teachers SET {', '.join(update_fields)} WHERE teacher_id = %s"
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def delete_teacher(self, teacher_id):
        """
        删除教师
        
        Args:
            teacher_id (int): 教师ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            self.db_service.start_transaction()
            
            # 删除教师班级关联记录
            delete_teacher_classes_query = "DELETE FROM TeacherClasses WHERE teacher_id = %s"
            self.db_service.execute_update(delete_teacher_classes_query, (teacher_id,))
            
            # 删除教师记录
            delete_teacher_query = "DELETE FROM Teachers WHERE teacher_id = %s"
            self.db_service.execute_update(delete_teacher_query, (teacher_id,))
            
            self.db_service.commit()
            return True
        except Exception as e:
            self.db_service.rollback()
            raise e
        finally:
            self.db_service.close()
    
    def get_teachers_by_subject(self, subject_id):
        """
        根据科目ID获取教师列表
        
        Args:
            subject_id (int): 科目ID
            
        Returns:
            list: 教师列表
        """
        db_service = None
        try:
            db_service = database_service.DatabaseService()
            query = """
                SELECT t.teacher_id, t.teacher_name, t.subject_id, s.subject_name
                FROM Teachers t
                LEFT JOIN Subjects s ON t.subject_id = s.subject_id
                WHERE t.subject_id = %s
                ORDER BY t.teacher_id
            """
            teachers = db_service.execute_query(query, (subject_id,))
            return teachers
        except Exception as e:
            raise e
        finally:
            if db_service:
                db_service.close()