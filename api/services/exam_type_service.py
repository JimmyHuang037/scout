"""考试类型服务模块，处理与考试类型相关的业务逻辑"""
from utils import DatabaseService


class ExamTypeService:
    """考试类型服务类"""
    
    def __init__(self):
        """初始化考试类型服务"""
        self.db_service = DatabaseService()
    
    def get_all_exam_types(self, page=1, per_page=10):
        """
        获取所有考试类型（带分页）
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 考试类型列表和分页信息
        """
        try:
            offset = (page - 1) * per_page
            
            # 获取总数
            count_query = "SELECT COUNT(*) as count FROM ExamTypes"
            total = self.db_service.get_count(count_query)
            
            # 获取考试类型列表
            query = """
                SELECT type_id, exam_type_name
                FROM ExamTypes
                ORDER BY type_id
                LIMIT %s OFFSET %s
            """
            exam_types = self.db_service.execute_query(query, (per_page, offset))
            
            return {
                'exam_types': exam_types,
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
    
    def get_exam_type_by_id(self, type_id):
        """
        根据ID获取考试类型详情
        
        Args:
            type_id (int): 考试类型ID
            
        Returns:
            dict: 考试类型信息
        """
        try:
            query = "SELECT type_id, exam_type_name FROM ExamTypes WHERE type_id = %s"
            return self.db_service.execute_query(query, (type_id,), fetch_one=True)
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def create_exam_type(self, exam_type_data):
        """
        创建考试类型
        
        Args:
            exam_type_data (dict): 考试类型信息
            
        Returns:
            dict: 创建的考试类型信息
        """
        try:
            query = "INSERT INTO ExamTypes (exam_type_name) VALUES (%s)"
            params = (exam_type_data.get('exam_type_name'),)
            self.db_service.execute_update(query, params)
            
            # 获取新创建的考试类型信息
            select_query = """
                SELECT type_id, exam_type_name
                FROM ExamTypes
                WHERE exam_type_name = %s
                ORDER BY type_id DESC
                LIMIT 1
            """
            select_params = (exam_type_data.get('exam_type_name'),)
            exam_type_info = self.db_service.execute_query(select_query, select_params, fetch_one=True)
            return exam_type_info
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def update_exam_type(self, type_id, exam_type_data):
        """
        更新考试类型信息
        
        Args:
            type_id (int): 考试类型ID
            exam_type_data (dict): 考试类型信息
            
        Returns:
            bool: 是否更新成功
        """
        try:
            query = "UPDATE ExamTypes SET exam_type_name = %s WHERE type_id = %s"
            params = (exam_type_data.get('exam_type_name'), type_id)
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()
    
    def delete_exam_type(self, type_id):
        """
        删除考试类型
        
        Args:
            type_id (int): 考试类型ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            query = "DELETE FROM ExamTypes WHERE type_id = %s"
            self.db_service.execute_update(query, (type_id,))
            return True
        except Exception as e:
            raise e
        finally:
            self.db_service.close()