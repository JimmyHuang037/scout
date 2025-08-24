"""科目服务模块，处理与科目相关的业务逻辑"""
from api.utils import DatabaseService


class SubjectService:
    """科目服务类"""
    
    def __init__(self):
        """初始化科目服务"""
        self.db_service = DatabaseService()
    
    def get_all_subjects(self, page=1, per_page=10):
        """
        获取所有科目（带分页）
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 科目列表和分页信息
        """
        try:
            offset = (page - 1) * per_page
            
            # 获取总数
            count_query = "SELECT COUNT(*) as count FROM Subjects"
            total = self.db_service.get_count(count_query)
            
            # 获取科目列表
            query = """
                SELECT subject_id, subject_name
                FROM Subjects
                ORDER BY subject_id
                LIMIT %s OFFSET %s
            """
            subjects = self.db_service.execute_query(query, (per_page, offset))
            
            return {
                'subjects': subjects,
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
    
    def get_subject_by_id(self, subject_id):
        """
        根据ID获取科目详情
        
        Args:
            subject_id (int): 科目ID
            
        Returns:
            dict: 科目信息
        """
        try:
            query = "SELECT subject_id, subject_name FROM Subjects WHERE subject_id = %s"
            return self.db_service.execute_query(query, (subject_id,), fetch_one=True)
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def create_subject(self, subject_data):
        """
        创建科目
        
        Args:
            subject_data (dict): 科目信息
            
        Returns:
            bool: 是否创建成功
        """
        try:
            query = "INSERT INTO Subjects (subject_name) VALUES (%s)"
            params = (subject_data.get('subject_name'),)
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def update_subject(self, subject_id, subject_data):
        """
        更新科目信息
        
        Args:
            subject_id (int): 科目ID
            subject_data (dict): 科目信息
            
        Returns:
            bool: 是否更新成功
        """
        try:
            query = "UPDATE Subjects SET subject_name = %s WHERE subject_id = %s"
            params = (subject_data.get('subject_name'), subject_id)
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def delete_subject(self, subject_id):
        """
        删除科目
        
        Args:
            subject_id (int): 科目ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            query = "DELETE FROM Subjects WHERE subject_id = %s"
            self.db_service.execute_update(query, (subject_id,))
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()