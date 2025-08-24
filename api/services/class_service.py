"""班级服务模块，处理与班级相关的业务逻辑"""
from .database_service import DatabaseService


class ClassService:
    """班级服务类"""
    
    def __init__(self):
        """初始化班级服务"""
        self.db_service = DatabaseService()
    
    def get_all_classes(self, page=1, per_page=10):
        """
        获取所有班级列表（带分页）
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 包含班级列表和分页信息的字典
        """
        try:
            offset = (page - 1) * per_page
            
            # 获取总数
            total_result = self.db_service.execute_query(
                "SELECT COUNT(*) as count FROM Classes", 
                fetch_one=True
            )
            total = total_result['count'] if total_result else 0
            
            # 获取班级列表
            classes_query = """
                SELECT class_id, class_name
                FROM Classes
                ORDER BY class_id
                LIMIT %s OFFSET %s
            """
            classes = self.db_service.execute_query(classes_query, (per_page, offset))
            
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
            query = "SELECT class_id, class_name FROM Classes WHERE class_id = %s"
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
            bool: 是否创建成功
        """
        try:
            query = "INSERT INTO Classes (class_name) VALUES (%s)"
            params = (class_data.get('class_name'),)
            self.db_service.execute_update(query, params)
            return True
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
            query = "UPDATE Classes SET class_name = %s WHERE class_id = %s"
            params = (class_data.get('class_name'), class_id)
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def delete_class(self, class_id):
        """
        删除班级
        
        Args:
            class_id (int): 班级ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            query = "DELETE FROM Classes WHERE class_id = %s"
            self.db_service.execute_update(query, (class_id,))
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()