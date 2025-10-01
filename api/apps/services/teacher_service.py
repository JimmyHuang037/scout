from apps.services.class_service import ClassService
from apps.utils.database_service import DatabaseService
"""教师服务模块，处理与教师相关的业务逻辑"""


class TeacherService:
    """教师服务类"""

    def __init__(self):
        """初始化教师服务"""
        self.db_service = DatabaseService()
        self.class_service = ClassService()

    def get_teacher_profile(self, teacher_id):
        """
        获取教师个人资料
        
        Args:
            teacher_id (str): 教师ID
            
        Returns:
            dict: 教师个人资料
        """
        try:
            query = """
                SELECT teacher_id, teacher_name
                FROM Teachers 
                WHERE teacher_id = %s
            """
            result = self.db_service.execute_query(query, (teacher_id,))
            return result[0] if result else None
        except Exception as e:
            raise e

    def get_teacher_classes(self, teacher_id):
        """
        获取教师授课班级列表
        
        Args:
            teacher_id (str): 教师ID
            
        Returns:
            list: 班级列表
        """
        try:
            query = """
                SELECT c.class_id, c.class_name
                FROM Classes c
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE tc.teacher_id = %s
                ORDER BY c.class_id
            """
            classes = self.db_service.execute_query(query, (teacher_id,))
            return {
                'classes': classes
            }
        except Exception as e:
            raise e

    def get_all_classes_students(self, teacher_id):
        """
        获取教师所有班级的学生列表
        
        Args:
            teacher_id (str): 教师ID
            
        Returns:
            dict: 所有班级的学生列表
        """
        try:
            query = """
                SELECT s.student_id, s.student_name, c.class_name, c.class_id
                FROM Students s
                JOIN Classes c ON s.class_id = c.class_id
                JOIN TeacherClasses tc ON c.class_id = tc.class_id
                WHERE tc.teacher_id = %s
                ORDER BY c.class_id, s.student_id
            """
            students = self.db_service.execute_query(query, (teacher_id,))
            
            # 按班级组织学生数据
            class_students = {}
            for student in students:
                class_id = student['class_id']
                if class_id not in class_students:
                    class_students[class_id] = {
                        'class_id': class_id,
                        'class_name': student['class_name'],
                        'students': []
                    }
                class_students[class_id]['students'].append({
                    'student_id': student['student_id'],
                    'student_name': student['student_name']
                })
            
            # 转换为列表格式
            result = list(class_students.values())
            
            return {
                'classes': result
            }
        except Exception as e:
            raise e

    def get_all_teachers(self, page=1, per_page=10):
        """
        获取所有教师列表（分页）
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            dict: 教师列表和分页信息
        """
        try:
            offset = (page - 1) * per_page
            
            # 获取总数
            count_query = "SELECT COUNT(*) as count FROM Teachers"
            total_result = self.db_service.execute_query(count_query)
            total = total_result[0]['count'] if total_result else 0
            
            # 获取教师列表
            query = """
                SELECT t.teacher_id, t.teacher_name, t.subject_id, s.subject_name
                FROM Teachers t
                LEFT JOIN Subjects s ON t.subject_id = s.subject_id
                ORDER BY t.teacher_id
                LIMIT %s OFFSET %s
            """
            teachers = self.db_service.execute_query(query, (per_page, offset))
            
            return {
                'teachers': teachers,
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': total,
                    'pages': (total + per_page - 1) // per_page
                }
            }
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get all teachers: {str(e)}")
            raise e

    def get_teacher_by_id(self, teacher_id):
        """
        根据ID获取教师详情
        
        Args:
            teacher_id (int): 教师ID
            
        Returns:
            dict: 教师信息
        """
        try:
            query = """
                SELECT t.teacher_id, t.teacher_name, t.subject_id, s.subject_name
                FROM Teachers t
                LEFT JOIN Subjects s ON t.subject_id = s.subject_id
                WHERE t.teacher_id = %s
            """
            result = self.db_service.execute_query(query, (teacher_id,))
            return result[0] if result else None
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to get teacher by id {teacher_id}: {str(e)}")
            raise e

    def create_teacher(self, teacher_data):
        """
        创建教师
        
        Args:
            teacher_data (dict): 教师信息
            
        Returns:
            bool: 是否创建成功
        """
        try:
            query = """
                INSERT INTO Teachers (teacher_name, subject_id, password)
                VALUES (%s, %s, %s)
            """
            params = (
                teacher_data.get('teacher_name'),
                teacher_data.get('subject_id'),
                teacher_data.get('password', 'pass123')  # 默认密码为pass123
            )
            self.db_service.execute_update(query, params)
            return True
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to create teacher: {str(e)}")
            raise e

    def update_teacher(self, teacher_id, teacher_data):
        """
        更新教师信息
        
        Args:
            teacher_id (int): 教师ID
            teacher_data (dict): 教师信息
            
        Returns:
            bool: 是否更新成功
        """
        connection = None
        try:
            # 获取数据库连接并开始事务
            connection = self.db_service.get_connection()
            connection.autocommit(False)
            
            with connection.cursor() as cursor:
                # 先检查教师是否存在
                check_query = "SELECT COUNT(*) as count FROM Teachers WHERE teacher_id = %s"
                cursor.execute(check_query, (teacher_id,))
                check_result = cursor.fetchone()
                
                if not check_result or check_result['count'] == 0:
                    current_app.logger.warning(f"Teacher {teacher_id} does not exist")
                    connection.rollback()
                    return False
                
                # 构建动态更新语句
                update_fields = []
                params = []
                
                if 'teacher_name' in teacher_data:
                    update_fields.append("teacher_name = %s")
                    params.append(teacher_data['teacher_name'])
                    
                if 'subject_id' in teacher_data:
                    update_fields.append("subject_id = %s")
                    params.append(teacher_data['subject_id'])
                    
                if 'password' in teacher_data:
                    update_fields.append("password = %s")
                    params.append(teacher_data['password'])
                
                if not update_fields:
                    connection.rollback()
                    return False
                    
                query = f"UPDATE Teachers SET {', '.join(update_fields)} WHERE teacher_id = %s"
                params.append(teacher_id)
                
                affected_rows = cursor.execute(query, params)
                connection.commit()
                return affected_rows > 0
        except Exception as e:
            if connection:
                connection.rollback()
            if current_app:
                current_app.logger.error(f"Failed to update teacher {teacher_id}: {str(e)}")
            raise e
        finally:
            if connection:
                connection.autocommit(True)
            # 不在这里关闭连接，让DatabaseService管理连接生命周期
    
    def delete_teacher(self, teacher_id):
        """
        删除教师
        
        Args:
            teacher_id (int): 教师ID
            
        Returns:
            bool: 是否删除成功
        """
        try:
            # 先检查教师是否存在
            check_query = "SELECT COUNT(*) as count FROM Teachers WHERE teacher_id = %s"
            check_result = self.db_service.execute_query(check_query, (teacher_id,))
            check_result = check_result[0] if check_result else None
            if not check_result or check_result['count'] == 0:
                current_app.logger.warning(f"Teacher {teacher_id} does not exist")
                return False
            
            # 按正确的顺序删除相关的外键约束记录
            # 先删除exams表中的相关记录
            delete_exams_query = "DELETE FROM exams WHERE teacher_id = %s"
            self.db_service.execute_update(delete_exams_query, (teacher_id,))
            
            # 再删除TeacherClasses表中的相关记录
            delete_tc_query = "DELETE FROM TeacherClasses WHERE teacher_id = %s"
            self.db_service.execute_update(delete_tc_query, (teacher_id,))
            
            # 最后删除Teachers表中的记录
            query = "DELETE FROM Teachers WHERE teacher_id = %s"
            affected_rows = self.db_service.execute_update(query, (teacher_id,))
            return affected_rows > 0
        except Exception as e:
            if current_app:
                current_app.logger.error(f"Failed to delete teacher {teacher_id}: {str(e)}")
            raise e
