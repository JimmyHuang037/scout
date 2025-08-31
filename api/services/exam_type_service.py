"""考试类型服务模块，处理与考试类型相关的业务逻辑"""
from utils import database_service


class ExamTypeService:
    """考试类型服务类"""
    
    def __init__(self):
        """初始化考试类型服务"""
        self.db_service = database_service.DatabaseService()
    
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
            # 获取总数
            count_query = "SELECT COUNT(*) as count FROM ExamTypes"
            total_result = self.db_service.execute_query(count_query, (), fetch_one=True)
            total = total_result['count'] if total_result else 0
            
            # 计算偏移量
            offset = (page - 1) * per_page
            
            # 获取考试类型列表
            query = """
                SELECT exam_type_id, exam_type_name
                FROM ExamTypes
                ORDER BY exam_type_id
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
    
    def get_exam_type_by_id(self, exam_type_id):
        """
        根据ID获取考试类型详情
        
        Args:
            exam_type_id (int): 考试类型ID
            
        Returns:
            dict: 考试类型信息
        """
        try:
            query = "SELECT exam_type_id, exam_type_name FROM ExamTypes WHERE exam_type_id = %s"
            return self.db_service.execute_query(query, (exam_type_id,), fetch_one=True)
        except Exception as e:
            raise e
        # 不在这里关闭数据库连接，由调用者负责关闭
    
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
                SELECT exam_type_id, exam_type_name
                FROM ExamTypes
                WHERE exam_type_id = LAST_INSERT_ID()
            """
            exam_type_info = self.db_service.execute_query(select_query, (), fetch_one=True)
            
            # 确保返回的字典包含正确的字段
            if exam_type_info:
                return {
                    'exam_type_id': exam_type_info['exam_type_id'],
                    'exam_type_name': exam_type_info['exam_type_name']
                }
            return None
        except Exception as e:
            raise e
    
    def update_exam_type(self, exam_type_id, exam_type_data):
        """
        更新考试类型信息
        
        Args:
            exam_type_id (int): 考试类型ID
            exam_type_data (dict): 考试类型信息
            
        Returns:
            bool: 是否更新成功
        """
        try:
            query = "UPDATE ExamTypes SET exam_type_name = %s WHERE exam_type_id = %s"
            params = (exam_type_data.get('exam_type_name'), exam_type_id)
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            raise e
        # 不在这里关闭数据库连接，由调用者负责关闭
    
    def delete_exam_type(self, exam_type_id):
        """
        删除考试类型（同时删除相关的成绩）
        
        Args:
            exam_type_id (int): 考试类型ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            # 检查是否已经在事务中，如果不是则开始事务
            transaction_started_here = False
            if not self.db_service.transaction_active:
                self.db_service.start_transaction()
                transaction_started_here = True
            
            # 删除与该考试类型相关的成绩
            delete_scores_query = "DELETE FROM Scores WHERE exam_type_id = %s"
            self.db_service.execute_update(delete_scores_query, (exam_type_id,))
            
            # 删除考试类型
            delete_exam_type_query = "DELETE FROM ExamTypes WHERE exam_type_id = %s"
            self.db_service.execute_update(delete_exam_type_query, (exam_type_id,))
            
            # 如果我们启动了事务，则提交它
            if transaction_started_here and self.db_service.transaction_active:
                self.db_service.commit()
            return True
        except Exception as e:
            # 如果我们启动了事务，则回滚它
            if transaction_started_here and self.db_service.transaction_active:
                self.db_service.rollback()
            raise e
        # 不在这里关闭数据库连接，由调用者负责关闭
