        # 构建查询
        query = """
            SELECT sc.score_id, sc.student_id, s.student_name, 
                   sc.subject_id, sub.subject_name,
                   sc.exam_type_id, et.exam_type_name, sc.score
            FROM Scores sc
            JOIN Students s ON sc.student_id = s.student_id
            JOIN Subjects sub ON sc.subject_id = sub.subject_id
            JOIN ExamTypes et ON sc.exam_type_id = et.exam_type_id
            JOIN TeacherClasses tc ON s.class_id = tc.class_id
            WHERE tc.teacher_id = %s
        """