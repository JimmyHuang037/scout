"""教师服务类"""

from flask import current_app
from apps.utils.database_service import DatabaseService


class TeacherService:
    """教师服务类"""

    def __init__(self):
        """初始化教师服务"""
        self.db_service = DatabaseService()

    def get_all_teachers(self, page=1, per_page=10):
        """
        获取所有教师列表（分页）
        
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
            if current_app:
                current_app.logger.error(f"Failed to get all teachers: {str(e)}")
            raise e
        finally:
            self.db_service.close()
    
    def get_teacher_by_id(self, teacher_id):
        """
        根据ID获取教师详情
        
        Args:
            teacher_id (int): 教师ID
            
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
            if current_app:
                current_app.logger.error(f"Failed to get teacher by id {teacher_id}: {str(e)}")
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
            if current_app:
                current_app.logger.error(f"Failed to create teacher: {str(e)}")
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
        connection = None
        try:
            # 获取数据库连接并开始事务
            connection = self.db_service.get_connection()
            connection.autocommit(False)
            
            with connection.cursor() as cursor:
                # 先检查教师是否存在
                check_query = "SELECT COUNT(*) as count FROM Teachers WHERE teacher_id = %s"
                cursor.execute(check_query, (teacher_id,))
                check_result = cursor.fetchone()
                
                if not check_result or check_result['count'] == 0:
                    current_app.logger.warning(f"Teacher {teacher_id} does not exist")
                    connection.rollback()
                    return False
                
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
                    connection.rollback()
                    return False
                    
                query = f"UPDATE Teachers SET {', '.join(update_fields)} WHERE teacher_id = %s"
                params.append(teacher_id)
                
                affected_rows = cursor.execute(query, params)
                connection.commit()
                return affected_rows > 0
        except Exception as e:
            if connection:
                connection.rollback()
            if current_app:
                current_app.logger.error(f"Failed to update teacher {teacher_id}: {str(e)}")
            raise e
        finally:
            if connection:
                connection.autocommit(True)
            # 不在这里关闭连接，让DatabaseService管理连接生命周期
    
    def delete_teacher(self, teacher_id):
        """
        删除教师
        
        Args:
            teacher_id (int): 教师ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            # 先检查教师是否存在
            check_query = "SELECT COUNT(*) as count FROM Teachers WHERE teacher_id = %s"
            check_result = self.db_service.execute_query(check_query, (teacher_id,), fetch_one=True)
            if not check_result or check_result['count'] == 0:
                current_app.logger.warning(f"Teacher {teacher_id} does not exist")
                return False
            
            query = "DELETE FROM Teachers WHERE teacher_id = %s"
            affected_rows = self.db_service.execute_update(query, (teacher_id,))
            return affected_rows > 0
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to delete teacher {teacher_id}: {str(e)}")
            raise e
        finally:
            self.db_service.close()