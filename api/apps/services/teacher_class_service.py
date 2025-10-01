"""教师班级关联服务类"""

from flask import current_app
from apps.utils.database_service import DatabaseService


class TeacherClassService:
    """教师班级关联服务类"""

    def __init__(self):
        """初始化教师班级关联服务"""
        self.db_service = DatabaseService()

    def get_teacher_classes(self, teacher_id, page=1, per_page=10):
        """
        根据教师ID获取其授课班级列表（分页）
        
        Args:
            teacher_id (int): 教师ID
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 包含班级列表和分页信息的字典
        """
        try:
            offset = (page - 1) * per_page

            # 获取总数
            count_query = """SELECT COUNT(*) as count FROM TeacherClasses WHERE teacher_id = %s"""
            total_result = self.db_service.execute_query(count_query, (teacher_id,), fetch_one=True)
            total = total_result['count'] if total_result else 0

            # 获取教师授课班级列表
            query = """
                SELECT tc.teacher_class_id, tc.teacher_id, tc.class_id, tc.subject_id,
                       t.teacher_name, c.class_name, s.subject_name
                FROM TeacherClasses tc
                JOIN Teachers t ON tc.teacher_id = t.teacher_id
                JOIN Classes c ON tc.class_id = c.class_id
                JOIN Subjects s ON tc.subject_id = s.subject_id
                WHERE tc.teacher_id = %s
                ORDER BY tc.class_id
                LIMIT %s OFFSET %s
            """
            classes = self.db_service.execute_query(query, (teacher_id, per_page, offset))

            return {
                'classes': classes,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }
        except Exception as e:
            current_app.logger.error(f"Failed to get teacher classes: {str(e)}")
            raise e

    def get_class_teachers(self, class_id, page=1, per_page=10):
        """
        根据班级ID获取其任课教师列表（分页）
        
        Args:
            class_id (int): 班级ID
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 包含教师列表和分页信息的字典
        """
        try:
            offset = (page - 1) * per_page

            # 获取总数
            count_query = """SELECT COUNT(*) as count FROM TeacherClasses WHERE class_id = %s"""
            total_result = self.db_service.execute_query(count_query, (class_id,), fetch_one=True)
            total = total_result['count'] if total_result else 0

            # 获取班级任课教师列表
            query = """
                SELECT tc.teacher_class_id, tc.teacher_id, tc.class_id, tc.subject_id,
                       t.teacher_name, c.class_name, s.subject_name
                FROM TeacherClasses tc
                JOIN Teachers t ON tc.teacher_id = t.teacher_id
                JOIN Classes c ON tc.class_id = c.class_id
                JOIN Subjects s ON tc.subject_id = s.subject_id
                WHERE tc.class_id = %s
                ORDER BY tc.subject_id
                LIMIT %s OFFSET %s
            """
            teachers = self.db_service.execute_query(query, (class_id, per_page, offset))

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
            current_app.logger.error(f"Failed to get class teachers: {str(e)}")
            raise e

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
            # 获取教师的科目ID
            teacher_query = "SELECT subject_id FROM Teachers WHERE teacher_id = %s"
            teacher_result = self.db_service.execute_query(teacher_query, (teacher_id,), fetch_one=True)
            if not teacher_result:
                raise ValueError("Teacher not found")
            
            subject_id = teacher_result['subject_id']
            
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
                INSERT INTO TeacherClasses (teacher_id, class_id, subject_id)
                VALUES (%s, %s, %s)
            """
            self.db_service.execute_update(insert_query, (teacher_id, class_id, subject_id))
            
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to create teacher class: {str(e)}")
            raise e


    def update_teacher_class(self, teacher_id, class_id, new_teacher_id):
        """
        更新教师班级关联信息（更换教师）
        
        Args:
            teacher_id (int): 原教师ID
            class_id (int): 班级ID
            new_teacher_id (int): 新教师ID
            
        Returns:
            bool: 更新是否成功
        """
        try:
            # 检查原关联是否存在
            check_query = "SELECT teacher_id FROM TeacherClasses WHERE teacher_id = %s AND class_id = %s"
            existing = self.db_service.execute_query(check_query, (teacher_id, class_id), fetch_one=True)
            if not existing:
                return False
                
            # 获取新教师的科目ID
            teacher_query = "SELECT subject_id FROM Teachers WHERE teacher_id = %s"
            teacher_result = self.db_service.execute_query(teacher_query, (new_teacher_id,), fetch_one=True)
            if not teacher_result:
                raise ValueError("New teacher not found")
            
            new_subject_id = teacher_result['subject_id']
            
            # 更新关联信息
            update_query = """
                UPDATE TeacherClasses 
                SET teacher_id = %s, subject_id = %s
                WHERE teacher_id = %s AND class_id = %s
            """
            self.db_service.execute_update(
                update_query,
                (new_teacher_id, new_subject_id, teacher_id, class_id)
            )
            
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to update teacher class: {str(e)}")
            return False

    def delete_teacher_class(self, teacher_class_id):
        """
        删除教师班级关联
        
        Args:
            teacher_class_id (int): 教师班级关联ID
            
        Returns:
            bool: 是否删除成功
        """
        # 检查关联是否存在
        if not self.get_teacher_class_by_id(teacher_class_id):
            return False
            
        # 删除关联
        delete_query = "DELETE FROM TeacherClasses WHERE teacher_class_id = %s"
        self.db_service.execute_update(delete_query, (teacher_class_id,))
        return True