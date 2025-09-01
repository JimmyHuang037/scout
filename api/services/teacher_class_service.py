"""教师班级关联服务模块"""
from utils import database_service
try:
    from flask import current_app
except ImportError:
    current_app = None


class TeacherClassService:
    """教师班级关联服务类"""

    def get_all_teacher_classes(self, page=1, per_page=10):
        """
        获取所有教师班级关联列表（分页）
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 教师班级关联列表和分页信息
        """
        db_service = database_service.DatabaseService()
        try:
            offset = (page - 1) * per_page
            
            # 获取总数
            count_query = "SELECT COUNT(*) as count FROM TeacherClasses"
            total = db_service.get_count(count_query)
            
            # 获取教师班级关联列表
            query = """
                SELECT tc.teacher_id, t.teacher_name, tc.class_id, c.class_name
                FROM TeacherClasses tc
                JOIN Teachers t ON tc.teacher_id = t.teacher_id
                JOIN Classes c ON tc.class_id = c.class_id
                ORDER BY tc.teacher_id, tc.class_id
                LIMIT %s OFFSET %s
            """
            teacher_classes = db_service.execute_query(query, (per_page, offset))
            
            return {
                'teacher_classes': teacher_classes,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }
            
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get all teacher classes: {str(e)}")
            raise e
        finally:
            db_service.close()
    
    def get_teacher_class_by_teacher(self, teacher_id):
        """
        根据教师ID获取教师班级关联详情
        
        Args:
            teacher_id (int): 教师ID
            
        Returns:
            list: 教师班级关联列表
        """
        db_service = database_service.DatabaseService()
        try:
            query = """
                SELECT tc.teacher_id, t.teacher_name, tc.class_id, c.class_name
                FROM TeacherClasses tc
                JOIN Teachers t ON tc.teacher_id = t.teacher_id
                JOIN Classes c ON tc.class_id = c.class_id
                WHERE tc.teacher_id = %s
                ORDER BY tc.class_id
            """
            return db_service.execute_query(query, (teacher_id,))
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get teacher class by teacher {teacher_id}: {str(e)}")
            raise e
        finally:
            db_service.close()
    
    def get_teacher_class_by_id(self, teacher_class_id):
        """
        根据ID获取教师班级关联详情
        
        Args:
            teacher_class_id (int): 教师班级关联ID
            
        Returns:
            dict: 教师班级关联信息
        """
        db_service = database_service.DatabaseService()
        try:
            query = """
                SELECT tc.teacher_id, t.teacher_name, tc.class_id, c.class_name
                FROM TeacherClasses tc
                JOIN Teachers t ON tc.teacher_id = t.teacher_id
                JOIN Classes c ON tc.class_id = c.class_id
                WHERE tc.teacher_class_id = %s
            """
            return db_service.execute_query(query, (teacher_class_id,), fetch_one=True)
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get teacher class by id {teacher_class_id}: {str(e)}")
            raise e
        finally:
            db_service.close()
    
    def create_teacher_class(self, teacher_id, class_id):
        """
        创建教师班级关联
        
        Args:
            teacher_id (int): 教师ID
            class_id (int): 班级ID
            
        Returns:
            int: 新创建的教师班级关联ID
        """
        db_service = database_service.DatabaseService()
        try:
            # 检查是否已存在相同的教师班级关联
            check_query = "SELECT COUNT(*) as count FROM TeacherClasses WHERE teacher_id = %s AND class_id = %s"
            existing = db_service.execute_query(check_query, (teacher_id, class_id), fetch_one=True)
            if existing and existing['count'] > 0:
                return None  # 已存在相同的关联
            
            # 插入新的教师班级关联
            insert_query = "INSERT INTO TeacherClasses (teacher_id, class_id) VALUES (%s, %s)"
            db_service.execute_update(insert_query, (teacher_id, class_id))
            
            # 获取新创建的关联ID
            select_query = "SELECT LAST_INSERT_ID() as id"
            result = db_service.execute_query(select_query, (), fetch_one=True)
            return result['id'] if result else None
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to create teacher class: {str(e)}")
            raise e
        finally:
            db_service.close()
    
    def update_teacher_class(self, teacher_id, class_id, new_teacher_id):
        """
        更新教师班级关联
        
        Args:
            teacher_id (int): 原教师ID
            class_id (int): 班级ID
            new_teacher_id (int): 新教师ID
            
        Returns:
            int: 更新后的教师班级关联ID
        """
        db_service = database_service.DatabaseService()
        try:
            # 更新教师班级关联
            update_query = "UPDATE TeacherClasses SET teacher_id = %s WHERE teacher_id = %s AND class_id = %s"
            db_service.execute_update(update_query, (new_teacher_id, teacher_id, class_id))
            
            # 获取更新后的关联信息
            select_query = """
                SELECT tc.teacher_class_id
                FROM TeacherClasses tc
                WHERE tc.teacher_id = %s AND tc.class_id = %s
            """
            result = db_service.execute_query(select_query, (new_teacher_id, class_id), fetch_one=True)
            return result['teacher_class_id'] if result else None
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to update teacher class: {str(e)}")
            raise e
        finally:
            db_service.close()
    
    def delete_teacher_class(self, teacher_class_id):
        """
        删除教师班级关联
        
        Args:
            teacher_class_id (int): 教师班级关联ID
            
        Returns:
            bool: 是否删除成功
        """
        db_service = database_service.DatabaseService()
        try:
            query = "DELETE FROM TeacherClasses WHERE teacher_class_id = %s"
            affected_rows = db_service.execute_update(query, (teacher_class_id,))
            return affected_rows > 0
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to delete teacher class {teacher_class_id}: {str(e)}")
            raise e
        finally:
            db_service.close()
    
    def delete_teacher_class_by_teacher_and_class(self, teacher_id, class_id):
        """
        根据教师ID和班级ID删除教师班级关联
        
        Args:
            teacher_id (int): 教师ID
            class_id (int): 班级ID
            
        Returns:
            bool: 是否删除成功
        """
        db_service = database_service.DatabaseService()
        try:
            query = "DELETE FROM TeacherClasses WHERE teacher_id = %s AND class_id = %s"
            affected_rows = db_service.execute_update(query, (teacher_id, class_id))
            return affected_rows > 0
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to delete teacher class by teacher {teacher_id} and class {class_id}: {str(e)}")
            raise e
        finally:
            db_service.close()