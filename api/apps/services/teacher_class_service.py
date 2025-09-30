"""教师班级关联服务类"""

from flask import current_app
from apps.utils.database_service import DatabaseService


class TeacherClassService:
    """教师班级关联服务类"""

    def __init__(self):
        """初始化教师班级关联服务"""
        self.db_service = DatabaseService()

    def get_teacher_classes(self, teacher_id):
        """
        获取教师授课班级列表
        
        Args:
            teacher_id (int): 教师ID
            
        Returns:
            list: 教师授课班级列表
        """
        query = """
            SELECT tc.teacher_class_id, tc.teacher_id, tc.class_id, tc.subject_id,
                   t.teacher_name, c.class_name, s.subject_name
            FROM teacher_classes tc
            JOIN teachers t ON tc.teacher_id = t.teacher_id
            JOIN classes c ON tc.class_id = c.class_id
            JOIN subjects s ON tc.subject_id = s.subject_id
            WHERE tc.teacher_id = %s
            ORDER BY tc.teacher_class_id
        """
        return self.db_service.execute_query(query, (teacher_id,))

    def get_class_teachers(self, class_id):
        """
        获取班级任课教师列表
        
        Args:
            class_id (int): 班级ID
            
        Returns:
            list: 班级任课教师列表
        """
        query = """
            SELECT tc.teacher_class_id, tc.teacher_id, tc.class_id, tc.subject_id,
                   t.teacher_name, c.class_name, s.subject_name
            FROM teacher_classes tc
            JOIN teachers t ON tc.teacher_id = t.teacher_id
            JOIN classes c ON tc.class_id = c.class_id
            JOIN subjects s ON tc.subject_id = s.subject_id
            WHERE tc.class_id = %s
            ORDER BY tc.teacher_class_id
        """
        return self.db_service.execute_query(query, (class_id,))

    def create_teacher_class(self, teacher_class_data):
        """
        创建教师班级关联
        
        Args:
            teacher_class_data (dict): 教师班级关联数据
            
        Returns:
            dict: 创建的教师班级关联信息
        """
        # 检查关联是否已存在
        check_query = """
            SELECT teacher_class_id FROM teacher_classes 
            WHERE teacher_id = %s AND class_id = %s AND subject_id = %s
        """
        existing = self.db_service.execute_query(
            check_query, 
            (teacher_class_data['teacher_id'], teacher_class_data['class_id'], teacher_class_data['subject_id'])
        )
        if existing:
            raise ValueError("Teacher-class-subject association already exists")
        
        # 插入新关联
        insert_query = """
            INSERT INTO teacher_classes (teacher_id, class_id, subject_id)
            VALUES (%s, %s, %s)
        """
        teacher_class_id = self.db_service.execute_update(
            insert_query, 
            (teacher_class_data['teacher_id'], teacher_class_data['class_id'], teacher_class_data['subject_id'])
        )
        
        # 返回创建的关联信息
        return self.get_teacher_class_by_id(teacher_class_id)

    def get_teacher_class_by_id(self, teacher_class_id):
        """
        根据ID获取教师班级关联信息
        
        Args:
            teacher_class_id (int): 教师班级关联ID
            
        Returns:
            dict: 教师班级关联信息
        """
        query = """
            SELECT tc.teacher_class_id, tc.teacher_id, tc.class_id, tc.subject_id,
                   t.teacher_name, c.class_name, s.subject_name
            FROM teacher_classes tc
            JOIN teachers t ON tc.teacher_id = t.teacher_id
            JOIN classes c ON tc.class_id = c.class_id
            JOIN subjects s ON tc.subject_id = s.subject_id
            WHERE tc.teacher_class_id = %s
        """
        result = self.db_service.execute_query(query, (teacher_class_id,))
        return result[0] if result else None

    def update_teacher_class(self, teacher_class_id, teacher_class_data):
        """
        更新教师班级关联信息
        
        Args:
            teacher_class_id (int): 教师班级关联ID
            teacher_class_data (dict): 教师班级关联数据
            
        Returns:
            dict: 更新后的教师班级关联信息
        """
        # 检查关联是否存在
        if not self.get_teacher_class_by_id(teacher_class_id):
            return None
            
        # 更新关联信息
        update_query = """
            UPDATE teacher_classes 
            SET teacher_id = %s, class_id = %s, subject_id = %s
            WHERE teacher_class_id = %s
        """
        self.db_service.execute_update(
            update_query,
            (teacher_class_data['teacher_id'], teacher_class_data['class_id'], 
             teacher_class_data['subject_id'], teacher_class_id)
        )
        
        # 返回更新后的关联信息
        return self.get_teacher_class_by_id(teacher_class_id)

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
        delete_query = "DELETE FROM teacher_classes WHERE teacher_class_id = %s"
        self.db_service.execute_update(delete_query, (teacher_class_id,))
        return True