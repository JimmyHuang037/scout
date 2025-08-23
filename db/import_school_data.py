import pandas as pd
import mysql.connector
from mysql.connector import Error
import numpy as np
import os

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'database': 'school_management',
    'user': 'root',
    'password': 'Newuser1'
}

# Excel文件路径
excel_file = os.path.join(os.path.dirname(__file__), 'school_management.xlsx')

def create_connection():
    """创建数据库连接"""
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("成功连接到MySQL数据库")
            return connection
    except Error as e:
        print(f"连接MySQL时出错: {e}")
        return None

def get_database_counts(connection):
    """从数据库获取每个表的记录数"""
    table_counts = {}
    cursor = connection.cursor()
    
    tables = ['Classes', 'Students', 'Teachers', 'Subjects', 'Scores', 'ExamTypes', 'TeacherClasses']
    
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            table_counts[table] = count
        except Exception as e:
            print(f"查询 {table} 表记录数时出错: {e}")
            table_counts[table] = -1
    
    return table_counts

def import_sheet_to_table(sheet_name, table_name, connection):
    """将工作表导入到数据库表中"""
    try:
        # 读取Excel工作表
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        print(f"正在处理工作表: {sheet_name}，数据行数: {len(df)}")
        
        if df.empty:
            print(f"工作表 {sheet_name} 为空")
            return
        
        cursor = connection.cursor()
        
        # 根据表名处理不同的导入逻辑
        if table_name == 'Classes':
            # 处理Classes表 (class_id, class_name)
            for index, row in df.iterrows():
                insert_query = "INSERT INTO Classes (class_id, class_name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE class_name=VALUES(class_name)"
                cursor.execute(insert_query, (row['class_id'], row['class_name']))
                
        elif table_name == 'Teachers':
            # 处理Teachers表 (teacher_id, teacher_name, subject_id, password)
            for index, row in df.iterrows():
                insert_query = "INSERT INTO Teachers (teacher_id, teacher_name, subject_id, password) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE teacher_name=VALUES(teacher_name), subject_id=VALUES(subject_id), password=VALUES(password)"
                cursor.execute(insert_query, (row['teacher_id'], row['teacher_name'], row['subject_id'], row['password']))
                
        elif table_name == 'TeacherClasses':
            # 处理TeacherClasses表 (teacher_id, class_id)
            for index, row in df.iterrows():
                # 转换numpy.int64为Python原生int类型
                teacher_id = int(row['teacher_id']) if not pd.isna(row['teacher_id']) else None
                class_id = int(row['class_id']) if not pd.isna(row['class_id']) else None
                insert_query = "INSERT INTO TeacherClasses (teacher_id, class_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE teacher_id=VALUES(teacher_id), class_id=VALUES(class_id)"
                cursor.execute(insert_query, (teacher_id, class_id))
                
        elif table_name == 'Students':
            # 处理Students表 (student_id, student_name, class_id, password)
            for index, row in df.iterrows():
                insert_query = "INSERT INTO Students (student_id, student_name, class_id, password) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE student_name=VALUES(student_name), class_id=VALUES(class_id), password=VALUES(password)"
                cursor.execute(insert_query, (row['student_id'], row['student_name'], row['class_id'], row['password']))
                
        elif table_name == 'Scores':
            # 处理Scores表 (score_id, student_id, subject_id, exam_type_id, score)
            for index, row in df.iterrows():
                insert_query = "INSERT INTO Scores (score_id, student_id, subject_id, exam_type_id, score) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE student_id=VALUES(student_id), subject_id=VALUES(subject_id), exam_type_id=VALUES(exam_type_id), score=VALUES(score)"
                cursor.execute(insert_query, (row['score_id'], row['student_id'], row['subject_id'], row['exam_type_id'], row['score']))
                
        elif table_name == 'ExamTypes':
            # 处理ExamTypes表 (type_id, exam_type_name)
            for index, row in df.iterrows():
                insert_query = "INSERT INTO ExamTypes (type_id, exam_type_name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE exam_type_name=VALUES(exam_type_name)"
                cursor.execute(insert_query, (row['type_id'], row['exam_type_name']))
                
        elif table_name == 'Subjects':
            # 处理Subjects表 (subject_id, subject_name)
            for index, row in df.iterrows():
                insert_query = "INSERT INTO Subjects (subject_id, subject_name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE subject_name=VALUES(subject_name)"
                cursor.execute(insert_query, (row['subject_id'], row['subject_name']))
                
        # 提交更改
        connection.commit()
        print(f"成功导入 {table_name} 表，共 {len(df)} 行数据")
        
    except Exception as e:
        print(f"导入 {sheet_name} 工作表时出错: {e}")
        import traceback
        traceback.print_exc()
        connection.rollback()

def main():
    # 检查Excel文件是否存在
    if not os.path.exists(excel_file):
        print(f"错误：找不到Excel文件 {excel_file}")
        return
    
    # 创建数据库连接
    connection = create_connection()
    if not connection:
        return
    
    try:
        # 先禁用外键检查以避免导入顺序问题
        cursor = connection.cursor()
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # 清空现有数据
        tables_to_truncate = ['TeacherClasses', 'Scores', 'Students', 'Teachers', 'Classes', 'ExamTypes', 'Subjects']
        for table in tables_to_truncate:
            try:
                cursor.execute(f"TRUNCATE TABLE {table}")
                print(f"已清空 {table} 表")
            except Exception as e:
                print(f"清空 {table} 表时出错: {e}")
        
        # 映射工作表名称到数据库表名称（注意顺序，先导入主表）
        sheet_to_table = [
            ('Subjects', 'Subjects'),      # 先导入Subjects表
            ('ExamTypes', 'ExamTypes'),    # 再导入ExamTypes表
            ('Classes', 'Classes'),        # 再导入Classes表
            ('Students', 'Students'),      # 再导入Students表
            ('Teachers', 'Teachers'),      # 再导入Teachers表
            ('Scores', 'Scores'),          # 最后导入Scores表
            ('TeacherClasses', 'TeacherClasses')  # 最后导入TeacherClasses表
        ]
        
        # 导入每个工作表
        for sheet_name, table_name in sheet_to_table:
            import_sheet_to_table(sheet_name, table_name, connection)
        
        # 重新启用外键检查
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        # 显示导入后的数据库记录数
        print("\n数据导入完成，数据库中的记录数:")
        db_counts = get_database_counts(connection)
        print("-" * 30)
        print(f"{'表名':<15} {'记录数':<10}")
        print("-" * 30)
        for table, count in db_counts.items():
            print(f"{table:<15} {count:<10}")
        print("-" * 30)
            
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL连接已关闭")

if __name__ == "__main__":
    main()