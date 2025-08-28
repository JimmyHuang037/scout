                # 获取exam_type_id
                select_type_query = "SELECT exam_type_id FROM ExamTypes WHERE exam_type = %s"
                cursor.execute(select_type_query, (row['type'],))
                type_result = cursor.fetchone()
                exam_type_id = type_result[0] if type_result else None