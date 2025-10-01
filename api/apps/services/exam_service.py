from apps.utils.database_service import DatabaseService
from flask import current_app
"""考试服务类"""



class ExamService:
    """考试服务类"""

    def __init__(self):
        """初始化考试服务"""
        self.db_service = DatabaseService()

    def get_exam_by_id(self, exam_id):
        """
        根据ID获取考试信息
        
        Args:
            exam_id (int): 考试ID
            
        Returns:
            dict: 考试信息
        """
        query = """
            SELECT e.exam_id, e.exam_name, e.exam_date, e.subject_id, e.teacher_id, 
                   e.exam_type_id, s.subject_name, t.teacher_name, et.exam_type_name
            FROM Exams e
            JOIN Subjects s ON e.subject_id = s.subject_id
            JOIN Teachers t ON e.teacher_id = t.teacher_id
            JOIN ExamTypes et ON e.exam_type_id = et.exam_type_id
            WHERE e.exam_id = %s
        """
        result = self.db_service.execute_query(query, (exam_id,))
        return result[0] if result else None

    def create_exam(self, exam_data):
        """
        创建新考试
        
        Args:
            exam_data (dict): 考试数据
            
        Returns:
            dict: 创建的考试信息
        """
        # 插入新考试
        insert_query = """
            INSERT INTO Exams (exam_name, exam_date, subject_id, teacher_id, exam_type_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        exam_id = self.db_service.execute_update(
            insert_query, 
            (exam_data['name'], exam_data['date'], exam_data['subject_id'], 
             exam_data['creator_id'], exam_data['exam_type_id'])
        )
        
        # 返回创建的考试信息
        return self.get_exam_by_id(exam_id)

    def update_exam(self, exam_id, exam_data):
        """
        更新考试信息
        
        Args:
            exam_id (int): 考试ID
            exam_data (dict): 考试数据
            
        Returns:
            dict: 更新后的考试信息
        """
        # 检查考试是否存在
        if not self.get_exam_by_id(exam_id):
            return None
            
        # 更新考试信息
        update_query = """
            UPDATE Exams 
            SET exam_name = %s, exam_date = %s, subject_id = %s, teacher_id = %s, exam_type_id = %s
            WHERE exam_id = %s
        """
        self.db_service.execute_update(
            update_query,
            (exam_data['name'], exam_data['date'], exam_data['subject_id'], 
             exam_data['creator_id'], exam_data['exam_type_id'], exam_id)
        )
        
        # 返回更新后的考试信息
        return self.get_exam_by_id(exam_id)

    def delete_exam(self, exam_id):
        """
        删除考试
        
        Args:
            exam_id (int): 考试ID
            
        Returns:
            bool: 是否删除成功
        """
        # 检查考试是否存在
        if not self.get_exam_by_id(exam_id):
            return False
            
        # 删除考试
        delete_query = "DELETE FROM Exams WHERE exam_id = %s"
        self.db_service.execute_update(delete_query, (exam_id,))
        return True

    def get_exams_by_class_and_subject(self, class_id, subject_id):
        """
        获取指定班级和科目的考试列表
        
        Args:
            class_id (int): 班级ID
            subject_id (int): 科目ID
            
        Returns:
            list: 考试列表
        """
        query = """
            SELECT e.exam_id, e.exam_name, e.exam_date, e.subject_id, e.teacher_id, 
                   e.exam_type_id, s.subject_name, t.teacher_name, et.exam_type_name
            FROM Exams e
            JOIN Subjects s ON e.subject_id = s.subject_id
            JOIN Teachers t ON e.teacher_id = t.teacher_id
            JOIN ExamTypes et ON e.exam_type_id = et.exam_type_id
            WHERE e.class_id = %s AND e.subject_id = %s
            ORDER BY e.exam_date DESC
        """
        return self.db_service.execute_query(query, (class_id, subject_id))

    def analyze_exam_performance(self, exam_id):
        """
        分析考试表现
        
        Args:
            exam_id (int): 考试ID
            
        Returns:
            dict: 考试表现分析
        """
        # 获取考试基本信息
        exam_info = self.get_exam_by_id(exam_id)
        if not exam_info:
            return None
            
        analysis = {
            'exam_info': exam_info
        }
        
        # 计算平均分
        avg_query = """
            SELECT AVG(score) as average_score, COUNT(*) as total_students
            FROM Scores 
            WHERE exam_id = %s
        """
        avg_result = self.db_service.execute_query(avg_query, (exam_id,))
        analysis['average_score'] = float(avg_result[0]['average_score']) if avg_result and avg_result[0]['average_score'] else 0
        analysis['total_students'] = avg_result[0]['total_students'] if avg_result else 0
        
        # 计算各分数段人数
        grade_ranges = [
            {'name': '优秀 (90-100)', 'min': 90, 'max': 100},
            {'name': '良好 (80-89)', 'min': 80, 'max': 89},
            {'name': '中等 (70-79)', 'min': 70, 'max': 79},
            {'name': '及格 (60-69)', 'min': 60, 'max': 69},
            {'name': '不及格 (0-59)', 'min': 0, 'max': 59}
        ]
        
        grade_distribution = []
        for range_info in grade_ranges:
            count_query = """
                SELECT COUNT(*) as count
                FROM Scores 
                WHERE exam_id = %s AND score >= %s AND score <= %s
            """
            count_result = self.db_service.execute_query(
                count_query, 
                (exam_id, range_info['min'], range_info['max'])
            )
            count = count_result[0]['count'] if count_result else 0
            grade_distribution.append({
                'range': range_info['name'],
                'count': count,
                'percentage': round((count / analysis['total_students'] * 100) if analysis['total_students'] > 0 else 0, 2)
            })
            
        analysis['grade_distribution'] = grade_distribution
        
        # 获取最高分和最低分
        score_query = """
            SELECT MAX(score) as max_score, MIN(score) as min_score
            FROM Scores 
            WHERE exam_id = %s
        """
        score_result = self.db_service.execute_query(score_query, (exam_id,))
        analysis['max_score'] = float(score_result[0]['max_score']) if score_result and score_result[0]['max_score'] else 0
        analysis['min_score'] = float(score_result[0]['min_score']) if score_result and score_result[0]['min_score'] else 0
        
        return analysis