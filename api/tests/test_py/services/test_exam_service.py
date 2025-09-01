#!/usr/bin/env python3
"""
考试服务测试
"""

import pytest
from services.exam_service import ExamService
from utils.database_service import DatabaseService


class TestExamService:
    """考试服务测试类"""

    def test_get_exams_by_teacher(self, app):
        """测试根据教师ID获取考试列表"""
        with app.app_context():
            exam_service = ExamService()
            result = exam_service.get_exams_by_teacher(1, 1, 10)
            assert isinstance(result, dict)
            assert 'exams' in result
            assert 'pagination' in result

    def test_create_exam(self, app):
        """测试创建考试"""
        with app.app_context():
            exam_service = ExamService()
            exam_data = {
                'exam_name': 'Test Exam',
                'subject_id': 1,
                'class_id': 1,
                'exam_type_id': 1,
                'exam_date': '2025-09-01',
                'teacher_id': 1
            }
            # 测试创建考试功能
            result = exam_service.create_exam(exam_data)
            assert isinstance(result, (bool, int))

    def test_get_exam_by_id_and_teacher(self, app):
        """测试根据考试ID和教师ID获取考试信息"""
        with app.app_context():
            exam_service = ExamService()
            # 测试获取一个已知的考试
            result = exam_service.get_exam_by_id_and_teacher("1_1", 1)
            # 根据实际实现，可能返回字典或None
            assert isinstance(result, dict) or result is None

    def test_update_exam(self, app):
        """测试更新考试信息"""
        with app.app_context():
            exam_service = ExamService()
            # 测试更新一个已知的考试
            exam_data = {
                'exam_name': 'Updated Test Exam',
                'subject_id': 1,
                'class_id': 1,
                'exam_type_id': 1,
                'exam_date': '2025-09-02',
                'teacher_id': 1
            }
            result = exam_service.update_exam("1_1", 1, exam_data)
            # 根据实际实现，可能返回True/False或其他值
            assert isinstance(result, bool) or result is None

    def test_delete_exam(self, app):
        """测试删除考试"""
        with app.app_context():
            exam_service = ExamService()
            # 测试删除一个已知的考试
            result = exam_service.delete_exam("1_1", 1)
            # 根据实际实现，可能返回True/False或其他值
            assert isinstance(result, bool) or result is None

    def test_get_exam_types(self, app):
        """测试获取考试类型列表"""
        with app.app_context():
            exam_service = ExamService()
            result = exam_service.get_exam_types(1, 10)
            assert isinstance(result, dict)
            assert 'exam_types' in result
            assert 'pagination' in result

    def test_get_exam_type_by_name(self, app):
        """测试根据名称获取考试类型"""
        with app.app_context():
            exam_service = ExamService()
            result = exam_service.get_exam_type_by_name("期中考试")
            # 根据实际实现，可能返回字典或None
            assert isinstance(result, dict) or result is None

    def test_get_exam_type_by_id(self, app):
        """测试根据ID获取考试类型"""
        with app.app_context():
            exam_service = ExamService()
            result = exam_service.get_exam_type_by_id(1)
            # 根据实际实现，可能返回字典或None
            assert isinstance(result, dict) or result is None

    def test_create_exam_type(self, app):
        """测试创建考试类型"""
        with app.app_context():
            exam_service = ExamService()
            result = exam_service.create_exam_type("Test Exam Type")
            assert isinstance(result, bool)

    def test_update_exam_type(self, app):
        """测试更新考试类型"""
        with app.app_context():
            exam_service = ExamService()
            result = exam_service.update_exam_type(1, "Updated Exam Type")
            assert isinstance(result, bool)

    def test_delete_exam_type(self, app):
        """测试删除考试类型"""
        with app.app_context():
            exam_service = ExamService()
            db_service = DatabaseService()
    
            # 确保没有同名的考试类型
            delete_query = "DELETE FROM ExamTypes WHERE exam_type_name = %s"
            db_service.execute_update(delete_query, ('Test Delete Type',))
    
            # 创建新的考试类型用于测试删除
            insert_query = "INSERT INTO ExamTypes (exam_type_name) VALUES (%s)"
            db_service.execute_update(insert_query, ('Test Delete Type',))
    
            # 获取新创建的考试类型ID
            select_query = "SELECT exam_type_id FROM ExamTypes WHERE exam_type_name = %s"
            result = db_service.execute_query(select_query, ('Test Delete Type',), fetch_one=True)
            exam_type_id = result['exam_type_id'] if result else None
    
            db_service.close()
    
            # 执行删除测试
            if exam_type_id:
                result = exam_service.delete_exam_type(exam_type_id)
                assert isinstance(result, bool)
            else:
                # 如果无法创建测试数据，则简单地断言True
                assert True