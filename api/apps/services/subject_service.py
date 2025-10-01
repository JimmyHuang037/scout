from apps.utils.database_service import DatabaseService
from flask import current_app
"""科目服务模块，处理与科目相关的业务逻辑"""


class SubjectService:
    """科目服务类"""

    def __init__(self):
        """初始化科目服务"""
        self.db_service = DatabaseService()

    def get_all_subjects(self, page=1, per_page=10):
        """
        获取所有科目列表
        
        Returns:
            list: 科目列表
        """
        try:
            # 计算偏移量
            offset = (page - 1) * per_page
            
            # 获取总数
            count_query = "SELECT COUNT(*) as total FROM Subjects"
            total_result = self.db_service.execute_query(count_query)
            total = total_result[0]['total'] if total_result else 0
            
            # 获取科目列表
            query = "SELECT subject_id, subject_name FROM Subjects ORDER BY subject_id LIMIT %s OFFSET %s"
            subjects = self.db_service.execute_query(query, (per_page, offset))
            
            # 计算总页数
            pages = (total + per_page - 1) // per_page
            
            return {
                'subjects': subjects,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages
                }
            }
        except Exception as e:
            current_app.logger.error(f"Failed to get all subjects: {str(e)}")
            raise e

    def get_subject_by_id(self, subject_id):
        """
        根据ID获取科目信息
        
        Args:
            subject_id (int): 科目ID
            
        Returns:
            dict: 科目信息
        """
        try:
            query = "SELECT subject_id, subject_name FROM Subjects WHERE subject_id = %s"
            result = self.db_service.execute_query(query, (subject_id,))
            return result[0] if result else None
        except Exception as e:
            current_app.logger.error(f"Failed to get subject by id {subject_id}: {str(e)}")
            raise e
    
    def create_subject(self, subject_data):
        """
        创建新科目
        
        Args:
            subject_data (dict): 科目数据
            
        Returns:
            int: 创建的科目ID
        """
        try:
            # 检查科目名称是否已存在
            check_query = "SELECT subject_id FROM Subjects WHERE subject_name = %s"
            existing = self.db_service.execute_query(check_query, (subject_data['subject_name'],))
            if existing:
                raise ValueError("Subject name already exists")
            
            # 插入新科目
            insert_query = "INSERT INTO Subjects (subject_name) VALUES (%s)"
            subject_id = self.db_service.execute_update(insert_query, (subject_data['subject_name'],))
            
            return subject_id
        except Exception as e:
            current_app.logger.error(f"Failed to create subject: {str(e)}")
            raise e
    
    def update_subject(self, subject_id, subject_data):
        """
        更新科目信息
        
        Args:
            subject_id (int): 科目ID
            subject_data (dict): 科目数据
            
        Returns:
            bool: 更新是否成功
        """
        try:
            # 检查科目是否存在
            if not self.get_subject_by_id(subject_id):
                return False
                
            # 更新科目信息
            update_query = "UPDATE Subjects SET subject_name = %s WHERE subject_id = %s"
            self.db_service.execute_update(update_query, (subject_data['subject_name'], subject_id))
            
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to update subject {subject_id}: {str(e)}")
            return False

    def delete_subject(self, subject_id):
        """
        删除科目
        
        Args:
            subject_id (int): 科目ID
            
        Returns:
            bool: 删除是否成功
        """
        try:
            # 检查科目是否存在
            if not self.get_subject_by_id(subject_id):
                return False
            
            # 删除科目
            delete_query = "DELETE FROM Subjects WHERE subject_id = %s"
            self.db_service.execute_update(delete_query, (subject_id,))
            
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to delete subject {subject_id}: {str(e)}")
            return False