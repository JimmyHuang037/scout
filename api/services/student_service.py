"""学生服务模块"""
from utils.database_service import DatabaseService
from flask import current_app


class StudentService:
    """学生服务类"""

    def __init__(self):
        """初始化学生服务"""
        self.db_service = DatabaseService()

    def get_teacher_students(self, teacher_id, class_id=None, page=1, per_page=10):
        """
        获取教师所教班级的学生列表
        
        Args:
            teacher_id (str): 教师ID
            class_id (str, optional): 班级ID
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 学生列表和分页信息
        """
        try:
            # 计算偏移量
            offset = (page - 1) * per_page
            
            # 构建查询语句
            base_query = """
                SELECT s.student_id, s.student_name, s.class_id, c.class_name
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                JOIN TeacherClasses tc ON s.class_id = tc.class_id
                WHERE tc.teacher_id = %s
            """
            count_query = """
                SELECT COUNT(*) as total
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                JOIN TeacherClasses tc ON s.class_id = tc.class_id
                WHERE tc.teacher_id = %s
            """
            params = [teacher_id]
            count_params = [teacher_id]
            
            # 如果指定了班级ID，则添加到查询条件中
            if class_id:
                base_query += " AND s.class_id = %s"
                count_query += " AND s.class_id = %s"
                params.append(class_id)
                count_params.append(class_id)
            
            base_query += " ORDER BY s.student_id LIMIT %s OFFSET %s"
            params.extend([per_page, offset])
            
            # 获取总数
            total_result = self.db_service.execute_query(count_query, count_params, fetch_one=True)
            total = total_result['total'] if total_result else 0
            
            # 执行查询
            students = self.db_service.execute_query(base_query, params)
            current_app.logger.info(f"Retrieved {len(students)} students for teacher {teacher_id}")
            
            # 计算总页数
            pages = (total + per_page - 1) // per_page
            
            return {
                'students': students,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': pages
                }
            }
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get teacher students: {str(e)}")
            raise

    def get_student_by_id(self, student_id):
        """
        根据学生ID获取学生详情
        
        Args:
            student_id (str): 学生ID
            
        Returns:
            dict: 学生信息
        """
        try:
            query = """
                SELECT s.student_id, s.student_name, s.class_id, c.class_name
                FROM Students s
                LEFT JOIN Classes c ON s.class_id = c.class_id
                WHERE s.student_id = %s
            """
            result = self.db_service.execute_query(query, (student_id,), fetch_one=True)
            return result
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get student by id {student_id}: {str(e)}")
            raise e
        finally:
            self.db_service.close()
            
    def update_student_name(self, student_id, student_name):
        """
        更新学生姓名
        
        Args:
            student_id (str): 学生ID
            student_name (str): 新的学生姓名
            
        Returns:
            bool: 更新是否成功
        """
        try:
            query = "UPDATE Students SET student_name = %s WHERE student_id = %s"
            params = (student_name, student_id)
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to update student name for {student_id}: {str(e)}")
            return False
        finally:
            self.db_service.close()
