#!/usr/bin/env python3
import sys
sys.path.append('/home/jimmy/repo/scout/api')

from app.factory import create_app
from utils.database_service import DatabaseService

app = create_app()

with app.app_context():
    db_service = DatabaseService()
    
    # 查询所有存在的考试类型
    query = "SELECT exam_type_id, exam_type_name FROM ExamTypes"
    exam_types = db_service.execute_query(query)
    
    print("当前数据库中的考试类型:")
    for exam_type in exam_types:
        print(f"考试类型 {exam_type['exam_type_id']}: {exam_type['exam_type_name']}")
    
    # 检查ID为1的考试类型是否存在
    check_query = "SELECT COUNT(*) as count FROM ExamTypes WHERE exam_type_id = 1"
    result = db_service.execute_query(check_query)
    print(f"\n考试类型ID为1存在: {'是' if result[0]['count'] > 0 else '否'}")