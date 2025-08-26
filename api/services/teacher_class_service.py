"""教师班级服务模块，处理与教师班级关联相关的业务逻辑"""
from utils import database_service


class TeacherClassService:
    """教师班级服务类"""
    
    def get_all_teacher_classes(self, page=1, per_page=10):
        """
        获取所有教师班级关联（带分页）
        
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
            raise e
        finally:
            db_service.close()
    
    def create_teacher_class(self, teacher_class_data):
        """
        创建教师班级关联
        
        Args:
            teacher_class_data (dict): 教师班级关联信息
            
        Returns:
            bool: 是否创建成功
        """
        db_service = database_service.DatabaseService()
        try:
            query = """
                INSERT INTO TeacherClasses (teacher_id, class_id)
                VALUES (%s, %s)
            """
            params = (
                teacher_class_data.get('teacher_id'),
                teacher_class_data.get('class_id')
            )
            db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            db_service.close()
    
    def delete_teacher_class(self, teacher_id, class_id):
        """
        删除教师班级关联
        
        Args:
            teacher_id (int): 教师ID
            class_id (int): 班级ID
            
        Returns:
            bool: 是否删除成功
        """
        db_service = database_service.DatabaseService()
        try:
            query = """
                DELETE FROM TeacherClasses 
                WHERE teacher_id = %s AND class_id = %s
            """
            db_service.execute_update(query, (teacher_id, class_id))
            return True
        except Exception as e:
            raise e
        finally:
            db_service.close()