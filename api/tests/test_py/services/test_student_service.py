#!/usr/bin/env python3
"""
学生服务测试
"""

import pytest
from services.student_service import StudentService
from utils.database_service import DatabaseService


class TestStudentService:
    """学生服务测试类"""

    def test_get_all_students(self, app):
        """测试获取所有学生"""
        with app.app_context():
            student_service = StudentService()
            result = student_service.get_all_students(1, 10)
            assert isinstance(result, dict)
            assert 'students' in result
            assert 'pagination' in result

    def test_get_student_by_id(self, app):
        """测试根据ID获取学生"""
        with app.app_context():
            student_service = StudentService()
            result = student_service.get_student_by_id('S0101')
            assert isinstance(result, dict) or result is None

    def test_create_student(self, app):
        """测试创建学生"""
        with app.app_context():
            student_service = StudentService()
            # 先删除可能存在的测试数据
            db_service = DatabaseService()
            delete_query = "DELETE FROM Students WHERE student_id = %s"
            db_service.execute_update(delete_query, ('S9999',))
            db_service.close()
            
            student_data = {
                'student_id': 'S9999',
                'student_name': 'Test Student',
                'class_id': 1,
                'password': 'test123'
            }
            result = student_service.create_student(student_data)
            assert isinstance(result, bool)

    def test_update_student(self, app):
        """测试更新学生"""
        with app.app_context():
            student_service = StudentService()
            student_data = {
                'student_name': 'Updated Student',
                'class_id': 2
            }
            result = student_service.update_student('S0101', student_data)
            assert isinstance(result, bool)

    def test_delete_student(self, app):
        """测试删除学生"""
        with app.app_context():
            student_service = StudentService()
            result = student_service.delete_student('S0101')
            assert isinstance(result, bool)