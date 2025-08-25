"""教师服务模块，处理与教师相关的业务逻辑"""
from utils import database_service


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
            teacher_id (int): 教师ID
            
        Returns:
            dict: 教师信息
        """
        try:
            query = """
                SELECT t.teacher_id, t.teacher_name, t.subject_id, s.subject_name
                FROM Teachers t
                JOIN Subjects s ON t.subject_id = s.subject_id
                WHERE t.teacher_id = %s
            """
            return self.db_service.execute_query(query, (teacher_id,), fetch_one=True)
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
            dict: 创建的教师信息
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
            
            # 获取新创建的教师信息
            select_query = """
                SELECT teacher_id, teacher_name, subject_id
                FROM Teachers
                WHERE teacher_name = %s AND subject_id = %s
                ORDER BY teacher_id DESC
                LIMIT 1
            """
            select_params = (
                teacher_data.get('teacher_name'),
                teacher_data.get('subject_id')
            )
            teacher = self.db_service.execute_query(select_query, select_params, fetch_one=True)
            return teacher
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
            bool: 是否更新成功
        """
        try:
            # 构建动态更新语句
            fields = []
            params = []
            
            for key, value in teacher_data.items():
                if key in ['teacher_name', 'subject_id']:
                    fields.append(f"{key} = %s")
                    params.append(value)
            
            if not fields:
                return False
            
            params.append(teacher_id)
            query = f"UPDATE Teachers SET {', '.join(fields)} WHERE teacher_id = %s"
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
            query = "DELETE FROM Teachers WHERE teacher_id = %s"
            self.db_service.execute_update(query, (teacher_id,))
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()