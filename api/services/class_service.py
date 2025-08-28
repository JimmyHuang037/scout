"""班级服务模块，处理与班级相关的业务逻辑"""
from utils import database_service


class ClassNotFoundError(Exception):
    """班级未找到异常"""
    pass


class ClassService:
    """班级服务类"""
    
    def __init__(self):
        """初始化班级服务"""
        self.db_service = database_service.DatabaseService()
    
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
        finally:
            self.db_service.close()
    
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
            return self.db_service.execute_query(query, (class_id,), fetch_one=True)
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
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
        finally:
            self.db_service.close()
    
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
        finally:
            self.db_service.close()
    
    def delete_class(self, class_id):
        """
        删除班级
        :param class_id: 班级ID
        :return: None
        """
        # 检查班级是否存在
        class_info = self.get_class_by_id(class_id)
        if not class_info:
            raise ClassNotFoundError(f"班级ID {class_id} 不存在")

        try:
            # 开始事务
            self.db_service.start_transaction()

            # 删除与该班级相关的成绩
            delete_scores_query = "DELETE FROM Scores WHERE student_id IN (SELECT student_id FROM Students WHERE class_id = %s)"
            self.db_service.cursor.execute(delete_scores_query, (class_id,))
            
            # 删除与该班级相关的教师班级关联
            delete_teacher_classes_query = "DELETE FROM TeacherClasses WHERE class_id = %s"
            self.db_service.cursor.execute(delete_teacher_classes_query, (class_id,))
            
            # 删除与该班级相关的学生
            delete_students_query = "DELETE FROM Students WHERE class_id = %s"
            self.db_service.cursor.execute(delete_students_query, (class_id,))
            
            # 删除班级
            delete_class_query = "DELETE FROM Classes WHERE class_id = %s"
            self.db_service.cursor.execute(delete_class_query, (class_id,))

            # 提交事务
            self.db_service.commit()
        except Exception as e:
            # 回滚事务
            self.db_service.rollback()
            raise e
        finally:
            self.db_service.close()