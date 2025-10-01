from apps.utils.database_service import DatabaseService
from flask import current_app
"""教师班级关联服务类"""



class TeacherClassService:
    """教师班级关联服务类"""

    def __init__(self):
        """初始化教师班级关联服务"""
        self.db_service = DatabaseService()

    def get_all_teacher_classes(self, page=1, per_page=10):
        """
        获取所有教师班级关联列表（分页）
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 教师班级关联列表和分页信息
        """
        try:
            offset = (page - 1) * per_page
            
            # 获取总数
            count_query = "SELECT COUNT(*) as count FROM TeacherClasses"
            total_result = self.db_service.execute_query(count_query, ())
            total = total_result[0]['count'] if total_result else 0
            
            # 获取教师班级关联列表
            query = """
                SELECT tc.teacher_id, tc.class_id,
                       t.teacher_name, c.class_name
                FROM TeacherClasses tc
                JOIN Teachers t ON tc.teacher_id = t.teacher_id
                JOIN Classes c ON tc.class_id = c.class_id
                ORDER BY tc.teacher_id, tc.class_id
                LIMIT %s OFFSET %s
            """
            teacher_classes = self.db_service.execute_query(query, (per_page, offset))
            
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
            current_app.logger.error(f"Failed to get all teacher classes: {str(e)}")
            raise e

    def get_teacher_class_by_teacher(self, teacher_id):
        """
        根据教师ID获取教师班级关联信息
        
        Args:
            teacher_id (int): 教师ID
            
        Returns:
            list: 教师班级关联信息列表
        """
        query = """
            SELECT tc.teacher_id, tc.class_id,
                   t.teacher_name, c.class_name
            FROM TeacherClasses tc
            JOIN Teachers t ON tc.teacher_id = t.teacher_id
            JOIN Classes c ON tc.class_id = c.class_id
            WHERE tc.teacher_id = %s
            ORDER BY tc.class_id
        """
        return self.db_service.execute_query(query, (teacher_id,))

    def get_teacher_class(self, teacher_id, class_id):
        """
        根据教师ID和班级ID获取特定的教师班级关联信息
        
        Args:
            teacher_id (int): 教师ID
            class_id (int): 班级ID
            
        Returns:
            dict: 教师班级关联信息
        """
        query = """
            SELECT tc.teacher_id, tc.class_id,
                   t.teacher_name, c.class_name
            FROM TeacherClasses tc
            JOIN Teachers t ON tc.teacher_id = t.teacher_id
            JOIN Classes c ON tc.class_id = c.class_id
            WHERE tc.teacher_id = %s AND tc.class_id = %s
        """
        result = self.db_service.execute_query(query, (teacher_id, class_id))
        return result[0] if result else None

    def create_teacher_class(self, teacher_id, class_id):
        """
        创建教师班级关联
        
        Args:
            teacher_id (int): 教师ID
            class_id (int): 班级ID
            
        Returns:
            bool: 创建是否成功
        """
        try:
            # 检查教师和班级是否存在
            teacher_query = "SELECT teacher_id FROM Teachers WHERE teacher_id = %s"
            class_query = "SELECT class_id FROM Classes WHERE class_id = %s"
            teacher_result = self.db_service.execute_query(teacher_query, (teacher_id,))
            class_result = self.db_service.execute_query(class_query, (class_id,))
            
            if not teacher_result:
                raise ValueError(f"Teacher with ID {teacher_id} not found")
            if not class_result:
                raise ValueError(f"Class with ID {class_id} not found")
            
            # 检查关联是否已存在
            check_query = """
                SELECT teacher_id FROM TeacherClasses 
                WHERE teacher_id = %s AND class_id = %s
            """
            existing = self.db_service.execute_query(check_query, (teacher_id, class_id))
            if existing:
                raise ValueError("Teacher-class association already exists")
            
            # 插入新关联
            insert_query = """
                INSERT INTO TeacherClasses (teacher_id, class_id)
                VALUES (%s, %s)
            """
            self.db_service.execute_update(insert_query, (teacher_id, class_id))
            
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to create teacher class: {str(e)}")
            raise e

    def update_teacher_class(self, teacher_id, class_id, new_teacher_id):
        """
        更新教师班级关联信息
        
        Args:
            teacher_id (int): 原教师ID
            class_id (int): 班级ID
            new_teacher_id (int): 新教师ID
            
        Returns:
            bool: 更新是否成功
        """
        try:
            # 检查关联是否存在
            check_query = "SELECT teacher_id FROM TeacherClasses WHERE teacher_id = %s AND class_id = %s"
            existing = self.db_service.execute_query(check_query, (teacher_id, class_id))
            current_app.logger.info(f"Checking if teacher class exists: teacher_id={teacher_id}, class_id={class_id}, existing={existing}")
            if not existing:
                return False
            if new_teacher_id:
                teacher_query = "SELECT teacher_id FROM Teachers WHERE teacher_id = %s"
                teacher_result = self.db_service.execute_query(teacher_query, (new_teacher_id,))
                if not teacher_result:
                    raise ValueError("New teacher not found")
            
            # 更新关联信息
            update_query = """
                UPDATE TeacherClasses 
                SET teacher_id = %s
                WHERE teacher_id = %s AND class_id = %s
            """
            self.db_service.execute_update(
                update_query,
                (new_teacher_id, teacher_id, class_id)
            )
            
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to update teacher class: {str(e)}")
            return False

    def delete_teacher_class(self, teacher_id, class_id):
        """
        删除教师班级关联
        
        Args:
            teacher_id (int): 教师ID
            class_id (int): 班级ID
            
        Returns:
            bool: 删除是否成功
        """
        try:
            # 检查关联是否存在
            check_query = "SELECT teacher_id FROM TeacherClasses WHERE teacher_id = %s AND class_id = %s"
            existing = self.db_service.execute_query(check_query, (teacher_id, class_id))
            if not existing:
                return False
            
            # 删除关联
            delete_query = "DELETE FROM TeacherClasses WHERE teacher_id = %s AND class_id = %s"
            self.db_service.execute_update(delete_query, (teacher_id, class_id))
            
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to delete teacher class: {str(e)}")
            return False