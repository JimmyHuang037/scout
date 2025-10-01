"""班级服务模块，处理与班级相关的业务逻辑"""
import logging
from flask import current_app
from apps.utils.database_service import DatabaseService


class ClassNotFoundError(Exception):
    """班级未找到异常"""
    pass


class ClassService:
    """班级服务类"""

    def __init__(self):
        """初始化班级服务"""
        self.db_service = DatabaseService()
    
    def get_all_classes(self, page=1, per_page=10):
        """
        获取所有班级（带分页）
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 班级列表和分页信息
        """
        try:
            offset = (page - 1) * per_page
            
            # 获取总数
            count_query = "SELECT COUNT(*) as count FROM Classes"
            total = self.db_service.get_count(count_query)
            
            # 获取班级列表
            query = """
                SELECT c.class_id, c.class_name, 
                       COUNT(s.student_id) as student_count
                FROM Classes c
                LEFT JOIN Students s ON c.class_id = s.class_id
                GROUP BY c.class_id, c.class_name
                ORDER BY c.class_id
                LIMIT %s OFFSET %s
            """
            classes = self.db_service.execute_query(query, (per_page, offset))
            
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
            raise e
    
    def get_class_by_id(self, class_id):
        """
        根据班级ID获取班级详情
        
        Args:
            class_id (int): 班级ID
            
        Returns:
            dict: 班级信息
        """
        try:
            query = """
                SELECT c.class_id, c.class_name, 
                       COUNT(s.student_id) as student_count
                FROM Classes c
                LEFT JOIN Students s ON c.class_id = s.class_id
                WHERE c.class_id = %s
                GROUP BY c.class_id, c.class_name
            """
            result = self.db_service.execute_query(query, (class_id,))
            return result[0] if result else None
        except Exception as e:
            raise e
    
    def create_class(self, class_data):
        """
        创建班级
        
        Args:
            class_data (dict): 班级信息
            
        Returns:
            dict: 创建的班级信息
        """
        try:
            query = "INSERT INTO Classes (class_name) VALUES (%s)"
            params = (class_data.get('class_name'),)
            self.db_service.execute_update(query, params)
            
            # 获取新创建的班级信息
            select_query = """
                SELECT class_id, class_name
                FROM Classes
                WHERE class_name = %s
                ORDER BY class_id DESC
                LIMIT 1
            """
            select_params = (class_data.get('class_name'),)
            class_info = self.db_service.execute_query(select_query, select_params, fetch_one=True)
            return class_info
        except Exception as e:
            raise e
    
    def update_class(self, class_id, class_data):
        """
        更新班级信息
        
        Args:
            class_id (int): 班级ID
            class_data (dict): 班级信息
            
        Returns:
            bool: 是否更新成功
        """
        try:
            # 构建动态更新语句
            fields = []
            params = []
            
            for key, value in class_data.items():
                if key in ['class_name']:
                    fields.append(f"{key} = %s")
                    params.append(value)
            
            if not fields:
                return False
            
            params.append(class_id)
            query = f"UPDATE Classes SET {', '.join(fields)} WHERE class_id = %s"
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
    
    def delete_class(self, class_id):
        """
        删除班级
        :param class_id: 班级ID
        :return: None
        """
        try:
            # 删除与该班级相关的成绩
            delete_scores_query = "DELETE FROM Scores WHERE student_id IN (SELECT student_id FROM Students WHERE class_id = %s)"
            self.db_service.execute_update(delete_scores_query, (class_id,))
            
            # 删除与该班级相关的教师班级关联
            delete_teacher_classes_query = "DELETE FROM TeacherClasses WHERE class_id = %s"
            self.db_service.execute_update(delete_teacher_classes_query, (class_id,))
            
            # 删除与该班级相关的学生
            delete_students_query = "DELETE FROM Students WHERE class_id = %s"
            self.db_service.execute_update(delete_students_query, (class_id,))
            
            # 删除班级
            delete_class_query = "DELETE FROM Classes WHERE class_id = %s"
            self.db_service.execute_update(delete_class_query, (class_id,))

            return True
        except Exception as e:
            raise e
    
    def get_class_students(self, class_id):
        """
        获取班级学生列表
        
        Args:
            class_id (int): 班级ID
            
        Returns:
            dict: 学生列表
        """
        try:
            query = """
                SELECT s.student_id, s.student_name, c.class_name
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                WHERE s.class_id = %s
                ORDER BY s.student_id
            """
            students = self.db_service.execute_query(query, (class_id,))
            return {
                'students': students
            }
        except Exception as e:
            raise e
            
    def get_students_by_class(self, class_id, teacher_id):
        """
        获取班级学生列表（教师权限验证版本）
        
        Args:
            class_id (int): 班级ID
            teacher_id (str): 教师ID
            
        Returns:
            dict: 学生列表
        """
        try:
            query = """
                SELECT s.student_id, s.student_name, c.class_name
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE s.class_id = %s AND tc.teacher_id = %s
                ORDER BY s.student_id
            """
            students = self.db_service.execute_query(query, (class_id, teacher_id))
            return {
                'students': students
            }
        except Exception as e:
            raise e