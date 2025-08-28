        # 构建查询
        query = """
            SELECT s.score_id, s.student_id, st.student_name,
                   s.subject_id, sub.subject_name,
                   s.exam_type_id, et.exam_type_name, s.score
            FROM Scores s
            JOIN Students st ON s.student_id = st.student_id
            JOIN Subjects sub ON s.subject_id = sub.subject_id
            JOIN ExamTypes et ON s.exam_type_id = et.exam_type_id
            WHERE s.student_id = %s
        """