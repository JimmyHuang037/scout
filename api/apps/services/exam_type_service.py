from apps.utils.database_service import DatabaseService
from flask import current_app
"""考试类型服务模块，处理与考试类型相关的业务逻辑"""


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
            # 获取总数
            count_query = "SELECT COUNT(*) as count FROM ExamTypes"
            total_result = self.db_service.execute_query(count_query, ())
            total = total_result[0]['count'] if total_result else 0
            
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
            if current_app:
                current_app.logger.error(f"Failed to get all exam types: {str(e)}")
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
            result = self.db_service.execute_query(query, (exam_type_id,))
            if not result:
                current_app.logger.warning(f"Exam type {exam_type_id} does not exist")
            return result[0] if result else None
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get exam type by id {exam_type_id}: {str(e)}")
            raise e
    
    def create_exam_type(self, exam_type_data):
        """
        创建考试类型
        
        Args:
            exam_type_data (dict): 考试类型信息
            
        Returns:
            int: 创建的考试类型ID
        """
        try:
            # 检查是否已存在同名考试类型
            check_query = "SELECT exam_type_id FROM ExamTypes WHERE exam_type_name = %s"
            existing = self.db_service.execute_query(check_query, (exam_type_data.get('exam_type_name'),))
            if existing:
                current_app.logger.warning(f"Exam type with name '{exam_type_data.get('exam_type_name')}' already exists")
                raise ValueError("Exam type name already exists")
            
            # 插入新考试类型
            insert_query = "INSERT INTO ExamTypes (exam_type_name) VALUES (%s)"
            exam_type_id = self.db_service.execute_update(insert_query, (exam_type_data.get('exam_type_name'),))
            
            return exam_type_id
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to create exam type: {str(e)}")
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
            # 检查考试类型是否存在
            if not self.get_exam_type_by_id(exam_type_id):
                current_app.logger.warning(f"Exam type {exam_type_id} does not exist")
                return False
            
            # 更新考试类型信息
            update_query = "UPDATE ExamTypes SET exam_type_name = %s WHERE exam_type_id = %s"
            self.db_service.execute_update(update_query, (exam_type_data.get('exam_type_name'), exam_type_id))
            
            return True
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to update exam type {exam_type_id}: {str(e)}")
            return False
    
    def delete_exam_type(self, exam_type_id):
        """
        删除考试类型（同时删除相关的成绩）
        
        Args:
            exam_type_id (int): 考试类型ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            # 检查考试类型是否存在
            if not self.get_exam_type_by_id(exam_type_id):
                current_app.logger.warning(f"Exam type {exam_type_id} does not exist")
                return False
            
            # 删除相关的成绩记录
            scores_query = "DELETE FROM Scores WHERE exam_type_id = %s"
            scores_deleted = self.db_service.execute_update(scores_query, (exam_type_id,))
            current_app.logger.info(f"Deleted {scores_deleted} scores for exam type {exam_type_id}")
            
            # 删除考试类型
            exam_type_query = "DELETE FROM ExamTypes WHERE exam_type_id = %s"
            self.db_service.execute_update(exam_type_query, (exam_type_id,))
            
            return True
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to delete exam type {exam_type_id}: {str(e)}")
            return False