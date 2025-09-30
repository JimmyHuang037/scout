"""科目服务模块，处理与科目相关的业务逻辑"""
from flask import current_app
from apps.utils.database_service import DatabaseService


class SubjectService:
    """科目服务类"""

    def __init__(self):
        """初始化科目服务"""
        self.db_service = DatabaseService()

    def get_all_subjects(self):
        """
        获取所有科目列表
        
        Returns:
            list: 科目列表
        """
        try:
            query = "SELECT subject_id, subject_name FROM Subjects ORDER BY subject_id"
            return self.db_service.execute_query(query)
        except Exception as e:
            current_app.logger.error(f"Failed to get all subjects: {str(e)}")
            raise e
        finally:
            self.db_service.close()

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
        finally:
            self.db_service.close()
    
    def create_subject(self, subject_data):
        """
        创建新科目
        
        Args:
            subject_data (dict): 科目数据
            
        Returns:
            dict: 创建的科目信息
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
            
            # 返回创建的科目信息
            return self.get_subject_by_id(subject_id)
        except Exception as e:
            current_app.logger.error(f"Failed to create subject: {str(e)}")
            raise e
        finally:
            self.db_service.close()
    
    def update_subject(self, subject_id, subject_data):
        """
        更新科目信息
        
        Args:
            subject_id (int): 科目ID
            subject_data (dict): 科目数据
            
        Returns:
            dict: 更新后的科目信息
        """
        try:
            # 检查科目是否存在
            if not self.get_subject_by_id(subject_id):
                return None
                
            # 更新科目信息
            update_query = "UPDATE Subjects SET subject_name = %s WHERE subject_id = %s"
            self.db_service.execute_update(update_query, (subject_data['subject_name'], subject_id))
            
            # 返回更新后的科目信息
            return self.get_subject_by_id(subject_id)
        except Exception as e:
            current_app.logger.error(f"Failed to update subject {subject_id}: {str(e)}")
            raise e
        finally:
            self.db_service.close()
    
    def delete_subject(self, subject_id):
        """
        删除科目（同时删除相关的成绩）
        
        Args:
            subject_id (int): 科目ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            # 先检查科目是否存在
            check_query = "SELECT COUNT(*) as count FROM Subjects WHERE subject_id = %s"
            check_result = self.db_service.execute_query(check_query, (subject_id,), fetch_one=True)
            if not check_result or check_result['count'] == 0:
                current_app.logger.warning(f"Subject {subject_id} does not exist")
                return False
            
            # 开始事务
            self.db_service.start_transaction()
            
            # 删除与该科目相关的成绩
            delete_scores_query = "DELETE FROM Scores WHERE subject_id = %s"
            self.db_service.execute_update(delete_scores_query, (subject_id,))
            
            # 删除科目
            delete_subject_query = "DELETE FROM Subjects WHERE subject_id = %s"
            affected_rows = self.db_service.execute_update(delete_subject_query, (subject_id,))
            
            # 提交事务
            self.db_service.commit()
            return affected_rows > 0
        except Exception as e:
            current_app.logger.error(f"Failed to delete subject {subject_id}: {str(e)}")
            # 回滚事务
            self.db_service.rollback()
            raise e
        finally:
            self.db_service.close()