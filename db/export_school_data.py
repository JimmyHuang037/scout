import pandas as pd
import mysql.connector
from mysql.connector import Error
import os

# 数据库连接配置
db_config = {
    'host': 'localhost',
    'database': 'school_management',
    'user': 'root',
    'password': 'Newuser1'
}

# 确保Excel文件保存在db目录下
db_directory = os.path.dirname(__file__)
excel_file = os.path.join(db_directory, 'school_management.xlsx')
views_excel_file = os.path.join(db_directory, 'school_management_views.xlsx')

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

def export_table_to_excel(table_name, query, connection, excel_writer):
    """将单个表导出到Excel的工作表中"""
    try:
        print(f"正在导出 {table_name} 表...")
        df = pd.read_sql(query, connection)
        df.to_excel(excel_writer, sheet_name=table_name, index=False)
        print(f"成功导出 {table_name} 表，共 {len(df)} 行数据")
        return len(df)
    except Exception as e:
        print(f"导出 {table_name} 表时出错: {e}")
        import traceback
        traceback.print_exc()
        return -1

def export_view_to_excel(view_name, connection, excel_writer):
    """将单个视图导出到Excel的工作表中"""
    try:
        print(f"正在导出 {view_name} 视图...")
        query = f"SELECT * FROM {view_name}"
        df = pd.read_sql(query, connection)
        df.to_excel(excel_writer, sheet_name=view_name, index=False)
        print(f"成功导出 {view_name} 视图，共 {len(df)} 行数据")
        return len(df)
    except Exception as e:
        print(f"导出 {view_name} 视图时出错: {e}")
        import traceback
        traceback.print_exc()
        return -1

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

def get_view_list(connection):
    """获取数据库中的所有视图名称"""
    try:
        cursor = connection.cursor()
        cursor.execute("SHOW FULL TABLES WHERE Table_type = 'VIEW'")
        views = [row[0] for row in cursor.fetchall()]
        return views
    except Exception as e:
        print(f"获取视图列表时出错: {e}")
        return []

def main():
    # 创建数据库连接
    connection = create_connection()
    if not connection:
        return
    
    try:
        # 获取数据库记录数
        db_counts = get_database_counts(connection)
        print("\n数据库中的记录数:")
        for table, count in db_counts.items():
            print(f"{table}: {count}")
        
        # 删除现有的Excel文件
        if os.path.exists(excel_file):
            os.remove(excel_file)
            print(f"\n已删除现有的 {os.path.basename(excel_file)} 文件")
        
        # 创建Excel写入器
        print(f"\n开始导出数据到Excel文件 {excel_file}...")
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # 导出每个表到Excel的不同工作表
            tables = [
                ('Classes', 'SELECT class_id, class_name FROM Classes'),
                ('Students', 'SELECT student_id, student_name, class_id, password FROM Students'),
                ('Teachers', 'SELECT teacher_id, teacher_name, subject_id, password FROM Teachers'),
                ('Subjects', 'SELECT subject_id, subject_name FROM Subjects'),
                ('Scores', 'SELECT score_id, student_id, subject_id, exam_type_id, score FROM Scores'),
                ('ExamTypes', 'SELECT exam_type_id, exam_type_name FROM ExamTypes'),
                ('TeacherClasses', 'SELECT teacher_id, class_id FROM TeacherClasses')
            ]
            
            excel_counts = {}
            success_count = 0
            for table_name, query in tables:
                count = export_table_to_excel(table_name, query, connection, writer)
                if count >= 0:
                    excel_counts[table_name] = count
                    success_count += 1
            
        print(f"\n数据导出完成，成功导出 {success_count}/7 个表到 {os.path.basename(excel_file)} 文件")
        print(f"文件保存位置: {excel_file}")
        
        # 比较记录数
        print("\n记录数比较结果:")
        print("-" * 50)
        print(f"{'表名':<15} {'数据库记录数':<15} {'Excel记录数':<15} {'一致性':<10}")
        print("-" * 50)
        
        all_consistent = True
        for table in db_counts.keys():
            db_count = db_counts.get(table, 0)
            excel_count = excel_counts.get(table, 0)
            consistent = "是" if db_count == excel_count else "否"
            
            if db_count != excel_count:
                all_consistent = False
                
            print(f"{table:<15} {db_count:<15} {excel_count:<15} {consistent:<10}")
        
        print("-" * 50)
        if all_consistent:
            print("所有表的记录数一致，数据导出成功！")
        else:
            print("部分表的记录数不一致，请检查数据。")
            
        # 导出视图到单独的Excel文件
        print(f"\n开始导出视图到Excel文件 {views_excel_file}...")
        
        # 删除现有的视图Excel文件
        if os.path.exists(views_excel_file):
            os.remove(views_excel_file)
            print(f"\n已删除现有的 {os.path.basename(views_excel_file)} 文件")
        
        # 获取视图列表
        views = get_view_list(connection)
        if not views:
            print("未找到任何视图，跳过视图导出。")
            return
            
        print(f"找到 {len(views)} 个视图: {', '.join(views)}")
        
        # 创建视图Excel写入器
        with pd.ExcelWriter(views_excel_file, engine='openpyxl') as writer:
            view_counts = {}
            success_views = 0
            
            for view_name in views:
                count = export_view_to_excel(view_name, connection, writer)
                if count >= 0:
                    view_counts[view_name] = count
                    success_views += 1
                    
        print(f"\n视图导出完成，成功导出 {success_views}/{len(views)} 个视图到 {os.path.basename(views_excel_file)} 文件")
        print(f"文件保存位置: {views_excel_file}")
        
        # 显示视图记录数
        print("\n视图记录数:")
        print("-" * 30)
        for view_name, count in view_counts.items():
            print(f"{view_name}: {count}")
        print("-" * 30)
        
    except Exception as e:
        print(f"导出数据时出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL连接已关闭")

if __name__ == "__main__":
    main()